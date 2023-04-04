import requests
import googletrans


def load_random_cat():
    # json_response = requests.get("https://aws.random.cat/meow").json()
    # cat_url = json_response["file"]

    cat_url = 'profile_pictures/basic.jpg'

    return cat_url


def load_random_joke():
    url = "https://official-joke-api.appspot.com/random_joke"

    response = requests.get(url).json()
    joke = f'- {response["setup"]}\n- {response["punchline"]}\n:)'
    return translate_joke(joke)


def translate_joke(text):
    translator = googletrans.Translator()
    result = translator.translate(text, dest="ru")
    row = (f'{result.text}\nOrigin: {result.origin}').split('\n')
    return row


def base_config():
    return {
        "cat_url": load_random_cat(),
        "joke_text": load_random_joke()
    }