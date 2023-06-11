from django.db import models
from users.models import CustomUser
# Create your models here.


class pdf_file_model(models.Model):
    def user_directory_path(instance, filename):
        return "user_{0}/{1}".format(instance.Owner.id, filename)
    
    pdf_name = models.CharField(max_length=100,blank=False, unique="True")
    Owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pdf_file = models.FileField(max_length=100, blank=False,upload_to=user_directory_path)
    
    
    def __str__(self):
        return self.pdf_name
    
class UserInvitationRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pdf_file = models.ForeignKey(pdf_file_model, on_delete=models.CASCADE)
    # additional fields for the relationship between user and PDF file
    class Meta:
        unique_together = ('user', 'pdf_file')
 
class comment(models.Model):
    comment = models.CharField(max_length=250,blank=False, default='None')
    pdf=models.ForeignKey(pdf_file_model, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.comment
    
    

    
