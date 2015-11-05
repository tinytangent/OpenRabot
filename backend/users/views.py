from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from users.managers import UsersManager
import json

# Create your views here.


@csrf_exempt
def user_registration_view(request):
    manager = UsersManager()

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode())
            uname = data['username']
            passwd = data['password']
            email = data['email']
        except KeyError:
            response_data = {
                'result': 'failed',
                'errorMessage': 'KeyError',
            }
        else:
            result = manager.registration(uname, passwd, email)

            if result[:9] == 'Succeeded':
                response_data = {
                    'result': 'succeeded',
                }
            else:
                response_data = {
                    'result': 'failed',
                    'errorMessage': result,
                }

        return HttpResponse(json.dumps(response_data))

    else:
        raise Http404


@csrf_exempt
def user_login_view(request):
    manager = UsersManager()

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode())
            uname = data['username']
            passwd = data['password']
        except KeyError:
            response_data = {
                'result': "failed",
                'errorMessage': 'KeyError',
            }
        else:
            result = manager.login(uname, passwd)

            if result[:9] == 'Succeeded':
                response_data = {
                    'result': 'succeeded',
                }
                cur_user = manager.get_cur_user()
                request.session['cur_user'] = cur_user.to_dict()
                request.session['logged_in'] = True

            else:
                response_data = {
                    'result': 'failed',
                    'errorMessage': result,
                }

        return HttpResponse(json.dumps(response_data))

    elif request.method == 'GET':
        cur_user = request.session.get('cur_user', None)
        if cur_user:
            logged_in = request.session.get('logged_in', False)
            response_data = {
                'result': 'succeeded',
                'loggedin': logged_in,
                'user': cur_user,
            }
        else:
            response_data = {
                'result': 'failed',
                'errorMessage': 'No user is logging in now.'
            }

        return HttpResponse(json.dumps(response_data))

    else:
        raise Http404


@csrf_exempt
def user_logout_view(request):
    manager = UsersManager()

    if request.method == 'GET':
        cur_user = request.session.get('cur_user', None)
        if cur_user:
            logged_in = request.session.get('logged_in', False)
            if logged_in:
                uid = cur_user['uid']
            else:
                uid = -1073741823
        else:
            uid = -1073741823

        result = manager.logout(uid)
        if result[:9] == 'Succeeded':
            response_data = {
                'result': 'succeeded',
            }
        else:
            response_data = {
                'result': 'failed',
                'errorMessage': result,
            }

        return HttpResponse(json.dumps(response_data))

    else:
        raise Http404


@csrf_exempt
def user_info_update(request):
    manager = UsersManager()

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode())
            old_passwd = data['oldPassword']
            new_passwd = data['newPassword']
            new_email = data['new_email']
        except KeyError:
            response_data = {
                'result': 'failed',
                'errorMessage': 'KeyError',
            }
        else:
            cur_user = request.session.get('cur_user', None)
            if cur_user:
                logged_in = request.session.get('logged_in', False)
                if logged_in:
                    uid = cur_user['uid']
                else:
                    uid = -1073741823
            else:
                uid = -1073741823

            result = manager.update(uid, old_passwd, new_passwd, new_email)

            if result[:9] == 'Succeeded':
                response_data = {
                    'result': 'succeeded',
                }
            else:
                response_data = {
                    'result': "failed",
                    'errorMessage': result
                }

        return HttpResponse(json.dumps(response_data))

    else:
        raise Http404

