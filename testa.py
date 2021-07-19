import threading

from flask import Flask
from flask import request
from flask import render_template
from flask import Response
from codevision.oldcare.camera import VideoCamera
from collectingfaces1 import runfacecollect
from variable import globalvar
app = Flask(__name__)
video_camera5=None
global_frame5=None

def video_stream5():
    global video_camera5
    global global_frame5
    globalvar.set_collect(True)
    t1 = threading.Thread(target=runfacecollect, args=(0, str(233),))
    t1.start()
    while True:
        if (globalvar.get_is_begin() is True):
            if (globalvar.get_collect() is False):
                break;
            else:
                frame = globalvar.get_global_frame5()
                if frame is not None:
                    global_frame5 = frame
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                else:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + global_frame5 + b'\r\n\r\n')

@app.route('/', methods=['GET', 'POST'])
def set_choice():
    return render_template('room.html')

@app.route('/video_viewer5')
def video_viewer5():
    return Response(video_stream5(), mimetype='multipart/x-mixed-replace; boundary=frame')

    # return None
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=5001)