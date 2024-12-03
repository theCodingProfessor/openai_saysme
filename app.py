from flask import Flask
from flask import render_template
from flask import request
import os
import pprint
import openai
openai.api_key = "your key goes here"
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/home', methods=['GET', 'POST'])
def run_home():  #
    return render_template('index.html')


@app.route('/whisper', methods=['GET', 'POST'])
def run_whisper():  #
    return render_template('./whisper.html')


@app.route('/chat', methods=['GET'])
def chat_get():
    return render_template('./chat.html')


@app.route('/chat', methods=['POST'])
def chat_post():
    # Sample gpt-3.5-turbo: completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[ {"role": "user", "content": "Hello!"}])
    text_from_user = request.form['user_text']
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": text_from_user}])
    response_content = completion.choices[0].message.content
    print(completion.id)
    pprint.pprint(completion)
    return render_template('./chat.html', dataToRender=response_content)


@app.route('/improve', methods=['POST'])
def improve_post():
    user_data = request.form['user_text']
    update_request = request.form['upgrade_type']
    completion = openai.Edit.create(
      model="text-davinci-edit-001",
      input=user_data,
      instruction=update_request,
    )
    response_content = completion.choices[0].text
    print(completion.choices[0].text)
    pprint.pprint(completion)
    return render_template('./improve.html', dataToRender=response_content, initial_text=user_data)


@app.route('/improve', methods=['GET'])
def improve_get():
    return render_template('./improve.html')


@app.route('/restate', methods=['POST'])
def restate_post():
    user_data = request.form['user_text']
    completion = openai.Completion.create(
      model="text-davinci-003",
      prompt=user_data,
      max_tokens=15,
      temperature=0,
      echo=False,
    )
    response_content = completion.choices[0].text
    print(completion.choices[0].text)
    pprint.pprint(completion)
    return render_template('./restate.html', dataToRender=response_content, initial_text=user_data)


@app.route('/restate', methods=['GET'])
def restate_get():
    return render_template('./restate.html')


if __name__ == '__main__':
    app.run()
