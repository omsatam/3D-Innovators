from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# def getPath(folder):
#     return 'dicom/dicomFiles/'+ str(folder)
# Create your models here.
# def _upload_path(instance,filename):
#     return instance.get_upload_path(filename)
# # user = models.

# # class Profile(models.Model):
# #     user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
# class saveDicomFiles(models.Model):
#     sno = models.AutoField(primary_key = True)
#     # user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
#     username = models.CharField(max_length=20)
#     dicomFiles = models.FileField(upload_to = _upload_path , default = '')
#     stlFiles = models.FileField(upload_to = 'dicom/stlFiles/' , default = '')
#     def get_upload_path(self,filename):
#         return 'dicom/dicomFiles/' + str(self.username) + "/" + filename
#     class Meta:
#         app_label = 'stlConverter'
#     def __str__(self):
#         return self.username

class saveContactData(models.Model):
    sno = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    email = models.EmailField(max_length=35,default = "",null = True)
    feedback = models.TextField(max_length=400,default = "",null = True)
    contactDateTime = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.fname + " " + self.lname + " written"