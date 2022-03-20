from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.core.mail import send_mail, EmailMessage

from .models import Document, Email
from Users.models import User, UserProfile


# ==============   Misc   ==============
def dashboard(request):
    '''
        create default user "RM user"(Relational Manager) if the default user is not created
        Logs the default user in if the request user is not logged in

        Queries the total number of:
            1. Clients belonging to this RM
            2. Emails belonging to this RM
            3. Documents belonging to this RM

    :param request:
    :return: render
    '''
    if request.user.is_anonymous:
        default_user = User.objects.filter(email="default@example.com").first()
        if not default_user: # default user does not exist, create default user
            user = User.objects.create_user(
                                email='default@example.com',
                                username='default_rm',
                                password='1234Abcd!')
            user.is_active = True
            user.is_superuser = True
            user.email_confirmed = True
            user.is_staff = True
            user.save()

            profile = UserProfile()
            profile.user = user
            profile.first_name = 'default'
            profile.last_name = 'user'
            profile.save()
            default_user = user

        # log in default user
        login(request, default_user, backend='django.contrib.auth.backends.ModelBackend')

    context = {
        'client_count' : User.objects.filter(primary_rm=request.user).count(),
        'email_count' : Email.objects.filter(rm=request.user).count(),
        'document_count': Document.objects.filter(uploaded_by_user=request.user).count()
    }
    return render(request, 'dashboard.html', context)



# ==============   Client CRUD   ==============
class Clients(View):
    '''
        Generic Class View to simply return all Client users belonging to this logged in RM user
    '''
    def get(self, request):
        context = {
            'all_rm_clients': User.objects.filter(primary_rm__id=request.user.id),
        }
        return render(request, 'clients.html', context)

class Client(View):
    '''
        Generic Class View to handle the CRUD of Client Users
    '''
    def get(self, request, client_id:int):
        '''
            Return a page view that details a single client
        :param request:
        :param client_id:
        :return:
        '''
        context = {}
        try:
            context = {
                'client': User.objects.get(id=client_id),
                'all_client_documents': Document.objects.filter(client_id=client_id)
            }
        except:
            return redirect('/clients/')
        return render(request, 'client.html', context)

    def post(self, request):
        '''
            Create a new client User
            The new client will belong to the current session/logged in RM User
        :param request:
        :return:
        '''
        new_client = _create_user(
            email = request.POST.get('email'),
            username = request.POST.get('email'),
            password = '1234Abcd!',
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            is_superuser = False,
            is_staff = False
        )
        new_client.primary_rm = request.user
        new_client.user_role = User.CLIENT
        new_client.save()

        # print(request.POST.get('email'))
        # create client
        # return HttpResponse(str([i for i in request.POST.items()]))
        return redirect(f'/client/{new_client.id}')



# ==============   Documents   ==============
class RequestDocument(View):
    '''
        Generic Class View to handle the RM's 'request document' form
        This view will
            1. save/write the document
            2. create a document db record
            3. create a email db record
            4. related the document to the email
            5. send the notification email to the client
    '''
    def post(self, request):

        client = User.objects.get(id=request.POST.get('client_id'))

        file = request.FILES['requested_file']

        # create document
        doc = Document()
        doc.name = file.name
        doc.document = file
        doc.uploaded_by_user = request.user
        doc.rm = request.user
        doc.client = client
        doc.email = None
        doc.uploaded_by = Document.RM
        doc.save()

        # create email
        email = Email()
        email.sender = request.user
        email.rm = request.user
        email.client = client
        email.reciever_email = client.email
        email.subject = request.POST.get('subject')
        email.body = request.POST.get('body')
        email.save()

        doc.email = email
        doc.save()

        email = {
            'subject': request.POST.get('subject'),
            'plain_body': request.POST.get('body'),
            'sender_title_and_email': 'RM name here <user_email@futureforex.com>',
            'recievers': ['client@email.com',],
            'html_body': request.POST.get('body'),
            'attachment_names': [''],
        }
        email_wrapper(email)

        return redirect(f'/client/{client.id}')

class ClientSubmitDocument(View):
    '''
        Generic Class View to handle client's document request form submission
        this view will:
            1. save/write the document
            2. create a document db record
            3. related the document to the RM's requesting email
            4. send the notification email to the RM of the fulfilled document request
    '''
    def get(self, request, token_uuid):
        '''
            returns the client requested document form page/view
        :param request:
        :param token_uuid:
        :return:
        '''
        context = {
            'email': Email.objects.get(uuid=token_uuid)
        }
        return render(request, 'client_document_request.html', context)

    def post(self, request):
        '''
            This method handles the client's requested document form submission
        :param request:
        :return:
        '''
        email = Email.objects.get(uuid=request.POST.get('token'))
        client = email.client
        rm = email.rm

        file = request.FILES['requested_file']

        # create document in db
        doc = Document()
        doc.name = file.name
        doc.document = file
        doc.uploaded_by_user = client
        doc.rm = rm
        doc.client = client
        doc.email = email
        doc.uploaded_by = Document.CLIENT
        doc.save()

        email = {
            'subject': 'CLIENT UPLOADED REQUESTED FILE',
            'plain_body': f'a client has uploaded the request file for email "{email.subject}" '
                          f'and file "{doc.name}". click here to view: http://127.0.0.1:8000/client/{client.id}',
            'sender_title_and_email': 'Internal Tooling <no-reply@futureforex.com>',
            'recievers': [rm.email],
            'html_body': '',
            'attachment_names': [''],
        }
        email_wrapper(email)

        return redirect(f'/client/{client.id}')



# ==============   Utility   ==============
def email_wrapper(email):
    '''
        A utility function to send a email's using Django email library
        this utility function also support including attachments
        therefor it utilizes EmailMessage rather than the simpler send_mail
    :param email:
    :return:
    '''
    # TODO: implement email host settings
    return

    # create list of File's to attach to email
        # https://stackoverflow.com/questions/34661771/django-emailmessage-attachments-attribute
    attachments = []  # start with an empty list
    for filename in data['filenames']:
        # create the attachment triple for this filename
        content = open(filename, 'rb').read()
        attachment = (filename, content, 'application/pdf')
        # add the attachment to the list
        attachments.append(attachment)

    # Send email
    email = EmailMessage(email.subject, email.body, f'{email.sender.full_name} {email.sender.email}',
                         [email.reciever], attachments=attachments)
    email.send()


def _create_user(
        email:str = '',
        username:str = '',
        password:str = '',
        first_name:str = '',
        last_name:str = '',
        is_superuser:bool = False,
        is_staff:bool = False,
        ):
    '''
        A utility function to create a User with a UserProfile
    :param email:
    :param username:
    :param password:
    :param first_name:
    :param last_name:
    :param is_superuser:
    :param is_staff:
    :return:
    '''
    user = User.objects.create_user(
        email=email,
        username=username,
        password=password)
    user.is_active = True
    user.is_superuser = is_superuser
    user.is_staff = is_staff
    user.email_confirmed = True
    user.save()

    profile = UserProfile()
    profile.user = user
    profile.first_name = first_name
    profile.last_name = last_name
    profile.save()

    return user



