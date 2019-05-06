import json

from .database.usages import store_usage
from .database.devices import initialize_device
from .mqtt_config import MQTT_PATH, MQTT_SERVER, MQTT_PORT

def null_action(data):
    return

def switch_action(action_type):
    actions = {
        'usage': store_usage,
        'initialize': initialize_device,
    }
    return actions.get(action_type, null_action)
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print('Connected to MQTT on ' + str(MQTT_SERVER) + ':' + str(MQTT_PORT))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    data = json.loads(message)
    # print(data)

    action_type = data.get('type', None)
    callback = switch_action(action_type)

    payload = data.get('payload', {})
    callback(payload)
