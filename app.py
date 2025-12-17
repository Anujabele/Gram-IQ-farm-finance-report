

from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate():
    pass

if __name__ == '__main__':
    app.run(debug=True)