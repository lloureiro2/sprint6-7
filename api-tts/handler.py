import json
import datetime
from utils.helpers import generate_id
from services.polly_service import generate_audio_and_store_in_s3
from services.dynamo_service import save_to_dynamodb, get_dynamodb

#Função para criar uma resposta HTTP com cabeçalhos configurados para UTF-8.
def response_with_headers(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json; charset=utf-8"
        },
        "body": json.dumps(body, ensure_ascii=False)
    }

# Função de verificação de saúde da API
def health(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }
    return response_with_headers(200, body)

# Função para descrição da versão da API
def v1_description(event, context):
    body = {"message": "TTS api version 1."}
    return response_with_headers(200, body)

# Função para processar a conversão de texto para fala
def text_to_speech(event, context):
    try:
        # Faz o parse do corpo da requisição JSON
        body = json.loads(event.get('body', '{}'))
        phrase = body.get('phrase')

        # Verifica se a frase foi fornecida
        if not phrase:
            return response_with_headers(400, {"error": "Frase não fornecida"})

        # Gera um ID único para a frase
        unique_id = generate_id(phrase)
        # Verifica se a frase já foi processada anteriormente
        existing_item = get_dynamodb(unique_id)

        if existing_item:
            # Se a frase já existe, retorna os dados existentes
            return response_with_headers(200, existing_item)

        # Gera o áudio e armazena no S3
        audio_url = generate_audio_and_store_in_s3(phrase, unique_id)
        # Salva os dados no DynamoDB
        save_to_dynamodb(phrase, unique_id, audio_url)

        # Retorna a resposta com os dados recém-criados
        response_body = {
            "received_phrase": phrase,
            "url_to_audio": audio_url,
            "created_audio": datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            "unique_id": unique_id
        }

        return response_with_headers(200, response_body)

    except Exception as e:
        # Retorna uma mensagem de erro em caso de exceção
        return response_with_headers(500, {"message": "Internal Server Error", "error": str(e)})
