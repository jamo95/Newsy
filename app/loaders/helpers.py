import re


def clean_html(html):
    # Remove header tags including content.
    html = re.sub(r'<h(\d).*?></h\1>', '', html)
    # Strip surrounding tags.
    text = re.sub(r'<.*?>', '', html)
    # Strip surrounding whitespace.
    return text.strip()
