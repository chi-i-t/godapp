#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template,request
# models.pyで定義したクラスをインポート
from models.models import Dream
# db_session.add(content)関数にmodelsオブジェクト（Dream）を引数として渡すため
from models.database import db_session
# Dreamオブジェクトを生成する際にタイムスタンプが必要になるため、datetime.now()を使えるようにする
from datetime import datetime


#Flaskオブジェクトの生成
app = Flask(__name__)


#「/」と「/index」へアクセスがあった場合に、「index.html」を返す
@app.route("/")
@app.route("/index")
def index():
    #クエリストリングからname属性の値を受け取る
    name = request.args.get("name")
    # .query.all()でテーブル内のデータを全件取得
    all_dream = Dream.query.all()
    #index.htmlに情報を送ってWebページを表示させる
    return render_template("index.html",name=name,all_dream=all_dream)


@app.route("/index",methods=["post"])
def post():
    name = request.form["name"]
    all_dream = Dream.query.all()
    return render_template("index.html",name=name,all_dream=all_dream)


# フォームのaction属性で指定した「/add」でルーティングを追加
@app.route("/add",methods=["post"])
def add():
    title = request.form["title"]
    body = request.form["body"]
    content = Dream(title,body,datetime.now())
    db_session.add(content)
    db_session.commit()
    return index()

# フォームのaction属性で指定した「/update」でルーティングを追加
@app.route("/update",methods=["post"])
def update():
    # 変更をかけるレコードを.query.filter_by(id=request.form["update"])で絞り込む
    content = Dream.query.filter_by(id=request.form["update"]).first()
    content.title = request.form["title"]
    content.body = request.form["body"]
    db_session.commit()
    return index()

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
    return index()


#app.pyをターミナルから直接呼び出した時だけ、app.run()を実行する
if __name__ == "__main__":
    app.run(debug=True)
