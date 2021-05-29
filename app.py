import flask
from flask import jsonify, Response, request
import re
import requests
import youtube_dl

app = flask.Flask(__name__)

@app.route('/youtube/data/video/<id>', methods=['GET'])
def video_info(id):
    if not is_valid_id(id):
        return Response("{'error':'The given ID is no valid ID.'}", status=400, mimetype='application/json')

    ydl_opts = {'simulate': True, 'quiet': True}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info('https://www.youtube.com/watch?v=' + id)
        return jsonify(info)

@app.route('/youtube/data/channel/byname/<id>', methods=['GET'])
def channel_info(id):
    if not is_valid_id(id):
        return Response("{'error':'The given ID is no valid ID.'}", status=400, mimetype='application/json')

    channel_url = 'https://www.youtube.com/c/' + id
    ydl_opts = {'simulate': True, 'quiet': True}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url)
        info['thumbnail'] = get_channel_thumbnail(info['id'])
        return jsonify(info)

@app.route('/youtube/data/channel/byname/<id>/videos', methods=['GET'])
def channel_videos(id):
    if not is_valid_id(id):
        return Response("{'error':'The given ID is no valid ID.'}", status=400, mimetype='application/json')
    
    ydl_opts = {'simulate': True, 'quiet': True, 'extract_flat': True}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info('https://www.youtube.com/c/' + id + '/videos')
        return jsonify(info['entries'])

def is_valid_id(id):
    return re.match('^[a-zA-Z0-9_-]+$', id)

def get_channel_thumbnail(channel_id):
    thumbnail_url = None
    try:
        headers = {"User-Agent":"Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"}
        url = 'https://notyoutube.org/channel/' + channel_id
        html = requests.get(url, headers=headers).text
        thumbnail_search_results = re.search('\"([^\"]+/ytc/[^\"]+)\"', html)
        if thumbnail_search_results != None:
            thumbnail_url = thumbnail_search_results.group(1)
            if thumbnail_url.startswith('/'):
                thumbnail_url = 'https://notyoutube.org' + thumbnail_url
    except:
        return None
    return thumbnail_url

if __name__ == '__main__':
    app.run()
