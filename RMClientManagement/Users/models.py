from django.db import models
from django.contrib.auth.models import User

import datetime

from RMClientManagement import globals
from RMClientManagement.globals import BaseModel



class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name()

    def full_name(self):
        details = self.profilebasicdetails
        full_name = f'{details.first_name} + ' \
               f'{details.middle_name} + ' \
               f'{details.last_name}'
        return full_name

class ProfileBasicDetails(BaseModel):
    profile = models.OneToOneField(Profile, on_delete=models.PROTECT)

    # Name
    first_name = models.CharField(max_length=255, default='', blank=True)
    middle_name = models.CharField(max_length=255, default='', blank=True)
    last_name = models.CharField(max_length=255, default='', blank=True)

    # Gender
    gender = models.CharField(max_length=255, choices=globals.USER_GENDER_CHOICES, default=globals.UNDEFINED_GENDER)

    # Date of birth
    date_of_birth = models.DateField(default=datetime.date(2000, 1, 1))

class ProfileExtendedDetails(BaseModel):
    profile = models.OneToOneField(Profile, on_delete=models.PROTECT)

    nickname = models.CharField(max_length=255, default='', blank=True)

    # Avatar
    # avatar = models.ImageField(upload_to="user_avatars", default='DEFAULT/_default_avatar.png')

    # Address
    address_0 = models.CharField(max_length=255, default='')
    address_1 = models.CharField(max_length=255, default='')

    # cell number
    cell_number = models.CharField(max_length=255, default='', blank=True)

    # website
    personal_website = models.CharField(max_length=255, default='', blank=True)








# ==============   OLD   ==============
# class MyUserManager(BaseUserManager):
#
#     def _create_user(self, username, email, password,
#                      is_staff, is_superuser, **extra_fields):
#         if not username:
#             raise ValueError('The given username must be set')
#
#         username = str(username).lower()
#
#         email = self.normalize_email(email)
#
#         user = self.model(username=username, email=email,
#                           is_staff=is_staff, is_active=True,
#                           is_superuser=is_superuser, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, username, email, password=None, **extra_fields):
#         return self._create_user(username, email, password, False, False,
#                                  **extra_fields)
#
#
#     def create_superuser(self, username, email, password, **extra_fields):
#
#         user = self._create_user(username, email, password, True, True,
#                                  **extra_fields)
#         profile = UserProfile(user=user)
#         profile.save()
#         return user
#
#
# class User(AbstractBaseUser, PermissionsMixin):
#
#     id = models.AutoField(primary_key=True)
#
#     username = models.CharField(max_length=200, unique=True)
#     email = models.EmailField(unique=True)
#
#
#     ADMINISTRATOR = 'ADMINISTRATOR'
#     USER = 'USER'
#     CLIENT = 'CLIENT'
#     user_role_choices = (
#                         (ADMINISTRATOR , 'Administrator user'),
#                         (USER , 'Default user'),
#                         (CLIENT , 'Client user'),
#                         )
#     user_role = models.CharField(max_length=255, choices=user_role_choices, default=USER)
#
#
#     # is_admin = models.BooleanField(default=False)
#
#     is_active = models.BooleanField(default=True)
#
#     email_confirmed = models.BooleanField(default=False)
#
#     is_staff = models.BooleanField(default=False)
#
#     created_on_utc      = models.DateTimeField(auto_now_add=True, null=True, editable=False)
#     last_modified_utc   = models.DateTimeField(auto_now=True, null=True)
#
#
#     objects = MyUserManager()
#
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']
#
#     primary_rm = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='rm_user')
#
#     def __str__(self):
#         return 'User - ' + self.full_name
#
#     @property
#     def full_name(self):
#         profile = self.profile
#         if profile:
#             return self.profile.full_name()
#         return ''
#
#     @property
#     def full_name_reverse(self):
#         profile = self.profile
#         if profile:
#             return self.profile.full_name_reverse()
#         return ''
#
#
#     def get_userprofile(self):
#         profile = UserProfile.objects.filter(user_id=self.id).first()
#         if profile is None:
#             return None
#         else:
#             return profile
#
#     profile = property(get_userprofile)
#

#
# class UserProfile(models.Model):
#     id = models.AutoField(primary_key=True)
#
#     user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name='user_for_profile')
#
#     # English Name
#     first_name = models.CharField(max_length=255, default='', blank=True)
#     middle_name = models.CharField(max_length=255, default='', blank=True)
#     last_name = models.CharField(max_length=255, default='', blank=True)
#
#     nickname = models.CharField(max_length=255, default='', blank=True)
#
#     # Avatar
#     # avatar = models.ImageField(upload_to="user_avatars", default='user_avatars/default_avatar.png', blank=True)
#
#     # Gender
#     MALE = 'MALE'
#     FEMALE = 'FEMALE'
#     OTHER = 'OTHER'
#     NOT_SPECIFIED = 'NOT_SPECIFIED'
#     USER_GENDER_CHOICES = ((MALE , 'MALE'),
#                                 (FEMALE , 'FEMALE'),
#                                 (OTHER , 'OTHER'),
#                                 (NOT_SPECIFIED , 'NOT_SPECIFIED'),
#                                 )
#     gender = models.CharField(max_length=255, choices=USER_GENDER_CHOICES, default=NOT_SPECIFIED)
#
#     # date of birth
#     date_of_birth = models.DateField(default=datetime.date(2000, 1, 1))
#
#     # Address
#     # address_0 = models.TextField(default='')
#     # address_1 = models.TextField(default='')
#
#     # cell number
#     # cell_number = models.CharField(max_length=255, default='', blank=True)
#
#     # website
#     personal_website = models.CharField(max_length=255, default='', blank=True)
#
#     created_on_utc      = models.DateTimeField(auto_now_add=True, null=True, editable=False)
#     last_modified_utc   = models.DateTimeField(auto_now=True, null=True)
#
#     def __str__(self):
#         return 'UserProfile - ' + self.full_name()
#
#     def full_name(self):
#         name = ''
#         if self.first_name:
#             name += self.first_name + ' '
#         if self.last_name:
#             name += self.last_name
#         return name
#
#

