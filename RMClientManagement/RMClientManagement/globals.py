from django.db import models


# ==============   Models   ==============
class BaseModel(models.Model):
    created_on_utc = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified_utc = models.DateTimeField(auto_now=True,)

    class Meta:
        abstract = True

RM = 'RM'
CLIENT = 'CLIENT'
UNDEFINED_ROLE = 'UNDEFINED_ROLE'
uploaded_by_choices = (
    (RM, 'Relational Manager'),
    (CLIENT, 'Client'),
    (UNDEFINED_ROLE, 'Undefined role'),
)

MALE = 'MALE'
FEMALE = 'FEMALE'
UNDEFINED_GENDER = 'UNDEFINED_GENDER'
USER_GENDER_CHOICES = (
    (MALE , 'Male'),
    (FEMALE , 'Female'),
    (UNDEFINED_GENDER , 'Undefined'),
)

OFFICIAL = 'OFFICIAL'
FINANCIAL = 'FINANCIAL'
UNDEFINED_DOCUMENT_TYPE = 'UNDEFINED_DOCUMENT_TYPE'
DOCUMENT_TYPE_CHOICES = (
    (OFFICIAL , 'Official document'),
    (FINANCIAL , 'Financial document'),
    (UNDEFINED_DOCUMENT_TYPE , 'Undefined document type'),
)
