import stomp
import time

class MyListener(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print(f'Error: {message}')
        
    def on_message(self, headers, message):
        print(f'Received message: {message}')

# ActiveMQ configuration
ACTIVE_MQ_HOST = '192.168.49.2'  # Assuming that this is the service name in Kubernetes
ACTIVE_MQ_PORT = 32729
QUEUE_NAME = '/queue/test'

# Establish connection to ActiveMQ
conn = stomp.Connection([(ACTIVE_MQ_HOST, ACTIVE_MQ_PORT)])
conn.set_listener('', MyListener())

# Using the default admin/admin credentials
conn.connect('admin', 'admin', wait=True)
conn.subscribe(destination=QUEUE_NAME, id=1, ack='auto')

# Keep the script running to consume messages
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    conn.disconnect()

