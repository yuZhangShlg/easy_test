# coding=utf-8
import hashlib
import os
import traceback

from functools import wraps
from string import capwords

import ldap
from flask import jsonify
from flask import current_app, request, flash, render_template, redirect
import requests
import json
# from models import data2dict
#
# # Find the stack on which we want to store the database connection.
# # Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# # before that we need to use the _request_ctx_stack.
# from lib.user import user_info
# from lib.workflow import get_respond_by_admin
# from models.auth.auth_token import AuthToken

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack
from flask import session, redirect, url_for


def delete_temp_token(token_temp):
    headers = {'Content-type': 'application/json', 'charset': 'utf-8'}
    data = {'zg_sso_token': token_temp}
    result = requests.post(current_app.config['SSO_URL'] + '/platform.information.sso.ui/sso/clearTokenBykey',
       data=json.dumps(data), headers=headers, timeout=5)

    return True


def put_sso_user(token, token_temp):
    content = get_sso_user(token_temp)
    if 'operatorVo' in content:
        ops_token = hashlib.sha1(os.urandom(24)).hexdigest()

        ret, token_list = AuthToken.get_by_query(None, content['operatorVo']['operatorLoginName'])
        count = token_list.count()
        if count == 0:
            AuthToken.add(content['operatorVo']['operatorLoginName'], ops_token)
        else:
            AuthToken.update(content['operatorVo']['operatorLoginName'], ops_token)

        session['ops_token'] = ops_token
        session['token'] = token
        session['lat_name'] = content['operatorVo']['operatorName']
        session['username'] = content['operatorVo']['operatorLoginName']

    ##同步用户到后台
    try:
        account = session.get('username')
        user = user_info(account)
        if user is not None:
            if user.has_key('email'):
                username = user['email'].split('@')[0].lower()
            else:
                username = user['loginName'].lower()
        else:
            username = session.get('username').lower()
        url = "/activiti-rest/service/identity/users/" + username
        flag, result = get_respond_by_admin("GET", url, "")
        if not flag:
            params = {"id": username, "password": username, "firstName": username, "lastName": username,
                      "email": username + "@china.zhaogang.com"}

            params_str = json.dumps(params)
            url = "/activiti-rest/service/identity/users"
            flag, result = get_respond_by_admin("POST", url, params_str)
    except Exception as e:
        current_app.logger.error(traceback.format_exc())


def get_sso_user(token):
    headers = {'Content-type': 'application/json', 'charset': 'utf-8'}
    data = {'zg_sso_token': token}
    result = requests.post(current_app.config['SSO_URL'] + '/platform.information.sso.ui/sso/getOperatorBySsoKey',
       data=json.dumps(data), headers=headers, timeout=5)
    return json.loads(result.content)


def login_required_special(f):
    """
    Decorator for views that require login.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if 'zg_sso_token' in request.args:
            put_sso_user(request.args['zg_sso_token'])

        if 'zg_sso_token_temp' in request.args:
            delete_temp_token(request.args['zg_sso_token_temp'])

        if 'ops_token' not in session or 'token' not in session or 'lat_name' not in session:
            return redirect(current_app.config['SSO_URL'] + '/login?redirectUrl=' +
                    request.url.replace('127.0.0.1:5001', current_app.config['SERVER_DOMAIN'])
                    + '&zg_sso_system_alias=' + current_app.config['SYSTEM_ALAIS'])

        if 'ops_token' in session:
            ret = verify_token(True)
            if ret:
                return f(*args, **kwargs)
            else:
                return redirect(current_app.config['SSO_URL'] + '/login?redirectUrl=' +
                        request.url.replace('127.0.0.1:5001', current_app.config['SERVER_DOMAIN'])
                        + '&zg_sso_system_alias=' + current_app.config['SYSTEM_ALAIS'])

        if request.method == 'POST':
            return jsonify({'redirect': current_app.config['SSO_URL'] + '/login'})

        return redirect(current_app.config['SSO_URL'] + '/login?redirectUrl=' +
                request.url.replace('127.0.0.1:5001', current_app.config['SERVER_DOMAIN'])
                + '&zg_sso_system_alias=' + current_app.config['SYSTEM_ALAIS'])

    return decorated


def verify_token(high_flag=False):
    verify_flag = False
    ops_token = session.get('ops_token')
    ret, token_list = AuthToken.get_by_query(ops_token, None)
    token_list = data2dict(token_list.all());

    for token in token_list:
        if token.get('username') == session.get('username'):
            verify_flag = True
            break

    if verify_flag and high_flag:
        if request.referrer is None:
            verify_flag = False

    return verify_flag


def login_required(f):
    """
    Decorator for views that require login.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if 'token' not in session or 'lat_name' not in session:
            # if 'zg_sso_token_temp' in request.args:
            #     delete_temp_token(request.args['zg_sso_token_temp'])

            if 'zg_sso_token_temp' in request.args and 'zg_sso_token' in request.args:
                put_sso_user(request.args['zg_sso_token'], request.args['zg_sso_token_temp'])

            if 'zg_sso_token_temp' in request.args:
                delete_temp_token(request.args['zg_sso_token_temp'])

        if 'ops_token' not in session or 'token' not in session or 'lat_name' not in session:
            if 'ops_token' in session:
                del session['ops_token']
            if 'lat_name' in session:
                del session['lat_name']
            if 'token' in session:
                del session['token']
            return redirect(current_app.config['SSO_URL'] + '/login?redirectUrl=' +
                    request.url.replace('127.0.0.1:5001', current_app.config['SERVER_DOMAIN'])
                    + '&zg_sso_system_alias=' + current_app.config['SYSTEM_ALAIS'])

        if 'ops_token' in session:
            ret = verify_token()
            if ret:
                return f(*args, **kwargs)
            else:
                if 'ops_token' in session:
                    del session['ops_token']
                if 'lat_name' in session:
                    del session['lat_name']
                if 'token' in session:
                    del session['token']
                return redirect(current_app.config['SSO_URL'] + '/login?redirectUrl=' +
                        request.url.replace('127.0.0.1:5001', current_app.config['SERVER_DOMAIN'])
                        + '&zg_sso_system_alias=' + current_app.config['SYSTEM_ALAIS'])

        if request.method == 'POST':
            return jsonify({'redirect': current_app.config['SSO_URL'] + '/login'})

        return redirect(current_app.config['SSO_URL'] + '/login?redirectUrl=' +
                request.url.replace('127.0.0.1:5001', current_app.config['SERVER_DOMAIN'])
                + '&zg_sso_system_alias=' + current_app.config['SYSTEM_ALAIS'])

    return decorated