

# Pull a pre-built alpine docker image with nginx and python3 installed
FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

RUN apk --update add bash nano vim git openssh build-base libressl \
    libffi-dev libressl-dev libxslt-dev libxml2-dev xmlsec-dev xmlsec
RUN ssh-keygen -A

# Indicate where uwsgi.ini lives
ENV UWSGI_INI uwsgi.ini

# Tell nginx where static files live.
ENV STATIC_URL /app/static

# Set the folder where uwsgi looks for the app
WORKDIR /app

# Copy the app contents to the image
COPY src/app /app/app

# Copy Python Requirements
COPY src/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# ssl
COPY Env/Prod/docker/nginx/conf/nginx.conf.dist /etc/nginx/conf.d/nginx.conf.dist

