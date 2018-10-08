import os

username = os.environ.get('IBM_USERNAME', 'dc554890-1e5e-4488-8194-e5549ffcb1a2')
password = os.environ.get('IBM_PASSWORD', 'IOWx0ee35iQT')
version = os.environ.get('IBM_VERSION', '2017-09-21')
url = os.environ.get('IBM_URL', 'https://gateway.watsonplatform.net/tone-analyzer/api')