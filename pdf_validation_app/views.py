from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from PyPDF2 import PdfReader, PdfWriter, PageObject
import qrcode
from PIL import Image
from django.core.files.base import ContentFile
from .models import PDFDocument
from django.views.decorators.csrf import csrf_exempt
import io
from django.utils.safestring import mark_safe
from io import BytesIO
import base64

# def generate_qr_code(request, document_id):
#     pdf_document = get_object_or_404(PDFDocument, id=document_id)

#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(pdf_document.data)
#     qr.make(fit=True)
#     qr_image = qr.make_image(fill_color="black", back_color="white")

#     image_buffer = io.BytesIO()
#     qr_image.save(image_buffer, format='JPEG')

#     filename = f"{pdf_document.id}_qr_code.jpg"
#     pdf_document.qr_code.save(filename, ContentFile(image_buffer.getvalue()))
#     pdf_document.save()

#     return JsonResponse({'status': 'success'})


def generate_qr_code(request, document_id):
    pdf_document = get_object_or_404(PDFDocument, id=document_id)

    # Generate QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(pdf_document.data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Create buffer to hold PDF file
    output_buffer = io.BytesIO()

    # Open PDF file
    with open(pdf_document.document_file.path, 'rb') as file:
        pdf_reader = PdfReader(file)
        pdf_writer = PdfWriter()

        # Iterate through PDF pages
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]

            # Add QR code image as an overlay on the page
            qr_image_pdf = io.BytesIO()
            qr_image.save(qr_image_pdf, format='PNG')
            qr_image_pdf.seek(0)
            qr_image_obj = PdfReader(qr_image_pdf).pages[0]
            merged_page = PageObject.merge_in_outlines(page, qr_image_obj)

            # Add the modified page to the new PDF document
            pdf_writer.add_page(merged_page)

        # Add EOF marker
        pdf_writer.add_metadata({})

        # Save the new PDF document to the buffer
        pdf_writer.write(output_buffer)

    # Save the new PDF document to the model field
    filename = f"{pdf_document.id}_modified.pdf"
    pdf_document.document_file.save(filename, ContentFile(output_buffer.getvalue()))
    pdf_document.save()

    return JsonResponse({'status': 'success'})





def my_view(request):
    # Generate a unique code
    unique_code = 'http://influencerhiring.com/'  # Replace this with your own code

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(unique_code)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Convert the QR code image to a data URI
    buffered = BytesIO()
    qr_image.save(buffered, format="PNG")
    qr_image_base64 = base64.b64encode(buffered.getvalue()).decode("ascii")
    qr_code_data_uri = f"data:image/png;base64,{qr_image_base64}"

    # Pass the QR code data URI and the unique code to the template context
    context = {
        'qr_code_data_uri': qr_code_data_uri,
        'unique_code': unique_code,
    }

    return render(request, 'home1.html', context)






@csrf_exempt
def validate_pdf_document(request):
    if request.method == 'POST':
        scanned_data = request.POST.get('scanned_data')
        pdf_document_id = request.POST.get('pdf_document_id')

        try:
            pdf_document = PDFDocument.objects.get(id=pdf_document_id)
            if pdf_document.data == scanned_data:
                return JsonResponse({'status': 'valid'})
            else:
                return JsonResponse({'status': 'invalid'})
        except PDFDocument.DoesNotExist:
            return JsonResponse({'status': 'not_found'})

    return JsonResponse({'status': 'error'})


def home1(request):
    pdf_documents = PDFDocument.objects.all()
    return render(request, 'home1.html', {'pdf_documents': pdf_documents})
