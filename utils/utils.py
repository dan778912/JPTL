import requests
import config

def translate_text_deepl(text, target_lang='EN'):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": config.DEEPL_API_KEY,
        "text": text,
        "target_lang": target_lang
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        return response.json()["translations"][0]["text"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


