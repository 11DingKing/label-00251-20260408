from app import create_app, socketio
import os

app = create_app()

if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    if debug:
        # 开发模式
        socketio.run(app, debug=True, host='0.0.0.0', port=5001, allow_unsafe_werkzeug=True)
    else:
        # 生产模式使用 gunicorn: gunicorn -k eventlet -w 1 -b 0.0.0.0:5001 run:app
        socketio.run(app, debug=False, host='0.0.0.0', port=5001)
