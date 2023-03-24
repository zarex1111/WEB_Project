import flask
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from base_config import base_config
from email_messages import messages

blueprint = flask.Blueprint(
    "email_sender",
    __name__,
    template_folder='templates'
)

password = 'f9x5sxfunCnRnWUXzhBb'
sender = 'doodle.testing@mail.ru'


@blueprint.route('/api/send_to_<string:email>/<int:id>')
def send_a_letter(email, id):
    msg = MIMEMultipart()

    text = messages[id]['message']

    msg.attach(MIMEText(text, 'plain'))

    server = smtplib.SMTP('smtp.mail.ru: 465')
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, email, msg.as_string())
    server.quit()

    return flask.render_template('email.html', message_text=messages[id]['message_on_page'], title="А вам письмо", **base_config)