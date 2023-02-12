import signal
from confluent_kafka import Producer

import json
from common import TOPIC_NAME, BROKER_HOST

p = Producer({
    "bootstrap.servers": BROKER_HOST
})


def deliver_reporter(err, msg):
    if err is not None:
        print(f"Message deliver failed: {msg}")
    else:
        print(f"Message deliver to topic={msg.topic()} partition={msg.partition()}")

def handle_signal():
    print("kafka_producer: close")
    p.close()

def produce():
    signal.signal(signal.SIGINT, handler=handle_signal)
    signal.signal(signal.SIGTERM, handler=handle_signal)

    for i in range(10):
        _data = {"test": i}
        _data_json = json.dumps(_data)

        p.poll(0)

        p.produce(TOPIC_NAME, _data_json.encode("utf-8"), on_delivery=deliver_reporter)
    
    p.flush()

if __name__ == '__main__':
    produce()



    