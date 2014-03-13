import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os
from settings import MAIL_USER, MAIL_PASS

def mail(to, subject, text, attach):
	msg = MIMEMultipart()
	
	msg['From'] = MAIL_USER
	msg['To'] = to
	print('>>Mail to: '+to+'<<')
	msg['Subject'] = subject
	
	msg.attach(MIMEText(text, 'plain', 'utf-8'))

	if(attach):
		for a in attach:
			if a.find('pdf') > 0:
				part = MIMEBase('application', 'pdf')
				part.set_payload(open(a, 'rb').read())
				encoders.encode_base64(part)
				part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(a))
			else:
				part = MIMEBase('application', 'octet-stream')
				part.set_payload(open(a, 'rb').read())
				encoders.encode_base64(part)
				part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(a))
			msg.attach(part)

	mailServer = smtplib.SMTP("smtp.gmail.com", 587)
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.login(MAIL_USER, MAIL_PASS)
	mailServer.sendmail(MAIL_USER, to, msg.as_string().encode('ascii'))
	# Should be mailServer.quit(), but that crashes...
	mailServer.close()

# Todo:
# Reimplement when mail option is again available
def generate_mail():
	return "Automated dummy response"

# For testing purposes
if __name__ == '__main__':
	mail(
		'andreas.frisch@gmail.com',
		generate_mail(),
		'Do not respond',
		None,
	)
