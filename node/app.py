from flask import Flask, request
from send_to_server import SendToServer

app = Flask(__name__)


@app.route('/node/ping', methods=['GET'])
def ping():
    return "pong"


@app.route('/node/check_packet', methods=['POST'])
def get_packet():
    data = request.get_json()

    sts = SendToServer()
    status = sts.process_packet(data["packet"])
    print("STATUS", status)
    return status


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
