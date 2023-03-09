# Esploro SWORD deposit
This application is a web form for depositing ETDs into UMs Esploro environment using the SWORD protocol.

For more information on Esploro: 
[Ex Libris Esploro](https://www.exlibrisgroup.com/products/esploro-research-services-platform/)

For more information on configuring SWORD in Esploro:
[SWORD Deposits](https://developers.exlibrisgroup.com/esploro/integrations/sword/)

## Components
* This is built on [Flask](https://flask.palletsprojects.com/en/1.1.x/), a web app framework for Python.
* Front end uses [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) templates (built into Flask) and 
[Bootstrap](https://getbootstrap.com/) for styling.
* For the full list of required Python libraries, check requirements.txt, but in general it requires 
[lxml](https://lxml.de/) and [requests](https://requests.readthedocs.io/en/master/).
All other libraries are built in to Python Standard Library.

## How it works
### User journey
1. User connects to the app via SSO
2. User clicks button to ORCID
3. User authenticates via ORCID
4. ORCID redirects back to the APP with user's ORCID ID and Token
5. App deposits ORCID ID and Token into Alma/Esploro via API
6. User sees "Congratulations" page on successful connection

### Tech
1. https://github.com/singingwolfboy/flask-dance
2. something else


## Azure/Docker
This app is Dockerized to work in Azure. For more information on deploying, see the next section:

# Python/Flask tutorial sample for Visual Studio Code

* This sample contains the completed program from the tutorial, make sure to visit the link: 
[Using Flask in Visual Studio Code](https://code.visualstudio.com/docs/python/tutorial-flask). Intermediate steps are 
not included.
* It also contains the Dockerfile and uwsgi.ini files necessary to build a container with a production server. 
The resulting image works both locally and when deployed to Azure App Service. See 
[Deploy Python using Docker containers](https://code.visualstudio.com/docs/python/tutorial-deploy-containers).

## Navigation

The `startup.py` file, for its part, is specifically for deploying to Azure App Service on Linux without containers. 
Because the app code is in its own *module* in the `app` folder (which has an `__init__.py`), trying to start the 
Gunicorn server within App Service on Linux produces an "Attempted relative import in non-package" error. The 
`startup.py` file, therefore, is just a shim to import the app object from the `hello_app` module, which then allows 
you to use startup:app in the Gunicorn command line (see `startup.txt`).

## Contributing

Contributions to the sample are welcome. When submitting changes, also consider submitting matching changes to the 
tutorial, the source file for which is 
[tutorial-flask.md](https://github.com/Microsoft/vscode-docs/blob/master/docs/python/tutorial-flask.md).

Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, 
and actually do, grant us the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot automatically determines whether you need to provide a CLA and decorate the 
PR appropriately (e.g., label, comment). Simply follow the instructions provided by the bot. You will only need to do 
this once across all repos using our CLA.

## Additional details

* This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
* For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
* Contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

