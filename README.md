# PysparkStreamingAnalysis
Problem statement:<br />
Create a Pyspark Streaming application that will continuously read data from Twitter, analyze them for their sentiment (sentiment classification - positive, neutral, negative), and send the sentiment values to Apache Kafka topic. Read the sentiment data from kafka topic using ElasticsearchLogstashKibana and visualize.
    
   **Twitter -> Spark -> sentiments -> kafka -> ELK** <br />
Steps to implement: <br />
1. Create a PySpark application that continuously reads tweets from Twitter relating to a search term e.g. #covid.
2. Create a topic for data exchange. The Spark Structured Streaming application should send sentiment data to Kafka.
3. Analyze the gathered tweets for their individual sentiment continuously. At the end of every window, a message containing the sentiment
should be sent to Kafka topic created above.
4. Configure Logstash, Elasticsearch, and Kibana to read from the Kafka topic and set up visualization of sentiment.
