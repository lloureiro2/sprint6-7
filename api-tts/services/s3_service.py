import boto3 # type: ignore
from botocore.exceptions import ClientError # type: ignore

# Inicializa o cliente S3 uma vez
s3_client = boto3.client('s3')

# Função para verificar se o bucket já existe
def check_bucket_exists(bucket_name):

    try:
        # Tenta obter o cabeçalho do bucket para verificar sua existência
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            return False
        else:
            # Levanta exceção se ocorrer um erro diferente de "bucket não encontrado"
            raise e

# Função para criar um bucket S3
def create_bucket(bucket_name, region=None):
    
    try:
        # Verifica se o bucket já existe
        if check_bucket_exists(bucket_name):
            print(f"Bucket '{bucket_name}' já existe")
            return False

        # Cria o bucket na região especificada
        if region is None:
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )

        print(f"Bucket '{bucket_name}' criado.")
        return True

    except ClientError as e:
        # Tratamento de erros específicos para nome de bucket já em uso
        error_code = e.response['Error']['Code']
        if error_code in ['BucketAlreadyOwnedByYou', 'BucketAlreadyExists']:
            print(f"Você já possui o bucket '{bucket_name}' ou o nome já está em uso globalmente.")
        else:
            print(f"Erro ao criar o bucket: {e}")
        return False
