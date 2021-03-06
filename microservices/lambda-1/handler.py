import json
import boto3
import sys
sys.path.insert(0, '/opt')

from env import Variables

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

xray_recorder.configure(service='My app')
patch_all()

def buscarUsuario(event, context):
    usuario = event['pathParameters']['usuario'];
    
    body = {
        "message": "O usuario enviado foi: " + str(usuario)
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
    
def criarUsuario(event, context):
    
    print('body: ' + str(event['body']))
    
    env = Variables();
    
    usuario = event['body'];

    print('Usuario: ' + str(usuario))
    
    sqs = boto3.resource('sqs')
    
    queue = sqs.get_queue_by_name(QueueName=env.get_sqs_url_dest())
    queue.send_message(MessageBody=usuario)
    
    print('mensagem enviada')
    
    body = {
        "message": "O usuario enviado foi cadastrado"
    }
    
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response