from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, DoubleType
from pyspark.sql.functions import to_timestamp, concat, lit
from pyspark.sql import  DataFrame

#TO-DO ALL: comentar todos os métodos:

def read_mt5_csv(ind_curr:str, timeframe:str, spark:SparkSession) -> DataFrame:

  file_path = "/csvs/work/" + ind_curr + "_" + timeframe + ".csv"

  dfHourlySchema = StructType([\
      StructField('cuote_date',StringType(),True),\
      StructField('cuote_time',StringType(),True),\
      StructField('cuote_open',DoubleType(),True),\
      StructField('cuote_high',DoubleType(),True),\
      StructField('cuote_low',DoubleType(),True),\
      StructField('cuote_close',DoubleType(),True),\
      StructField('tick_volume',DoubleType(),True),\
      StructField('volume',DoubleType(),True),\
      StructField('spread',IntegerType(),True) \
    ])

  
  dfDailySchema = StructType([\
      StructField('cuote_date',StringType(),True),\
      StructField('cuote_open',DoubleType(),True),\
      StructField('cuote_high',DoubleType(),True),\
      StructField('cuote_low',DoubleType(),True),\
      StructField('cuote_close',DoubleType(),True),\
      StructField('tick_volume',DoubleType(),True),\
      StructField('volume',DoubleType(),True),\
      StructField('spread',IntegerType(),True) \
    ])

  if timeframe == "1d" or timeframe == "1w":
    dfSchema = dfDailySchema
  else:
    dfSchema = dfHourlySchema

  dfAux = spark.read.options(header='False', delimiter='\t') \
    .schema(dfSchema) \
    .csv(file_path)

  if timeframe == "1d" or timeframe == "1w":
    dfAux0 = dfAux.withColumn('cuote_time', lit("00:00:00"))
  else:
    dfAux0 = dfAux


  dfAux1 = dfAux0.withColumn('cuote_timestamp', to_timestamp(concat(dfAux0['cuote_date'], dfAux0['cuote_time']),'yyyy.MM.ddHH:mm:ss')) \
                .withColumn('index', lit(ind_curr)) 

  return dfAux1
