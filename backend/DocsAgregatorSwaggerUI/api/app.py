
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

import api.conf as conf

app = Flask(__name__)

SWAGGER_URL = '/docs/swagger'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    None,
    config={
        'urls': conf.urls_docs_swagger
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=conf.DEBUG)
