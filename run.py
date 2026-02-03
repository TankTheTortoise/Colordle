from app import create_app, socketio

flask_app = create_app()

if __name__ == "__main__":

    socketio.run(flask_app, allow_unsafe_werkzeug=True, debug=True)
