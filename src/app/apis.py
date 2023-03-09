from app import app

from flask import session
from requests import get, put, post
from json import dumps as json_dumps
import json
from time import sleep

### Alma API functions

##
 # save ORCID and trust token (if researcher) to Alma/Esploro user account
 ##
def save_orcid_to_alma(cnum, orcid_id):

    orcid_status = False
    token_status = False

    # search for orcid in two places in user object and return if found
    def extract_orcid_from_user(user_obj):

        alma_orcid_id = False

        def get_orcid(identifiers):
            if not identifiers: return False
            orcid = False
            for identifier in identifiers:
                if identifier['id_type']['value'] == 'ORCID':
                    orcid = identifier['value']
                    break
            return orcid

        # the orcid can exist in two places in the user data tree (at least?)
        alma_orcid_id = get_orcid(user_obj.get('user_identifier'))
        if not alma_orcid_id:
            if user['is_researcher']:
                try:
                    alma_orcid_id = get_orcid(user_obj.get('researcher').get('user_identifier'))
                except AttributeError:
                    print("no researcher user_idenfier")

        return alma_orcid_id

    # get alma user
    user = get_exl_api(app.config['ALMA_USER_API'], cnum)


    if user.status_code == 200:
        # check for existing orcid
        user = user.json()
        orcid_id_alma = extract_orcid_from_user(user)

        # create new orcid object in user data tree and send to alma user account
        if not orcid_id_alma:

            print("user does not have orcid")

            new_orcid_id = {
                "id_type": {
                    "desc": "ORCID",
                    "value": "ORCID"
                },
                "note": None,
                "segment_type": "Internal",
                "status": "ACTIVE",
                "value": orcid_id
            }
            user['user_identifier'].append(new_orcid_id)

            #send without any user roles
            #roles - if the incoming list does not contain roles, existing roles will be kept.
            try:
                if user['user_role']:
                    del user['user_role']
            except KeyError:
                print("no 'user_role'")

            orcid_put = put_exl_api(app.config['ALMA_USER_API'], cnum, user)
            orcid_status = orcid_put.status_code

        else:

            # check for mismatch
            if orcid_id != orcid_id_alma:
                print('mismatched orcid')
                orcid_status = 'mismatch'

            # otherwise return success code since orcid already existed in alma user
            else:
                print('orcid exists and matches')
                orcid_status = 200

        # check if researcher then save the token
        researcher = get_exl_api(app.config['ESPLORO_RESEARCHER_API'], cnum)
        if researcher.status_code == 200:
            print("is researcher")
            if orcid_status == 200:
                token_status = esploro_token_api()
            else:
                token_status = 'token_not_saved'

            # researcher = researcher.json()
            # if researcher['researcher']['profile_identifier_url']:
            #    session['profile_identifier_url'] = researcher['researcher']['profile_identifier_url']

        # otherwise discard the token and set the response
        else:

            print("not researcher")
            token_status = 'not_researcher'

        # return response codes
        return orcid_status, token_status

    else:
        return False, False


##
 # make get request to ExLibris API
 ##
def get_exl_api(api, cnum):

    url = api + cnum

    headers = {
        'Accept': 'application/json'
    }
    payload = {
        'apikey': app.config['EXL_APIKEY']
    }

    # send request
    print("*** sending GET request ***")
    response = get(url, headers=headers, params=payload)
    print("*********GET RESPONSE*************")
    # print(response.text)
    print(response.status_code)

    return response


##
 # make put request to ExLibris API
 ##
def put_exl_api(api, cnum, user):

    url = api + cnum
    print(url)

    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'apikey': app.config['EXL_APIKEY']
    }

    # send request
    print("*** sending PUT request ***")
    response = put(url, headers=headers, params=payload, data=json_dumps(user))
    print("*********PUT RESPONSE*************")
    print(response.text)
    print(response.status_code)

    return response


### Esploro API functions


##
 # save ORCiD trust token to Esploro user account through Esploro API
 # NOTE: private to apis.py
 ##
def esploro_token_api():
    print("*** IN TOKEN API ***")
    if 'token' in session:
        url = app.config['ESPLORO_TOKEN_API'].format(orcid=session['token']['orcid'])
        print(url)

        token = {
            'access.token': session['token']['access_token'],
            'token.type': session['token']['token_type'],
            'refresh.token': session['token']['refresh_token'],
            'expiry': str(session['token']['expires_in']),
            'scopes': ['/read-limited', '/activities/update', '/person/update']
        }
        print(token)

        headers = { 'Content-Type': 'application/json' }
        payload = { 'apikey': app.config['EXL_APIKEY'] }

        # send request inside loop that waits for ORCID to exist in Esploro user
        attempt_count = 0
        token_response = False
        while True:
            attempt_count += 1
            print('attempt',attempt_count)
            response = post(url, headers=headers, params=payload, json=token)
            token_response = response.status_code

            # move on if response has no errors
            if 'errorsExist' not in response.text: break

            # move on if we have tried too many times
            if attempt_count > 10: 
                token_response = 'too_many_token_retries'
                break

            # wait for a bit and repeat
            sleep(1)
                
        print("*********TOKEN PUT RESPONSE*************")
        print(response.text)
        print(response.status_code)
        return token_response
        
    else:
        print('no token session')
        return 'session_fail_token_save'
