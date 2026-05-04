from urllib.parse import urlparse


class URLAnalyzer:

    @staticmethod
    def analyze(url):
        """
        تحليل رابط واحد واستخراج خصائصه الأساسية
        """

        parsed_url = urlparse(url)

        scheme = parsed_url.scheme
        domain = parsed_url.netloc
        path = parsed_url.path

        suspicious_reasons = []

        if scheme != "https":
            suspicious_reasons.append("URL does not use HTTPS")

        if "-" in domain:
            suspicious_reasons.append("Domain contains hyphen")

        if len(domain) > 30:
            suspicious_reasons.append("Domain is unusually long")

        return {
            "url": url,
            "scheme": scheme,
            "domain": domain,
            "path": path,
            "is_suspicious": len(suspicious_reasons) > 0,
            "reasons": suspicious_reasons
        }