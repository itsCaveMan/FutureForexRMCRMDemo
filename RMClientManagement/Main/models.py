from django.db import models

import uuid as uuid
import os

from Main.emailing import email_wrapper
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

    def recipient_notification_email(self, document=None):
        email = {
            'subject': self.subject,
            'plain_body': self.body,
            'html_body': self.body,
            'sender_title_and_email': f"<RM Name> <user_email@futureforex.com>",
            'recievers': [self.recipient.id],
        }
        if document:
            email['attachment_names'] = document.document.url,
        email_wrapper(email)

    def requester_notification_email(self, document=None):
        email = {
            'subject': self.subject,
            'plain_body': self.body,
            'html_body': self.body,
            'sender_title_and_email': f"<RM Name> <user_email@futureforex.com>",
            'recievers': [self.sender.id],
        }
        if document:
            email['attachment_names'] = document.document.url,
        email_wrapper(email)

class Document(BaseModel):

    # Who uploaded this document
    uploaded_by = models.ForeignKey(User, on_delete=models.PROTECT)

    # Email record this document is linked to
    email = models.ForeignKey(Email, on_delete=models.SET_NULL, blank=True, null=True) # TODO: nullable due to form validation

    # a custom name given to this document
    custom_name = models.CharField(max_length=255, default='', blank=True)

    # File
    document = models.FileField(upload_to='documents/%Y/%m/%d/', blank=True, default='DEFAULT/_placeholder.txt')

    # Gender
    document_type = models.CharField(max_length=255, choices=globals.DOCUMENT_TYPE_CHOICES, default=globals.UNDEFINED_DOCUMENT_TYPE)

    def extension(self):
        '''
            return the file type of this document
            e.g ".jpg"
        '''
        name, extension = os.path.splitext(self.document.name)
        return extension

    def name(self):
        '''
            return the name of the document
            e.g "scan_001.png"
        '''
        return os.path.basename(self.document.name)










