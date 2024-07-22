import boto3 # type: ignore
from services.s3_service import create_bucket

# Inicia a sessão boto3 e cria recursos para Polly e S3
session = boto3.Session()
polly = session.client('polly')
s3 = session.client('s3')
region = session.region_name
bucket_name = 'seu Bucket'

# Cria o bucket se ele não existir
create_bucket(bucket_name, region)

# Função para gerar áudio e armazenar no S3
def generate_audio_and_store_in_s3(phrase, unique_id):
    # Especifica o engine 'neural' e a voz 'Thiago' para português
    engine = 'neural'
    voice_id = 'Thiago'

    # Tenta sintetizar o discurso usando Polly
    try:
        response = polly.synthesize_speech(
            Text=phrase,
            OutputFormat='mp3',
            VoiceId=voice_id,
            Engine=engine  # Especifica o engine como 'neural'
        )

        audio_key = f'audio-{unique_id}.mp3'
        s3.put_object(Bucket=bucket_name, Key=audio_key, Body=response['AudioStream'].read())

        return f'https://{bucket_name}.s3.amazonaws.com/{audio_key}'

    except Exception as e:
        print(f"Erro ao gerar áudio: {e}")
        raise e
