
# LIBRARY IMPORTS
import findspark
findspark.init()
import nltk
#nltk.download('wordnet')
import re
from nltk.corpus import stopwords
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
stop_words = set(stopwords.words('english'))
from pyspark.ml import Pipeline
from pyspark.sql import Row, Column, SparkSession
from textblob import TextBlob
import pyspark.sql.types as tp
sc = SparkContext(appName = "Text Cleaning")
strc = StreamingContext(sc, 3)
spark = SparkSession.builder.master("local[1]").appName("read tweet").getOrCreate()

# LOAD DATA FROM TCP SOCKET
text_data = strc.socketTextStream('127.0.0.1', 5555)

# PRE-PROCESS DATA
def get_prediction(sentence): 
    sentence = sentence.lower()
    sentence = re.sub("\s+"," ", sentence)
    sentence = re.sub("\W"," ", sentence)
    sentence = re.sub(r"http\S+", "", sentence)
    sentence = ' '.join(word.lower() for word in sentence.split() if word not in stop_words and len(word) > 3)
    sentence = re.sub(r'\b\w{1,3}\b', '', sentence)
    res = TextBlob(sentence)
    senti = res.sentiment.polarity
    if senti > 0:
        senti = 'positive'
    elif senti < 0:
        senti = 'negative'
    elif senti == 0:
        senti = 'neutral'
    return str(senti)


# WRITE SENTIMENTS TO KAFKA TOPIC
def convt(rdd):
    
    if rdd.isEmpty():
        my_sch = tp.StructType([tp.StructField('value', tp.StringType(), True)])
        rdd = sc.emptyRDD()
        
        df = spark.createDataFrame(rdd, my_sch)  
    else:
        schema = tp.StructType([tp.StructField('value', tp.StringType(), True)])
        rdd = sc.parallelize(rdd.collect())
        rdd = rdd.map(lambda x:[x]) # transform the rdd
 
        df = spark.createDataFrame(rdd, schema)

    
    df.printSchema()
    
    df.write.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").option("topic", "sentiments").save()
	
	
r = text_data.map(lambda x: get_prediction(x))
r.foreachRDD(convt)

r.pprint()

strc.start()
strc.awaitTermination()
