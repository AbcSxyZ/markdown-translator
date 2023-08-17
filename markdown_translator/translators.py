import requests
from .configuration import config
from .exceptions import MarkdownTranslatorError

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
        "auth_key": config.DEEPL_KEY,
        "text": html_content,
        "source_lang": lang_from,
        "target_lang": lang_to,
        "tag_handling": "html",
    }
    response = requests.post(endpoint, headers=headers, data=data)

    if response.status_code != 200:
        error_msg = f"HTTP Error {response.status_code} on DeepL API"
        if response.text:
            error_msg += " (" + response.json()["message"] + ")"
        raise MarkdownTranslatorError(error_msg)

    return response.json()['translations'][0]['text']
