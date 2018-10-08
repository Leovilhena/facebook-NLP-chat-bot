import os


# IBM
username = os.environ.get('IBM_USERNAME', '')
password = os.environ.get('IBM_PASSWORD', '')
version = os.environ.get('IBM_VERSION', '')
url = os.environ.get('IBM_URL', '')

# Facebook
access_token = os.environ.get('PAGE_ACCESS_TOKEN', '')