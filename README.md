# ORCID Esploro Integration Application

## Libraries
Flask, Flask-Dance, OneSaml

## User flow
Users first select the option whether they have an ORCID iD or not. If they don't, the ORCID sign-up page opens in a new tab. Users are to complete the registration process then return back to the app at step 2. If they al;ready have an ORCID iD, they proceed directly to step 2. At step 2, users log in to UM via SSO. They then click the "Connect to ORCID" button which takes them through the ORCID OAuth process. Upon authorization they are returned to the app with a success message, which includes a link to their ORCID record and a link to the Scholarship@Miami (Esploro) repository.

## Data flow


