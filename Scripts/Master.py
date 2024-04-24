from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import subprocess
from threading import Thread
import webbrowser
from time import sleep

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes, for all domains

Folder_Path = "C:\\Users\\nikhi\\Documents\\GitHub\\gvsu-gis\\"
GEE_Project_ID = "ee-sharmani"

@app.route('/')
def index():
    return "Flask server is running!"

@app.route('/polygon')
def polygon():
    return send_from_directory(app.static_folder, 'Polygon.html')

@app.route('/video-player')
def video_player():
    return send_from_directory(app.static_folder, 'video_player.html')

@app.route('/video-content/<filename>')
def video_content(filename):
    video_directory = os.path.join(Folder_Path, 'data', 'video')
    return send_from_directory(video_directory, filename)

@app.route('/save-json', methods=['POST'])
def save_json():
    data_directory = os.path.join(Folder_Path, "data")
    os.makedirs(data_directory, exist_ok=True)
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    filename = "selected_coordinates.json"
    file_path = os.path.join(data_directory, filename)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    script_path = os.path.join(Folder_Path, "scripts", "GoogleEarth_Engine_Script.py")
    Thread(target=run_script, args=(script_path, Folder_Path, GEE_Project_ID, 'http://127.0.0.1:5000/video-player')).start()
    return jsonify({"message": "JSON file saved successfully, running the script."}), 200

def run_script(script_path, folder_path, gee_project_id, url):
    try:
        subprocess.run(["python", script_path, folder_path, gee_project_id], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Script {script_path} completed successfully.")
        webbrowser.open_new(url)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {script_path}: {e}")

def open_browser(url='http://127.0.0.1:5000/polygon'):
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        sleep(1)
        webbrowser.open_new(url)

if __name__ == '__main__':
    Thread(target=open_browser).start()  # Default URL is the polygon page
    app.run(debug=True)
