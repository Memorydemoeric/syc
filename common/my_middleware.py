from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from user.models import UserInfo


class SignInCheck(MiddlewareMixin):
    def process_request(self, request):
        user_token = request.session.get('token', 'none_token!')
        if (not (request.path == '/check_out_passwd/' or request.path == '/sign_in/')) and not UserInfo.objects.filter(load_in_token=user_token):
                return redirect('/sign_in/')
