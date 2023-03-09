# production config settings
import os

from flask import Flask  # Import the Flask class

from flask_mail import Mail
# from flask_debugtoolbar import DebugToolbarExtension
# from werkzeug.middleware.profiler import ProfilerMiddleware
app = Flask(__name__)    # Create an instance of the class for our use

app.config.update(
    DEBUG=True,
    SECRET_KEY='',
    SAML_PATH=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saml'),
    MAIL_SERVER='',
    MAIL_PORT=25,
    #MAIL_USE_SSL=True
    EXL_APIKEY='',
    ESPLORO_RESEARCHER_API='https://api-na.hosted.exlibrisgroup.com/esploro/v1/researchers/',
    ALMA_USER_API='https://api-na.hosted.exlibrisgroup.com/almaws/v1/users/',
    ESPLORO_TOKEN_API='https://api-na.hosted.exlibrisgroup.com/esploro/v1/researchers/{orcid}/token?',
    ORCID_OAUTH_CLIENT_ID='',
    ORCID_OAUTH_CLIENT_SECRET='',
    SLACK_WEBHOOK='',
    EMAIL_ADMIN='',
    EMAIL_TECHNICAL='',
    EMAIL_SUPPORT='',
    ORCID_URL='https://orcid.org',
    ORCID_SANDBOX=False
)
mail = Mail(app)

from . import app # For application discovery by the 'flask' command.
from . import views  # For import side-effects of setting up routes.

# app.debug = True
# toolbar = DebugToolbarExtension(app)
#
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app)