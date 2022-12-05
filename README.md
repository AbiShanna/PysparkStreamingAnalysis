# PysparkStreamingAnalysis
<br />
## Problem statement:<br />
Create a Pyspark Streaming application that will continuously read data from Twitter, analyze them for their sentiment (sentiment classification - positive, neutral, negative), and send the sentiment values to Apache Kafka topic. Read the sentiment data from kafka topic using ElasticsearchLogstashKibana and visualize.
<br /><br />
## Architecture:<br />

<br/><img src="flowchart.png" alt="flowchart" /><br/>
   <br /><br />
## Steps to implement: <br />

1.	Start the zookeeper server: 
.\zookeeper-server-start.bat ..\..\config\zookeeper.properties inside kafka\bin\windows

2. Start the Kafka server: 
.\kafka-server-start.bat ..\..\config\server.properties inside kafka\bin\windows

3. Create kafka topic: (inside kafka\bin\windows)
.\kafka-topics.bat --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic twittersenti 

4. Configure Logstash (logstash.conf) to read from kafka topic i.e. source and write to elasticsearch index. <br/>

	*input {*<br/>
	 *kafka {* <br/>
	    *bootstrap_servers => "localhost:9092"*
	    <br/>
	    *topics => "sentiments"*
	    <br/>
	    *}* 
	    <br />
	*}* <br/>

	*output {* <br />
	  *elasticsearch {* <br />
	    *hosts => ["http://localhost:9200"]* <br/>
		*index => "sentiments"* <br/>
	  *}*<br/>
	*}<br/>*

5. Start elastic search by running the command elasticsearch inside the bin directory of elasticsearch <br/>

6. Start logstash by running the following command inside logstash folder
<br/>bin\logstash.bat -f config\logstash.conf<br/>

7. Start Kibana by running the command .\kibana.bat inside the bin directory of kibana <br/>

8. To check if elastic search is working fine, type the following command and you should see the attached output <br/>
<br/><br/> &nbsp;&nbsp;  http://localhost:9200/_cat/indices/twittersenti <br/>
This should display the health status as yellow denoting that index is set.<br/>

9. Run the read_tweets.py followed by write_tweets.ipynb <br/>
	○	#covid tweets are filtered <br/>
	○	Once the last cell of the write_tweets.ipynb is run, tweets gets classified based on sentiments and kibana displays real-time insights <br/>

10. Enter http://localhost:5601/
	○	Create index pattern: Stack Management => Data Views => Create Data Views<br/>
	○	In the ‘Discover’ section, choose the kafka topic twittersenti<br/>
	○	Real-time statistics on tweets will then be displayed<br/>
	○	To generate graphs, create them in the dashboard with required fields.<br/>

	<br/><img src="1.png" alt="1" /><br/>
	<br/><img src="2.png" alt="2" /><br/>
	<br/><img src="3.png" alt="3" /><br/>


