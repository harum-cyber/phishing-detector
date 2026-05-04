import email
from email import policy
from email.parser import BytesParser


class EmailParser:

    @staticmethod
    def parse_eml(file_path):
        """
        قراءة ملف .eml واستخراج:
        - subject
        - sender
        - body (HTML أو text)
        """

        with open(file_path, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)

        subject = msg['subject']
        sender = msg['from']

        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()

                if content_type == "text/html":
                    body = part.get_content()
                    break
                elif content_type == "text/plain":
                    body = part.get_content()

        else:
            body = msg.get_content()

        return {
            "subject": subject,
            "sender": sender,
            "body": body
        }