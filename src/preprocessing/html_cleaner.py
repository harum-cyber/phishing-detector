import re
from bs4 import BeautifulSoup


class HTMLCleaner:

    @staticmethod
    def clean(html):
        """
        تنظيف HTML واستخراج النص والروابط
        """
        soup = BeautifulSoup(html, "html.parser")

        links = []
        for tag in soup.find_all("a", href=True):
            links.append(tag["href"])

        text = soup.get_text()

        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)

        return {
            "text": text.strip(),
            "links": links
        }