
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect

from Users.models import Profile, ProfileExtendedDetails, ProfileBasicDetails

class GeneralMiddleware():

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        '''
            Create and/or login a default RM user as a super user
        '''
        if request.user.is_anonymous:
            default_user = User.objects.filter(email="rm1@futureforex.com").first()
            if not default_user:  # default user does not exist, create default user
                default_user = User.objects.create_user('rm1@futureforex.com', 'rm1@futureforex.com', 'Abcd1234!')
                default_user.is_superuser = True
                default_user.is_staff = True
                default_user.is_active = True
                default_user.first_name = "default"
                default_user.last_name = "RM"
                default_user.save()

                profile = Profile(user=default_user)
                profile.save()

                ProfileBasicDetails(profile=profile).save()
                ProfileExtendedDetails(profile=profile, managing_rm=default_user).save()

            # log in default user
            login(request, default_user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('index')
