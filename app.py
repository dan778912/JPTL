from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from preprocessing.preprocess_text import preprocess
from utils.utils import translate_text_deepl, kanji_to_hiragana
from models.sentiment_models import analyze_emotion
import pytesseract
from PIL import Image
import os

app = Flask(__name__, static_folder='frontend/jlpt-frontend/build', static_url_path='/')
CORS(app)

# Configure Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Change path as needed

def ocr_image(image_path, lang='jpn'):
    with Image.open(image_path) as img:
        text = pytesseract.image_to_string(img, lang=lang)
    return text

@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['file']
    image_path = 'uploaded_image.png'
    file.save(image_path)

    # OCR part
    text = ocr_image(image_path)
    print(f'OCR Text: {text}')

    # Preprocess text
    preprocessed_text = preprocess(text)
    print(f'Preprocessed Text: {preprocessed_text}')

    # Convert Kanji to Hiragana
    hiragana_text = kanji_to_hiragana(preprocessed_text)
    print(f'Hiragana Text: {hiragana_text}')
    
    # Translate text
    translated_text = translate_text_deepl(preprocessed_text)
    print(f'Translated Text: {translated_text}')

    # Analyze emotion
    sentiment = analyze_emotion(translated_text)
    print(f'Sentiment: {sentiment}')

    return jsonify({
        'original_text': preprocessed_text,
        'hiragana_text': hiragana_text,
        'translated_text': translated_text,
        'sentiment': sentiment
    })

if __name__ == '__main__':
    app.run(debug=True)
