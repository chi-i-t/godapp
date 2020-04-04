from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

#パスを定義してdbを作成します。
databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'dream.db')
engine = create_engine('sqlite:///' + databese_file, convert_unicode=True)

#データベースにアクセスするためにセッションを作成します。
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))

#Baseオブジェクトを作った後、query_property()を使ってBaseオブジェクトに検索クエリを持たせます。
#後でデータベースから検索する時に楽
Base = declarative_base()
Base.query = db_session.query_property()

 #データベースの初期化用です。初期化したいときに呼びます。
def init_db():
    import models.models
    Base.metadata.create_all(bind=engine)