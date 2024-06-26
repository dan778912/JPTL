from flask import Flask, request, jsonify
from flask_cors import CORS
from preprocessing.preprocess_text import preprocess
from utils.utils import translate_text_deepl
from models.sentiment_models import analyze_emotion
from utils.furigana import print_html
import pytesseract
from PIL import Image
import os

app = Flask(__name__)
CORS(app)

# Configure Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Change path as needed

def ocr_image(image_path, lang='jpn'):
    with Image.open(image_path) as img:
        text = pytesseract.image_to_string(img, lang=lang)
    return text

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

    # Convert Kanji to Hiragana using print_html from furigana.py
    furigana_html = print_html(preprocessed_text)
    print(f'Furigana HTML: {furigana_html}')
    
    # Translate text
    translated_text = translate_text_deepl(preprocessed_text)
    print(f'Translated Text: {translated_text}')

    # Analyze emotion
    sentiment = analyze_emotion(translated_text)
    print(f'Sentiment: {sentiment}')

    return jsonify({
        'original_text': preprocessed_text,
        'furigana_html': furigana_html,
        'translated_text': translated_text,
        'sentiment': sentiment
    })

if __name__ == '__main__':
    app.run(debug=True)
