if __name__ == '__main__':

    class working_with_mail:
        def __init__(self, GMAIL_SMTP, GMAIL_IMAP, email_address, password, subject, message):
            self.GMAIL_SMTP = GMAIL_SMTP
            self.GMAIL_IMAP = GMAIL_IMAP
            self.email_address = email_address
            self.password = password
            self.subject = subject
            self.recipients = []
            self.msg = MIMEMultipart()
            self.message = message
            self.header = None

        def sending_address(self, recipients):
            self.recipients.append(recipients)

        def send_message(self):
            self.msg['From'] = self.email_address
            self.msg['To'] = ', '.join(self.recipients)
            self.msg['Subject'] = self.subject
            self.msg.attach(MIMEText(self.message))

        def identify_gmail_client(self):
            server = smtplib.SMTP(self.GMAIL_SMTP, 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.email_address, self.password)
            server.sendmail(self.email_address, self.recipients, self.msg.as_string())
            server.quit()

        def recieve(self):
            mail = imaplib.IMAP4_SSL(self.GMAIL_IMAP)
            mail.login(self.email_address, self.password)
            mail.list()
            mail.select("inbox")
            criterion = '(HEADER Subject "%s")' % self.header if self.header else 'ALL'
            result, data = mail.uid('search', None, criterion)
            assert data[0], 'There are no letters with current header'
            latest_email_uid = data[0].split()[-1]
            result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = data[0][1]
            email.message_from_bytes(raw_email)
            mail.logout()



    import email
    import smtplib
    import imaplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    email_address = input('Введите email отправителя:')
    password = input('Введите пароль:')
    message = input('Введите сообщение:')

    working_mail = working_with_mail('smtp.gmail.com', 'imap.gmail.com', email_address, password, 'Subject', message)
    recipients = input('Введите адреса получателей через запятую:')
    working_mail.sending_address(recipients)
    working_mail.send_message()
    working_mail.identify_gmail_client()
    working_mail.recieve()









