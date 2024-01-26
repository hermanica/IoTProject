import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from datetime import datetime
import database 

reader = SimpleMFRC522()


MQTT_BROKER = "10.108.33.126"
MQTT_TOPIC = "rfid"

conn = database.create_connection("pythonsqlite.db")

def handle_card_detected(card_id):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = database.check_card_status(conn, str(card_id))
    
    if status is None or status == 0:  
        database.insert_card_entry(conn, (str(card_id), current_time))
        mqtt_client.publish(MQTT_TOPIC, f"{card_id},{'entered'},{'Cars inside:' + str(database.get_cards_amount(conn))},{current_time}")
        
    else:  # card is inside
        entry_time = str(database.get_entry_time(conn, card_id))
        database.update_card_exit(conn, str(card_id), current_time)
        mqtt_client.publish(MQTT_TOPIC, f"{card_id},{'exited'},{'Cars inside:' + str(database.get_cards_amount(conn))},{'entered at:' + entry_time},{'exited at:' + current_time}")

try:
    mqtt_client = mqtt.Client()
    mqtt_client.connect(MQTT_BROKER)

    while True:
        card_id, _ = reader.read()
        handle_card_detected(card_id)
        time.sleep(2)
        
except KeyboardInterrupt:
    GPIO.cleanup()
    conn.close()


