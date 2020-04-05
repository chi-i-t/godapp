#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template,request,session,redirect,url_for
# models.pyで定義したクラスをインポート
from models.models import Dream,User
# db_session.add(content)関数にmodelsオブジェクト（Dream）を引数として渡すため
from models.database import db_session
# Dreamオブジェクトを生成する際にタイムスタンプが必要になるため、datetime.now()を使えるようにする
from datetime import datetime
# ログインにて必要
from app import key
from hashlib import sha256


#Flaskオブジェクトの生成
app = Flask(__name__)

# 暗号化キーを定義(ユーザのなりすまし防止）
app.secret_key = key.SECRET_KEY


#「/」と「/index」へアクセスがあった場合に、「index.html」を返す
@app.route("/")
@app.route("/index")
def index():
    # セッション情報にユーザ名が入っているか判定
    if "user_name" in session:
        name = session["user_name"]
        # .query.all()でテーブル内のデータを全件取得
        all_dream = Dream.query.all()
        #index.htmlに情報を送ってWebページを表示させる
        return render_template("index.html",name=name,all_dream=all_dream)
    else:
        # 非ログインユーザなので、ログイン画面にリダイレクト
        return redirect(url_for("top"))


# フォームのaction属性で指定した「/add」でルーティングを追加
@app.route("/add",methods=["post"])
def add():
    title = request.form["title"]
    body = request.form["body"]
    content = Dream(title,body,datetime.now())
    db_session.add(content)
    db_session.commit()
    return redirect(url_for("index"))


# フォームのaction属性で指定した「/update」でルーティングを追加
@app.route("/update",methods=["post"])
def update():
    # 変更をかけるレコードを.query.filter_by(id=request.form["update"])で絞り込む
    content = Dream.query.filter_by(id=request.form["update"]).first()
    content.title = request.form["title"]
    content.body = request.form["body"]
    db_session.commit()
    return redirect(url_for("index"))


# フォームのaction属性で指定した「/delete」でルーティングを追加
@app.route("/delete",methods=["post"])
def delete():
    id_list = request.form.getlist("delete")
    # request.form.getlist("delete")で受け取ったid_listに対してor文を回して１件ずつ削除
    for id in id_list:
        content = Dream.query.filter_by(id=id).first()
        # modelsオブジェクトDream（=content）をdb_session.delete()関数の引数に渡す
        db_session.delete(content)
    db_session.commit()
    return redirect(url_for("index"))


@app.route("/top")
def top():
    status = request.args.get("status")
    return render_template("top.html",status=status)


@app.route("/login",methods=["post"])
def login():
    # フォームに入力されたユーザ名を取得し、
    user_name = request.form["user_name"]
    # そのユーザ名を持つDBレコードをusersテーブルから抽出
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        # もしDBレコードがあった場合、フォームに入力されたパスワードを取得してハッシュ化（sha256という暗号化方式を使用）
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        # DBレコードのハッシュ化パスワードと一致するか判定
        if user.hashed_password == hashed_password:
            # 一致した場合、セッション情報にユーザ名を追加して/indexにリダイレクト
            session["user_name"] = user_name
            return redirect(url_for("index"))
        else:
            return redirect(url_for("top",status="wrong_password"))
    else:
        return redirect(url_for("top",status="user_notfound"))


@app.route("/newcomer")
def newcomer():
    status = request.args.get("status")
    return render_template("newcomer.html",status=status)


@app.route("/registar",methods=["post"])
def registar():
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        # もしDBレコードがあった場合、/newcomer?status=exist_userにリダイレクト
        return redirect(url_for("newcomer",status="exist_user"))
    else:
        # DBレコードが無かった場合、パスワードのハッシュ化を行い、
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        # usersテーブルへのDBレコード追加
        user = User(user_name, hashed_password)
        db_session.add(user)
        db_session.commit()
        # セッション情報にユーザ名を埋め込んで
        session["user_name"] = user_name
        # /indexにリダイレクト
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("user_name", None)
    return redirect(url_for("top",status="logout"))


#app.pyをターミナルから直接呼び出した時だけ、app.run()を実行する.
# app.pyを実行した状態でファイルを開いて中身を書き換えるとその内容が反映されるので、コードを変えて上書きしてその結果を確認しつつ作業したいときに便利
if __name__ == "__main__":
    app.run(debug=True)
