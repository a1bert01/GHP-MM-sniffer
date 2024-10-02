communication between the unit and the controller:
```
- modbus 9600 8n1 (B - brown A - red wire to the controller, or L_A L_B to U19 on the base board)
- master: unit; slave: controller (id: 240)
```
```
-unit regularly writes its operating data to the  at addr position 300+40 see manual - parameter reading ( M + down arrow buttons )
-the unit regularly writes temperatures and something (addr position 1000): GHP/10/240/1000: [0, 21, 44, 21, 0]
0 - status  (1-oil return)
21 - return temp
44 - DHW temp
21 - output temp
0 -  (error code??)

-the unit regularly reads the driver status (addr position 2000): GHP/3/240/2000: [8, 1, 16, 20, 26, 43, 27]:
8 - current operational mode 
1 - controller is on (0 - off)
16 - some bit mask 16 = 00001000 5th bit night mode enabled
20 - cooling temperature
43 - DHW temperature
27 - heating temperature
- the unit regularly queries the registers (operation 0x04, address 0)

    ID: 240, Read Input Registers: 0x04, Read address: 0, Read Quantity: 4
    ID: 240, Read Input Registers: 0x04, Read byte count: 8, Read data: [00 00 00 00 00 00 00 00 00 00 00]

- when service settings are changed, the 1st register is set to 1 and the unit reads the current setting several times in succession
- write requests for slaves 251 and 224 can be seen on bus too (with no response)

```
a sample communication,  "GHP/10/240/400" is my topic for MQTT message means operation 0x10,slave 240, address 400, followed by json array of short integers

```
GHP/10/240/400: [0, 0, 0, 0, 17665]  ???
GHP/10/240/316: [23, 0, 0, 0, 65, 0, 25, 2, 0, 0, 0, 0, 44, 21, 2, 0] write status variables 17-32
GHP/3/240/2000: [8, 1, 16, 20, 26, 43, 27] read controller status 
GHP/10/240/400: [0, 0, 0, 0, 17665] ??
GHP/10/240/300: [0, 96, 12, 21, 20, 20, 14, 17, 0, 0, 0, 0, 0, 0, 0, 0] write status variables 1-16
GHP/3/240/2000: [8, 1, 16, 20, 26, 43, 27]
GHP/10/240/400: [0, 0, 0, 0, 17665]
GHP/10/240/1000: [0, 21, 44, 21, 0]  
GHP/10/240/400: [0, 0, 0, 0, 17665]
GHP/3/240/2000: [8, 1, 16, 20, 26, 43, 27]
GHP/10/240/400: [0, 0, 0, 0, 17665]
GHP/10/240/300: [0, 96, 12, 21, 20, 20, 14, 17, 0, 0, 0, 0, 0, 0, 0, 0]
GHP/3/240/2000: [8, 1, 16, 20, 26, 43, 27]
GHP/10/240/400: [0, 0, 0, 0, 17665]
GHP/10/240/1000: [0, 21, 44, 21, 0]
GHP/10/240/400: [0, 0, 0, 0, 17665]
GHP/10/240/332: [14, 0, 0, 0, 6, 0, 0, 2]
GHP/3/240/2000: [8, 1, 16, 20, 26, 43, 27]
GHP/10/240/400: [0, 0, 0, 0, 17665]
GHP/3/240/2000: [8, 1, 16, 20, 26, 43, 27]
GHP/10/240/400: [0, 0, 0, 0, 17665]
GHP/10/240/1000: [0, 21, 44, 21, 0]
GHP/10/240/400: [0, 0, 0, 0, 17665]
GHP/10/240/332: [14, 0, 0, 0, 6, 0, 0, 2]
GHP/3/240/2000: [8, 1, 16, 20, 26, 43, 27]
GHP/10/240/400: [0, 0, 0, 0, 17665]
GHP/10/240/316: [23, 0, 0, 0, 65, 0, 25, 2, 0, 0, 0, 0, 44, 21, 2, 0]
GHP/3/240/2000: [8, 1, 16, 20, 26, 43, 27]
GHP/10/240/400: [0, 0, 0, 0, 17665]
GHP/10/240/300: [0, 96, 12, 21, 21, 20, 14, 17, 0, 0, 0, 0, 0, 0, 0, 0]
ID: 240, Read Input Registers: 0x04, Read address: 0, Read Quantity: 4
ID: 240, Read Input Registers: 0x04, Read byte count: 8, Read data: [00 01 00 00 00 00 00 00] service settings have been changed
GHP/3/240/2100: [2, 5, 0, -1, 68, 68, 68, 80, 80, 80, -5, 12, 40, 96, 60, 85] read service settings from controller
GHP/3/240/2116: [1, 55, 65, 30, 0, 72, 76, 0, 0, 4, 0, 5, 0, 5, 0, 24]
GHP/3/240/2132: [3, 3, -30, 0, 0, 0, 17, 10, -20, 15, 10, 50, 2, -5, 26, 0]
GHP/3/240/2148: [0, 0, 35, 60, 17, 53, 44, 40, 5, 0, 0, 0, 90, 70, 1, 3]
GHP/3/240/2164: [6, 0, 30, 30, 60, 80, 80, 40, 80, 0, 6, 0, 1, 3, 1, 4]
GHP/3/240/2180: [6, 5, 6, 4, 60, 10, 120, 1, 3, 60, 27, 38, 0, 60, 0, 40]
GHP/3/240/2196: [-15, 65, 0]
GHP/3/240/2100: [2, 5, 0, -1, 68, 68, 68, 80, 80, 80, -5, 12, 40, 96, 60, 85]
GHP/3/240/2116: [1, 55, 65, 30, 0, 72, 76, 0, 0, 4, 0, 5, 0, 5, 0, 24]
GHP/3/240/2132: [3, 3, -30, 0, 0, 0, 17, 10, -20, 15, 10, 50, 2, -5, 26, 0]
GHP/3/240/2148: [0, 0, 35, 60, 17, 53, 44, 40, 5, 0, 0, 0, 90, 70, 1, 3]
GHP/3/240/2164: [6, 0, 30, 30, 60, 80, 80, 40, 80, 0, 6, 0, 1, 3, 1, 4]
GHP/3/240/2180: [6, 5, 6, 4, 60, 10, 120, 1, 3, 60, 27, 38, 0, 60, 0, 40]
GHP/3/240/2196: [-15, 65, 0]
GHP/3/240/2100: [2, 5, 0, -1, 68, 68, 68, 80, 80, 80, -5, 12, 40, 96, 60, 85]
GHP/3/240/2116: [1, 55, 65, 30, 0, 72, 76, 0, 0, 4, 0, 5, 0, 5, 0, 24]
GHP/3/240/2132: [3, 3, -30, 0, 0, 0, 17, 10, -20, 15, 10, 50, 2, -5, 26, 0]
GHP/3/240/2148: [0, 0, 35, 60, 17, 53, 44, 40, 5, 0, 0, 0, 90, 70, 1, 3]
GHP/3/240/2164: [6, 0, 30, 30, 60, 80, 80, 40, 80, 0, 6, 0, 1, 3, 1, 4]
GHP/3/240/2180: [6, 5, 6, 4, 60, 10, 120, 1, 3, 60, 27, 38, 0, 60, 0, 40]
GHP/3/240/2196: [-15, 65, 0]
GHP/3/240/2100: [2, 5, 0, -1, 68, 68, 68, 80, 80, 80, -5, 12, 40, 96, 60, 85]
GHP/3/240/2116: [1, 55, 65, 30, 0, 72, 76, 0, 0, 4, 0, 5, 0, 5, 0, 24]
GHP/3/240/2132: [3, 3, -30, 0, 0, 0, 17, 10, -20, 15, 10, 50, 2, -5, 26, 0]
GHP/3/240/2148: [0, 0, 35, 60, 17, 53, 44, 40, 5, 0, 0, 0, 90, 70, 1, 3]
GHP/3/240/2164: [6, 0, 30, 30, 60, 80, 80, 40, 80, 0, 6, 0, 1, 3, 1, 4]
GHP/3/240/2180: [6, 5, 6, 4, 60, 10, 120, 1, 3, 60, 27, 38, 0, 60, 0, 40]
GHP/3/240/2196: [-15, 65, 0]
GHP/3/240/2100: [2, 5, 0, -1, 68, 68, 68, 80, 80, 80, -5, 12, 40, 96, 60, 85]
GHP/3/240/2116: [1, 55, 65, 30, 0, 72, 76, 0, 0, 4, 0, 5, 0, 5, 0, 24]
GHP/3/240/2132: [3, 3, -30, 0, 0, 0, 17, 10, -20, 15, 10, 50, 2, -5, 26, 0]
GHP/3/240/2148: [0, 0, 35, 60, 17, 53, 44, 40, 5, 0, 0, 0, 90, 70, 1, 3]
GHP/3/240/2164: [6, 0, 30, 30, 60, 80, 80, 40, 80, 0, 6, 0, 1, 3, 1, 4]
GHP/3/240/2180: [6, 5, 6, 4, 60, 10, 120, 1, 3, 60, 27, 38, 0, 60, 0, 40]
GHP/3/240/2196: [-15, 65, 0]
GHP/3/240/2100: [2, 5, 0, -1, 68, 68, 68, 80, 80, 80, -5, 12, 40, 96, 60, 85]
GHP/3/240/2116: [1, 55, 65, 30, 0, 72, 76, 0, 0, 4, 0, 5, 0, 5, 0, 24]
GHP/3/240/2132: [3, 3, -30, 0, 0, 0, 17, 10, -20, 15, 10, 50, 2, -5, 26, 0]
GHP/3/240/2148: [0, 0, 35, 60, 17, 53, 44, 40, 5, 0, 0, 0, 90, 70, 1, 3]
GHP/3/240/2164: [6, 0, 30, 30, 60, 80, 80, 40, 80, 0, 6, 0, 1, 3, 1, 4]
GHP/3/240/2180: [6, 5, 6, 4, 60, 10, 120, 1, 3, 60, 27, 38, 0, 60, 0, 40]
GHP/3/240/2196: [-15, 65, 0]
GHP/3/240/2000: [8, 1, 16, 20, 26, 43, 27]
GHP/10/240/400: [0, 0, 0, 0, 17665]
GHP/3/240/2000: [8, 1, 16, 20, 26, 43, 27]
GHP/10/240/400: [0, 0, 0, 0, 17665]
GHP/10/240/316: [23, 0, 0, 0, 65, 0, 25, 2, 0, 0, 0, 0, 44, 21, 2, 0]
GHP/3/240/2000: [8, 1, 16, 20, 26, 43, 27]
GHP/10/240/400: [0, 0, 0, 0, 17665]
GHP/10/240/300: [0, 96, 12, 21, 20, 20, 14, 17, 0, 0, 0, 0, 0, 0, 0, 0]
GHP/3/240/2000: [8, 1, 16, 20, 26, 43, 27]
GHP/10/240/400: [0, 0, 0, 0, 17665]
GHP/3/240/2000: [8, 1, 16, 20, 26, 43, 27]
```


unit boot:

```
říj 02 11:53:17 nilan grundig2mqtt.py[14735]: WARNING:__main__:No data received.
říj 02 11:53:17 nilan grundig2mqtt.py[14735]: WARNING:__main__:No data received.
říj 02 11:53:18 nilan grundig2mqtt.py[14735]: WARNING:__main__:No data received.
říj 02 11:53:18 nilan grundig2mqtt.py[14735]: WARNING:__main__:No data received.
říj 02 11:53:18 nilan grundig2mqtt.py[14735]: WARNING:__main__:No data received.
říj 02 11:53:19 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/0: [256, 99, 40]
říj 02 11:53:19 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/500: [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
říj 02 11:53:20 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/516: [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1]
říj 02 11:53:20 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/532: [0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0]
říj 02 11:53:20 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/548: [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1]
říj 02 11:53:20 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/564: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
říj 02 11:53:21 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/580: [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
říj 02 11:53:21 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/596: [1, 1, 0]
říj 02 11:53:21 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/600: [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
říj 02 11:53:21 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/616: [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0]
říj 02 11:53:21 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/632: [1, 0, 0, 0, 0, 0, 0, 0]
říj 02 11:53:22 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/100: [5, 15, 15, 10, 120, 120, 120, 96, 96, 96, 0, 15, 90, 96, 120, 120]
říj 02 11:53:22 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/116: [1, 120, 75, 120, 2, 120, 120, 120, 120, 40, 1, 20, 0, 10, 1, 30]
říj 02 11:53:22 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/132: [4, 3, -21, 1, 1, 1, 96, 40, 20, 25, 20, 60, 2, 0, 100, 1]
říj 02 11:53:22 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/148: [15, 1, 100, 67, 34, 67, 67, 60, 20, 67, 67, 67, 100, 100, 1, 10]
říj 02 11:53:23 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/164: [25, 96, 96, 96, 100, 96, 96, 100, 96, 96, 100, 15, 1, 3, 1, 15]
říj 02 11:53:23 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/196: [0, 80, 120]
říj 02 11:53:24 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/200: [1, 2, -10, -5, 20, 20, 20, 0, 0, 0, -15, 0, 20, 0, 30, 30]
říj 02 11:53:24 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/232: [0, 0, -40, 0, 0, 0, 0, 0, -20, 10, 1, 30, 1, -15, 20, 0]
říj 02 11:53:24 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/248: [-10, 0, 10, 14, 14, 34, 34, 20, -10, 0, 0, 0, 50, 50, 0, 0]
říj 02 11:53:24 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/264: [-5, 0, 0, 0, 20, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0]
říj 02 11:53:25 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/280: [0, 0, 0, 0, 30, 1, 0, 0, 1, 40, 20, 20, 0, 0, 0, 10]
říj 02 11:53:25 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/296: [-30, 50, 0]
říj 02 11:53:25 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/2100: [2, 2, 0, -1, 68, 68, 68, 80, 80, 80, -5, 12, 40, 96, 60, 85]
říj 02 11:53:26 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/2116: [1, 55, 65, 30, 0, 72, 76, 0, 0, 4, 0, 5, 0, 5, 0, 24]
říj 02 11:53:26 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/2132: [3, 0, -30, 0, 0, 0, 17, 10, -20, 15, 10, 50, 2, -5, 26, 0]
říj 02 11:53:26 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/2148: [0, 0, 35, 60, 17, 53, 44, 40, 5, 0, 0, 0, 90, 50, 0, 3]
říj 02 11:53:26 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/2164: [6, 0, 30, 30, 60, 80, 80, 40, 80, 0, 6, 0, 1, 3, 1, 4]
říj 02 11:53:27 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/2180: [6, 5, 6, 4, 60, 10, 120, 1, 1, 60, 27, 38, 0, 60, 0, 40]
říj 02 11:53:27 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/2196: [-15, 65, 0]
říj 02 11:53:27 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/2000: [2, 0, 0, 21, 25, 43, 27]
říj 02 11:53:28 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/400: [0, 0, 0, 0, 0]
říj 02 11:53:28 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/300: [0, 17, 10, 22, 16, 14, 11, 11, 0, 0, 0, 0, 0, 0, 0, 0]
říj 02 11:53:28 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/316: [23, 0, 0, 0, 65, 0, 25, -1, 0, 0, 0, 0, 48, 22, 0, 0]
říj 02 11:53:29 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/332: [11, 0, 0, 0, 5, 0, 0, 2]
říj 02 11:53:29 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/1000: [0, 22, 48, 22, 0]
říj 02 11:53:30 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/3/240/2000: [2, 0, 0, 21, 25, 43, 27]
říj 02 11:53:31 nilan grundig2mqtt.py[14735]: WARNING:__main__:No data received.
říj 02 11:53:32 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/400: [0, 0, 0, 0, 0]
říj 02 11:53:33 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/300: [0, 13, 10, 22, 16, 14, 11, 11, 0, 0, 0, 0, 0, 0, 0, 0]
říj 02 11:53:33 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/316: [23, 0, 0, 0, 65, 0, 25, -1, 0, 0, 0, 0, 48, 22, 0, 0]
říj 02 11:53:33 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/332: [11, 0, 0, 0, 5, 0, 0, 2]
říj 02 11:53:33 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/1000: [0, 22, 48, 22, 0]
říj 02 11:53:34 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/3/240/2000: [2, 0, 0, 21, 25, 43, 27]
říj 02 11:53:26 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/2148: [0, 0, 35, 60, 17, 53, 44, 40, 5, 0, 0, 0, 90, 50, 0, 3]
říj 02 11:53:26 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/2164: [6, 0, 30, 30, 60, 80, 80, 40, 80, 0, 6, 0, 1, 3, 1, 4]
říj 02 11:53:27 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/2180: [6, 5, 6, 4, 60, 10, 120, 1, 1, 60, 27, 38, 0, 60, 0, 40]
říj 02 11:53:27 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/2196: [-15, 65, 0]
říj 02 11:53:27 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/2000: [2, 0, 0, 21, 25, 43, 27]
říj 02 11:53:28 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/400: [0, 0, 0, 0, 0]
říj 02 11:53:28 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/300: [0, 17, 10, 22, 16, 14, 11, 11, 0, 0, 0, 0, 0, 0, 0, 0]
říj 02 11:53:28 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/316: [23, 0, 0, 0, 65, 0, 25, -1, 0, 0, 0, 0, 48, 22, 0, 0]
říj 02 11:53:29 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/332: [11, 0, 0, 0, 5, 0, 0, 2]
říj 02 11:53:29 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/1000: [0, 22, 48, 22, 0]
říj 02 11:53:30 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/3/240/2000: [2, 0, 0, 21, 25, 43, 27]
říj 02 11:53:31 nilan grundig2mqtt.py[14735]: WARNING:__main__:No data received.
říj 02 11:53:32 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/400: [0, 0, 0, 0, 0]
říj 02 11:53:33 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/300: [0, 13, 10, 22, 16, 14, 11, 11, 0, 0, 0, 0, 0, 0, 0, 0]
říj 02 11:53:33 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/316: [23, 0, 0, 0, 65, 0, 25, -1, 0, 0, 0, 0, 48, 22, 0, 0]
říj 02 11:53:33 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/332: [11, 0, 0, 0, 5, 0, 0, 2]
říj 02 11:53:33 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/1000: [0, 22, 48, 22, 0]
říj 02 11:53:34 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/3/240/2000: [2, 0, 0, 21, 25, 43, 27]
říj 02 11:53:36 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/400: [0, 0, 0, 0, 0]
říj 02 11:53:36 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/300: [0, 24, 10, 22, 16, 14, 11, 11, 0, 0, 0, 0, 0, 0, 0, 0]
říj 02 11:53:36 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/316: [23, 0, 0, 0, 65, 0, 25, 0, 0, 0, 0, 0, 48, 22, 0, 0]
říj 02 11:53:37 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/332: [11, 0, 0, 0, 5, 0, 0, 2]
říj 02 11:53:37 nilan grundig2mqtt.py[14735]: INFO:__main__:GHP/10/240/1000: [0, 22, 48, 22, 0]
```
