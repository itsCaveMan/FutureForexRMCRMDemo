from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, ProfileBasicDetails, ProfileExtendedDetails

admin.site.register(Profile)
admin.site.register(ProfileBasicDetails)
admin.site.register(ProfileExtendedDetails)
