from flask import Flask, render_template, request
from pybot import pybot
import os

app = Flask(__name__)
is_colab = True
try:
  os.environ['COLAB_GPU']
except KeyError:
  is_colab = False
if is_colab:
    from flask_ngrok import run_with_ngrok
    run_with_ngrok(app)


@app.route('/hello')
def hello():
    return render_template('pybot_template.html', input_text='', output_text='')


@app.route('/hello', methods=['POST'])
def do_hello():
    input_text = request.form['input_text']
    input_image = request.files['input_image']
    output_text = pybot(input_text, input_image)
    return render_template('pybot_template.html', input_text=input_text, output_text=output_text)


if __name__ == '__main__':
    if not is_colab:
        app.debug = True
    app.run()
