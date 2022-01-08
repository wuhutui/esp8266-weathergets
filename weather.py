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
oled.show()

net=network.WLAN(network.STA_IF)# create station interface
net.active(True)
if not net.isconnected():
	net.active(True)
	net.connect("chiaki","123456789") 
while not net.isconnected():
	pass
print("network config:", net.ifconfig())# get the interface's IP/netmask/gw/DNS addresses

url='https://api.seniverse.com/v3/weather/daily.json?key=SGn6boc1Jsz1OSXFG&location=yaan&language=zh-Hans&unit=c&start=0&days=5'


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


oled.pixel(0,0,3)
oled.show()

oled.pixel(63,0,3)
oled.show()

oled.pixel(0,47,3)
oled.show()

oled.pixel(63,47,3)
oled.show()


result=urequests.get(url)
if not net.isconnected():
	machine.reset()
j=ujson.loads(result.text)
'''city=j['results'][0]['location']['path']
oled.text("today"+city+"weather",0,0)'''

temperature=j['results'][0]['daily'][0]['code_day']
oled.text('TEMP is',2,5)
oled.text(temperature,2,15)

oled.show()


'''weather=j['results'][0]['daily'][0]['text_day']
oled.text('weather is'+weather,0,20)'''

oled.fill(1)

result.close()

		