import boto3
import os
from image_api_client import ImageApiClient
from jwt_validate import JWTValidator


def get_dynamodb(is_offline):
    if is_offline:
        return boto3.resource('dynamodb', region_name='localhost', endpoint_url=os.environ['LOCAL_DYNAMODB'])

    return boto3.resource('dynamodb')


class GDLConfig:
    IS_OFFLINE = os.getenv('IS_OFFLINE', False)
    GAMES_TABLE = get_dynamodb(IS_OFFLINE).Table(os.environ['GAMES_TABLE'])
    GDL_ENVIRONMENT = os.getenv('GDL_ENVIRONMENT', 'prod')
    IMAGE_API_CLIENT = ImageApiClient(
        os.environ['IMAGE_API_OFFLINE_ADDRESS'] if IS_OFFLINE else 'http://image-api.gdl-local')
    JWT_VALIDATOR = JWTValidator(GDL_ENVIRONMENT)