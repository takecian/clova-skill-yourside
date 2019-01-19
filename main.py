# coding: utf-8

from flask import Flask, request, jsonify
import os, random
import cek

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
    message = cek.Message(message="赤ちゃんが落ち着く音を再生します。", language="ja")
    sound_url = cek.URL("https://s3-ap-northeast-1.amazonaws.com/takecian-clova/plastic_sound.mp3")
    response = clova.response([message, sound_url, sound_url, sound_url, sound_url])
    return response


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
