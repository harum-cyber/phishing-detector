from email.utils import parseaddr


class SenderAnalyzer:

    @staticmethod
    def analyze(sender):
        """
        تحليل المرسل واستخراج الإيميل والدومين
        """

        name, email_address = parseaddr(sender)

        domain = ""

        if "@" in email_address:
            domain = email_address.split("@")[-1].lower()

        suspicious_reasons = []

        if not email_address:
            suspicious_reasons.append("Sender email is missing")

        if domain in ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]:
            suspicious_reasons.append("Sender uses a free email provider")

        return {
            "sender": sender,
            "name": name,
            "email": email_address,
            "domain": domain,
            "is_suspicious": len(suspicious_reasons) > 0,
            "reasons": suspicious_reasons
        }