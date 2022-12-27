from geventwebsocket.handler import WebSocketHandler
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import subprocess
import csv

app = Flask(__name__)

# initialize socketio
socketio = SocketIO(app, async_mode='threading', handler_class=WebSocketHandler)

# list to store album data
data = []

# read csv file and store data in the albums list
with open('albums.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)

# route to render the index template
@app.route('/')
def index():
    albums_dict = []
    with open('albums.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            album = {
                    'artist': row[0],
                    'album': row[1],
                    'url': row[2],
                    'cover': row[3]
                    }
            albums_dict.append(album)
    return render_template('index.html', albums=albums_dict)

# route to add a new album
@app.route('/submit', methods=['POST'])
def submit():
    artist = request.form['Artist']
    album = request.form['Album']
    url = request.form['Url']
    cover = request.form['Album cover']

    with open('albums.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([artist, album, url, cover])

    return redirect('/')

# route to clear the albums list and csv file
@app.route('/clear')
def clear():
    # clear albums list
    data.clear()
    # write empty list to csv file
    with open('albums.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([])
    # redirect to the index route
    return redirect(url_for('index'))

@socketio.on('download')
def download():
    # run the dl.sh script and capture the output
    process = subprocess.Popen(['sh', 'dl.sh'], stdout=subprocess.PIPE)
    print(process)
    # listen for new output from the process
    while True:
        line = process.stdout.readline()
        if line:
            # send the output to the frontend
            socketio.emit('output', line )
        else:
            break
    socketio.emit('download_complete')

@app.route('/download', methods=['POST'])
def download_route():
    # run the dl.sh script and capture the output
    result = subprocess.run(['bash', 'dl.sh'], stdout=subprocess.PIPE)
    # return the output to the frontend
    return result.stdout

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
