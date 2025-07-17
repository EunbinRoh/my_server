from flask import Flask

# html문서를 load!
# 단, templates 폴더에 있는 html만 바라볼 수 있다
from flask import render_template # html문서를 load!
from flask import request, redirect, make_response
from aws import detect_labels_local_file as label
from aws import compare_faces 
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 서버주소/ 주소하나에 함수하나 매핑
# /로 들어오면 reuturn html 문서
@app.route("/")
def index():
    return render_template("home.html")

@app.route("/detect", methods=["POST"])
def detect():
    try:
        if request.method == "POST":
            f = request.files["file"]
            
            # 서버에 클라이언트가 보낸 이미지를 저장
            filename = secure_filename(f.filename)
            f.save("static/" + filename)
            r = label("static/" + filename)
            #  외부에서 온 이미지, 파일 등을 마음대로 저장할 수 없음

            return r
            
    except:  
        return "감지 실패"
    
    return "객체 탐지 페이지"

@app.route("/compare", methods=["POST"])
def compare():
    try:
        if request.method == "POST":
            f1 = request.files["file1"]
            f2 = request.files["file2"]
            
            # 서버에 클라이언트가 보낸 이미지를 저장
            f1_filename = secure_filename(f1.filename)
            f2_filename = secure_filename(f2.filename)

            f1.save("static/" + f1_filename)
            f2.save("static/" + f2_filename)
            r = compare_faces("static/" + f1_filename, "static/" + f2_filename)
            #  외부에서 온 이미지, 파일 등을 마음대로 저장할 수 없음

            return r
    except:  
        return "얼굴 비교 실패"
    
    return "얼굴 비교 페이지"

@app.route("/mbti", methods =["POST"])
def mbti():
    try:
        if request.method == "POST":
            mbti = request.form["mbti"]

            return f"당신의 MBTI는 {mbti}입니다"
    except:
        return "데이터 수신 실패"

@app.route("/login", methods = ["GET"])
def login():
    try :
        if request.method == "GET":
            login_id = request.args["login_id"]
            login_pw = request.args["login_pw"]

            if (login_id == "roheunbin") and (login_pw == "1234") :

                response = make_response(redirect("/login/success"))
                response.set_cookie("user", login_id)

                return response
            
            else:
                return redirect("/")

    except : 
        return "로그인 실패"

@app.route("/login/success", methods=["GET"])
def login_success():

    login_id = request. cookies.get("user")
    return f"{login_id}님 환영합니다"


if __name__== "__main__":
    # 1. host (loclahost = 127.0.0.1)
    # 2. port
    app.run(host="0.0.0.0")


