# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
# from Users.models import User

#
# class AuthenticationEmailBackend(object):
#     def authenticate(self, request, **kwargs):
#         # UserModel = get_user_model()
#
#         return None # just return None for now. dont email auth for now
#
#         email = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = User.objects.filter(email=email).first()
#
#         if user is None:
#             return None # no user in the database with this email
#         else:
#             return user # user exists
#
#         # try:
#         #     user = Users.objects.get(email=username)
#
#         # no user by this email
#         # except User.DoesNotExist:
#         #     return None
#
#         # user with this email exists
#         # else:
#             # if getattr(user, 'is_active', False) and user.check_password(password):
#             #     return user
#             # return user
#
#         # return None
#
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None
