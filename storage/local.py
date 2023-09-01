import requests
from pdf_generator import settings


def save(file_path: str, file_name: str):
    url = settings.CDN_BASE_URL + 'upload'
    file = open(file_path, 'rb')
    files = [
        ('files', (file_name, file, 'application/pdf'))
    ]

    session = requests.Session()
    session.trust_env = False # Because i use container, i have to set False for trust_env
    response = session.request("POST", url, files=files)
    if not response.ok:
        raise Exception('An error occurred while uploading file.')
