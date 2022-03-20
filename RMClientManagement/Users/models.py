from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
import django.utils.timezone
# from django.apps import apps

# ModelName = apps.get_model('ModelName', 'ModelName')

import datetime
import uuid
# import arrow
import traceback
import json

class MyUserManager(BaseUserManager):

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')

        username = str(username).lower()

        email = self.normalize_email(email)

        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)


    def create_superuser(self, username, email, password, **extra_fields):

        user = self._create_user(username, email, password, True, True,
                                 **extra_fields)
        profile = UserProfile(user=user)
        profile.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    id = models.AutoField(primary_key=True)

    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(unique=True)


    ADMINISTRATOR = 'ADMINISTRATOR'
    USER = 'USER'
    CLIENT = 'CLIENT'
    user_role_choices = (
                        (ADMINISTRATOR , 'Administrator user'),
                        (USER , 'Default user'),
                        (CLIENT , 'Client user'),
                        )
    user_role = models.CharField(max_length=255, choices=user_role_choices, default=USER)


    # is_admin = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    email_confirmed = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    created_on_utc      = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    last_modified_utc   = models.DateTimeField(auto_now=True, null=True)


    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    primary_rm = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='rm_user')

    def __str__(self):
        return 'User - ' + self.full_name

    @property
    def full_name(self):
        profile = self.profile
        if profile:
            return self.profile.full_name()
        return ''

    @property
    def full_name_reverse(self):
        profile = self.profile
        if profile:
            return self.profile.full_name_reverse()
        return ''


    def get_userprofile(self):
        profile = UserProfile.objects.filter(user_id=self.id).first()
        if profile is None:
            return None
        else:
            return profile

    profile = property(get_userprofile)



class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name='user_for_profile')

    # English Name
    first_name = models.CharField(max_length=255, default='', blank=True)
    middle_name = models.CharField(max_length=255, default='', blank=True)
    last_name = models.CharField(max_length=255, default='', blank=True)

    nickname = models.CharField(max_length=255, default='', blank=True)

    # Avatar
    # avatar = models.ImageField(upload_to="user_avatars", default='user_avatars/default_avatar.png', blank=True)

    # Gender
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'
    NOT_SPECIFIED = 'NOT_SPECIFIED'
    USER_GENDER_CHOICES = ((MALE , 'MALE'),
                                (FEMALE , 'FEMALE'),
                                (OTHER , 'OTHER'),
                                (NOT_SPECIFIED , 'NOT_SPECIFIED'),
                                )
    gender = models.CharField(max_length=255, choices=USER_GENDER_CHOICES, default=NOT_SPECIFIED)

    # date of birth
    date_of_birth = models.DateField(default=datetime.date(2000, 1, 1))

    # Address
    # address_0 = models.TextField(default='')
    # address_1 = models.TextField(default='')

    # cell number
    # cell_number = models.CharField(max_length=255, default='', blank=True)

    # website
    personal_website = models.CharField(max_length=255, default='', blank=True)

    created_on_utc      = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    last_modified_utc   = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return 'UserProfile - ' + self.full_name()

    def full_name(self):
        name = ''
        if self.first_name:
            name += self.first_name + ' '
        if self.last_name:
            name += self.last_name
        return name










# class UserPreference(models.Model):
#
#     # The Name
#     user = models.ForeignKey('User', on_delete=models.CASCADE)
#     created_datetime = models.DateTimeField(default=django.utils.timezone.now) # timezone.now is a wrapper for datetime.utcnow().replace(tzinfo=utc)
#
#     type = models.CharField(max_length=255, default='', blank=True)
#     preference = models.CharField(max_length=255, default='', blank=True)
#
#     last_modified_utc   = models.DateTimeField(auto_now=True, null=True)
#     created_on_utc      = models.DateTimeField(auto_now_add=True, null=True, editable=False)
#
#
#     def __str__(self):
#         return 'Preference for:: ' + self.user.full_name + ' - type:: ' + self.type + ' - pref:: ' + self.preference
#
#
# class PasswordReset(models.Model):
#
#     # The Name
#     user = models.ForeignKey('User', on_delete=models.CASCADE)
#     created_on_datetime = models.DateTimeField(default=django.utils.timezone.now) # timezone.now is a wrapper for datetime.utcnow().replace(tzinfo=utc)
#     uuid = models.CharField(max_length=255, default=uuid.uuid4, blank=True)
#
#     # Has this reset been used
#     used = models.BooleanField(default=False)
#
#     last_modified_utc   = models.DateTimeField(auto_now=True, null=True)
#     created_on_utc      = models.DateTimeField(auto_now_add=True, null=True, editable=False)
#
#     def __str__(self):
#         return 'Password Reset for:: ' + self.user.full_name + ' - created on:: ' + self.created_on_datetime.strftime('%Y - %b - %d')
#
#
# class EmailConfirmation(models.Model):
#
#     # The User
#     user = models.ForeignKey('User', on_delete=models.CASCADE)
#
#     # created_on_datetime_utc = models.DateTimeField(default=django.utils.timezone.now) # timezone.now is a wrapper for datetime.utcnow().replace(tzinfo=utc)
#     last_sent_on_datetime_utc      = models.DateTimeField(default=None, null=True, blank=True, editable=False)
#
#     # The Token
#     uuid = models.CharField(max_length=255, default=uuid.uuid4)
#
#     used = models.BooleanField(default=False)
#
#     last_modified_utc   = models.DateTimeField(auto_now=True, null=True)
#     created_on_utc      = models.DateTimeField(auto_now_add=True, null=True, editable=False)
#
#     def __str__(self):
#       return 'Email Confirmation Token for:: ' + self.user.full_name + ' - created on:: ' + self.created_on_utc.strftime('%Y - %b - %d')
#
#     def has_five_minutes_past_since_last_sent(self):
#         five_minutes_ago = arrow.get().shift(minutes=-5) # get a datetime of 5 minutes ago
#         # is the 'last_sent_on' datetime less then 5 minutes ago?
#         if self.last_sent_on_datetime_utc and self.last_sent_on_datetime_utc > five_minutes_ago:
#             return True # yes, it was sent more then 5 minutes ago
#         return False
#
# class EmailChange(models.Model):
#
#     user = models.ForeignKey('User', on_delete=models.CASCADE)
#
#     uuid = models.CharField(max_length=255, default=uuid.uuid4)
#
#     # the existing email address
#     from_email = models.CharField(max_length=255, default='')
#
#     # the new email address
#     to_email = models.CharField(max_length=255, default='')
#
#     used = models.BooleanField(default=False)
#
#     last_modified_utc   = models.DateTimeField(auto_now=True, null=True)
#     created_on_utc      = models.DateTimeField(auto_now_add=True, null=True, editable=False)
#
#     def __str__(self):
#       return "Email Change: " + self.user.full_name
#

