from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
##start_date is myself
start_date = os.environ['START_DATE']
start_date1 = os.environ['START_DATE1']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
birthday1 = os.environ['BIRTHDAY1']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id1 = os.environ["USER_ID1"]
template_id = os.environ["TEMPLATE_ID"]

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=汕头"
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  x = int(weather['temp'])
  return weather['weather'],x

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_count1():
  delta = today - datetime.strptime(start_date1, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_birthday1():
  next = datetime.strptime(str(date.today().year) + "-" + birthday1, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_words1():
  words = "日光给你镀上成熟，月华增添你的妩媚，生日来临之际，愿朋友的祝福汇成你快乐的源泉愿祝福萦绕着你，在你永远与春天接壤的梦幻里。祝你：心想事成幸福快乐！生日快乐！"
  return words

# def get_proe():
#   proe = requests.get("http://yijuzhan.com/api/word.php?m=json")
#   if proe.status_code != 200:
#     return get_proe()
#   re = proe.json()['content']
#   return re
# def get_proe():
#   proe = requests.get("http://yijuzhan.com/api/word.php?m=json")
#   if proe.status_code != 200:
#     return get_proe()
#   re1 = proe.json()['content']
#   re2 = proe.json()['source']
#   re3 = re1+'--'+re2
#   return re3

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)
  #return "#3399FF"
  
def get_random_color_to_birthday():
  return "red"


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
def get_weathers():
  wea='good'
  temperature=random.randint(12, 20)
  
#wea,temperature = get_weathers()
wea="晴"
temperature=22
next1 = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
print(next1)
print(datetime.now())
bday = (next1 - today).days
# if next1 == datetime.now():
#     # next1 = next1.replace(year=next1.year + 1)
#     bday = (next1 - today).days



#if bday == 0 :
  #data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words1(),"color":get_random_color_to_birthday()}}
# res = wm.send_template(user_id, template_id, data)
  #res1 = wm.send_template(user_id,template_id,data)
  #print(res1)
#else:
# data = {"weather":{"value":'good'},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(),"color":get_random_color()}}
 #res = wm.send_template(user_id, template_id, data)
  #res1 = wm.send_template(user_id,template_id,data)
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(),"color":get_random_color()}}
data1 = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count1()},"birthday_left":{"value":get_birthday1()},"words":{"value":get_words(),"color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
res1 = wm.send_template(user_id1,template_id,data1)

# proe = get_proe()
#data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(),"color":get_random_color()}}
#data1 = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count1()},"birthday_left":{"value":get_birthday1()},"words":{"value":get_words(),"color":get_random_color()}}

#res = wm.send_template(user_id, template_id, data)
#res1 = wm.send_template(user_id1,template_id,data1)
print(res)
print(res1)

# def get_weather():
#   url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
#   res = requests.get(url).json()
#   weather = res['data']['list'][0]
#   return weather['weather'], math.floor(weather['temp'])

# def get_count():
#   delta = today - datetime.strptime(start_date, "%Y-%m-%d")
#   return delta.days

# def get_birthday():
#   next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
#   if next < datetime.now():
#     next = next.replace(year=next.year + 1)
#   return (next - today).days

# def get_words():
#   words = requests.get("https://api.shadiao.pro/chp")
#   if words.status_code != 200:
#     return get_words()
#   return words.json()['data']['text']

# def get_proe():
#   proe = requests.get("http://yijuzhan.com/api/word.php?m=json")
#   if proe.status_code != 200:
#     return get_proe()
#   re = proe.json()['content']
#   return re

# def get_random_color():
#   return "#%06x" % random.randint(0, 0xFFFFFF)


# client = WeChatClient(app_id, app_secret)

# wm = WeChatMessage(client)
# wea, temperature = get_weather()
# data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(),"color":get_random_color()}}
# res = wm.send_template(user_id, template_id, data)
# print(res)
