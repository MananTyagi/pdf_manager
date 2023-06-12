from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import pdf_file_model, comment, UserInvitationRecord
from .forms import PdfUploadForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
import base64
from urllib.parse import urlencode
from urllib.parse import parse_qs
from users. models import CustomUser
import smtplib


secret_key = 'mysecretkeyblablabla1234'

# Create your views here.
def send_mail_for_invite( email, encoded):
    try:
        subject = 'Invitation for collaboration to a document'
        message = f'Hi! click on the following link to view  pdf http://127.0.0.1:8000/view_invited_pdf/{encoded}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message , email_from ,recipient_list, fail_silently=False )
    except Exception as e:
        raise smtplib.SMTPException
    
    
    
def homepage(request):
        return render(
        request=request,
        template_name = "app/homepage.html",
    )
        
        
def upload_pdf_file(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PdfUploadForm(request.POST, request.FILES)
            if form.is_valid():
                pdf_file = form.cleaned_data['pdf_file']
                
                if not pdf_file.name.endswith('.pdf'):
                    messages.error(request, "This is not a PDF file. Please upload a valid PDF file")
                    return redirect('upload')
                form.instance.Owner = request.user

                form.save()
                messages.success(request, "Your Pdf file is uploaded successfully! you can add another one")
                return redirect('upload')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        else:
            form = PdfUploadForm()
        return render(request, "app/upload_pdf.html", {"form": form})
    else:
        messages.info(request, "Please login to your account first")
        return redirect("homepage")

    
    
def dashboard(request):
    
    if request.user.is_authenticated:
        owned_pdf_files=pdf_file_model.objects.filter(Owner=request.user)
        invited_records = UserInvitationRecord.objects.filter(user=request.user)
        invited_pdf_files = [record.pdf_file for record in invited_records]
        print(invited_pdf_files)
        print(list(owned_pdf_files))
        pdf_files=invited_pdf_files + list(owned_pdf_files)

        return render(request, 'app/dashboard.html', {'pdf_files': pdf_files})
        
    else:
        messages.info(request, "Please login to your account first to view all pdfs")
        return redirect("homepage")


    
    
def pdf_file_viewer(request, id):
    if request.user.is_authenticated:
        pdf_file_object=pdf_file_model.objects.get(id=id)
        comments=comment.objects.filter(pdf=pdf_file_object)
        print(pdf_file_object.pdf_file.url)
        print(comments)
        return render(request, 'app/pdf_file.html', {'pdf_file_object': pdf_file_object, 'comments':comments})
        
    else:
        messages.info(request, "Please login to your account first to view pdf")
        return redirect("homepage")
    
    

@login_required    
def invite_form(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        print(request.body)
        email = request.POST.get('email')
        id = request.POST.get('id')
             
        invited_user=CustomUser.objects.filter(email=email)
        print(invited_user,  "http://manan.pythonanywhere.com/")
        if invited_user.exists():
            pdf_file_object=pdf_file_model.objects.get(id=id)
            new_invite_record = UserInvitationRecord(user=invited_user.first(), pdf_file=pdf_file_object)
            new_invite_record.save()
        
        data = {'pdf_id': id, 'secret_key': secret_key}
        encoded_data = base64.urlsafe_b64encode(urlencode(data).encode()).decode()
        send_mail_for_invite(email, encoded_data)
        response_data = {'message': 'Email sent successfully!'}
        return JsonResponse(response_data)
    
    response_data = {'message': 'Invalid request'}
    return JsonResponse(response_data, status=400)


def view_invited_pdf(request, encoded):
    decoded_data = base64.urlsafe_b64decode(encoded).decode()
    parsed_data = parse_qs(decoded_data)
    pdf_id = int(parsed_data['pdf_id'][0])
    secret_key_ = parsed_data['secret_key'][0]
    print(pdf_id,secret_key_)
    
    if secret_key_==secret_key:
        pdf_file_object=pdf_file_model.objects.get(id=pdf_id)
        if pdf_file_object is not None:
            comments=comment.objects.filter(pdf=pdf_file_object)
            return render(request, 'app/view_invited_pdf.html', {'pdf_file_object': pdf_file_object, 'comments': comments})

    response_data ={'message': 'Invalid request'}
    return JsonResponse(response_data, status=400)


def comment_adder(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        print(request.body)
        comment_text = request.POST.get('comment')
        id = request.POST.get('id')
        try: 
            pdf_file_object=pdf_file_model.objects.get(id=id)
            new_comment = comment(comment=comment_text, pdf=pdf_file_object)
            new_comment.save()
            response_data ={'message':"Succesfully add comment to the pdf"}
        except:
            response_data ={'message':"internal servererror"}
        return JsonResponse(response_data)
    
    response_data = {'message': 'Invalid request'}
    return JsonResponse(response_data, status=400)



def invitechecker(pdf_file_object, user_name):
    invite_records = UserInvitationRecord.objects.filter(pdf_file=pdf_file_object)
    for record in invite_records:
        if record.user.username==user_name:
            return True
    return False
    
    
  
@login_required
def search_pdf(request):
    if request.method == 'GET' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        pdf_name = request.GET.get('query')
        print(pdf_name)
        if pdf_name:
            try:
                pdf_file = pdf_file_model.objects.get(pdf_name__iexact=pdf_name)
                current_user=request.user
                if pdf_file.Owner==request.user or invitechecker(pdf_file,current_user.username):
                    data = {
                        'pdf_name': pdf_file.pdf_name,
                        'first_name': pdf_file.Owner.first_name,
                        'last_name': pdf_file.Owner.last_name,
                        'pdf_id': pdf_file.id
                    }
                    return JsonResponse(data)
                else:
                    error_message = 'No PDF file found with the given name.'
                    return JsonResponse({'error_message': error_message}, status=404)
                    
            except pdf_file_model.DoesNotExist:
                error_message = 'No PDF file found with the given name.'
                return JsonResponse({'error_message': error_message}, status=404)

    return JsonResponse({})

        

    