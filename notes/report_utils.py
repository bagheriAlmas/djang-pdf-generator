import os
from django.template.loader import get_template
from xhtml2pdf import pisa
from pdf_generator import settings


def generate_pdf_report(template_context: dict, template_name: str, file_name: str):
    template = get_template(template_name)
    html = template.render(template_context)

    file_directory = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(file_directory, exist_ok=True)

    pdf_filename = f'{file_name}.pdf'
    pdf_file_path = os.path.join(file_directory, pdf_filename)

    with open(pdf_file_path, 'wb') as pdf_file:
        pisa_status = pisa.CreatePDF(html, dest=pdf_file)
        if pisa_status.err:
            raise Exception(f'PDF creation error - {pisa_status.err}')

    pdf_url = os.path.join(settings.MEDIA_URL, 'reports', pdf_filename)

    return pdf_url
