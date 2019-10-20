from gpiozero import Buzzer
from time import sleep
import pika
url = 'amqp://fyudxazs:HjIOZIVvw-RKjY5einv0GssN4m3VlkmA@salamander.rmq.cloudamqp.com/fyudxazs'
params = pika.URLParameters(url)
params.socket_timeout = 5

buzzer = Buzzer(4)

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
queue_name = 'blinky'
channel.queue_declare(queue=queue_name) # Declare a queue

#create a function to process the message
def process_message(body):
    print("processing msg")
    print("msg:",body)
    # play a song
    global buzzer
    buzzer.on()
    sleep(1)
    buzzer.off()
    sleep(1)



# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  process_message(body)

# set up subscription on the queue
channel.basic_consume(queue_name,
  callback,
  auto_ack=True)

# start consuming (blocks)
channel.start_consuming()
connection.close()

