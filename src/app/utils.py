from app import app
from flask import Flask, render_template
from slack_webhook import Slack
from flask_mail import Mail, Message

def slackmsg(msg):
    webhook = app.config['SLACK_WEBHOOK']
    slack = Slack(url=webhook)
    slack.post(text=msg)

# app.config['EMAIL_SUPPORT']
def sendemail():
    try:
        mail = Mail()
        msg = Message("ORCiD Authorization: A new ORCID Alma connection has been established by ",
                      sender="noreply@miami.edu",
                      recipients=[app.config['EMAIL_TECHNICAL']])

        msg.html = render_template("email.html")
        mail.send(msg)
    except Exception as ex:
        return str(ex)