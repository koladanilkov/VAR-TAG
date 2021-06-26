import time
import network
import app.secrets as secrets
from app.mymqtt import MQTTClient
from .hardwear import client_id
import machine


mqtt_server = '109.248.175.51'
topic_sub_scan = b'test/scan'
topic_sub_ip = b'test/'+ client_id + b'/get/ip'
topic_sub_reset = b'test/'+ client_id + b'/reset'
topic_sub_reset_all = b'test/reset'
topic_sub_web_repl = b'test/'+ client_id + b'/web_repl'


topic_pub_health_check = b'test/' + client_id + b'/health_check'
topic_pub_reset = b'test/'+ client_id + b'/reset/ok'
topic_pub_scan = b'test/' + client_id
topic_pub_status = b'test/' + client_id + b'/status'
topic_pub_ip = b'test/' + client_id + b'/ip'

machineIp = '(0, 0, 0, 0)'
client = None


def connectToWiFi():
  global machineIp
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
  print('conneting to wifi..')
  while not station.isconnected():
      pass
  print('Connection successful')
  print(station.ifconfig())
  machineIp = station.ifconfig()[0]

def health_check_pub(msg):
  client.publish(topic_pub_health_check, str(msg))
  
def reset_pub():
  client.publish(topic_pub_reset, '1')


def sub_cb(topic, msg):
  print((topic, msg))
  if topic == topic_sub_scan and msg == b'1':
    client.publish(topic_pub_scan, "1")
  elif (topic == topic_sub_reset or topic == topic_sub_reset_all) and msg == b'1':
    print('mqtt => reset')
    reset_pub()
    machine.reset()
  elif (topic == topic_sub_ip and msg == b'1'):
    print('mqtt => get ip')
    client.publish(topic_pub_ip, machineIp)
  elif (topic == topic_sub_web_repl):
    reset_pub()
    webReplOn()
    
def connect_and_subscribe():
  client = MQTTClient(client_id, mqtt_server, user = b'test', password = b'P@ssw0rd!')
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub_scan)
  client.subscribe(topic_sub_reset)
  client.subscribe(topic_sub_reset_all)
  client.subscribe(topic_sub_ip)
  client.subscribe(topic_sub_web_repl)
  
  print('Connected to %s MQTT broker, subscribed to topics: \n %s \n %s \n %s \n %s \n %s' % (mqtt_server,  topic_sub_scan, topic_sub_reset, topic_sub_reset_all, topic_sub_ip, topic_sub_web_repl))
  return client


def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()  
  
  
def connectToMQTT():
  global client
  try:
    client = connect_and_subscribe()
  except OSError as e:
    restart_and_reconnect()
    
def webReplOn():
    import btree
    f = open("mydb", "w+b")
    db = btree.open(f)
    db[b"wr"] = b"1"
    db.flush()
    machine.reset()
    
def webReplOff():
    import btree
    f = open("mydb", "w+b")
    db = btree.open(f)
    db[b"wr"] = b"0"
    db.flush()
    machine.reset()
    
