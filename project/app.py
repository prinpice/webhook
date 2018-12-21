from flask import Flask, request
import os
from pprint import pprint as pp
import requests
import random

app = Flask(__name__)

token = os.getenv('TELEGRAM_TOKEN')
# chat_id = os.getenv('CHAT_ID')
base_url = "https://api.hphk.io/telegram"
my_url = "https://webhook-piie.c9users.io" # c9 주소
naver_id = os.getenv('NAVER_ID')
naver_secret = os.getenv('NAVER_SECRET')


# 상태변화가 올때마다(메세지를 받을 때) 알리미가 오는 서비스

# 웹훅을 통해 정보가 들어올 route
@app.route('/{}'.format(token), methods=['POST'])
def telegram():
    doc = request.get_json() #json으로 파싱
    # request : 요청을 받았을 때 요청을 보낸 사람, 내용 들을 알려준다 . cf. requests : request를 보내준다.
    pp(doc)
    # 어떤 메세지가 들어오던 '닥쳐'라고 하는 챗봇
    chat_id = doc["message"]["chat"]["id"]
    # msg = doc["message"]["text"] # key가 없으면 에러가 발생한다.
    # msg = doc.get["message"].get["text"] # key가 없으면 none을 return하고 넘어간다.
    # if msg == "로또":
    #     msg = str(random.sample(range(1, 46), 6))
    # # elif msg == '목요웹툰':
    # #     url = "https://m.comic.naver.com/webtoon/weekday.nhn?week=thu"
    # #     res  = requests.get(url).text
    # #     doc = bs(res, 'html.parser')
        
        
    # # 조건문이 많아지면 딕셔너리로 관리하는 것이 편함
    #  send_url = "{}/bot{}/sendMessage?chat_id={}&text={}".format(base_url, token, chat_id, msg)
    
   
    
    ## 파일처리
    img = False
    
    if doc.get('message').get('photo') is not None:
        img = True
    
    if img:
        file_id = doc.get('message').get('photo')[-1].get('file_id')
        file = requests.get("{}/bot{}/getFile?file_id={}".format(base_url, token, file_id))
        file_url = "{}/file/bot{}/{}".format(base_url, token, file.json().get('result').get('file_path'))
        
        # 네이버로 요청
        res = requests.get(file_url, stream=True)
        clova_res = requests.post('https://openapi.naver.com/v1/vision/celebrity',
            headers={
                'X-Naver-Client-Id':naver_id,
                'X-Naver-Client-Secret':naver_secret
            },
            files={
                'image':res.raw.read()
            })
        if clova_res.json().get('info').get('faceCount'):
            print(clova_res.json().get('faces'))
            text = "{}".format(clova_res.json().get('faces')[0].get('celebrity').get('value'))
        else:
            text = "인식된 사람이 없습니다."
    else:
    	# text 처리
    	text = doc['message']['text']
    
    send_url = "{}/bot{}/sendMessage?chat_id={}&text={}".format(base_url, token, chat_id, text)
    
    requests.get(send_url)
    return '', 200 # 200으로 응답해주지 않으면 응답이 올때까지 계속 알림을 보낸다. 즉 무한반복된다.
    

# 웹훅 설정(set webhook) == 텔레그램에게 알리미를 해달라고 하는 것
@app.route('/setwebhook')
def setwebhook():
    # "base_url" + "/bot{token}" + "/setWebhook"
    url = "{}/bot{}/setwebhook?url={}/{}".format(base_url, token, my_url, token) 
    res = requests.get(url)
    
    return '{}'.format(res), 200 # statuscode인 200을 return 해줘야 알림을 멈춘다.
    # ('{}'.format(res), 200) 위의 return 값에 ()가 생략되어 있다.
# 텔레그램이 우리에게 알림을 줄 때 사용할 route
#   만약 특정 유저가 우리 봇으로 메세지를 보내게 되면,
#       텔레그램이 우리에게 알림을 보내온다.(json)
# @app.route()
