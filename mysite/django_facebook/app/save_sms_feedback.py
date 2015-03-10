#!/usr/bin/env python
import datetime
import sys,json
#sys.path.insert(0, 'C:\\workspace\\test\\helloword\\sqlalchemy.zip')
#sys.path.insert(0, 'sqlalchemy.zip')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.sms_feedback_module import Feedback,db,dbconn
from collections import OrderedDict


class QueueFeedback:
     def __init__(self,myjson):
          self.myjson=myjson
          

     def saveFeedbackInDB(self):
          
          
          result={}
          allow_insert=1
          # Get data from fields
          try:
          
               message=self.myjson["message"] 
               recipient=self.myjson["recipient"]
               #url=self.myjson["url"]
               #pic=self.myjson["pic"]
               #name=self.myjson["name"]
               #caption=self.myjson["caption"]
               #description=self.myjson["description"]
               
               e="Error"
                        
                             
          except Exception as e:
               messages_tuples={}
               messages_tuple={}
     
               key1="R"
               key2="F"
               first_posn=0
               second_posn=0
               messages_tuple[key2+"%d"%second_posn]=e
               second_posn=second_posn+1
                                                                                                                                                                             
                                                                                                                                                                           
               messages_tuple[key2+"%d"%second_posn]=-1
               second_posn=0 
               if first_posn<10:
                    key1="R0"
               else:
                    key1="R"
                                                                                                                                            
               messages_tuples[key1+"%d"%first_posn]=messages_tuple
                                                                                                                                          
               first_posn=first_posn+1
               messages_tuple={}
               return(json.JSONEncoder().encode(OrderedDict(sorted(messages_tuples.items(), key=lambda t: t[0]))))
          
                                        
                         
                         

          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
          
               new_feedback=Feedback(recipient,message)
                    
               session.add(new_feedback)
          
          
               # commit the record the database
          
          
               session.commit()
               result["message"]="The post was recorded successfully"
               
          except Exception as e:
               session.close()
               engine.dispose()
               result["message"]=e
               return (json.JSONEncoder().encode(result)) 
          
          session.close()
          engine.dispose() 
          print "Message queue"
          return (json.JSONEncoder().encode(result))
 
#myjson={"message":"Hello","url":"no url","pic":"no pic","name":"no name","caption":"no caption","description":"description"}
#obj=QueuePosts(myjson)
#result=obj.savePostsInDB()
#print result
