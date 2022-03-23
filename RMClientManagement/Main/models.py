
from django.db import models

import uuid as uuid
import os

from Users.models import User
from RMClientManagement import globals
from RMClientManagement.globals import BaseModel


class Email(BaseModel):

    # User who created this email
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sender_user')

    # User intended to receive this email
    recipient = models.ForeignKey(User, on_delete=models.PROTECT, related_name='recipient_user')

    # email subject
    subject = models.TextField(default='', blank=True)

    # email body
    body = models.TextField(default='', blank=True)

    # token  - used by url to identify this email
    uuid = models.CharField(max_length=255, default=uuid.uuid4)

class Document(BaseModel):

    # Who uploaded this document
    uploaded_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='doc_uploaded_by_user')

    # Email record this document is linked to
    email = models.ForeignKey(Email, on_delete=models.PROTECT, related_name='doc_client_user')

    # The name of the uploaded document
    document_name = models.CharField(max_length=255, default='', blank=True)

    # a custom name given to this document
    custom_name = models.CharField(max_length=255, default='', blank=True)

    # File
    document = models.FileField(upload_to='documents/%Y/%m/%d/', blank=True, default='DEFAULT/_placeholder.txt')

    # Gender
    document_type = models.CharField(max_length=255, choices=globals.DOCUMENT_TYPE_CHOICES, default=globals.UNDEFINED_DOCUMENT_TYPE)

    def extension(self):
        '''
            return the file type of this document
        :return:
        '''
        name, extension = os.path.splitext(self.document.name)
        return extension













