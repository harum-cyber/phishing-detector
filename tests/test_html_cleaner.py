import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from preprocessing.html_cleaner import HTMLCleaner


sample_html = """
<html>
  <body>
    <h1>Urgent: Verify Your Account</h1>
    <p>Please click the link below to avoid suspension.</p>
    <a href="http://fake-bank-login.com">Verify Now</a>
  </body>
</html>
"""

result = HTMLCleaner.clean(sample_html)

print("Cleaned Text:")
print(result["text"])

print("\nExtracted Links:")
print(result["links"])