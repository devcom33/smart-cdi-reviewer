import pika, json, redis
from app.services.contract_review.indexing import index_contract
from app.services.contract_review import Generation

r = redis.Redis(host="localhost", port=6379, db=0)

def process_message(ch, method, properties, body):
    message = json.loads(body)
    contract_id = message.get("id")
    file_name = message.get("fileName")
    text = message.get("extractedText")
    header = message.get("header")

    print(f"Processing contract {contract_id} - {file_name}")

    index_contract(text)
    result = Generation.generate_issues()

    if hasattr(result, "body"):
        result_json = result.body
        r.set(contract_id, result_json.decode("utf-8"))
        r.publish("contract_results", json.dumps({"id": contract_id, "result": result_json.decode("utf-8")}))
    else:
        r.set(contract_id, json.dumps(result))
        r.publish("contract_results", json.dumps({"id": contract_id, "result": json.dumps(result)}))
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