import pika
import os

class mqConsumer(mqConsumerInterface):

    setupRMQConnection()
    pass

class mqConsumerInterface:

    def __init__(self, binding_key , exchange_name , queue_name ):
        # Save parameters to class variables
        self.name = exchange_name
        self.key = binding_key
        self.queue = queue_name

        # Call setupRMQConnection
        self.setupRMQConnection()

        pass

    def setupRMQConnection(self):
        
        # Set-up Connection to RabbitMQ service
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=con_params)

        # Establish Channel
        self.channel = self.connection.channel()

        # Create Queue if not already present
        self.channel.queue_declare(queue="Queue Name")

        # Create the exchange if not already present
        self.exchange = self.channel.exchange_declare(exchange="Exchange Name")

        # Bind Binding Key to Queue on the exchange
        self.channel.queue_bind(
            queue = self.queue,
            routing_key = self.key,
            exchange= self.name,
        )


        # Set-up Callback function for receiving messages
        self.channel.basic_consume(
             self.queue, self.setupRMQConnection(), auto_ack=False
        )

        pass


    def on_message_callback(self, channel, method_frame, header_frame, body):
        # Acknowledge message
        self.channel.basic_ack(method_frame, header_frame, False)

        #Print message (The message is contained in the body parameter variable)
        print(body)

        pass
        

    def startConsuming(self):
        # Print " [*] Waiting for messages. To exit press CTRL+C"
        print("[*] Waiting for messages. To exit press CTRL+C")

        # Start consuming messages
        self.channel.start_consuming()

        pass
    
    def __del__(self):
        # Print "Closing RMQ connection on destruction"
        print("Closing RMQ connection on destruction")

        # Close Channel
        self.channel.close()

        # Close Connection
        self.connection.close()
        
        pass
