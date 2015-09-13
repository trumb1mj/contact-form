"""
Serves a simple contact form.
Takes email username and password as space separated arguments.
"""

import sys
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, Response, jsonify, render_template, url_for

app = Flask(__name__)

@app.route('/')
def media():
    url_for('static', filename='main.css')
    url_for('static', filename='background.png')
    url_for('static', filename='OptionsCity-Logo-Black.png')
    return

@app.route('/contact/')
def index():
    return render_template('index.html', message="Learn more about us by leaving your email here.")

@app.route('/send_email/<email_address>')
def send_email(email_address):

    # pass username and password as options to server
    EMAIL_HOST_USER = sys.argv[1]
    EMAIL_HOST_PASSWORD = sys.argv[2]

    # create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Thanks for your interest in OptionsCity!"
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = email_address

    #   message body
    html = '''<html><body><table style="text-align: left;">
                <tr>
                    <td>To quickly start hacking, grab an <a href="http://devservices.optionshop.com/mhacks">API Access Token URL</a>.</td>
                </tr>
                <tr>
                    <td>To learn more about our API, check out our <a href="https://devservices.optionshop.com/docs">docs</a>.</td>
                </tr>
                <tr>
                    <td>To learn more about our job opportunities, head to the <a href="http://www.optionscity.com/careers/">OptionsCity jobs</a> section.</td>
                </tr>
            </table></body></html>'''

    # record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(html, 'plain')
    part2 = MIMEText(html, 'html')

    # attach parts into message container.
    msg.attach(part1)
    msg.attach(part2)

    # send the message via local SMTP server.
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    s.sendmail(EMAIL_HOST_USER, email_address, msg.as_string())
    s.quit()

    return jsonify({"success": True})


if __name__ == '__main__':
    app.run()
