# import boto3
import json
import uuid
from datetime import datetime
from geopy.geocoders import Nominatim

# def connect_dynamodb():
#     return boto3.resource('dynamodb', region_name="ap-southeast-2"), boto3.client('dynamodb',
#                                                                                   region_name="ap-southeast-2")
#
#
# resource, client = connect_dynamodb()
# table = resource.Table('system')
# new_dict = {'uid': 'australian_university_list'}
# user_dict = {}
# response = table.get_item(
#     Key={
#         'uid': 'australian_university_list',
#     }
# )
# if 'Item' in response:
#     user_dict = response['Item']
# new_dict.update(user_dict)
# welp = ["Australian National University",
#         "University of Canberra",
#         "University of New England",
#         "Charles Sturt University",
#         "Southern Cross University",
#         "University of Newcastle",
#         "Australian Catholic University",
#         "Macquarie University",
#         "University of New South Wales",
#         "University of Sydney",
#         "Sydney University of Technology",
#         "University of Western Sydney",
#         "University of Wollongong",
#         "Charles Darwin University",
#         "Griffith University",
#         "Queensland University of Technology",
#         "University of Queensland",
#         "Bond University",
#         "University of the Sunshine Coast",
#         "CQ University",
#         "University of Southern Queensland",
#         "James Cook University",
#         "Carnegie Mellon University",
#         "Flinders University",
#         "University of Adelaide",
#         "University College London",
#         "University of South Australia",
#         "Torrens University Australia",
#         "University of Tasmania",
#         "Federation University of Australia",
#         "Deakin University",
#         "La Trobe University",
#         "RMIT University",
#         "Monash University",
#         "Swinburne University of Technology",
#         "University of Divinity",
#         "University of Melbourne",
#         "Victoria University",
#         "University of Notre Dame Australia",
#         "Curtin University",
#         "Edith Cowan University",
#         "Murdoch University",
#         "University of Western Australia"]
#
# new_dict['data'] = []
# for i in welp:
#     new_dict['data'].append(i)
# print(new_dict)
# table.put_item(
#     Item=new_dict
# )

import requests
#
# url = "https://currency-converter5.p.rapidapi.com/currency/convert"
#
# querystring = {"format":"json","from":"AUD","to":"CAD","amount":"1"}
#
# headers = {
#         'x-rapidapi-key': "209d311956msh6a394e3d9816c96p1b0205jsncdf19d65071c",
#         'x-rapidapi-host': "currency-converter5.p.rapidapi.com"
# }
#
# response = requests.request("GET", url, headers=headers, params=querystring)
#
# print(response.text)

# http://api.exchangeratesapi.io/v1/latest?access_key=89df0d3203d7ecd9dc2000acd9e91802

#
# def forecast_weather():
#     now = datetime.now()
#     time = now.strftime("%H:%M:%S")
#     date = now.strftime("%Y-%m-%d")
#     city = "Melbourne"
#     nominatim = Nominatim(user_agent="forecast")
#     location = nominatim.geocode(city)
#     latitude = round(location.latitude, 2)
#     longitude = round(location.longitude, 2)
#     url = f"https://api.weather.com/v2/turbo/vt1dailyForecast?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode={latitude}%2C{longitude}&language=en-IN&units=m"
#     print(url)
#     response = requests.get(url)
#     response_data = response.json()
#     print(response_data)
#     try:
#         dates_time_list = response_data["vt1dailyForecast"]["validDate"]
#         dates_list = [_.split("T0")[0] for _ in dates_time_list]
#         date_index = dates_list.index(date)
#     except Exception as e:
#         print("Please check the date format. [Y-m-d]")
#
#     try:
#         # day
#         temperature_day = response_data["vt1dailyForecast"][
#             "day"]["temperature"][date_index]
#         precipitate_day = response_data["vt1dailyForecast"][
#             "day"]["precipPct"][date_index]
#         uv_description_day = response_data["vt1dailyForecast"][
#             "day"]["uvDescription"][date_index]
#         wind_speed_day = response_data["vt1dailyForecast"][
#             "day"]["windSpeed"][date_index]
#         humidity_day = response_data["vt1dailyForecast"][
#             "day"]["humidityPct"][date_index]
#         phrases_day = response_data["vt1dailyForecast"][
#             "day"]["phrase"][date_index]
#         narrative_day = response_data["vt1dailyForecast"][
#             "day"]["narrative"][date_index]
#
#         forecast_output = {"place": city, "time": time, "date": date, "day": {"temperature": temperature_day,
#                                                                               "precipitate": precipitate_day,
#                                                                               "uv_description": uv_description_day,
#                                                                               "wind_speed": wind_speed_day,
#                                                                               "humidity": humidity_day,
#                                                                               "phrases": phrases_day,
#                                                                               "narrative": narrative_day
#                                                                               }, }
#
#     except Exception as e:
#         return "Exception while fetching data"
#
#     return forecast_output

# forecast_weather()

# url = 'https://api.openweathermap.org/data/2.5/weather?q=Melbourne&appid=a4d4c5d09f808e4f1618c6aec3417215&units=metric'
#
# response = requests.get(url)
# response_data = response.json()
# print(response_data)
# print(response_data.get('main'))
#
# # import requests

# url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
#
# querystring = {"term":"wat"}
#
# headers = {
#     'x-rapidapi-key': "209d311956msh6a394e3d9816c96p1b0205jsncdf19d65071c",
#     'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
# }
#
# response = requests.request("GET", url, headers=headers, params=querystring)
# word_list = []
# di = json.loads(response.content.decode())
# print(di.get('list'))
# for i in di.get('list'):
#     print(i.get('definition'))
#     word_list.append(i.get('definition'))
#
# print(word_list)
# c1 = 'USD'
# c2 = 'INR'
# url = 'https://free.currconv.com/api/v7/convert?q=USD_INR&compact=ultra&apiKey=22d5822ef51811e044a5'
# # url = 'https://free.currconv.com/api/v7/currencies?apiKey=22d5822ef51811e044a5'
# # /api/v7/currencies?apiKey=[YOUR_API_KEY]
# response = requests.get(url)
# response_data = response.json()
# # print(response_data)
# print(response_data.get(c1 + '_' + c2))
# results =response_data.get('results')
# print(results)
# for i in results:
#     print(i)
#     print(results[i])
# return response_data.get('main')

# a = 2.045
#
# print(a*73.18105)

import boto3

# client = boto3.client('s3')
#
# # f.save('/tmp/temp.jpg')
#
# # f = open('/tmp/temp.jpg')
# # f = open('./static/res/bot.jpg')
# f = open('./tmp/b.jpg', 'w+')
# f.close()
# # client.upload_file('./static/res/bot.jpg', 'unimate-user-s3', 'user-images/hello' + '.jpg',
#                    ExtraArgs={'ACL': 'public-read'})

cohort_id = "rmit-university-2020-1-computer-science"
auth_id = "29d80997-77f1-493c-a708-ee50c99f9f49"
resource = boto3.resource('dynamodb')
client = boto3.client('dynamodb')

table_list = client.list_tables()['TableNames']

if not cohort_id in table_list:
    print(False)
else:
    table = resource.Table(cohort_id)

    res = table.scan()

    print(res)

    cohort_dict = {'uid': str(uuid.uuid4())}
    cohort_dict['author'] = auth_id
    cohort_dict['author_name'] = "Nyet"
    cohort_dict[
        'author_userImage'] = "https://unimate-user-s3.s3.ap-southeast-2.amazonaws.com/user-images/29d80997-77f1-493c-a708-ee50c99f9f49.jpg"
    cohort_dict['subject'] = "Whats up"
    cohort_dict['message'] = "Hey how are you?"
    cohort_dict['contact'] = "abhi"
    cohort_dict['date'] = str(datetime.now())

    table = resource.Table(cohort_id)

    # res = table.put_item(Item=cohort_dict)

    res_dict = dict(res)
    print(res_dict.get('Items'))
    print(cohort_dict)