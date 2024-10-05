from datetime import timezone, datetime, timedelta
from shutil import copyfile
from types import NoneType

import MetaTrader5 as mt5

import time

import numpy
 

account=3007777777
password="XXXXXXXXX"
server="Rico-DEMO"

# conecte-se ao MetaTrader 5z
if not mt5.initialize(path="C:/Program Files/MetaTrader 5 - Copia/terminal64.exe",login=account, password=password, server=server):
    print("initialize() failed. error code:",mt5.last_error())
    mt5.shutdown()
else:
    print("mt5 initialized")

# consultamos o estado e os parâmetros de conexão
print(mt5.terminal_info())
# obtemos informações sobre a versão do MetaTrader 5
print(mt5.version())
 
# importing the requests module
import requests
import json

url = "http://192.168.15.119:8090/b3assets"

req = requests.get(url)
#print(req.content)
assets = json.loads(req.content)
print(len(assets))
iCount = 0
#for asset in assets:
#    iCount = iCount+1
#    print(str(iCount) + " - " + asset["symbol"])


id_timeframes = [mt5.TIMEFRAME_M30,mt5.TIMEFRAME_H1, mt5.TIMEFRAME_H4, mt5.TIMEFRAME_D1, mt5.TIMEFRAME_W1]
bForceWeek =  False # True #- p/  carga zero
qtde_dias = 1 # 1000  #- p/ carga zero
qtde_semanas = 1 # 200   #- p/ carga zero
qtde_bars = [qtde_dias*48,qtde_dias*24, qtde_dias*6, qtde_dias*1, qtde_semanas*1]

sufix_filename = ["30m","1h","4h","1d","1w"]
strfmt = "{0:.5f}"
separator = '\t'
qtdeLines = len(id_timeframes)
dtAgora = datetime.now()

for asset in assets:
    for iCount in range(qtdeLines):
        filename = asset["symbol"] + "_" + sufix_filename[iCount]+".csv"
        if(iCount == 4 and dtAgora.weekday() != 0) and not bForceWeek:
            print(dtAgora.strftime("%Y.%m.%d\t%H:%M:%S") + " - Obs: por não ser domingo[" + str(dtAgora.weekday()) +"], pulando o arquivo:" + filename)
        else:
            print(dtAgora.strftime("%Y.%m.%d\t%H:%M:%S") + " - appendando no arquivo:" + filename)
            rates = None
            iAttemptCount = 0
            while type(rates) is NoneType and iAttemptCount < 7 :
                iAttemptCount = iAttemptCount +1
                rates = mt5.copy_rates_from(asset["symbol"], id_timeframes[iCount], datetime(dtAgora.year,dtAgora.month,dtAgora.day,20,30), qtde_bars[iCount])
                #rates = mt5.copy_rates_from(moeda, id_timeframes[iCount], datetime(2023,2,6,13), qtde_bars[iCount])
                if type(rates) is NoneType:
                    print ("tentativa " + str(iAttemptCount) + " de mt5.copy_rates_from falhou: cod:" + str(mt5.last_error()) + " " +  datetime.now().strftime("%Y.%m.%d\t%H:%M:%S") + " waiting... ")
                    time.sleep(iAttemptCount)

            cotacoes = []
            if type(rates) is numpy.ndarray:
                for val in rates:
                    dtCotacao = datetime.fromtimestamp(val[0],tz=timezone(timedelta(hours=0)))
                    data = dtCotacao.strftime("%Y.%m.%d")
                    data_hora = dtCotacao.strftime("%Y.%m.%d\t%H:%M:%S")
                    dOpen = val[1]
                    dHigh = val[2]
                    dLow = val[3]
                    dClose = val[4]
                    dVolumeTick = val[5]
                    dVolume = val[6]
                    dSpread = val[7]
                    if iCount > 2: # timeframes diario e semanal nao possuem hora....
                        linha = data + separator + strfmt.format(dOpen) + separator + strfmt.format(dHigh) + separator + strfmt.format(dLow) + separator + strfmt.format(dClose) + separator + str(dVolumeTick) + separator + str(dVolume) + separator + str(dSpread)
                    else:
                        linha = data_hora + separator + strfmt.format(dOpen) + separator + strfmt.format(dHigh) + separator + strfmt.format(dLow) + separator + strfmt.format(dClose) + separator + str(dVolumeTick) + separator + str(dVolume) + separator + str(dSpread)
                
                    cotacoes.append(linha)

            f = open("./work/" +filename,'a')
            f.writelines("%s\n" % t for t in cotacoes)
            f.close()
    # copiando arquivos para diretório distribuido
    for iCount in range(qtdeLines):
        filename = asset["symbol"]  + "_" + sufix_filename[iCount]+".csv"
        print(datetime.now().strftime("%Y.%m.%d\t%H:%M:%S") + " - copiando para pasta distribuida o arquivo:" + filename)
        copyfile("./work/" + filename,"Z:\\work\\" + filename)

# concluímos a conexão ao MetaTrader 5
mt5.shutdown()
