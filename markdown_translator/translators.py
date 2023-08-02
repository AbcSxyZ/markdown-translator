import requests
from .config import DEEPL_KEY

def translate_deepl(html_content, lang_to, lang_from=None):
    """
    Translate HTML content using DeepL API. See API documentation for available
    languages : https://www.deepl.com/fr/docs-api/translate-text/

    DeepL can't convert raw markdown, it will break syntax and text translation.
    """
    endpoint = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "auth_key": DEEPL_KEY,
        "text": html_content,
        "source_lang": lang_from,
        "target_lang": lang_to,
        "tag_handling": "xml",
    }
    response = requests.post(endpoint, headers=headers, data=data)
    translated_text = response.json()
    return translated_text['translations'][0]['text']
