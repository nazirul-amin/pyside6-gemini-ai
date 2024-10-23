import os
import google.generativeai as genai
import pypinyin
import logging

from flask import Flask, request
from gevent.pywsgi import WSGIServer
from urllib.parse import unquote
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

http_server = None

genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_system_prompt(text):
    """Generates a system prompt for translation."""
    return (
        f'Translate the following text: "{text}" from Simplified Chinese into English, ensuring a direct and accurate translation while preserving the original meaning and context. '
        'Edit and restructure the sentence to flow naturally in English, but without changing the intended message. Keep special characters as they are and use Pinyin romanization for Chinese names or terms. '
        'The translation should be clear and concise, with no added words or interpretations beyond the original text. Only return the translated text without any remarks or notes.'
    )

def handle_translation(text):
    """Handles the translation of the input text."""
    text = unquote(text)
    prompt = generate_system_prompt(text)

    try:
        response = model.generate_content(prompt)
        translation = response.text
        return convert_pinyin_to_english(translation)
    except Exception as e:
        print(f"There was a problem with the request! Error message: {e}")
        logging.error(f"There was a problem with the request! Error message: {e}")
        return False

@app.route('/translate', methods=['GET'])
def translate():
    """API endpoint for text translation."""
    text = request.args.get('text')
    print(f"Received Text: {text}")
    logging.info(f"Received Text: {text}")

    with ThreadPoolExecutor() as executor:
        try:
            translation = executor.submit(handle_translation, text).result()
            if translation:
                print(f"Translated Text: {translation}")
                logging.info(f"Translation Response: {translation}")
                return translation
            else:
                return "Translation failed", 500
        except Exception as e:
            print(f"Error during translation: {e}")
            logging.info(f"Error during translation: {e}")
            return "Translation failed", 500

def convert_pinyin_to_english(pinyin):
    """Converts Pinyin characters to English equivalents."""
    english = pypinyin.pinyin(pinyin, style=pypinyin.NORMAL)
    english = ''.join([i[0] for i in english])

    pinyin_to_english_map = {
        'ü': 'u',
        'üe': 'ue',
        'üi': 'ui',
        'üo': 'uo',
        'üa': 'ua',
        'üe': 'ue',
        'üai': 'uai',
        'üao': 'uao',
        'üan': 'uan',
        'üang': 'uang',
        'üe': 'ue',
        'üei': 'uei',
        'üo': 'uo',
        'üai': 'uai',
        'üao': 'uao',
        'üan': 'uan',
        'üang': 'uang',
        'ā': 'a',
        'ǎ': 'a',
        'à': 'a',
        'á': 'a',
        'ē': 'e',
        'ě': 'e',
        'è': 'e',
        'é': 'e',
        'ī': 'i',
        'ǐ': 'i',
        'ì': 'i',
        'í': 'i',
        'ō': 'o',
        'ǒ': 'o',
        'ò': 'o',
        'ó': 'o',
        'ū': 'u',
        'ǔ': 'u',
        'ù': 'u',
        'ú': 'u',
        'ǖ': 'u',
        'ǘ': 'u',
        'ǚ': 'u',
        'ǜ': 'u',
        'āi': 'ai',
        'ǎi': 'ai',
        'ài': 'ai',
        'ái': 'ai',
        'ēi': 'ei',
        'ěi': 'ei',
        'èi': 'ei',
        'éi': 'ei',
        'īi': 'ii',
        'ǐi': 'ii',
        'ìi': 'ii',
        'íi': 'ii',
        'ōi': 'oi',
        'ǒi': 'oi',
        'òi': 'oi',
        'ói': 'oi',
        'ūi': 'ui',
        'ǔi': 'ui',
        'ùi': 'ui',
        'úi': 'ui',
        'ǖi': 'ui',
        'ǘi': 'ui',
        'ǚi': 'ui',
        'ǜi': 'ui',
        'āu': 'au',
        'ǎu': 'au',
        'àu': 'au',
        'áu': 'au',
        'ēu': 'eu',
        'ěu': 'eu',
        'èu': 'eu',
        'éu': 'eu',
        'īu': 'iu',
        'ǐu': 'iu',
        'ìu': 'iu',
        'íu': 'iu',
        'ōu': 'ou',
        'ǒu': 'ou',
        'òu': 'ou',
        'óu': 'ou',
        'ūu': 'uu',
        'ǔu': 'uu',
        'ùu': 'uu',
        'úu': 'uu',
        'ǖu': 'uu',
        'ǘu': 'uu',
        'ǚu': 'uu',
        'ǜu': 'uu',
        'āng': 'ang',
        'ǎng': 'ang',
        'àng': 'ang',
        'áng': 'ang',
        'ēng': 'eng',
        'ěng': 'eng',
        'èng': 'eng',
        'éng': 'eng',
        'īng': 'ing',
        'ǐng': 'ing',
        'ìng': 'ing',
        'íng': 'ing',
        'ōng': 'ong',
        'ǒng': 'ong',
        'òng': 'ong',
        'óng': 'ong',
        'ūng': 'ung',
        'ǔng': 'ung',
        'ùng': 'ung',
        'úng': 'ung',
        'ǖng': 'ung',
        'ǘng': 'ung',
        'ǚng': 'ung',
        'ǜng': 'ung',
        'ān': 'an',
        'ǎn': 'an',
        'àn': 'an',
        'án': 'an',
        'ēn': 'en',
        'ěn': 'en',
        'èn': 'en',
        'én': 'en',
        'īn': 'in',
        'ǐn': 'in',
        'ìn': 'in',
        'ín': 'in',
        'ōn': 'on',
        'ǒn': 'on',
        'òn': 'on',
        'ón': 'on',
        'ūn': 'un',
        'ǔn': 'un',
        'ùn': 'un',
        'ún': 'un',
        'ǖn': 'un',
        'ǘn': 'un',
        'ǚn': 'un',
        'ǜn': 'un',
        'āng': 'ang',
        'ǎng': 'ang',
        'àng': 'ang',
        'áng': 'ang',
        'ēng': 'eng',
        'ěng': 'eng',
        'èng': 'eng',
        'éng': 'eng',
        'īng': 'ing',
        'ǐng': 'ing',
        'ìng': 'ing',
        'íng': 'ing',
        'ōng': 'ong',
        'ǒng': 'ong',
        'òng': 'ong',
        'óng': 'ong',
        'ūng': 'ung',
        'ǔng': 'ung',
        'ùng': 'ung',
        'úng': 'ung',
        'ǖng': 'ung',
        'ǘng': 'ung',
        'ǚng': 'ung',
        'ǜng': 'ung',
    }

    for pinyin_char, english_char in pinyin_to_english_map.items():
        english = english.replace(pinyin_char, english_char)

    return english

def run_translation():
    global http_server
    print("Server starting at http://127.0.0.1:4000")
    http_server = WSGIServer(('127.0.0.1', 4000), app, log=None, error_log=None)
    http_server.serve_forever()
    
def stop_translation():
    global http_server
    if http_server:
        print("Stopping the server...")
        http_server.stop()
        print("Server stopped.")

if __name__ == "__main__":
    run_translation()