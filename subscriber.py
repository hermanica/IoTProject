import paho.mqtt.client as mqtt
import time
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331
import neopixel
import board
import RPi.GPIO as GPIO


MQTT_BROKER = "10.108.33.126"
pixels=neopixel.NeoPixel(board.D18, 8,brightness=1.0/32, auto_write=False)
buzzerPin = 23
GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.output(buzzerPin, 1)

def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(",")

    print("id:"+message_decoded[0]+" "+"status "+message_decoded[1])
    buzzer(True)
    pixels_show(message_decoded)
    display_info(message_decoded)
    output_clear()
    
    
def buzzer(state):
    GPIO.output(buzzerPin, not state) 
        
        
def display_info(msg):
	disp.clear()
	
	image_message = Image.new("RGB",(disp.width, disp.height), "WHITE")
	draw_message=ImageDraw.Draw(image_message)
	
	font_large=ImageFont.truetype('./lib/oled/Font.ttf',11)
	
	text_width, text_height =draw_message.textsize("id:"+msg[0], font=font_large)
	draw_message.text((0,0),"id:"+msg[0], font=font_large, fill="BLACK")
	draw_message.text((0,12),"status"+msg[1], font=font_large, fill="BLACK")
	draw_message.text((0,24),msg[2], font=font_large, fill="BLACK")

	disp.ShowImage(image_message,0,0)
	
def pixels_show(msg):
		
		if(msg[1]=="entered"):
			pixels.fill((0,255,0))
		else:
			pixels.fill((255,0,0))
		pixels.show()
		

def output_clear():
	time.sleep(0.5)
	buzzer(False)
	time.sleep(1)
	pixels.fill((0,0,0))
	pixels.show()
	disp.clear()
	

	

if __name__ == "__main__":
	disp = SSD1331.SSD1331()
	disp.Init()
	disp.clear()
	client = mqtt.Client()
	client.connect(MQTT_BROKER)
	client.on_message = process_message
	client.subscribe("rfid")
	client.loop_forever()
