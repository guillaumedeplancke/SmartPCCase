from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# repositories
from repositories.DataRepository import DataRepository
from repositories.SensorRepository import SensorRepository
from repositories.OutputRepository import OutputRepository
from repositories.CategoryRepository import CategoryRepository

# libraries
from libraries.DS18B20 import DS18B20
from libraries.LCD_I2C import LCD

# other
import time
import serial
import sys, os
import threading
from RPi import GPIO
from utils import serialize, get_interface_ipaddress
from easysettings import JSONSettings, load_json_settings

print("Backend aan het initialiseren...")

# Init app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'RandomSecureKey' # TODO: finals: generate random secret

socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False, ping_timeout=1)
CORS(app)

GPIO.setmode(GPIO.BCM)

# Variables
temperature_category = CategoryRepository.get_one_by_slug('temperature')
temperature_sensor_db = SensorRepository.get_for_category(temperature_category)[0]

endpoint = '/api/v1'
tempsensor = DS18B20(temperature_sensor_db.input_pin, temperature_sensor_db)
lcd = LCD(0x27)

voltage_sensor = SensorRepository.find_one_by_unit('V')
current_sensor = SensorRepository.find_one_by_unit('A')

power_button_id = None

custom_message = None

outputs = {}

for output in OutputRepository.all():
    GPIO.setup(output.output_num, GPIO.OUT)

    if output.is_pwm:
        output.pwm_object = GPIO.PWM(output.output_num, 100)
        output.pwm_object.start(0)
        output.set_value(0)
    elif output.name == 'Power button':
        power_button_id = output.id

    outputs[output.id] = output

sensors = {}

for sensor in SensorRepository.all():
    if sensor.input_bus == 'one_wire':
        sensor.hardware_object = tempsensor

    sensors[sensor.id] = sensor

latest_data = {}
latest_voltage = 0.00
latest_current = 0.00

categories = CategoryRepository.all()
fans_category = CategoryRepository.get_one_by_slug('fan')
ledstrips_category = CategoryRepository.get_one_by_slug('ledstrip')

# Electronics init
def init():
    wlan_ip = get_interface_ipaddress('wlan0')
    
    lcd.set_cursor(0, 0)
    
    if wlan_ip != 'offline':
        lcd.write_message(wlan_ip)
    else:
        lcd.write_message(get_interface_ipaddress('eth0'))

    lcd.set_cursor(1, 0)
    lcd.write_message("Temp: ")

    lcd.set_cursor(1, 12)
    lcd.write_character(chr(0xDF))
    lcd.write_character('C')


init()

# Threads
def main():
    global latest_data
    global latest_voltage
    global latest_current
    global custom_message

    while True:
        temperatuur = round(tempsensor.read_temperature(), 2)

        voltage_sensor.create_history_entry(latest_voltage)
        current_sensor.create_history_entry(latest_current)

        if custom_message is None:
            lcd.set_cursor(1, 6)
            lcd.write_message(str(temperatuur))
            lcd.set_cursor(1, 20)

        for sensor in sensors.values():
            if sensor.hardware_object is not None:
                sensor.create_history_entry(temperatuur)
            elif sensor.unit is 'V':
                sensor.create_history_entry(latest_voltage)
            elif sensor.unit is 'A':
                sensor.create_history_entry(latest_current)
            else:
                print('todo')

        json_data_out = []

        devices = []

        for output in outputs.values():
            devices.append(output)

        for sensor in sensors.values():
            devices.append(sensor)

        for category in categories:
            category_data = {
                "id": category.id,
                "name": category.name,
                "input": category.input,
                "output": category.output,
            }

            category_devices = []
            
            for device in devices:
                if device.category_id == category.id:
                    device_data = {
                        "id": device.id,
                        "name": device.name,
                        "value": device.latest_value
                    }

                    if hasattr(device, 'is_pwm'):
                        device_data['is_pwm'] = device.is_pwm

                    if hasattr(device, 'unit'):
                        device_data['unit'] = device.unit

                    category_devices.append(device_data)

            category_data["devices"] = category_devices
            json_data_out.append(category_data)

        latest_data = json_data_out

        socketio.emit('B2F_new_data', json_data_out)

        time.sleep(2.5)

main_thread = threading.Thread(target=main)
main_thread.start()

GPIO.setup(18, GPIO.OUT) # enable pin for arduino

def serial_worker():
    global latest_voltage
    global latest_current

    serialPort = serial.Serial('/dev/serial0')
    print(f"Connected to {serialPort.name}")

    GPIO.output(18, True)

    while True:
        data_in = serialPort.readline().strip().decode(encoding='utf-8', errors='replace')
        if data_in.count(" ") >= 3:
            data_in = data_in.split("A")
            latest_voltage = float(data_in[0].split(" ")[1])
            latest_current = float(data_in[1].split(" ")[1])

            if (latest_voltage < 20.0):
                latest_voltage = 0.0

            if (latest_voltage == 0.0):
                latest_current = 0.0
            # print(f"Values: {latest_voltage} V <-> {latest_current} A")

serial_thread = threading.Thread(target=serial_worker)
serial_thread.start()

def power_check_worker():
    global outputs
    global power_button_id
    global custom_message
    global config
    global fans_category
    global ledstrips_category

    test_counter = 0
    on_counter = 0
    enabled_outputs = False
    disabled_outputs = True

    while True:
        if latest_current < 0.3: # computer can be marked as off
            on_counter = 0

            if disabled_outputs == False:
                for output in outputs.values():
                    if output.is_pwm:
                        output.set_value(0)
                
                disabled_outputs = True
                enabled_outputs = False

                if custom_message is not None:
                    custom_message = None
                    
                    lcd.set_cursor(1, 0)
                    lcd.write_message("Temp:         ")
                    lcd.set_cursor(1, 12)
                    lcd.write_character(chr(0xDF))
                    lcd.write_message("C   ")
        elif on_counter > 4: # computer can be marked as on since the flowing current is higher than 0.25A for 5 seconds
            if enabled_outputs == False:
                for output in outputs.values():
                    if output.is_pwm:
                        if output.category_id == fans_category.id and config['spin_fans_on_boot'] == True:
                            output.set_value(50)
                        elif output.category_id == ledstrips_category.id and config['leds_on_boot'] == True:
                            output.set_value(50)
                        elif output.category_id != ledstrips_category.id and output.category_id != fans_category.id:
                            output.set_value(50)
                
                enabled_outputs = True
                disabled_outputs = False
        elif on_counter < 5: # wait 4 seconds before indicating that the computer is on
            on_counter += 1

        if outputs[power_button_id].latest_value == 1:
            if latest_current < 0.3:
                socketio.emit('B2F_alert', {'message': 'Booting computer...'})
            
            time.sleep(0.5)
            outputs[power_button_id].set_value(0)
            socketio.emit('B2F_output_changed', {'output': serialize(outputs[power_button_id])})

        time.sleep(0.5)

power_check_thread = threading.Thread(target=power_check_worker)
power_check_thread.start()

# Config init         
project_path = os.path.dirname(sys.argv[0])

config = load_json_settings(project_path + '/config.json')

if not hasattr(config, 'spin_fans_on_boot'):
    config['spin_fans_on_boot'] = True
    config.save()

if not hasattr(config, 'leds_on_boot'):
    config['leds_on_boot'] = True
    config.save()


# API Endpoints
@app.route('/')
def index():
    return f"Server is running. Go to {endpoint} to get data from this server."

@app.route(endpoint)
def api_index():
    return f"You are now in the right direction for getting data from the API :). Please check the postman collection for more information about the available routes."

import routes


# Socket IO
@socketio.on('connect')
def connect():
    print('A new client connected')
    socketio.emit('B2F_new_data', latest_data)

@socketio.on('F2B_change_output')
def change_output(msg):
    global custom_message
    
    output_id = int(msg['output_id'])
    output_value = int(msg['change_to'])
    
    print(f"change {output_id} requested to {output_value}")
    outputs[output_id].set_value(output_value)
    
    if output_id == power_button_id and latest_current > 0.3:
        socketio.emit('B2F_alert', {'message': 'Shutting down computer...'})

        custom_message = 'shutting down...'
        print('shutting down')
        lcd.set_cursor(1, 0)
        lcd.write_message(custom_message)
        lcd.set_cursor(1, 20)

    socketio.emit('B2F_output_changed', {'output': serialize(outputs[output_id], '_pwm')})

# Start app
try:
    if __name__ == '__main__':
        print("Backend is running...")
        socketio.run(app, debug=False, host='0.0.0.0')
except KeyboardInterrupt as e:
    print(e)
finally:
    GPIO.output(18, False)

    for output in outputs.values():
        if output.is_pwm:
            output.pwm_object.stop()

    GPIO.cleanup()

    print('Backend stopped...')
