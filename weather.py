from bmp180 import BMP180
import network
import time
import ujson
import utime
import urequests
from machine import Pin ,I2C,RTC
i2c= I2C(scl=Pin(5),sda=Pin(4))
from ssd1306 import SSD1306_I2C
oled = SSD1306_I2C(64,48,i2c)

oled.fill(0)

net=network.WLAN(network.STA_IF)# create station interface
net.active(True)
if not net.isconnected():
	net.active(True)
	net.connect("chiaki","123456789") 
while not net.isconnected():
	print("wrong connecting")
	pass
print("network config:", net.ifconfig())# get the interface's IP/netmask/gw/DNS addresses

'''开机小动画'''
 
oled.rect(6,6,52,36,2)#+右，+下，宽，长，像素
oled.rect(10,10,44,28,2)#电视框

oled.line(31,6,8,0,4)
oled.line(31,6,56,0,4)#天线

oled.line(15,18,25,18,4)
oled.line(38,18,48,18,4)#眼睛

oled.line(26,25,29,32,4)
oled.line(32,25,29,32,4)
oled.line(32,25,35,32,4)
oled.line(35,32,38,25,4)#嘴巴

oled.show()
utime.sleep(5)#5s
oled.fill(0)


url='https://api.seniverse.com/v3/weather/daily.json?key=SGn6boc1Jsz1OSXFG&location=yaan&language=en&unit=c&start=0&days=5'
result=urequests.get(url)
if not net.isconnected():
	machine.reset()
j=ujson.loads(result.text)

date=j['results'][0]['daily'][0]['date']
list_d = str.split(date,"-")
oled.text('Today',2,5)
oled.text(list_d[0],2,15)
oled.text(list_d[1],2,25)
oled.text(list_d[2],2,35)
oled.show()
utime.sleep(5)
oled.fill(0)

city=j['results'][0]['location']['name']
oled.text("CITY:",2,5) 
oled.text(city,2,15) 

Htemperature=j['results'][0]['daily'][0]['high']
oled.text('HTEMP:',2,25)
oled.text(Htemperature,2,35)

oled.show()
utime.sleep(5)
oled.fill(0)

Ltemperature=j['results'][0]['daily'][0]['low']
oled.text('LTEMP:',2,0)
oled.text(Ltemperature,2,10)
weather=j['results'][0]['daily'][0]['text_day']
list_w = str.split(weather," ")
oled.text('WEATHER:' ,2,18)
oled.text(list_w[0],2,27)
if ' 'in weather :
	oled.text(list_w[1],2,35)
oled.show()
utime.sleep(5)
oled.fill(0)

result.close()
'''压敏传感器获取气温、气压、海拔'''
bmp180 = BMP180(i2c)
bmp180.oversample_sett = 2
bmp180.baseline = 101325
while(1):
	t = bmp180.temperature
	p = bmp180.pressure
	altitude = bmp180.altitude
	oled.text('T:' + str(int(t)), 1, 1) #实时气温
	oled.text('P:' + str(int(p)), 1, 10) #压强
	oled.text('A:' + str(int(altitude)), 1, 20) #海拔
	oled.show()
	utime.sleep(1)
	oled.fill(0)


		