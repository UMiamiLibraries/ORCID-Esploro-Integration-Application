##
# view controllers for University of Miami ORCiD Esploro integration
##

from app import app
from flask import Flask, render_template, request, redirect, make_response, session, url_for, jsonify

from flask_dance.contrib.orcid import make_orcid_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error

from app.utils import slackmsg, sendemail
from app.apis import save_orcid_to_alma, get_exl_api, put_exl_api
from app.adfs import init_saml_auth, get_self_url, prepare_flask_request

##
# Create Flask-Dance blueprint for ORCiD
##

blueprint = make_orcid_blueprint(
    scope=['/read-limited', '/activities/update', '/person/update'],
    sandbox=app.config['ORCID_SANDBOX']
)

app.register_blueprint(blueprint)

##
 # render all errors the same way
 ##
@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(415)
@app.errorhandler(500)
@app.errorhandler(502)
@app.errorhandler(504)
def http_error_handler(error):
    return render_template('error.html')

##
# Receive SAML user data from UM login and redirect user to ORCiD
##
@app.route('/login/', methods=['GET', 'POST'])
def login():

    # handle case when user successfully logged into UM with caneid
    if 'samlUserdata' in session:
        success = True
        #print("**** IN LOGIN SAMLUSERDATA ****")
        #print(session)
        if len(session['samlUserdata']) > 0:
            #attributes = session['samlUserdata'].items()
            cnum = session['samlUserdata']['UMID'][0]
            firstname = session['samlUserdata']['FIRSTNAME'][0]
            lastname = session['samlUserdata']['LASTNAME'][0]
            #print('C# *****************')
            #print('C#:' + session['samlUserdata']['UMID'][0])
            return redirect(url_for("connect_orcid"))

    return render_template('login.html')


##
 # Provide route for ORCiD button
 ##
@app.route("/orcid")
def orcid():
    return redirect(url_for("orcid.login"))


##
 # Redirect for after user trusts UM from ORCiD
 ##
@oauth_authorized.connect
def redirect_to_next_url(blueprint, token):
    # save the orcid trust token in the blueprint storage backend
    blueprint.token = token
    session['token'] = token
    print("************* orcid token *************")
    print(token)
    print(token['orcid'])
    print(session['samlUserdata']['UMID'][0])

    # save token to Alma/Esploro through API
    orcid_status, token_status = save_orcid_to_alma(session['samlUserdata']['UMID'][0], token['orcid'])
    session['orcid_status'] = orcid_status
    session['token_status'] = token_status

    # slack webhook
    msg = session['samlUserdata']['UMID'][0] + " " + token['orcid'] + " " + str(orcid_status) + " " + str(token_status)
    slackmsg(msg)

    if orcid_status == 200:
        return redirect(url_for('success'))
    else:
        return redirect(url_for('fail'))


@oauth_error.connect
def oauth_error(self, error, error_description, error_uri):
    print("in oauth_error")
    print(error)
    print(error_description)
    print(error_uri)

    session['orcid_status'] = error

    #return redirect(url_for('fail'))


##
 # Render success if entire process finished
 ##
@app.route('/success', methods=['GET'])
def success():

    cnum = False
    firstname = False
    lastname = False
    orcid_id = False

    if 'samlUserdata' in session:
        if len(session['samlUserdata']) > 0:
            firstname = session['samlUserdata']['FIRSTNAME'][0]
            lastname = session['samlUserdata']['LASTNAME'][0]

    if 'token' in session:
        if len(session['token']) > 0:
            orcid_id = session['token']['orcid']

    return render_template(
        "success.html",
        firstname=firstname,
        lastname=lastname,
        orcid_id=orcid_id,
        orcid_url=app.config['ORCID_URL']
    )


@app.route('/create_orcid', methods=['GET', 'POST'])
def create_orcid():
    return render_template('create_orcid.html')


@app.route('/connect_orcid', methods=['GET', 'POST'])
def connect_orcid():
    return render_template('connect_orcid.html')

##
 # Render fail if the process fails
 ##
@app.route('/fail', methods=['GET'])
def fail():

    firstname = False
    lastname = False
    orcid_status = False
    token_status = False
    support_email = app.config['EMAIL_SUPPORT']

    if 'samlUserdata' in session:
        if len(session['samlUserdata']) > 0:
            firstname = session['samlUserdata']['FIRSTNAME'][0]
            lastname = session['samlUserdata']['LASTNAME'][0]

    if 'orcid_status' in session:
        orcid_status = session['orcid_status']
        session.pop('orcid_status', None)

    if 'token_status' in session:
        token_status = session['token_status']

    session.clear()

    return render_template(
        "fail.html", 
        firstname=firstname,
        lastname=lastname,
        orcid_status=orcid_status,
        token_status=token_status,
        support_email=support_email
    )


##
# Render down for maintenance page
##
@app.route('/down', methods=['GET'])
def down():
    return render_template("down.html")


##
# Render index page for app
##
@app.route('/', methods=['GET', 'POST'])
def index():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    errors = []
    error_reason = None
    not_auth_warn = False
    success_slo = False
    attributes = False
    paint_logout = False

    # if 'sso' in request.args:
    # return redirect(auth.login())
    # If AuthNRequest ID need to be stored in order to later validate it, do instead
    # sso_built_url = auth.login()
    # request.session['AuthNRequestID'] = auth.get_last_request_id()
    # return redirect(sso_built_url)
    if 'sso2' in request.args:
        return_to = '%slogin/' % request.host_url
        return redirect(auth.login(return_to))
    elif 'slo' in request.args:
        name_id = session_index = name_id_format = name_id_nq = name_id_spnq = None
        if 'samlNameId' in session:
            name_id = session['samlNameId']
        if 'samlSessionIndex' in session:
            session_index = session['samlSessionIndex']
        if 'samlNameIdFormat' in session:
            name_id_format = session['samlNameIdFormat']
        if 'samlNameIdNameQualifier' in session:
            name_id_nq = session['samlNameIdNameQualifier']
        if 'samlNameIdSPNameQualifier' in session:
            name_id_spnq = session['samlNameIdSPNameQualifier']
        return redirect(
            auth.logout(name_id=name_id, session_index=session_index,
                        nq=name_id_nq, name_id_format=name_id_format,
                        spnq=name_id_spnq))
    elif 'acs' in request.args:
        request_id = None
        if 'AuthNRequestID' in session:
            request_id = session['AuthNRequestID']

        auth.process_response(request_id=request_id)
        errors = auth.get_errors()
        not_auth_warn = not auth.is_authenticated()
        if len(errors) == 0:
            if 'AuthNRequestID' in session:
                del session['AuthNRequestID']
            session['samlUserdata'] = auth.get_attributes()
            session['samlNameId'] = auth.get_nameid()
            session['samlNameIdFormat'] = auth.get_nameid_format()
            session['samlNameIdNameQualifier'] = auth.get_nameid_nq()
            session['samlNameIdSPNameQualifier'] = auth.get_nameid_spnq()
            session['samlSessionIndex'] = auth.get_session_index()
            self_url = get_self_url(req)
            if 'RelayState' in request.form and self_url != request.form[
                'RelayState']:
                # To avoid 'Open Redirect' attacks, before execute the redirection confirm
                # the value of the request.form['RelayState'] is a trusted URL.
                return redirect(auth.redirect_to(request.form['RelayState']))
        elif auth.get_settings().is_debug_active():
            error_reason = auth.get_last_error_reason()
    elif 'sls' in request.args:
        request_id = None
        if 'LogoutRequestID' in session:
            request_id = session['LogoutRequestID']
        dscb = lambda: session.clear()
        url = auth.process_slo(request_id=request_id, delete_session_cb=dscb)
        errors = auth.get_errors()
        if len(errors) == 0:
            if url is not None:
                # To avoid 'Open Redirect' attacks, before execute the redirection confirm
                # the value of the url is a trusted URL.
                return redirect(url)
            else:
                success_slo = True
        elif auth.get_settings().is_debug_active():
            error_reason = auth.get_last_error_reason()

    if 'orcid_status' in session:
        if session['orcid_status'] == 'access_denied':
            return redirect(url_for('connect_orcid'))

    # return render_template('index.html')
    return render_template('down.html')


##
 # Return metadata for this app
 ##
@app.route('/metadata/')
def metadata():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = make_response(metadata, 200)
        resp.headers['Content-Type'] = 'text/xml'
    else:
        resp = make_response(', '.join(errors), 500)
    return resp


##############
# Entry point
##############

if __name__ == '__main__':
    app.run(debug=True)
