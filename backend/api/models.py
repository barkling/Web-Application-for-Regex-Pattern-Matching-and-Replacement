from django.db import models

# Create your models here.

class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    original_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10)  # csv or xlsx
    created_at = models.DateTimeField(auto_now_add=True)
    processed_data = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return self.original_filename
