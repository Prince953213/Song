from flask import Flask, jsonify, request, render_template
import json

app = Flask(__name__)

SONG_FILE = "songs.json"

def load_songs():
    with open(SONG_FILE, "r") as f:
        return json.load(f)

def save_songs(songs):
    with open(SONG_FILE, "w") as f:
        json.dump(songs, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/songs', methods=['GET'])
def get_songs():
    return jsonify(load_songs())

@app.route('/api/songs', methods=['POST'])
def add_song():
    new_song = request.json
    songs = load_songs()
    new_song["id"] = max([s["id"] for s in songs], default=0) + 1
    songs.append(new_song)
    save_songs(songs)
    return jsonify({"status": "success"}), 201

@app.route('/api/songs/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    songs = load_songs()
    songs = [s for s in songs if s["id"] != song_id]
    save_songs(songs)
    return jsonify({"status": "deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
    
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render PORT env le raha hai
    app.run(host='0.0.0.0', port=port)
