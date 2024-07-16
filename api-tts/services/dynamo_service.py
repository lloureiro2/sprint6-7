import datetime
import boto3 # type: ignore

# Inicia a sessão boto3 e cria recurso para DynamoDB
session = boto3.Session()
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('tabletts')

# Função para salvar dados no DynamoDB
def save_to_dynamodb(phrase, unique_id, audio_url):
    table.put_item(
        Item={
            'unique_id': unique_id,
            'received_phrase': phrase,
            'url_to_audio': audio_url,
            'created_audio': datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        }
    )

# Função para obter dados do DynamoDB
def get_dynamodb(unique_id):
    response = table.get_item(Key={'unique_id': unique_id})
    return response.get('Item')
