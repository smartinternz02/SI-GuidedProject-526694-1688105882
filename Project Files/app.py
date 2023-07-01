from flask import Flask, render_template, request, jsonify
import http.client
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    image_url = request.form['imageURL']
    if image_url:
        conn = http.client.HTTPSConnection("openalpr.p.rapidapi.com")
        payload = f"image_url={image_url}"
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'X-RapidAPI-Key': "f702f985bcmsh99c9982e34a8b66p13a274jsn360379ced8a6",
            'X-RapidAPI-Host': "openalpr.p.rapidapi.com"
        }
        conn.request("POST", "/recognize_url?country=eu", payload, headers)
        res = conn.getresponse()
        data = res.read()
        response_data = json.loads(data.decode("utf-8"))

        if 'results' in response_data and len(response_data['results']) > 0:
            results = response_data['results'][0]  # Assuming the first result is the most confident one
            plate = results['plate']
            confidence = results['confidence']
            output_data = {'plate': plate, 'confidence': confidence}
            response = jsonify(output_data)
        else:
            response = jsonify({'error': 'No license plate found.'})
        
        return response
    else:
        response = jsonify({'error': 'No image URL provided.'})
        return response

@app.route('/static/css/<path:path>')
def static_css(path):
    return app.send_static_file('css/' + path)

if __name__ == '__main__':
    app.run(debug=True)
