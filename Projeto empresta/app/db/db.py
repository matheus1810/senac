from config.Config import settings


from sqlmodel import create_engine,Session

url = f"mysql+pymysql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

engine = create_engine(url)

    
def get_db():
        with Session(engine) as session:
            yield session
