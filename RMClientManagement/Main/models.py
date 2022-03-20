import os
from Users.models import *

class Email(models.Model):

    # rm user
    rm = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='email_rm_user')

    # client user
    client = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='email_client_user')

    # sender
    sender = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='email_sender_user')

    # recieving email
    reciever_email = models.CharField(max_length=255, default='', blank=True)

    # subject
    subject = models.TextField(default='', blank=True)

    # body
    body = models.TextField(default='', blank=True)

    # token  - used by url to identify this email row
    uuid = models.CharField(max_length=255, default=uuid.uuid4)

    # created on
    created_on_utc      = models.DateTimeField(auto_now_add=True, null=True, editable=False)

    # last modifeid on
    last_modified_utc   = models.DateTimeField(auto_now=True, null=True)

class Document(models.Model):

    # name
    name = models.CharField(max_length=255, default='', blank=True)

    # File
    # url = models.CharField(max_length=255, default='', blank=True)
    document = models.FileField(upload_to='documents/%Y/%m/%d/', blank=True, null=True)

    # rm user
    uploaded_by_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='doc_uploaded_by_user')

    # rm user
    rm = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='doc_rm_user')

    # client user
    client = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='doc_client_user')

    # The email this document is related to
    email = models.ForeignKey(Email, on_delete=models.CASCADE, blank=True, null=True, related_name='doc_client_user')

    RM = 'RM'
    CLIENT = 'CLIENT'
    uploaded_by_choices = (
                        (RM , 'Relational Manager'),
                        (CLIENT , 'Client'),
                        )
    uploaded_by = models.CharField(max_length=255, choices=uploaded_by_choices, default=CLIENT)

    # created on
    created_on_utc      = models.DateTimeField(auto_now_add=True, null=True, editable=False)

    # last modifeid on
    last_modified_utc   = models.DateTimeField(auto_now=True, null=True)

    def extension(self):
        name, extension = os.path.splitext(self.document.name)
        return extension













