import os
from dotenv import load_dotenv, find_dotenv

load_dotenv()

DEBUG = (bool(int(os.getenv("DEBUG", 1))))

urls_docs_swagger_env = list(
    filter(lambda x: str(x).startswith("URL_DOCS_SWAGGER_SERVICE_"), os.environ.keys())
)
urls_docs_swagger = []
for env_key in urls_docs_swagger_env:
    item = os.getenv(env_key)
    if item:
        url, name = item.split(';')
        urls_docs_swagger.append({'url': url, 'name': name})
