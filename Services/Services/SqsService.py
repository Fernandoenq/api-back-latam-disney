from Application.Configuration import Configuration
import boto3
import json

sqs_client = boto3.client(
    "sqs",
    aws_access_key_id=Configuration.aws_access_key_id,
    aws_secret_access_key=Configuration.aws_secret_access_key,
    region_name=Configuration.region_name
)


class SqsService:
    @staticmethod
    def notify(message, name: str, phone: str) -> bool:
        try:
            response = sqs_client.send_message(
                QueueUrl=Configuration.sqs_queue_url,
                MessageBody=json.dumps(message)
            )

            if response.get('MessageId'):
                print(f"Mensagem enviada com sucesso para {name} / {phone}. "
                      f"ID da mensagem: {response['MessageId']}")
                return True
            else:
                print(f"Falha ao enviar mensagem para {name} / {phone}.")
                return False

        except Exception as e:
            print(f"Erro ao enviar mensagem para {name} / {phone}: {e}")
            return False
