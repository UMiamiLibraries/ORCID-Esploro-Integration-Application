from app import app
from app.onelogin.saml2.auth import OneLogin_Saml2_Auth
from app.onelogin.saml2.utils import OneLogin_Saml2_Utils

def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=app.config['SAML_PATH'])
    return auth

def get_self_url(req):
    url = OneLogin_Saml2_Utils.get_self_url(req)
    return url

##
 # filter request in case of proxys or balancers
 ##
def prepare_flask_request(request):
    # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'script_name': request.path,
        'get_data': request.args.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': True,
        'post_data': request.form.copy()
    }