# production config settings
import os

from flask import Flask  # Import the Flask class

from flask_mail import Mail
# from flask_debugtoolbar import DebugToolbarExtension
# from werkzeug.middleware.profiler import ProfilerMiddleware
app = Flask(__name__)    # Create an instance of the class for our use

app.config.update(
    DEBUG=True,
    SECRET_KEY='$4d^URjlhGQzRAfCW%t13Zc5w9Wd##',
    SAML_PATH=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saml'),
    MAIL_SERVER='smtp.umail.miami.edu',
    MAIL_PORT=25,
    #MAIL_USE_SSL=True
    EXL_APIKEY='l8xxb34ba7ed439b4b8096615fd11993e5ec',
    ESPLORO_RESEARCHER_API='https://api-na.hosted.exlibrisgroup.com/esploro/v1/researchers/',
    ALMA_USER_API='https://api-na.hosted.exlibrisgroup.com/almaws/v1/users/',
    ESPLORO_TOKEN_API='https://api-na.hosted.exlibrisgroup.com/esploro/v1/researchers/{orcid}/token?',
    ORCID_OAUTH_CLIENT_ID='APP-TQL0JRATUMCBFL5Q',
    ORCID_OAUTH_CLIENT_SECRET='9ac640ec-ef34-49c1-a8ee-e7dfbaeb972a',
    SLACK_WEBHOOK='https://hooks.slack.com/services/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',
    EMAIL_ADMIN='eprieto502@miami.edu',
    EMAIL_TECHNICAL='cgb37@miami.edu',
    EMAIL_SUPPORT='repository.library@miami.edu',
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