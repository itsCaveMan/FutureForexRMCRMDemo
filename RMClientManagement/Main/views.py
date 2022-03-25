from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User

from Main.forms import ClientForm, RequestDocumentForm, SubmitDocumentForm
from .models import Document, Email
from Users.models import Profile, ProfileBasicDetails, ProfileExtendedDetails
from RMClientManagement import globals

def dashboard(request):
    '''
        Dashboard/Index/Landing page
        returns some basic metrics
    '''

    context = {
        'client_count' : User.objects.filter(profile__profileextendeddetails__managing_rm=request.user).count(),
        'email_count' : Email.objects.filter(sender=request.user).count(),
        'document_count': Document.objects.filter(uploaded_by=request.user).count()
    }
    return render(request, 'dashboard.html', context)

def clients(request):
    '''
        View all clients being managed by this RM
    '''
    context = {
        'new_client_form': ClientForm(),
        'all_rm_clients': User.objects.filter(profile__profileextendeddetails__managing_rm__id=request.user.id),
    }
    return render(request, 'clients.html', context)

class Client(View):
    '''
        Generic Class View to handle the CRUD of Client Users
    '''

    def get(self, request, client_id:int):
        '''
            Return a page view that details a single client
            with a form to update the client user
            a form to request a new document
            and all the documents and emails related to this client
        '''
        client = get_object_or_404(User, id=client_id)

        context = {
            'client': client,
            'client_crud': ClientForm(instance=client),
            'all_client_documents': Document.objects.filter(email__recipient=client),
            'all_client_emails': Email.objects.filter(sender=request.user, recipient__id=client_id),
            'request_document_form': RequestDocumentForm(initial={'sender': request.user, 'recipient': client}),
            'submit_document_form': SubmitDocumentForm(initial={'uploaded_by': request.user, 'email': Email()}),
        }
        return render(request, 'client.html', context)

    def post(self, request):
        '''
            Create a new client User
            The new client will belong to the current session/logged in RM User
        :param request:
        :return:
        '''

        client_id = request.POST.get('client_id')

        if client_id: # update
            form = ClientForm(request.POST or None, instance = get_object_or_404(User, id=client_id))
            if form.is_valid():
                user = form.save()
                return redirect('view_client', client_id=user.id)

        else: # create
            form = ClientForm(request.POST)

            if form.is_valid():
                user = form.save()
                profile = Profile(user=user)
                profile.save()
                ProfileBasicDetails(profile=profile).save()
                ProfileExtendedDetails(profile=profile, managing_rm=request.user, role=globals.CLIENT).save()
                return redirect('view_client', client_id=user.id)

        return redirect('clients')

class RequestDocument(View):
    '''
        Generic Class View to handle the RM's 'RequestDocument' and 'SubmitDocument' forms
    '''
    def post(self, request):

        request_form = RequestDocumentForm(request.POST)
        email = None
        if request_form.is_valid():
            email = request_form.save()

        doc_form = SubmitDocumentForm(request.POST, request.FILES)
        if doc_form.is_valid():
            doc = doc_form.save() # TODO: find solution to email failing validation. can not set in views
            doc.email = email
            doc.save()

        email.recipient_notification_email()

        return redirect('view_client', client_id=request_form.cleaned_data["recipient"].id)

class ClientSubmitDocument(View):
    '''
        Generic Class View to handle a client's document request form submission
    '''
    def get(self, request, token_uuid):
        '''
            returns the client requested document form page/view
        '''
        email = get_object_or_404(Email, uuid=token_uuid)
        context = {
            'email': email,
            'submit_document_form': SubmitDocumentForm(initial={'uploaded_by': email.recipient,
                                                                'email': email,
                                                                'document_type': globals.UNDEFINED_DOCUMENT_TYPE
                                                                }),
        }
        return render(request, 'client_document_request.html', context)

    def post(self, request):
        '''
            This method handles the client's requested document form submission
        '''
        email = get_object_or_404(Email, uuid=request.POST.get('token'))

        doc_form = SubmitDocumentForm(request.POST, request.FILES)
        if doc_form.is_valid():
            doc = doc_form.save()
            doc.email.requester_notification_email()

        return redirect('thank_you')

def thank_you(request):
    '''Thank you page'''
    return render(request, 'thank_you.html', {})


