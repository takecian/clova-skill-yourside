# coding: utf-8

from flask import Flask, request, jsonify
import os, random
import cek
import random

app = Flask(__name__)

clova = cek.Clova(
    application_id="com.takecian.clova.yourside",
    default_language="ja",
    debug_mode=True)


@app.route('/', methods=['GET', 'POST'])
def lambda_handler(event=None, context=None):
    app.logger.info('Lambda function invoked index()')
    return 'hello from Flask!'


@app.route('/clova', methods=['POST'])
def my_service():
    body_dict = clova.route(body=request.data, header=request.headers)
    response = jsonify(body_dict)
    response.headers['Content-Type'] = 'application/json;charset-UTF-8'
    return response


@clova.handle.launch
def launch_request_handler(clova_request):
    open_message = "こんにちは、いつでもあなたの味方です"
    welcome_japanese = cek.Message(message=open_message, language="ja")
    response = clova.response([welcome_japanese])
    return response


@clova.handle.intent("SupportIntent")
def play_sound_intent_handler(clova_request):
    app.logger.info("Intent started")
    message = cek.Message(message=get_support_message(), language="ja")
    response = clova.response([message])
    return response


def get_support_message():
    messages = ["毎日頑張ってますね、あまり無理しないでくださいね。", "いつも側で応援していますよ、今日も頑張ってくださいね。"]
    return random.choice(messages)

@clova.handle.end
def end_handler(clova_request):
    # Session ended, this handler can be used to clean up
    app.logger.info("Session ended.")


@clova.handle.default
def default_handler(request):
    return clova.response("理解できませんでした")


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.debug = True
    app.run(host="0.0.0.0", port=port)
