import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
import gc


######################### Change Following Code ################################

# Your Connection Credentials
SSID = 'Your WiFi SSID'
PASSWORD = 'Your WiFi Password'

YOUR_GROUP_NAME = 'Your Group Name'
PASSWORD = 'Your Password'

################################################################################


######################### Do Not Change Following Code #########################

esp.osdebug(None)
gc.collect()

# MQTT Broker Information
mqtt_server = 'broker.hivemq.com'


# MQTT Client Information
mqtt_user = f"Rgen-Foresight-{YOUR_GROUP_NAME}"
mqtt_pass = PASSWORD
client_id = ubinascii.hexlify(machine.unique_id())


# MQTT Topics
topic_sub = f'rgen-foresight/{YOUR_GROUP_NAME}/sub'
topic_pub = f'rgen-foresight/{YOUR_GROUP_NAME}/pub'


last_message = 0
message_interval = 5
counter = 0


# Initialize WiFi Connection
station = network.WLAN(network.STA_IF)
station.active(True)

# Connect to WiFi
station.connect(SSID, PASSWORD)
print('Connecting to WiFi...', end='')

max_retries = 10
while station.isconnected() == False:
    if max_retries == 0:
        print('Failed to connect to WiFi')
        break
    print('.', end='')
    max_retries -= 1
    time.sleep(1)


print('Connection successful')

###############################################################################
