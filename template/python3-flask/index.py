# Copyright (c) Alex Ellis 2017. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

from flask import Flask, request, Response
from function import handler
#from gevent.wsgi import WSGIServer
from gevent.pywsgi import WSGIServer
from gevent.queue import Queue
from gevent.pool import Pool
from gevent.pywsgi import StreamServer
import json
import random
import gevent

app = Flask(__name__)
event_queue = Queue()


@app.before_request
def fix_transfer_encoding():
    """
    Sets the "wsgi.input_terminated" environment flag, thus enabling
    Werkzeug to pass chunked requests as streams.  The gunicorn server
    should set this, but it's not yet been implemented.
    """

    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == u"chunked":
        request.environ["wsgi.input_terminated"] = True

def get_events():
    event = event_queue.get()
    return event

@app.route("/stream", methods=["GET"])
def stream():
    #if event_queue.empty():
    #    return "Queue is empty"
    def event_stream():
        #try:
        while True:
            die_rolls = {u"1D6": random.randint(1, 6),
                        u"1D20": random.randint(1, 20)}
            yield "data: " + json.dumps(die_rolls) + "nn"

        with app.app_context():
            gevent.sleep(0.2)
        #except GeneratorError:
        #    print("nope")
    return Response(event_stream(), mimetype="text/event-stream")

@app.route("/", defaults={"path": ""}, methods=["POST", "GET"])
@app.route("/<path:path>", methods=["POST", "GET"])
def main_route(path):
    zip_file = request.files.getlist('files')[0]
    job = gevent.spawn(handler.handle, zip_file, event_queue)
    job.get(timeout=300)
    return 'OK'
