#!/usr/bin/env python
import datetime,calendar
import sys,json
from sqlalchemy import create_engine,distinct,func,asc
from sqlalchemy.orm import sessionmaker
from wellness.applogic.sound_module import Sound,db,dbconn
from collections import OrderedDict
import os

        

class RetrieveSound:
    def __init__(self,sound_id):
         self.sound_id=sound_id
    
    def retrieveSoundUrl(self):
         result={}         
         try:
              engine=db
              #create a Session
              Session = sessionmaker(bind=engine)
              session = Session()

         
              res= session.query(Sound).filter(Sound.id==self.sound_id).first()
              result["url"]=res.url
              #result["url"]=res
              session.close()
              engine.dispose()
              dbconn.close()
                   
              return (json.JSONEncoder().encode(result))                   
                                  
         except Exception as e:
                        
              #print "Content-type: text/html\n" 
              session.close()
              engine.dispose() 
              dbconn.close()
                                
              result["message"]="Error: %s"%e
              print "Exception thrown in function retrieveSoundUrl(): %s"%e
              return (json.JSONEncoder().encode(result))
