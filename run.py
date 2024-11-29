from app import app, socketio
from flask_script import Manager

if __name__ == '__main__':
    socketio.run(app, debug=True, port=80, host="0.0.0.0")
    #manager.run()