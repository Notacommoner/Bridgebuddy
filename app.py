from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

class LanguageTranslator:
    def __init__(self, api_url):
        self.api_url = api_url

    def translate(self, text, source_lang, target_lang, formality='neutral'):
        payload = {
            'q': text,
            'source': source_lang,
            'target': target_lang,
            'format': 'text'
        }
        
        if formality in ['formal', 'casual']:
            payload['formality'] = formality
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json().get('translatedText', 'Translation result not found.')
        except requests.exceptions.RequestException as e:
            return f"Error: Translation could not be performed. {str(e)}"

translator = LanguageTranslator("https://libretranslate.com/translate")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    source_lang = data.get('source_lang')
    target_lang = data.get('target_lang')
    formality = data.get('formality', 'neutral')
    
    translation = translator.translate(text, source_lang, target_lang, formality)
    return jsonify({'translation': translation})

if __name__ == "__main__":
    app.run(debug=True)
