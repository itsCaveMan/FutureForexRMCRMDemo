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
        full_name = f'{self.user.first_name} + ' \
               f'{self.profilebasicdetails.middle_name} + ' \
               f'{self.user.last_name}'
        return full_name

class ProfileBasicDetails(BaseModel):
    '''
        fields that are general to any human user
    '''

    profile = models.OneToOneField(Profile, on_delete=models.PROTECT)

    # Name
    middle_name = models.CharField(max_length=255, default='', blank=True)

    # Gender
    gender = models.CharField(max_length=255, choices=globals.USER_GENDER_CHOICES, default=globals.UNDEFINED_GENDER)

    # Date of birth
    date_of_birth = models.DateField(default=datetime.date(2000, 1, 1))

class ProfileExtendedDetails(BaseModel):
    '''
        fields that usage can very and evolve
    '''

    profile = models.OneToOneField(Profile, on_delete=models.PROTECT)

    role = models.CharField(max_length=255, choices=globals.USER_ROLE_CHOICES, default=globals.UNDEFINED_ROLE)

    managing_rm = models.ForeignKey(User, on_delete=models.PROTECT)

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





