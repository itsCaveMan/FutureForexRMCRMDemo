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
