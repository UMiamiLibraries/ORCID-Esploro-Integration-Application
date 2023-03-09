import os

from flask import Flask  # Import the Flask class
from flask_debugtoolbar import DebugToolbarExtension

from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.middleware.profiler import ProfilerMiddleware

app = Flask(__name__)    # Create an instance of the class for our use

#from . import utils

app.config.update(
    DEBUG=True,
    SECRET_KEY='wYc9PQRAp*jv9kv2VY17bGJN9S7IvQ',
    SAML_PATH=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saml'),
    MAIL_SERVER='smtp.umail.miami.edu',
    MAIL_PORT=25,
    #MAIL_USE_SSL=True
    EXL_APIKEY='l8xx685c01ea135645bc91db002f0e132b2f',
    ESPLORO_RESEARCHER_API='https://api-na.hosted.exlibrisgroup.com/esploro/v1/researchers/',
    ALMA_USER_API='https://api-na.hosted.exlibrisgroup.com/almaws/v1/users/',
    ORCID_OAUTH_CLIENT_ID='APP-L0SEY2X8CZ86A586',
    ORCID_OAUTH_CLIENT_SECRET='9d2cccc3-6595-49e7-8ebf-1143aa37c133',
    SLACK_WEBHOOK='https://hooks.slack.com/services/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',
    EMAIL_ADMIN='eprieto502@miami.edu',
    EMAIL_TECHNICAL='cgb37@miami.edu',
    EMAIL_SUPPORT='repository.library@miami.edu',
    ORCID_URL='https://sandbox.orcid.org',
    ORCID_SANDBOX=True
)
mail = Mail(app)

from . import app # For application discovery by the 'flask' command.
from . import views  # For import side-effects of setting up routes.

# app.debug = True
# toolbar = DebugToolbarExtension(app)

#app.wsgi_app = ProfilerMiddleware(app.wsgi_app)