import gc
gc.collect()

import utime
import app.hardwear as hardwear
import app.conection as conection
import machine

conection.connectToWiFi()
conection.connectToMQTT()
    
timeLastReconect = utime.ticks_ms()
timeLastReboot = utime.ticks_ms()
timeLastPubHealthCheck = utime.ticks_ms()



from machine import WDT
wdt = WDT(timeout=3000)
wdt.feed()

while True:
  
    wdt.feed()
    conection.client.check_msg()
    if utime.ticks_ms() - timeLastReconect > 300000:
        conection.connectToMQTT()
        timeLastReconect = utime.ticks_ms()
    if utime.ticks_ms() - timeLastPubHealthCheck > 60000:
    	conection.health_check_pub(gc.mem_free())
    	timeLastPubHealthCheck = utime.ticks_ms()
    
      
  
