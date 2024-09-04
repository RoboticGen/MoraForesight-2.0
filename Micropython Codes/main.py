from machine import Pin, I2C
from time import sleep
import BME280
import ujson as json
import dht

def sub_cb(topic, msg):
  print("MQTT msg received :")
  print(f"Topic: {topic.decode('utf-8')}")
  print(f"Message: {msg.decode('utf-8')}")

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server, user=mqtt_user, password=mqtt_pass)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(1)

# Initialize I2C (SCL: 22, SDA: 21)
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)

# Initialize BME280
bme = BME280.BME280(i2c=i2c)

# Initialize DHT22
dht_sensor = dht.DHT22(Pin(14))

while True:
  try:
    # Connect to MQTT Broker
    client = connect_and_subscribe()
  except OSError as e:
    # Restart and Reconnect
    restart_and_reconnect()
  try:

    # Check for MQTT Messages
    client.check_msg()

    # Read DHT22 Sensor Data
    dht_sensor.measure()
    temp = dht_sensor.temperature()
    hum = dht_sensor.humidity()

    # Read BME280 Sensor Data
    pres = bme.pressure

    # Print Data
    print(f"Temperature: {temp}°C | Humidity: {hum}% | Pressure: {pres}hPa")

    # Prepare Data
    data = {'Temperature':temp,'Humidity':hum ,'Pressure':pres}

    # Publish Data
    if (time.time() - last_message) > message_interval:
      msg = json.dumps(data)
      client.publish(topic_pub, msg)
      last_message = time.time()
      counter += 1
    sleep(5)

  except OSError as e:
    restart_and_reconnect()
