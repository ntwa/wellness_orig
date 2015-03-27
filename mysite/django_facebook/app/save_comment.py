#!/usr/bin/env python
import datetime,time,calendar
import sys,json
#sys.path.insert(0, 'C:\\workspace\\test\\helloword\\sqlalchemy.zip')
#sys.path.insert(0, 'sqlalchemy.zip')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.intermediary_module import Intermediary,Beneficiary,Comment,db,dbconn
from save_sms_feedback import QueueFeedback
from collections import OrderedDict
from manage_avatars import ManageAvatars


class SaveComment:
     def __init__(self,myjson,b_id,i_id):
          self.myjson=myjson
          self.b_id=b_id
          self.i_id=i_id
     def first_day_of_month(self,d):
          return datetime.date(d.year, d.month, 1)
      
     def last_day_of_month(self,d):
          t=(calendar.monthrange(d.year,d.month))
          return datetime.date(d.year,d.month,t[1])

     def getComments(self,event_type):
      result={}


      try:

        engine=db
                    # create a Session
        Session = sessionmaker(bind=engine)
                    
        session = Session()

        res=session.query(Comment,Beneficiary).filter(Beneficiary.id==Comment.beneficiary_id).filter(Beneficiary.id==self.b_id).filter(Comment.event_type==event_type).all()

        key2="Q"
        first_posn=0

        if res == []:
          result["P00"]={"Q0":-1,"Q1":"No comments!"}
          return (json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))

        if res is None:
          result["P00"]={"Q0":-1,"Q1":"No comments!"}
          return (json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))
        for comment,beneficiary in res:
          
          if first_posn<10:
            key1="P0"
          else:
            key1="P" 

        
          comment_tuple={}
          second_posn=0
     
          intermediary_id=comment.teamcommented

          #Get the team where the commenter belongs to
          res2=session.query(Beneficiary).filter(Beneficiary.intermediary_id==comment.teamcommented).first()
          if res2 is None:
            result["P00"]={"Q0":-1,"Q1":"No comments!"}
            return (json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))
          else:
            teamcommented=res2.team_name

           
          

          #Find the avatar of the team made the comments

          avatarmyjson={"IntermediaryId":intermediary_id}
          obj=ManageAvatars(avatarmyjson)
          res=obj.getAvatarUrl()
          avatardata=json.loads(res)
          avatarurl=avatardata["AvatarUrl"]

          #the avatar should go first
          comment_tuple[key2+"%s"%second_posn]="%s"%avatarurl
          second_posn=second_posn+1




          # the name should come next
          comment_tuple[key2+"%s"%second_posn]="%s"%teamcommented
          second_posn=second_posn+1



          #comments should be listed last
          comment_tuple[key2+"%s"%second_posn]="%s"%comment.commentdetails
          second_posn=second_posn+1  










          result[key1+"%s"%first_posn]=(OrderedDict(sorted(comment_tuple.items(), key=lambda t: t[0])))
          first_posn=first_posn+1 



        return (json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))
        





      except Exception as e:
        result["P00"]={"Q0":e,"Q1":-1,"Q2":-1}
        return (json.JSONEncoder().encode(result))


     def saveCommentInDB(self):
          
          commentdetails="" 
          date_captured="" 
          time_captured="" 
          event_type=""
          message_sent_status=""
          result={}
          teamname=""
          allow_insert=1
          
          # Get data from fields
          try:
                            
               commentdetails=self.myjson["MessageBody"] 
               date_captured=datetime.date.today()# today's date
               time_captured=time.strftime("%H:%M:%S")
               teamname=self.myjson["TeamName"]
               optionaltext=self.myjson["OptionalText"]
               event_type=self.myjson["EventType"]
               message_sent_status=False          
               

               
                
          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]='There was an error in processing a JSON object:%s'%e
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
          

          if (commentdetails=="None")  and (event_type=="None"):
               #print "Content-type: text/html\n" 
               result["message"]="There is an error in saving your message due to missing of some information"
               return (json.JSONEncoder().encode(result)) 



               
          try:
            if teamname=="None":
              b_id=self.b_id
            else:
              #get beneficiary id of the team that owns an event being commmented
              engine=db
              Session = sessionmaker(bind=engine)
                    
              session = Session()

              res=session.query(Beneficiary).filter(Beneficiary.team_name==teamname).first()
              if res is None:
                result["message"]="The team you are trying to comment doesn't exist"
                return (json.JSONEncoder().encode(result))
              else:
                b_id=res.id






          except Exception as e:
            pass
          if allow_insert==1:           
               try:
                    
                    #print "Content-Type: text/html\n"
                    #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False)
                    engine=db
                    # create a Session
                    Session = sessionmaker(bind=engine)
                    
                    session = Session()
                    
                    # Create food
                    #new_food=FoodAndBeverage('KTLNTW00',datetime.date(1988,12,01))
                    
                    new_comment=Comment(b_id,self.i_id,commentdetails,date_captured,time_captured,event_type,message_sent_status)
                                            
                    
                    
                    session.add(new_comment)
                    
                    
                    # commit the record the database
                    
                    
                    session.commit()




                    if teamname=="None":

                      res=session.query(Intermediary,Beneficiary).filter(Intermediary.intermediary_id==Beneficiary.intermediary_id).filter(Intermediary.intermediary_id==self.i_id).first()
                      if res is None:
                        result["message"]="Error failed to send a message"
                        return (json.JSONEncoder().encode(result))
                      else:
                        interm,ben=res
                        ben_mobile=ben.beneficiary_mobile
                        interm_mobile=interm.mobile
                        feedback_message=commentdetails

                        myjson2={"recipient":ben_mobile,"message":feedback_message}
                        obj=QueueFeedback(myjson2)
                        res=obj.saveFeedbackInDB()
                        
                    
                    else:
                      res=session.query(Intermediary,Beneficiary).filter(Intermediary.intermediary_id==Beneficiary.intermediary_id).filter(Beneficiary.team_name==teamname).first()
                      if res is None:
                        result["message"]="Error: You can't leave a comment to this team since it doesn't exist"
                        return (json.JSONEncoder().encode(result))            
                      else:
                        interm,ben=res
                        interm_mobile=interm.mobile
                        ben_mobile=ben.beneficiary_mobile
                        team_name=ben.team_name
                        feedback_message=optionaltext
                        
                        myjson2={"recipient":interm_mobile,"message":feedback_message}
                        obj=QueueFeedback(myjson2)
                        res=obj.saveFeedbackInDB()
                       
                        myjson2={"recipient":ben_mobile,"message":feedback_message}
                        obj=QueueFeedback(myjson2)
                        res=obj.saveFeedbackInDB()


                    session.close()
                    engine.dispose()
                    dbconn.close()                 
                     
                    
               except Exception as e:
                    session.close()
                    engine.dispose()
                    dbconn.close()

                    result["message"]=e
                    return (json.JSONEncoder().encode(result)) 
               
               result["message"]="Your comment has been added. Also the message has been sent to team %s to notify them of your new comment"%team_name;
               return (json.JSONEncoder().encode(result))
     
     
#myjson={"MessageBody":"Hi mom. You have reached your activity goal this week. Keep it up!!","EventType":"Aquarium", "TeamName":"None","OptionalText":"Team y has left a comment in you aquarium"}
#obj=SaveComment(myjson,2,'pacomeambasa')
#msg=obj.saveCommentInDB()
#msg=obj.getComments("Aquarium")
#print msg
