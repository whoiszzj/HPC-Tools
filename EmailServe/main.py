import smtplib
from email.mime.text import MIMEText
import argparse
parser = argparse.ArgumentParser("HUST Email Server")
parser.add_argument("-s", "--subject", type=str, default="Info-From-HUST-Server", help="email's subject")
parser.add_argument("-c", "--content", type=str, default="Hello master, I am running!", help="email's content")
args = parser.parse_args()

def send_email(subject, content):
    host = 'mail.hust.edu.cn'
    port = 465
    sender = 'xxxxxxxx@hust.edu.cn' # Your email address
    passwd = 'xxxxxxxxxx'  # Your email password
    receiver = 'xxxxx@outlook.com'  # Receiver's email address
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['from'] = sender
    msg['to'] = receiver
    msg['subject'] = subject
    try:
        smtp_obj = smtplib.SMTP_SSL(host=host, port=port)
        smtp_obj.login(user=sender, password=passwd)
        smtp_obj.sendmail(from_addr=sender, to_addrs=receiver, msg=msg.as_string())
        print('Successfully send email to %s' % receiver)
    except Exception as e:
        print("Error! ", e)


if __name__ == '__main__':
    send_email(args.subject, args.content)

