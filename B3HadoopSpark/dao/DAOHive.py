from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, years, months
from pyspark.sql import  DataFrame

#TO-DO ALL: comentar todos os métodos:

def de_para_b3_database(timeframe) -> str:
  # De-Para dos timeframes do numeros do MEtatrader para o nome das colections criadas no mongo:
  # M30...(30 minutos):
  if timeframe == "30m":
      return "b3_m30"
  # H1...(60 minutos):
  elif timeframe == "1h":
      return "b3_h1"
  # H4...(4 horas):
  elif timeframe == "4h":
      return "b3_h4"
  # d1...(1 dia):
  elif timeframe == "1d":
      return "b3_d1"
  # w1...(1 semana):
  elif timeframe == "1w":
      return "b3_w1"
  return ""

def read_market_from_hive(index:str, timeframe:str, spark:SparkSession) -> DataFrame:

    hive_table = de_para_b3_database(timeframe)

    dfHiveAux = read_data_from_hive ("markets", hive_table, spark)

    dfHiveAux0 = dfHiveAux.filter(dfHiveAux["index"] == lit(index))

    return dfHiveAux0


def read_data_from_hive (hive_database:str, hive_table:str, spark:SparkSession) -> DataFrame:

    dfHiveAux = spark.read.table(hive_database + "."+ hive_table)

    return dfHiveAux


def load_b3_to_hive(ind_curr, timeframe, spark, dfAux1, cargaZero):

  hive_table = de_para_b3_database(timeframe)

  load_markets_to_hive(ind_curr, hive_table, spark, dfAux1, cargaZero)

  
def load_markets_to_hive(ind_curr, hive_table, spark, dfDadosOrigem, cargaZero):

  if not cargaZero:

    dfHiveAux = read_data_from_hive ("markets", hive_table, spark)

    dfHiveAux0 = dfHiveAux.filter(dfHiveAux["index"] == lit(ind_curr))

    dfHiveAux1 = spark.sparkContext.parallelize(dfHiveAux0.orderBy(dfHiveAux0["cuote_timestamp"].desc()).collect(),3).collect()

    close_row = dfHiveAux1[0]['cuote_timestamp']

    #close_row = dfHiveAux0.groupBy().max("cuote_timestamp").collect()[0][0]
    print("close_row: " + str(close_row))

    dfAux2 = dfDadosOrigem.filter(dfDadosOrigem["cuote_timestamp"] > close_row)

    append_data_to_hive("markets",hive_table,dfAux2)

    #dfAux3 = dfHiveAux0.drop("_id").union(dfAux2)

    #return dfAux3
  else:

    spark.sql("alter table markets." + hive_table + " drop IF EXISTS partition (index = \"" + ind_curr + "\")")

    append_data_to_hive("markets",hive_table,dfDadosOrigem)

    #return dfAux1


def append_data_to_hive (hive_database:str, hive_table:str, dfDadosOrigem:DataFrame):

    dfDadosOrigem.write.partitionBy("index",years("cuote_timestamp"),months("cuote_timestamp")).format("hive").mode("append").saveAsTable(hive_database + "."+ hive_table)

