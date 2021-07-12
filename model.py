import boto3
import uuid
import logging
import json
import requests
from cryptography.fernet import Fernet

# logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename='tmp.log', filemode='a',
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


def connect_dynamodb():
    return boto3.resource('dynamodb', region_name="ap-southeast-2"), boto3.client('dynamodb',
                                                                                  region_name="ap-southeast-2")


def connect_s3():
    return boto3.resource('s3', region_name="ap-southeast-2"), boto3.client('s3',
                                                                            region_name="ap-southeast-2")


def settings():
    establish_dynamodb()
    establish_s3()
    return True


def establish_s3(resource=None, client=None):
    logging.debug('model.py establish_s3 BEGIN')
    if client is None or resource is None:
        resource, client = connect_s3()
    bucket_list = client.list_buckets().get('Buckets')
    if 'unimate-user-s3' in str(bucket_list):
        return True
    client.create_bucket(
        ACL='public-read',
        Bucket='unimate-user-s3',
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-southeast-2'
        },
        ObjectLockEnabledForBucket=False
    )
    client.get_waiter('bucket_exists').wait(Bucket='unimate-user-s3')
    logging.debug('model.py establish_s3 END')
    return True


def establish_dynamodb(resource=None, client=None):
    logging.info('database.py establish_dynamodb BEGIN')
    if client is None or resource is None:
        resource, client = connect_dynamodb()
    table_list = client.list_tables()['TableNames']
    if 'users' in table_list:
        logging.info('database.py establish_dynamodb users table already exists')
    else:
        table = resource.create_table(
            TableName='users',
            KeySchema=[
                {
                    'AttributeName': 'uid',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'uid',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName='users')

    if 'system' in table_list:
        logging.info('database.py check_dynamodb system table already exists')
    else:
        table = resource.create_table(
            TableName='system',
            KeySchema=[
                {
                    'AttributeName': 'uid',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'uid',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName='system')
    return True


def dynamodb_creat_cohort_ifnotexists(cohort, resource=None, client=None):
    logging.info('database.py dynamodb_creat_cohort_ifnotexists BEGIN')
    if client is None or resource is None:
        resource, client = connect_dynamodb()
    table_list = client.list_tables()['TableNames']
    if cohort in table_list:
        logging.info('database.py establish_dynamodb cohort table already exists')
    else:
        table = resource.create_table(
            TableName=cohort,
            KeySchema=[
                {
                    'AttributeName': 'uid',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'uid',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=cohort)
    return True


def upload_user_image_s3(auth_id, resource=None, client=None):
    if client is None or resource is None:
        resource, client = connect_s3()
    client.upload_file('/home/ec2-user/images/' + auth_id + '.jpg', 'unimate-user-s3', 'user-images/' + auth_id + '.jpg',
                       ExtraArgs={'ACL': 'public-read'})
    return True


def dynamodb_user_table_put(user_dict: dict, client=None, resource=None):
    logging.debug('model.py dynamodb_user_table_put BEGIN')
    if client is None or resource is None:
        resource, client = connect_dynamodb()
    table = resource.Table('users')
    if 'uid' not in user_dict:
        return False
    new_dict = {}
    response = table.get_item(
        Key={
            'uid': user_dict.get('uid'),
        }
    )
    if 'Item' in response:
        new_dict = response['Item']
    print("PUTT ", new_dict)
    print(user_dict)
    # user_dict.pop('uid')
    new_dict.update(user_dict)
    table.put_item(
        Item=new_dict
    )
    logging.debug('model.py dynamodb_user_table_put END')
    return True


def dynamodb_user_table_get(uid, client=None, resource=None):
    logging.debug('model.py dynamodb_user_table_put BEGIN')
    if client is None or resource is None:
        resource, client = connect_dynamodb()
    table = resource.Table('users')
    if not 'uid':
        return False
    response = table.get_item(
        Key={
            'uid': uid,
        }
    )
    if 'Item' in response:
        return response['Item']
    logging.debug('model.py dynamodb_user_table_put END')
    return False


def dynamodb_system_get_university_list(client=None, resource=None):
    logging.debug('model.py dynamodb_system_get_university_list BEGIN')
    if client is None or resource is None:
        resource, client = connect_dynamodb()
    table = resource.Table('system')

    response = table.get_item(
        Key={
            'uid': 'australian_university_list',
        }
    )
    # print(response)
    if 'Item' in response:
        return response['Item'].get('data')
    logging.debug('model.py dynamodb_user_table_put END')
    return False


def dynamodb_system_get_subject_list(client=None, resource=None):
    logging.debug('model.py dynamodb_system_get_university_list BEGIN')
    # if client is None or resource is None:
    #     resource, client = connect_dynamodb()
    # table = resource.Table('system')

    # response = table.get_item(
    #     Key={
    #         'uid': 'australian_university_list',
    #     }
    # )
    # print(response)
    # if 'Item' in response:
    #     return response['Item'].get('data')
    # logging.debug('model.py dynamodb_user_table_put END')
    # return False
    return ["Computer Science", "Physics", "Chemistry", "Math"]


def rds_user_table_put(user_dict: dict):
    logging.debug('model.py rds_user_table_put BEGIN')
    if 'username' not in user_dict or 'password' not in user_dict or 'uid' not in user_dict:
        return False
    new_dict = user_dict
    new_dict['authentication'] = 'idontknow'
    new_dict['sql'] = 'insert'
    response = requests.post("https://1lubspxlkd.execute-api.ap-southeast-2.amazonaws.com/dev/update",
                             data=json.dumps(user_dict))
    print(response.content.decode())
    logging.debug('model.py rds_user_table_put END')
    if 'success' in response.content.decode():
        return True
    return False


def rds_user_table_change_password(uid, old, new):
    logging.debug('model.py rds_user_table_change_password BEGIN')
    if not old or not new or not uid:
        return False
    new_dict = {}
    new_dict['authentication'] = 'idontknow'
    new_dict['sql'] = 'update'
    new_dict['password'] = new
    new_dict['uid'] = uid
    response = requests.post("https://1lubspxlkd.execute-api.ap-southeast-2.amazonaws.com/dev/update",
                             data=json.dumps(new_dict))
    print(response.content.decode())
    logging.debug('model.py rds_user_table_put END')
    if 'success' in response.content.decode():
        return True
    return False


def authenticate_login(username, password):
    logging.debug('model.py authenticate_login BEGIN')
    json_body = {'authentication': "idontknow"}
    json_body['username'] = username
    json_body['password'] = password
    json_body['sql'] = 'check'
    response = requests.post("https://1lubspxlkd.execute-api.ap-southeast-2.amazonaws.com/dev/check",
                             data=json.dumps(json_body))
    logging.debug('model.py authenticate_login END')
    if 'success' in response.content.decode():
        response_dict = json.loads(response.content.decode())
        return response_dict['uid']
    return False


def check_username_exists(username):
    logging.debug('model.py check_username_exists BEGIN')
    json_body = {'authentication': "idontknow"}
    json_body['username'] = username
    json_body['password'] = "None"
    json_body['sql'] = 'check'
    response = requests.post("https://1lubspxlkd.execute-api.ap-southeast-2.amazonaws.com/dev/check",
                             data=json.dumps(json_body))
    print(response.content.decode())
    response_dict = json.loads(response.content.decode())
    print(response_dict)
    logging.debug('model.py check_username_exists END')
    if response_dict['username'] is False:
        return False
    else:
        return True


def register_new_user(username, password):
    if check_username_exists(username):
        return "Username Exists", False
    uid = str(uuid.uuid4())
    new_dict = {'username': username, 'password': password, 'uid': uid, 'details_updated': False}
    if not rds_user_table_put(new_dict):
        return "RDS error", False
    new_dict.pop('password')
    dynamodb_user_table_put(new_dict)
    return True, True


def update_user_details(user_dict):
    return dynamodb_user_table_put(user_dict)


def get_user_details(uid):
    u = dynamodb_user_table_get(uid)
    if not u:
        return False
    return u


def check_cohorts(cohorts: list):
    for i in cohorts:
        dynamodb_creat_cohort_ifnotexists(i)
    return True


def urban_dictionary(word):
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    word_list = []
    querystring = {"term": word}

    headers = {
        'x-rapidapi-key': "209d311956msh6a394e3d9816c96p1b0205jsncdf19d65071c",
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    di = json.loads(response.content.decode())
    print(di.get('list'))
    for i in di.get('list'):
        print(i.get('definition'))
        word_list.append(i.get('definition'))

    return word_list


def user_post_new_event(cohort_id, event_dict):
    return True


def currency_exchange(currency1, currency2):
    url = 'https://free.currconv.com/api/v7/convert?q=' + currency1 + '_' + currency2 + '&compact=ultra&apiKey=22d5822ef51811e044a5'

    response = requests.get(url)
    response_data = response.json()
    # print(response_data)
    # print(response_data.get('main'))
    # print()

    return response_data.get(currency1 + '_' + currency2)


def get_currency_list():
    url = 'https://free.currconv.com/api/v7/currencies?apiKey=22d5822ef51811e044a5'
    response = requests.get(url)
    response_data = response.json()
    results = response_data.get('results')
    return results


def forecast_weather():
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Melbourne&appid=a4d4c5d09f808e4f1618c6aec3417215&units=metric'

    response = requests.get(url)
    response_data = response.json()
    # print(response_data)
    # print(response_data.get('main'))
    return response_data.get('main')


def encrypt(message):
    try:
        if type(message) is str:
            message = message.encode()
        key = b'D5bCbqDLxmSyCx27JOnN9QvRUltE-GbljGoGsJ1ZAVo='
        return Fernet(key).encrypt(message).decode()
    except:
        return None


def decrypt(token):
    try:
        if type(token) is str:
            token = token.encode()
        key = b'D5bCbqDLxmSyCx27JOnN9QvRUltE-GbljGoGsJ1ZAVo='
        return Fernet(key).decrypt(token).decode()
    except:
        return None
