from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET']) # methods=['']가 생략되면 get방식
def index():
    return render_template('index.html')
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    
    # # get방식일 때 받는 방법
    # request.args.get('email')
    # request.args.get('password')
    
    #Post방식일 때 받는 방법
    email = request.form.get('email')
    password = request.form.get('password')
    
    # return render_template('signup.html', email)
    
    adminEmail = "qwer@qwer.com"
    adminPassword = "12341234"
    
    # # 만약에 회원가입한 회원이 admin일 경우
    # #   "관리자님 환영합니다."
    # # 아닐경우,
    # #   "꺼지셈"
    # msg = ""
    
    # if email==adminEmail and password==adminPassword:
    #     msg = "관리자님 환영합니다."
    # else:
    #     msg = "꺼지셈"
    # return render_template('signup.html', msg=msg)
    
    # 만약에 회원가입한 회원이 admin일 경우
    #   "관리자님 환영합니다."
    # 아닐경우,
    #   만약에 아이디만 맞는 경우는
    #       "관리자님 비번이 틀렸어요, 좀만 더 생각해보세요"
    #   아이디도 틀릴 경우는
    #       "꺼지셈"
    if email==adminEmail and password==adminPassword:
        msg = "관리자님 환영합니다."
    # elif email == adminEmail and password!=adminPassword:
    #     msg = "관리자님 비번이 틀렸어요, 좀만 더 생각해보세요"
    # else:
    #     msg = "꺼지셈"
    else:
        if email==adminEmail:
            msg = "관리자님 비번이 틀렸어요, 좀만 더 생각해보세요"
        else:
            msg = "꺼지셈"
    return render_template('signup.html', msg=msg)