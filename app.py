from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load the dataset
with open('laws.json', 'r') as f:
    laws = json.load(f)

# Search endpoint
@app.route('/api/search', methods=['GET'])
def search_laws():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    # Search by title or keywords
    results = [
        law for law in laws 
        if query in law['title'].lower() or any(query in kw.lower() for kw in law['keywords'])
    ]
    return jsonify(results)

# Chatbot endpoint (rule-based AI)
@app.route('/api/chat', methods=['POST'])
def chat():
    message = request.json.get('message', '').lower()
    if not message:
        return jsonify({'reply': 'Please ask me something about student laws!'})

    # Simple rule-based logic to match keywords
    for law in laws:
        if any(kw in message for kw in law['keywords']):
            return jsonify({
                'reply': f"Based on your query, here’s a suggestion: **{law['title']}** - {law['description']}"
            })

    # Default response if no match
    return jsonify({
        'reply': "I couldn’t find a specific law for that. Try asking about education, ragging, university rights, or fees!"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)