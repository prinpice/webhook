# SSAFY Start Camp 챗봇 퀘스트

서울1정찬미, https://github.com/prinpice

## I. 스펙(Specification)

사용자가 Telegram을 통해 챗봇에게 전송한 데이터를 분석한다.

### (1) 답장 기능

* 사용자가 '로또'를 입력하면 6개의 랜덤 숫자를 답장한다.
* 그 외의 단어를 입력하면 입력한 단어를 반환한다.

```python
# 웹훅을 통해 정보가 들어올 route
@app.route('/{}'.format(token), methods=['POST'])
def telegram():
    doc = request.get_json() #json으로 파싱
    # request : 요청을 받았을 때 요청을 보낸 사람, 내용 들을 알려준다 . cf. requests : request를 보내준다.
    pp(doc)
    # 특정 메세지가 들어오면 답장하는 챗봇
    chat_id = doc["message"]["chat"]["id"]
    msg = doc["message"]["text"]
    if msg == "로또":
    	msg = str(random.sample(range(1, 46), 6))
    send_url = "{}/bot{}/sendMessage?chat_id={}&text={}".format(base_url, token, chat_id, msg)
    
    requests.get(send_url)
    return '', 200 # 200으로 응답해주지 않으면 응답이 올때까지 계속 알림을 보낸다. 즉 무한반복된다.
```



### (2) 얼굴인식 기능

* 사용자가 jpg파일을 보내는 경우, 네이버의 오픈 API를 활용한 얼굴인식 기능을 통하여 해당 인물의 이름을 답장한다.

```python
# 웹훅을 통해 정보가 들어올 route
@app.route('/{}'.format(token), methods=['POST'])
def telegram():
    doc = request.get_json() #json으로 파싱
    # request : 요청을 받았을 때 요청을 보낸 사람, 내용 들을 알려준다 . cf. requests : request를 보내준다.
    pp(doc)
    # # 어떤 메세지가 들어오던 '닥쳐'라고 하는 챗봇
    chat_id = doc["message"]["chat"]["id"]

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
```





## II. 회고(Retrospective)

* 챗봇에 이미지를 보낼 때, jpg파일을 보내야 하기 때문에 Telegram Desktop버전으로 보내야 한다.



## III. 보완 계획(Feedback)

* 인식 가능한 이미지 파일의 종류를 다양화하여 mobile에서도 기능을 사용할 수 있도록 개발하고 싶다.
* 선호하는 웹툰(webtoon)의 이름을 작성하면, 해당 웹툰에 들어가 볼 수 있게 하는 기능을 추가적으로 개발하고 싶다.

