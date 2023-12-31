import time
from django.db.models import Q
from datetime import datetime
from notes.models import Report, Note
from pdf_generator.celery import app
from celery import shared_task
from users.models import CustomUser
from .report_utils import generate_pdf_report


@app.task
def generate_report_data_for_user(user_id: int, start_date, end_date):
    print(f"start date :{start_date}")
    print(f"end date :{end_date}")

    username = CustomUser.objects.only('username').get(pk=user_id).username
    notes = Note.objects.filter(
        Q(author_id=user_id) &
        Q(created_at__gte=start_date) &
        Q(created_at__lte=end_date)
    )
    time.sleep(10)
    context = {
        'notes': notes
    }

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f'{username}-Reports-{timestamp}'

    try:
        pdf_url = generate_pdf_report(context, 'reports/pdf_template.html', file_name)
    except Exception as ex:
        raise Exception(f'user : {user_id} - {ex}')

    Report.objects.create(
        author_id=user_id,
        file=file_name + '.pdf'
    )


@shared_task
def remove_reports():
    reports_to_delete = Report.objects.filter(read=True)
    reports_to_delete.delete()
