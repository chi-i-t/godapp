#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template,request

#Flaskオブジェクトの生成
app = Flask(__name__)


#「/」と「/index」へアクセスがあった場合に、「index.html」を返す
@app.route("/")
@app.route("/index")
def index():
    #クエリストリングからname属性の値を受け取る
    name = request.args.get("name")
    spell = ["あああ","いいい","ううう"]
    #index.htmlにnameの情報を送ってWebページを表示させる
    return render_template("index.html",name=name,spell=spell)

@app.route("/index",methods=["post"])
def post():
    name = request.form["name"]
    spell = ["あああ","いいい","ううう"]
    return render_template("index.html",name=name,spell=spell)

#app.pyをターミナルから直接呼び出した時だけ、app.run()を実行する
if __name__ == "__main__":
    app.run(debug=True)
