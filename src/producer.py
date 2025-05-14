import uuid
from datetime import datetime, timedelta
import requests
import uuid
import json
from kafka import KafkaProducer
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CONFIG = {
    'KAFKA_TOPIC': "users_created",
    'KAFKA_BOOTSTRAP_SERVERS': "localhost:29092",
    'KAFKA_CONSUMER_GROUP': "user_group",
    'OUTPUT_FILE': "/home/tienanh/kafka-demo/data/output.json",
}


def extract_data():
    res = requests.get("https://randomuser.me/api/")
    data = res.json()
    user = data['results'][0]  

    with open(CONFIG['OUTPUT_FILE'], 'w') as f:
        json.dump(data, f, indent=4)

    return user

def transform_data(res):
    try:
        data = {}
        location = res['location']
        data['id'] = res['id']['value']
        data['first_name'] = res['name']['first']
        data['last_name'] = res['name']['last']
        data['gender'] = res['gender']
        data['address'] = f"{location['street']['number']} {location['street']['name']}, " \
                          f"{location['city']}, {location['state']}, {location['country']}"
        data['post_code'] = location['postcode']
        data['email'] = res['email']
        data['username'] = res['login']['username']
        data['dob'] = res['dob']['date']
        data['registered_date'] = res['registered']['date']
        data['phone'] = res['phone']
        data['picture'] = res['picture']['medium']

        print(f"[format_data] Formatted data: {data}")
        return data
    
    except KeyError as e:
        print(f"[format_data] Missing key: {e}")
        return None

def send_to_kafka():
    producer = KafkaProducer(
        bootstrap_servers=CONFIG['KAFKA_BOOTSTRAP_SERVERS'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    curr_time = time.time()
    while True:
        if time.time() > curr_time + 60:
            break
        try:
            user = extract_data()
            formatted_data = transform_data(user)

            if formatted_data is not None:
                producer.send(
                    topic=CONFIG['KAFKA_TOPIC'],
                    value=formatted_data
                )
            producer.flush()
            print(f"[send_to_kafka] Sent data to Kafka")
        except Exception as e:
            print(f"[send_to_kafka] Error sending data to Kafka: {e}")
            continue


if __name__ == "__main__":
    try:
        send_to_kafka()
        logger.info("Kafka producer started successfully.")
    except Exception as e:
        logger.error("Error starting Kafka producer: %s", str(e))

# python3 src/producer.py