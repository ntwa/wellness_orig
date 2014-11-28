#!/usr/bin/env python
import datetime,calendar
import sys,json
from sqlalchemy import create_engine,distinct,func
from sqlalchemy.orm import sessionmaker
from wellness.applogic.activity_module import PhysicalActivity,db



id_delete=[673,671,687]

# create a Session
engine=db
Session = sessionmaker(bind=engine)
session = Session()
for d_id in id_delete:
    res = session.query(PhysicalActivity).filter(PhysicalActivity.id==d_id).first()
    session.delete(res)
    session.commit()


session.close()
engine.dispose()