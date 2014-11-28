#!/usr/bin/env python
import datetime
import sys,json
#sys.path.insert(0, 'C:\\workspace\\test\\helloword\\sqlalchemy.zip')
#sys.path.insert(0, 'sqlalchemy.zip')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.fbposts_module import ObjectActivity,db,dbconn
from random import randint
#import urllib2
import sys,json

class FacebookNotification:
     def __init__(self,myjson,b_id):
          self.myjson=myjson
          self.b_id=b_id
     def queueNotification(self):

          event_url=""
          event_object=""
        
          object_owner=""
      
          event_type=""
          allow_insert=1

          result={}
               
          
          # Get data from fields
          try:
               event_url=self.myjson["EventUrl"]
               event_object=self.myjson["EventObject"]
               object_owner=self.myjson["ObjectOwner"]
               date_of_display=self.myjson["DateDisplayed"]# An object can either be an aquarium or a score garden. 
               if event_object=="Aquarium":
                    event_object="Fitness Aquarium/Fish Tank"
                    pic="http://ict4d01.cs.uct.ac.za/static/django_facebook/images/aqua%s.jpeg"%randint(1,6)
               elif event_object=="Garden":
                    pic="http://ict4d01.cs.uct.ac.za/static/django_facebook/images/gard%s.jpeg"%randint(1,6)
          except Exception:
               #print "Content-type: text/html\n" 
               result["message"]='There was an error in processing a JSON object'
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
      
          #check if the event already exists
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()

               # querying for a record in the physical_activity pattern table
               res= session.query(ObjectActivity).filter(ObjectActivity.event_url==event_url).filter(ObjectActivity.event_type=="Like").first()
               if res is None:
                    
                    message="Likes received on a %s  dated %s"%(event_object,date_of_display)

                    new_message=ObjectActivity(message,event_url,event_object,object_owner,"Like",date_of_display,pic,"Notification","What others think of the progess","Progress in Helping your Family Member",0,0)


                    session.add(new_message)


                    # commit the record the database


                    session.commit()
                    



               res= session.query(ObjectActivity).filter(ObjectActivity.event_url==event_url).filter(ObjectActivity.event_type=="Post").first()
               if res is None:
                    
                    message="Comments received on a %s  dated %s"%(event_object,date_of_display)

                    new_message=ObjectActivity(message,event_url,event_object,object_owner,"Post",date_of_display,pic,"Notification","What others think of the progess","Progress in Helping your Family Member",0,0)


                    session.add(new_message)


                    # commit the record the database


                    session.commit()
                    
               res= session.query(ObjectActivity).filter(ObjectActivity.event_url==event_url).filter(ObjectActivity.event_type=="Views").first()
               if res is None:


                    message="Views received on a %s  dated %s"%(event_object,date_of_display)
                    new_message=ObjectActivity(message,event_url,event_object,object_owner,"Views",date_of_display,pic,"Notification","What others think of the progess","Progress in Helping your Family Member",1,1)


                    session.add(new_message)

                     #errorcode["message"]="gfgfgfg"
                    #status=json.JSONEncoder().encode(errorcode) 


                    # commit the record the database


                    session.commit()
                    


               else:
                   viewcounter=res.counter
                   viewcounter=viewcounter+1
                   res.counter=viewcounter
                   session.commit()                    



               session.close()
               engine.dispose()
               dbconn.close()
               

               result["R00"]={"F1":1,"F0":"The post was captured sucessfully"}
               return (json.JSONEncoder().encode(result))




          except Exception as e:
               session.close()
               engine.dispose()
               dbconn.close()
    
               #print "Content-type: text/html\n" 

               result["message"]="Error: %s"%e
               #print      
               return (json.JSONEncoder().encode(result))
          
           
               


         

   

#myjson={"EventObject":"Aquarium","EventUrl":"http://ict4d01.cs.uct.ac.za/","DateDisplayed":"22nd September","ObjectOwner":"8"}


#obj=FacebookNotification(myjson,8)
#msg=obj.queueNotification()
#print msg

