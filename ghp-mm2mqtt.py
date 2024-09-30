#!/usr/bin/env python3

import sys
import serial
import paho.mqtt.client as mqtt
import struct
import json
import time
import logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

#serial port
serial_port='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A5069RR4-if00-port0';

# MQTT broker settings
MQTT_BROKER = "172.16.1.254"  # Replace with your broker address
MQTT_PORT = 1883  # Default MQTT port
MQTT_TOPIC_PREFIX= "GHP"
MQTT_USERNAME = "ghp"  # Replace with your MQTT username
MQTT_PASSWORD = "asdf"  # Replace with your MQTT password

#experimental write msg, sent only once and only if not empty, have to be valid modbus datagram including crc
#write slave 241 addr 2000 data: 8 0 0 21 26 43 27
#writemsg=b'\xF0\x10\x07\xD0\x00\x07\x0E\x00\x08\x00\x00\x00\x00\x00\x15\x00\x1A\x00\x2B\x00\x1B\x4E\x84'
#writemsg=b'\xF0\x10\x07\xD0\x00\x07\x0E\x00\x08\x00\x01\x00\x10\x00\x15\x00\x1A\x00\x2B\x00\x1B\x87\xB8'
writemsg=''



# Function to calculate Modbus CRC16
def modbus_crc16(data: bytes) -> int:
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if (crc & 0x0001) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc

# Function to verify the CRC of a Modbus message
def verify_modbus_crc(data: bytes) -> bool:
    if len(data) < 4:  # Minimal Modbus frame size with CRC
        return False
    received_crc = struct.unpack('<H', data[-2:])[0]  # Last 2 bytes are the CRC
    calculated_crc = modbus_crc16(data[:-2])  # CRC of the data without the last 2 CRC bytes
    _logger.debug(f"received crc: {received_crc} = calculated_crc {calculated_crc}");
    return received_crc == calculated_crc

def publish(slave,op,addr,data):
    data = json.dumps(data)
    MQTT_TOPIC=f"{MQTT_TOPIC_PREFIX}/{op}/{slave}/{addr}"
    _logger.info(f"{MQTT_TOPIC}: {data}")
    mqtt_client.publish(MQTT_TOPIC, data)

def decodeModbus():
    global buffer
    global readAddr
    global writemsg
    global ser
    
    _logger.debug(f"buffer={buffer}")
    buflen=len(buffer)
    if buflen < 8:
        return
    index = buffer.find(240) #find slave 240
    if index < 0 or buflen-index < 8:
        return
    buffer = buffer[index:] #discard all data before
    _logger.debug(f"found on postion {index}\nbuffer={buffer}\n")
    if buffer[1] == 3:  # 0x3 read command
     if verify_modbus_crc(buffer[0:8]): #test Read Request (fixed sized)
      readAddr=struct.unpack('>h',buffer[2:4])[0] # valid ReadRequest, save target address
      buffer = buffer[8:]
     else:  #Read response
      psize=buffer[2]+5 # id + 03 + size + data + crc1 +crc2
      if verify_modbus_crc(buffer[0:psize]):
        numshorts=int((psize-5)/2)
        publish(buffer[0],3,readAddr,struct.unpack(f'>{numshorts}h',buffer[3:psize-2]))
        if len(writemsg) > 5: 
          _logger.info(f"WRITE {writemsg}\n")
          ser.write(writemsg)  
          writemsg='';
        buffer = buffer[psize:]
      else:
       buffer = buffer[1:]  #no valid crc, could be xf0x03 sequence in data, skip 1st byte
    elif buffer[1] == 16: # 0x10 write command
      psize=buffer[6]+9 # id + 03 + size + data + crc1 +crc2
      _logger.debug(f"psize={psize} packet={buffer[0:psize]}")
      if buflen > psize and verify_modbus_crc(buffer[0:psize]):
       readAddr=struct.unpack('>h',buffer[2:4])[0]
       numshorts=int((psize-9)/2)
       publish(buffer[0],10,readAddr,struct.unpack(f">{numshorts}h",buffer[7:psize-2]))
       buffer = buffer[psize:]
      else:
       buffer = buffer[1:] #no valid crc, could be xf0x10 sequence in data, skip 1st byte
    else: #not 0x03 or 0x10 skip
     buffer = buffer[1:]
 
    decodeModbus()


# Initialize and connect to the MQTT broker with authentication
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)  # Set username and password
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

buffer=bytearray(0)
readAddr=0

# Open serial port
ser = serial.Serial(
    port=serial_port,
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=0  # blocking read
)

# Check if the port is open
if ser.is_open:
    _logger.info(f"Serial port {ser.port} opened successfully!")
    ser.reset_input_buffer()
try:
    while True:
        data = ser.read(1)
        data += ser.read(ser.inWaiting())
        if data:
            buffer+=data
            decodeModbus()                
        else:
            _logger.warning("No data received.")
        time.sleep(0.3)             

except KeyboardInterrupt:
    _logger.info("Exiting program...")

finally:
    ser.close()
    mqtt_client.disconnect()
    _logger.info("Serial port and MQTT connection closed.")
