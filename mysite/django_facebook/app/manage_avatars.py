#!/usr/bin/env python
import datetime,calendar
import sys,json
from sqlalchemy import create_engine,distinct,func,asc
from sqlalchemy.orm import sessionmaker
from wellness.applogic.avatar_module import Avatars,UserAvatars,db,dbconn
from retrieve_intermediary import RetrieveIntermediary
from collections import OrderedDict
from random import randint


class ManageAvatars:
     def __init__(self,myjson):
          self.myjson=myjson
          
     def getAllAvatars(self):
          result={}
          
          try:
               #now fetch url
               engine=db
               data={}
               counter=0
               #create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               res=session.query(Avatars).all()
               for avatar in res:
                    if counter<10:
                         Key1="R0"
                    else:
                         Key1="R"
                    data["D0"]=avatar.id  
                    data["D1"]=avatar.avatar_url
                    result["%s%s"%(Key1,counter)]=OrderedDict(sorted(data.items(), key=lambda t: t[0]))
                    counter=counter+1
               
               

                    
             
          except Exception as e:
               result["R00"]={"D0":"%s"%e,"D1":-1}
               
               session.close()
               engine.dispose()
               return (json.JSONEncoder().encode(result))
          
          session.close()
          engine.dispose()
          return (json.JSONEncoder().encode(result))
          
     
     def getAvatarUrl(self):
          result={}
          try:
               
               intermediary_id=self.myjson["IntermediaryId"]
          except Exception as e:
               result["D0"]="%s"%e
               result["D1"]=-1
               return (json.JSONEncoder().encode(result))
          
          
             
          try:
               #now fetch url
               engine=db
               #create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               res=session.query(Avatars,UserAvatars).filter(Avatars.id==UserAvatars.avatar_id).filter(UserAvatars.intermediary_id==intermediary_id).first()
               
               if res is None:
                
                    result["AvatarId"]=0
                    result["AvatarUrl"]="http://ict4d01.cs.uct.ac.za/static/django_facebook/images/avatars/default.jpeg"
               else:
                    avatar,useravatar=res
                    result["AvatarUrl"]=avatar.avatar_url
                    result["AvatarId"]=avatar.id
                    
             
          except Exception as e:
               result["AvatarUrl"]="%s"%e
               result["AvatarId"]=-1
               session.close()
               engine.dispose()
               return (json.JSONEncoder().encode(result))
          
          session.close()
          engine.dispose()
          return (json.JSONEncoder().encode(result))

     def setAvatar(self):
          result={}
          
          try:
               
               intermediary_id=self.myjson["IntermediaryId"]
               avatar_id=self.myjson["AvatarId"]
          except Exception as e:
               result["D0"]="%s"%e
               result["D1"]=-1
               return (json.JSONEncoder().encode(result))
          
          
          try:
               #now fetch url
               engine=db
               #create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               res=session.query(Avatars,UserAvatars).filter(Avatars.id==UserAvatars.avatar_id).filter(UserAvatars.intermediary_id==intermediary_id).first()
               
               if res is None:
                    allow_insert=1
               else:
                    #update
                    avatar, useravatar=res
                    allow_insert=0
                    useravatar.avatar_id=avatar_id
                    session.commit()

                    
             
          except Exception as e:
               result["D0"]=">>%s"%e
               result["D1"]=-1
               session.close()
               engine.dispose()
               return (json.JSONEncoder().encode(result))
          
          if allow_insert:
               try:
                    new_user_avatar=UserAvatars(intermediary_id,avatar_id)
                    session.add(new_user_avatar)
                    session.commit()   
    
               except Exception as e:
                    result["D0"]="%s"%e
                    result["D1"]=-1
                    session.close()
                    engine.dispose()
                    return (json.JSONEncoder().encode(result))
               
               
          result["D0"]="Avatar updated successfully"
          result["D1"]=1     
               
          session.close()
          engine.dispose()
          
          
          return (json.JSONEncoder().encode(result))    
                    
                    
          
          
     
     def removeAvatar(self):
     
          result={}
          try:
               
               intermediary_id=self.myjson["IntermediaryId"]
          except Exception as e:
               result["D0"]="%s"%e
               result["D1"]=-1
               return (json.JSONEncoder().encode(result))
          
          
          
          try:
               #now fetch url
               engine=db
               #create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               res=session.query(Avatars,UserAvatars).filter(Avatars.id==UserAvatars.avatar_id).filter(UserAvatars.intermediary_id==intermediary_id).first()
               
               if res is None:
                    result["D0"]="The record you attempted to delete deosn't exist"
                    result["D1"]=2
               else:
                    avatar,useravatar=res
                    session.delete(useravatar)
                    session.commit()
                    result["D0"]="The record was deleted successfully"
                    result["D1"]=1
                    session.close()
                    engine.dispose()
                    
             
          except Exception as e:
               result["D0"]="%s"%e
               result["D1"]=-1
               session.close()
               engine.dispose()
               return (json.JSONEncoder().encode(result))   
          
          
          return (json.JSONEncoder().encode(result))
          
          
#myjson={"IntermediaryId":'ntwakatule',"AvatarId":'6'}
#obj=ManageAvatars(myjson)
#result=obj.getAllAvatars()
#print result

     
    
