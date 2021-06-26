def connectToWifiAndUpdate():
    import time, machine, network, gc, app.secrets as secrets
    time.sleep(1)
    print('Memory free', gc.mem_free())

    from app.ota_updater import OTAUpdater
	
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    otaUpdater = OTAUpdater('https://github.com/koladanilkov/stl-006_A', main_dir='app', secrets_file="secrets.py")
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        machine.reset()
    else:
        del(otaUpdater)
        gc.collect()

def startApp():
    import app.start


try:
    f = open("mydb", "r+b")
    db = btree.open(f)
except OSError:
    f = open("mydb", "w+b")
    db = btree.open(f)
    db[b"wr"] = b"0"
    db.flush()


if (db[b"wr"] == b"1"):
    import webrepl
    webrepl.start()
else:
    startApp()
