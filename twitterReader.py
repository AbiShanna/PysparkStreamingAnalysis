import tweepy
from tweepy import Stream
#from tweepy.streaming import Stream
from tweepy import OAuthHandler
import socket
import json

consumer_key='*********************'
consumer_secret='****************************'
access_token ='*****************************************'
access_secret='******************************'

class TweetsListener(Stream):
  def __init__(self, *args, csocket):
    super().__init__(*args)
    self.client_socket = csocket
  def on_data(self, data):
    try:  
      msg = json.loads( data )
      if "extended_tweet" in msg:
        
        self.client_socket\
            .send(str(msg['extended_tweet']['full_text']+"t_end")\
            .encode('utf-8'))         
        print(msg['extended_tweet']['full_text'])
      else:
        self.client_socket\
            .send(str(msg['text']+"t_end")\
            .encode('utf-8'))
        print(msg['text'])
      return True
    except BaseException as e:
        print("Error on_data: %s" % str(e))
    return True
  def on_error(self, status):
    print(status)
    return True

def sendData(c_socket):
  twitter_stream = TweetsListener(consumer_key, consumer_secret, access_token, access_secret, csocket= c_socket)
  twitter_stream.filter(track = 'russia', languages=["en"])

if __name__ == "__main__":
    
    s = socket.socket()
    host = "127.0.0.1"    
    port = 5555
    s.bind((host, port))
    s.listen(4)    
    c_socket, addr = s.accept()
   
    sendData(c_socket)
