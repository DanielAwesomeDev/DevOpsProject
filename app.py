from flask import Flask
import stomp

app = Flask(__name__)

ACTIVE_MQ_HOST = 'nodemq.default.svc'  # Use the name of the ActiveMQ service in Kubernetes
ACTIVE_MQ_PORT = 444  # Default STOMP port for ActiveMQ
QUEUE_NAME = '/queue/test'

@app.route('/')
def hello_world():
    send_message("Accessed Flask App!")
    return 'Hello, World!'

def send_message(message):
    conn = stomp.Connection([(ACTIVE_MQ_HOST, ACTIVE_MQ_PORT)])
    #conn.start()
    # Please replace 'admin' and 'password' with the actual credentials you have for ActiveMQ.
    conn.connect(login='admin', passcode='admin', wait=True)  
    conn.send(body=message, destination=QUEUE_NAME)
    conn.disconnect()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

