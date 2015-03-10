from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.avatar_module import Avatars, db, dbconn

engine=db
#create a Session
Session = sessionmaker(bind=engine)
session = Session()

for x in range(1,81):
    
    url="http://ict4d01.cs.uct.ac.za/static/django_facebook/images/avatars/cartoon%s.jpeg"%x
    new_avatar=Avatars(url)
                         
    session.add(new_avatar)
    session.commit()

    
session.close()
engine.dispose()
dbconn.close()
    
