import sqlite3
import pandas as pd
from datetime import datetime
import sys
import os

current_time = datetime.now()


def print_tables():
    conn = sqlite3.connect('plantdata.db')
    cursor = conn.cursor()
    print_tables = ("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:")
    print(tables)
    conn.close()
    

def print_plant():
    conn = sqlite3.connect('plantdata.db')
    cursor = conn.cursor()    
    df = pd.read_sql_query('SELECT * from plant', conn)
    print(df.head())
    conn.close()

def print_sensor():
    conn = sqlite3.connect('plantdata.db')
    cursor = conn.cursor()
    df = pd.read_sql_query('SELECT * from sensorevent', conn)
    print(df.head())
    conn.close()

def print_plantsensor():
    conn = sqlite3.connect('plantdata.db')
    cursor = conn.cursor()
    df = pd.read_sql_query('SELECT * from plantsensor', conn)
    print(df.head())
    conn.close()

def print_sensor1():
    conn = sqlite3.connect('plantdata.db')
    cursor = conn.cursor()
    df = pd.read_sql_query('SELECT * from SENSOR', conn)
    print(df.head())
    conn.close()

def delete_plant_data():
    conn = sqlite3.connect('plantdata.db')
    cursor = conn.cursor()
    delete_query = "DELETE FROM plant;"
    cursor.execute(delete_query)
    conn.commit()
    print('table data cleared')
    conn.close()

def delete_sensor_data():
    conn = sqlite3.connect('plantdata.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SENSOR")
    print("Data before deletion:")
    print(cursor.fetchall())
    cursor.execute("DELETE FROM SENSOR")
    conn.commit()
    cursor.execute("SELECT * FROM SENSOR")
    print("\nData after deletion:")
    print(cursor.fetchall())
    conn.close()

def delete_sensor_event():
    conn = sqlite3.connect('plantdata.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SENSOREVENT")
    print("Data before deletion:")
    print(cursor.fetchall())
    cursor.execute("DELETE FROM SENSOREVENT")
    conn.commit()
    cursor.execute("SELECT * FROM SENSOREVENT")
    print("\nData after deletion:")
    print(cursor.fetchall())
    conn.close()

def ldr_sensor():
    conn = sqlite3.connect('plantdata.db')
    cursor = conn.cursor()
    insert_plant_data = 'INSERT INTO SENSOR(ID, Type, Active) VALUES (?, ?, ?)'
    cursor.execute(insert_plant_data, ('1', 'LDR', 'active'))
    print('Sensor Registered!')
    df = pd.read_sql_query('SELECT * from SENSOR', conn)
    print(df.head())
    conn.commit()
    conn.close()


def soil_moisture_sensor():
    conn = sqlite3.connect('plantdata.db')
    cursor = conn.cursor()
    insert_plant_data = 'INSERT INTO SENSOR (ID, Type, Active) VALUES (?, ?, ?)'
    cursor.execute(insert_plant_data, ('2', 'Soil Moisture', 'active'))
    print('Sensor Registered!')
    df = pd.read_sql_query('SELECT * from SENSOR', conn)
    print(df.head())
    conn.commit()
    conn.close()


def insert_data_into_plantsensor():
    conn = sqlite3.connect('plantdata.db')
    cursor = conn.cursor()
    insert_plant_data = 'INSERT INTO PLANTSENSOR (PlantID, SensorID, StartDate, EndDate) VALUES (?, ?, ?, ?)'
    print('Which Sensor?')
    sensor_id = input()
    cursor.execute(insert_plant_data, ('1', sensor_id, current_time, 'active'))
    df = pd.read_sql_query('SELECT * from PLANTSENSOR', conn)
    print(df.head())
    conn.commit()
    conn.close()

def delete_plantsensor():
    conn = sqlite3.connect('plantdata.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PLANTSENSOR")
    print("Data before deletion:")
    print(cursor.fetchall())
    cursor.execute("DELETE FROM PLANTSENSOR")
    conn.commit()
    cursor.execute("SELECT * FROM PLANTSENSOR")
    print("\nData after deletion:")
    print(cursor.fetchall())
    conn.close()
def restart():
    python = sys.executable
    os.execv(python, [python] + sys.argv)

print('Table commands: ')
print('1. print all tables\n2. print plant table\n3. print sensor data\n4. delete plant table data\n5. add ldr sensor\n6. add soil moisture\n7. print sensors\n8. delete sensor data\n9. delete collected sensor data\n10. delete plantsensor data\n11. register plantsensor\n12. print plantsensor')
commands = input()
if commands == '1':
    print_tables()
    restart()
elif commands == '2':
    print_plant()
    restart()
elif commands == '3':
    print_sensor()
    restart()
elif commands == '4':
    delete_plant_data()
    restart()
elif commands == '5':
    ldr_sensor()
    restart()
elif commands == '6':
    soil_moisture_sensor()
    restart()
elif commands == '7':
    print_sensor1()
    restart()
elif commands == '8':
    delete_sensor_data()
    restart()
elif commands == '9':
    delete_sensor_event()
    restart()
elif commands == '10':
    delete_plantsensor()
    restart()
elif commands == '11':
    insert_data_into_plantsensor()
    restart()
elif commands == '12':
    print_plantsensor()
    restart()



