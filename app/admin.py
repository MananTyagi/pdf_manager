from django.contrib import admin
from .models import pdf_file_model, comment, UserInvitationRecord
# Register your models here.
admin.site.register(comment)
admin.site.register(pdf_file_model)
admin.site.register(UserInvitationRecord)