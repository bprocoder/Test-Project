from django.db import models

# Create your models here.
class PDFDocument(models.Model):
    document_file = models.FileField(upload_to='pdf_documents/')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    data = models.CharField(max_length=255)