from config.Config import settings


from sqlmodel import create_engine,Session

from sqlalchemy import URL

url = URL.create("mysql+pymysql", username=settings.db_user, password=settings.db_password,
                 host=settings.db_host, port=settings.db_port, database=settings.db_name)

engine = create_engine(url)

    
def get_db():
        with Session(engine) as session:
            yield session
