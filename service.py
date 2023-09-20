from flask import Flask, jsonify, request
import json
import requests
from business.chatbot.const import API_KEY


class BackendManager:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_endpoints()

    def setup_endpoints(self):
        self.add_cors_headers(self.app)
        self.app.route('/api/data', methods=['GET'])(self.get_data)
        self.app.route('/api/save_questions', methods=['POST'])(self.post_data)
        self.app.route('/api/conversation_chat', methods=['GET'])(self.chatgpt)

    @staticmethod
    def add_cors_headers(app):
        @app.after_request
        def add_cors_headers(response):
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response

    def chatgpt(self):
        headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
        link = 'https://api.openai.com/v1/chat/completions'
        id_modelo = 'gpt-3.5-turbo'
        body = {
            "model": id_modelo,
            "messages": [{"role": "user", "content": "Olá Chat"}]
        }
        body = json.dumps(body)
        requisicao = requests.post(link, headers=headers, data=body)
        return requisicao.json()
        #mensagem = resposta['choises'][0]['message']['content']
        #return mensagem


    def get_data(self):
        data = {'message': 'GET request successful'}
        return jsonify(data)

    def post_data(self):
        content = request.get_json()
        if content is None:
            return jsonify({'error': 'Invalid JSON'}), 400

        message = content.get('message')
        if message is None:
            return jsonify({'error': 'Message not found in JSON'}), 400

        response_data = {'message': f'POST request successful. Received message: {message}'}
        return jsonify(response_data)

    def run(self, host='localhost', port=5000):
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    api = BackendManager()
    api.run()