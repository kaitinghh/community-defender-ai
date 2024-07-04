from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import threading
import httpx
from deepgram import DeepgramClient, DeepgramClientOptions, LiveTranscriptionEvents, LiveOptions
from dotenv import load_dotenv
import os
import time
from flask_cors import CORS

# app = Flask(__name__, static_folder='static')

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")

load_dotenv()
API_KEY = os.getenv("DEEPGRAM_API_KEY")
config = DeepgramClientOptions(
            options={"keepalive": "true"} # Comment this out to see the effect of not using keepalive
        )
full_transcript = []
TAG = 'SPEAKER '

def transcribe(url, timeout, lang, send_transcription):
    try:
        deepgram = DeepgramClient(API_KEY, config)
        dg_connection = deepgram.listen.live.v("1")

        def on_message(self, result, **kwargs):
            if result.is_final:
                lines = []
                words = result.channel.alternatives[0].words
                curr_speaker = 0
                curr_line = ''
                for word_struct in words:
                    word_speaker = word_struct["speaker"]
                    word = word_struct["punctuated_word"]
                    if word_speaker == curr_speaker:
                        curr_line += ' ' + word
                    else: ## if change speaker
                        lines = []
                        tag = TAG + str(curr_speaker) + ':'
                        full_line = curr_line # tag + 
                        if curr_line != "":
                            lines.append(full_line)
                            full_transcript.append(full_line)
                        curr_speaker = word_speaker
                        curr_line = ' ' + word
                if curr_line != "":
                    full_line = curr_line # TAG + str(curr_speaker) + ':' + 
                    lines.append(full_line)
                    full_transcript.append(full_line)
                print(full_transcript)
                if curr_speaker == 0: # operator
                    send_transcription({"sender": "Operator", "text": lines})
                else:
                    send_transcription({"sender": "Caller", "text": lines})

        def on_metadata(self, metadata, **kwargs):
            print(f"\n\n{metadata}\n\n")

        def on_error(self, error, **kwargs):
            print(f"\n\n{error}\n\n")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)

        if lang == "eng": 
            print("yes")
            options = LiveOptions(
            model="nova-2",
            language="en-US",
            diarize=True,
            smart_format=True,
        )
        else: 
            options = LiveOptions(
            model="nova-2",
            language="zh",
            diarize=True,
            smart_format=True,
        )

        dg_connection.start(options)
        print("started")

        lock_exit = threading.Lock()
        exit = False

        def myThread():
            with httpx.stream("GET", url) as r:
                for data in r.iter_bytes():
                    lock_exit.acquire()
                    if exit:
                        break
                    lock_exit.release()
                    dg_connection.send(data)

        myHttp = threading.Thread(target=myThread)
        myHttp.start()

        def finish_connection():
            time.sleep(timeout)
            dg_connection.finish()
            print("Connection finished after", timeout, "seconds")

        timer_thread = threading.Thread(target=finish_connection)
        timer_thread.start()

        input("Press Enter to stop recording...\n\n")

        lock_exit.acquire()
        exit = True
        lock_exit.release()

        myHttp.join()
        dg_connection.finish()

        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return

@app.route('/transcribe', methods=['POST'])
def transcribe_route():
    data = request.get_json()
    print(data)
    url = data['url']
    caller_id = data['caller_id']  # Get the caller ID from the request
    lang = data['lang']
    timeout = 80 # temporarily set
    print(lang)

    def send_transcription(line):
        socketio.emit('transcription_update', {'caller_id': caller_id, 'line': line})

    threading.Thread(target=transcribe, args=(url, timeout, lang, send_transcription)).start()
    return jsonify({'status': 'Transcription started'})

# @app.route('/')
# def serve_index():
#     return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, allow_unsafe_werkzeug=True)








# from flask import Flask, request, jsonify, send_from_directory
# from flask_socketio import SocketIO, emit
# import threading
# import httpx
# from deepgram import DeepgramClient, DeepgramClientOptions, LiveTranscriptionEvents, LiveOptions
# from dotenv import load_dotenv
# import os
# import time

# app = Flask(__name__, static_folder='static')
# socketio = SocketIO(app, cors_allowed_origins="*")

# load_dotenv()
# API_KEY = os.getenv("DEEPGRAM_API_KEY")
# config = DeepgramClientOptions(
#             options={"keepalive": "true"} # Comment this out to see the effect of not using keepalive
#         )
# full_transcript = []
# TAG = 'SPEAKER '

# def transcribe(url, timeout, send_transcription):
#     try:
#         deepgram = DeepgramClient(API_KEY, config)
#         dg_connection = deepgram.listen.live.v("1")

#         def on_message(self, result, **kwargs):
#             if result.is_final:
#                 lines = []
#                 words = result.channel.alternatives[0].words
#                 curr_speaker = 0
#                 curr_line = ''
#                 for word_struct in words:
#                     word_speaker = word_struct["speaker"]
#                     word = word_struct["punctuated_word"]
#                     if word_speaker == curr_speaker:
#                         curr_line += ' ' + word
#                     else:
#                         lines = []
#                         tag = TAG + str(curr_speaker) + ':'
#                         full_line = tag + curr_line
#                         if curr_line != "":
#                             lines.append(full_line)
#                             full_transcript.append(full_line)
#                         curr_speaker = word_speaker
#                         curr_line = ' ' + word
#                 if curr_line != "":
#                     full_line = TAG + str(curr_speaker) + ':' + curr_line
#                     lines.append(full_line)
#                     full_transcript.append(full_line)
#                 print(full_transcript)
#                 send_transcription(full_transcript)

#         def on_metadata(self, metadata, **kwargs):
#             print(f"\n\n{metadata}\n\n")

#         def on_error(self, error, **kwargs):
#             print(f"\n\n{error}\n\n")

#         dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
#         dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
#         dg_connection.on(LiveTranscriptionEvents.Error, on_error)

#         options = LiveOptions(
#             model="nova-2",
#             language="en-US",
#             diarize=True,
#             smart_format=True,
#         )

#         dg_connection.start(options)

#         lock_exit = threading.Lock()
#         exit = False

#         def myThread():
#             with httpx.stream("GET", url) as r:
#                 for data in r.iter_bytes():
#                     lock_exit.acquire()
#                     if exit:
#                         break
#                     lock_exit.release()
#                     dg_connection.send(data)

#         myHttp = threading.Thread(target=myThread)
#         myHttp.start()

#         def finish_connection():
#             time.sleep(timeout)
#             dg_connection.finish()
#             print("Connection finished after", timeout, "seconds")

#         timer_thread = threading.Thread(target=finish_connection)
#         timer_thread.start()

#         input("Press Enter to stop recording...\n\n")

#         lock_exit.acquire()
#         exit = True
#         lock_exit.release()

#         myHttp.join()
#         dg_connection.finish()

#         print("Finished")

#     except Exception as e:
#         print(f"Could not open socket: {e}")
#         return

# @app.route('/transcribe', methods=['POST'])
# def transcribe_route():
#     data = request.get_json()
#     url = data['url']
#     timeout = 70 # temporarily set
#     print(url)

#     def send_transcription(transcript):
#         socketio.emit('transcription_update', {'transcript': transcript})

#     threading.Thread(target=transcribe, args=(url, timeout, send_transcription)).start()
#     return jsonify({'status': 'Transcription started'})

# @app.route('/')
# def serve_index():
#     return send_from_directory(app.static_folder, 'index.html')

# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=5001, allow_unsafe_werkzeug=True)
