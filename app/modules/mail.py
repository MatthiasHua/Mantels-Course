from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from app import config
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

for i in config.items("Mail"):
    if i[0] == 'from':
        from_addr = i[1]
    if i[0] == 'password':
        password = i[1]
    if i[0] == 'smtp':
        smtp_server = i[1]

def send_email(to_addr, title, p):
	msg = MIMEText( '<p>' + p + '</p><hr> <p>请勿回复此邮件，如果对邮件内容有疑问，请邮件咨询。<br>客服:<br>custom-service@mail.mantels.top<br>开发:<br>matthias@mail.mantels.top<br>tatjana@mail.mantels.top</p>', 'html', 'utf-8')
	msg['From'] = _format_addr('Mantels公告 <%s>' % from_addr)
	msg['To'] = _format_addr('用户 <%s>' % to_addr)
	msg['Subject'] = Header(title, 'utf-8').encode()

	server = smtplib.SMTP_SSL(smtp_server, 465, timeout = 120)
	server.set_debuglevel(1)
	server.login(from_addr, password)
	server.sendmail(from_addr, [to_addr], msg.as_string())
	server.quit()
