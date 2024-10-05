import time
from types import NoneType
import MetaTrader5 as mt5
from datetime import datetime
import numpy
#mport numpy as np


account=3088888888
password="YYYYYYYYY"
server="Rico-DEMO"

# conecte-se ao MetaTrader 5z
if not mt5.initialize(path="C:/Program Files/MetaTrader 5 - Copia/terminal64.exe",login=account, password=password, server=server):
    print("initialize() failed. error code:",mt5.last_error())
    mt5.shutdown()
else:
    print("mt5 initialized")

print(mt5.account_info())

#authorized = mt5.login(account,password,server,60)

#if authorized:
#    print("mt5 authorized")
#else:
#    print("mt5 not authorized")

#print(mt5.account_info())
# get symbols whose names do not contain USD, EUR, JPY and GBP
group_symbols=mt5.symbols_get()#group="*") #"*,!*USD*,!*EUR*,!*JPY*,!*GBP*")
#print('len(*,!*USD*,!*EUR*,!*JPY*,!*GBP*):', len(group_symbols))

print("mt5 initialized")
iCount = 1
# importing the requests module
import requests

#url = "http://192.168.15.21:8090/b3assets"
urlprefix = "http://192.168.15.119:8090/registerb3asset"


for s in group_symbols:
    #print(s.path[0:15])
    if(s.path[0:15] == "BOVESPA\A VISTA" and s.volume > 0): # and s.name[0:4] == "PETR"):#and iCount < 3):
        rates = None
        iAttemptCount = 0
        while type(rates) is NoneType and iAttemptCount < 7 :
            iAttemptCount = iAttemptCount +1
            dtAgora = datetime.now()
            # print(s)
            rates = mt5.copy_rates_from(s.name, mt5.TIMEFRAME_D1, datetime(dtAgora.year,dtAgora.month,dtAgora.day,dtAgora.hour,dtAgora.minute), 1)
            #print(str(type(rates)))
            if type(rates) is NoneType:
                print ("tentativa " + str(iAttemptCount) + " de mt5.copy_rates_from falhou: cod:" + str(mt5.last_error()) + " " +  datetime.now().strftime("%Y.%m.%d\t%H:%M:%S") + " waiting... ")
                time.sleep(iAttemptCount)

        if type(rates) is numpy.ndarray:
            #print(str(len(rates)))
            for val in rates:
                dVolume = val[7]
                dVolumeTick = val[5]
                if(dVolumeTick > 1000 and dVolume > 5000000):
                    print(str(iCount), " - " , s.name)
                    url = urlprefix + "?symbol=" + s.name + "&description=" + s.description + "&volume="  + str(dVolume) + "&tickVolume=" + str(dVolumeTick) + "&status=open"
                    print(url)

                    # Uploadin the asset info by sending the request to the URL
                    req = requests.get(url)
                    #print(str(iCount))
                    iCount = iCount+1

# concluímos a conexão ao MetaTrader 5
mt5.shutdown()
        
