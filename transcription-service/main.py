from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import threading
import httpx
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from dotenv import load_dotenv
import os

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*")

load_dotenv()
API_KEY = os.getenv("DEEPGRAM_API_KEY")
full_transcript = []
TAG = 'SPEAKER '

def transcribe(url, send_transcription):
    try:
        deepgram = DeepgramClient(API_KEY)
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
                    else:
                        lines = []
                        tag = TAG + str(curr_speaker) + ':'
                        full_line = tag + curr_line
                        if curr_line != "":
                            lines.append(full_line)
                            full_transcript.append(full_line)
                        curr_speaker = word_speaker
                        curr_line = ' ' + word
                if curr_line != "":
                    full_line = TAG + str(curr_speaker) + ':' + curr_line
                    lines.append(full_line)
                    full_transcript.append(full_line)
                send_transcription(full_transcript)

        def on_metadata(self, metadata, **kwargs):
            print(f"\n\n{metadata}\n\n")

        def on_error(self, error, **kwargs):
            print(f"\n\n{error}\n\n")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)

        options = LiveOptions(
            model="nova-2",
            language="en-US",
            diarize=True,
            smart_format=True,
        )

        dg_connection.start(options)

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
    url = data['url']

    def send_transcription(transcript):
        socketio.emit('transcription_update', {'transcript': transcript})

    threading.Thread(target=transcribe, args=(url, send_transcription)).start()
    return jsonify({'status': 'Transcription started'})

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, allow_unsafe_werkzeug=True)
