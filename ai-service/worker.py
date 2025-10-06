import pika, json, redis
from app.services.contract_review.generation_workflow import process_contract_workflow

r = redis.Redis(host="localhost", port=6379, db=0)

def process_message(ch, method, properties, body):
    message = json.loads(body)
    contract_id = message.get("id")
    file_name = message.get("fileName")
    text = message.get("extractedText")
    header = message.get("header")
    
    print(f"Processing contract {contract_id} - {file_name}")
    
    # Process contract in one call
    result = process_contract_workflow(text)
    
    # Store result in Redis
    result_json = json.dumps(result)
    r.set(contract_id, result_json)
    r.publish("contract_results", json.dumps({"id": contract_id, "result": result_json}))
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="contract-queue", durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="contract-queue", on_message_callback=process_message)
    print(" [*] Worker started. Waiting for messages...")
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()