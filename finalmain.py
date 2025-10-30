import schedule
import time
import cv2
import numpy as np
from inference_sdk import InferenceHTTPClient
from PIL import Image
import sqlite3
from datetime import datetime
import requests
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_dht
from pprint import pprint
import pandas as pd
import os
import sys



current_time = datetime.now()
#MCP setup
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.CE0)
mcp = MCP.MCP3008(spi, cs) 

#channel
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)


flowerish_menu_str = "✿✿✿ Flowerish Menu ✿✿✿\n1. Register Plant\n2. Test Notification\n3. Start Data Collection\n4. Print Data Collection\n5. Register Sensor\nType in the number corresponding with desired option"
print(flowerish_menu_str)
user_input = input()

def weather():
    try:
        sensor = adafruit_dht.DHT22(board.D4)
        temperature_c = sensor.temperature
        humidity = sensor.humidity
        requests.post("https://ntfy.sh/#########",
            data=('Temp={0:0.1f}C, Humidity={1:0.1f}%'.format(temperature_c, humidity)).encode(encoding='utf-8'))
    except RuntimeError:
        weather()
    else:
        None
    

def sensor_read():
    conn = sqlite3.connect('plantdata.db')
    cursor = conn.cursor() 
    #convert string --> float
    ldr_voltage_results = str(chan1.voltage)
    ldr_voltage = float(ldr_voltage_results)
    soil_moisture_voltage_results = str(chan0.voltage)
    soil_moisture_voltage = float(soil_moisture_voltage_results)

    #bad or good light detection
    if ldr_voltage > 1:
        print('Good light')
    elif ldr_voltage < 1:
        print('Bad light')
        requests.post("https://ntfy.sh/#########",
            data="Plant Light low, turning on light".encode(encoding='utf-8'))
        
    if soil_moisture_voltage >= 3.261:
        print('Moisture is bad')
        requests.post("https://ntfy.sh/##########",
            data="Plant moisture is bad, watering plant".encode(encoding='utf-8'))
    elif soil_moisture_voltage < 3.261:
        print('Moisture is fine')
    
    #plant data insertion into sql
    insert_plant_data = 'INSERT INTO SENSOREVENT (SensorID, DateTime, Value) VALUES (?, ?, ?)'
    cursor.execute(insert_plant_data, ( '1', current_time, ldr_voltage))
    cursor.execute(insert_plant_data, ('2', current_time, soil_moisture_voltage))
    print('data inserted')
    conn.commit()
    conn.close()
    

def print_plant():  
    conn = sqlite3.connect('plantdata.db')
    cursor = conn.cursor()
    df = pd.read_sql_query('SELECT * from SensorEvent', conn)
    pprint(df.head())
    conn.close()

def register_sensor():
    conn = sqlite3.connect('plantdata.db')
    cursor = conn.cursor()
    print('What sensor are you registering?\n1. LDR sensor\n2. Soil moisture')
    sensor_response = input()
    if sensor_response == '1':
        insert_plant_data = 'INSERT INTO SENSOR(ID, Type, Active) VALUES (?, ?, ?)'
        cursor.execute(insert_plant_data, ('1', 'LDR', 'active'))
        requests.post("https://ntfy.sh/############",
            data="LDR sensor registered".encode(encoding='utf-8'))
        print('Sensor Registered!')
    elif sensor_response == '2':
        insert_plant_data = 'INSERT INTO SENSOR (ID, Type, Active) VALUES (?, ?, ?)'
        cursor.execute(insert_plant_data, ('2', 'Soil Moisture', 'active'))
        requests.post("https://ntfy.sh/############",
            data="Soil moisture sensor registered".encode(encoding='utf-8'))
        print('Sensor Registered!')
    conn.commit()
    conn.close()



def take_image():
    current_time = datetime.now()

#cam setup
    cam = cv2.VideoCapture(0)
    cam.set(3,640)
    cam.set(4,480)

#Inference
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="#################"
)

    conn = sqlite3.connect('plantdata.db')
    cursor = conn.cursor()
    
    ret, frame = cam.read()
    print('image taken')
    cam.release()

    #convert image
    img_convert = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    PIL_image = Image.fromarray(img_convert)
    model_id ="only3houseplants-rfr31/7"

    #inference result
    result = CLIENT.infer(PIL_image, model_id)

    #search for class
    for predictions in result['predictions']:
        plant_type = predictions['class']
    
    #data added to sql
    try:
        insert_data_query = 'INSERT INTO PLANT (Type, Active, Registered) VALUES (?, ?, ?)'
        cursor.execute(insert_data_query, (plant_type, 'active', current_time))
        conn.commit()
        print('data inserted')

    except UnboundLocalError:
        print('No plant found, trying again')
        take_image()
    else:
    #notification
        requests.post("https://ntfy.sh/########",
            data=f'Registered: {plant_type}, At: {current_time}'.encode(encoding='utf-8'))
    conn.close()
    print('Registration Process completed!')

def restart():
    python = sys.executable
    os.execv(python, [python] + sys.argv)
if user_input =='1':
    print('Plant Registering Process Started!')
    take_image()
    restart()
if user_input =='2':
    print('Testing Notifications!')
    requests.post("https://ntfy.sh/##############",
            data='Test Notification'.encode(encoding='utf-8'))
    restart()
if user_input =='3':
    print('Data Collection Started')
    sensor_read()
    schedule.every().day.at('09:00').do(weather)
    schedule.every(.25).minutes.do(sensor_read)  
if user_input =='4':
    print('Printing Collected Data')
    print_plant()
    restart()
if user_input =='5':
    print('Sensor registration started!')
    register_sensor()
    restart()


while True:
    schedule.run_pending()



 
    




