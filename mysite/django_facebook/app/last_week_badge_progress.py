#This script runs every monday morning
#!/usr/bin/env python
import datetime,calendar
import sys,json
from sqlalchemy import create_engine,distinct,func,asc
from sqlalchemy.orm import sessionmaker
from wellness.applogic.points_module import Points,db
from wellness.applogic.badges_module import Badges,AttainedUserBadges
from retrieve_intermediary import RetrieveIntermediary
from wellness.applogic.intermediary_module import Intermediary
from collections import OrderedDict
from save_factors import ManageFactors
from save_sms_feedback import QueueFeedback
import os
from wellness.applogic.activity_module import PhysicalActivity,dbconn
#from wellness.applogic.intermediary_module import Beneficiary
from random import randint


def bubblesort(A,X,Y,Z,U,V,W,L,M,B,C):
  
  for i in range( len( A ) ):
    for k in range( len( A ) - 1, i, -1 ):
      if ( A[k]> A[k - 1] ):
        swap( A, k, k - 1 )
        swap(X, k, k - 1 )
        swap(Y, k, k - 1 )
        swap(Z, k, k - 1 )
        swap(U, k, k - 1 )
        swap(V, k, k - 1 )
        swap(W, k, k - 1 )
        swap(L, k, k - 1 )
        swap(M, k, k - 1 )
        swap(B, k, k - 1 )
        swap(C, k, k - 1 )
  return A
 
def swap( A, x, y ):
  tmp = A[x]
  A[x] = A[y]
  A[y] = tmp
  

class RetrievePoints:
    def __init__(self,myjson,intermediary_id,last_date_specified):
         self.myjson=myjson
         self.intermediary_id=intermediary_id
         self.last_date_specified=last_date_specified
   
    def first_day_of_month(self,d):
       return datetime.date(d.year, d.month, 1)
    def last_day_of_month(self,d):
       t=(calendar.monthrange(d.year,d.month))
       return datetime.date(d.year,d.month,t[1])

    #get weekly steps
    def getSteps(self,beneficiary_id):
        

        try:
            engine=db
            #create a Session
            Session = sessionmaker(bind=engine)
            session = Session()

            currentdate=datetime.date.today()
            
            #get the date for the first day of this week
            day_of_week=currentdate.weekday()
            week_start_date=currentdate-datetime.timedelta(days=day_of_week)            
            
          
            
 
            res=session.query(func.sum(PhysicalActivity.stepscounter).label("sum_steps")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).filter(PhysicalActivity.datecaptured>=week_start_date).filter(PhysicalActivity.datecaptured<=currentdate).first()
            
            
            if res.sum_steps==None:
                sum_steps=0
            else:
                sum_steps=int(res.sum_steps)
            result={}
            result["steps"]=sum_steps
     

        except Exception as e:
            print "Exception thrown in function getSteps(): %s"%e 
            result["steps"]=0
            result["dates_counter"]=1
        
        
        #self.steps=sum_steps
        session.close()
        engine.dispose()
        dbconn.close()

        return (json.JSONEncoder().encode(result))





       
    
    def retrieveIntermediaryClickPoints(self):
         result={}       
         try:
              #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
              engine=db
              # create a Session
              Session = sessionmaker(bind=engine)
              session = Session()
                                  

              #if self.last_date_specified==1:
              #    day=self.myjson["Day"]
              #    if day=="Today":
              #       day=datetime.date.today()
                           
              #res= session.query(func.sum(Points.scoredpoints).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).filter(Points.datecaptured<=day).first()
              #get points by number of days an application has been used.
              #res=session.query(func.count(distinct(Points.datecaptured)).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).filter(Points.datecaptured<=day).first()
              #else:
                  #res= session.query(func.sum(Points.scoredpoints).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).first()
              res=session.query(func.count(distinct(Points.datecaptured)).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).first()


              
              retrieved_points_sum=0# initialize how many distinct dates are in the database
              #for retrieved_points_sum in res:
              #     break               
              
              
              if res.sum_points is None:
                   
                   retrieved_points_sum="0"
                   result["message"]="You have no points"
                   result["points"]=int(retrieved_points_sum)
              else: 
                   result["message"]="You have some points so far."
                   retrieved_points_sum=int(res.sum_points)
                   result["points"]=int(retrieved_points_sum)
 

            





 
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
              print "Exception thrown in function getIntermediaryClickPoints(): %s"%e
              print "The day captured=%s"%day
              return (json.JSONEncoder().encode(result))
              #sys.exit()    
              


    def assignBadges(self):
        result={}
        try:
            
             day=self.myjson["Day"]
                                 
        except Exception as e:
             #print "Content-type: text/html\n" 
             result["message"]="Error%s"%e.message
             return (json.JSONEncoder().encode(result))

        
        if day is not None:
            #if day=="Today":
            #    today_date=datetime.date.today()
            #    date_str="%s"%today_date 
            #else:
            date_str="%s"%day
        else:
             result["message"]="Error: The option '%s' is invalid"%day
             return (json.JSONEncoder().encode(result))
             
             
        try:
          
          myjson={'Fname':'Dummy','Lname':'Dummy','Username':'dummy'}
          obj=RetrieveIntermediary(myjson)
          res=obj.retrieveIntermediaryInDB()
          
          intermediaries_tuple=json.loads(res)
          intermediaries_emails=[]
          intermediary_names=[]
          orig_emails=[]
          beneficiary_ids=[]
          beneficiary_names=[]
          intermediary_mobiles=[]
          beneficiary_relations=[]
          posn=0
          gardens=[]
          competitors_counter=0
          
          garden_label=date_str.replace("-","_")   
          first_posn=0
          second_posn=0
  
          key2="D"    
          tree_array=[]
          flower_array=[]
          total_plants=[]
          urls=[]
          usage_points=[]
          bonus_points=[]
          badges=[]
          badges_urls=[]
          
          currentdate=datetime.datetime.today()
          #get the date for the first day of this week
          day_of_week=currentdate.weekday()
          week_start_date=currentdate-datetime.timedelta(days=day_of_week)   
         
          #get the first and end date of last week
          previous_week_end_date=week_start_date-datetime.timedelta(days=1) #go to last sunday
          previous_week_start_date=previous_week_end_date-datetime.timedelta(days=6)#go to last monday
          
          
          #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
          engine=db
          # create a Session
          Session = sessionmaker(bind=engine)
          session = Session()
          
          res2=session.query(AttainedUserBadges,Badges,Intermediary).filter(Intermediary.intermediary_id==AttainedUserBadges.intermediary_id).filter(AttainedUserBadges.status==1).filter(AttainedUserBadges.badge_id==Badges.rank).filter(AttainedUserBadges.date_attained>=previous_week_start_date).filter(AttainedUserBadges.date_attained<=previous_week_end_date).all()
          users_with_progress_str="|"
          
          
          users_with_progress=0
          
          
          for rel1,rel2,rel3 in res2:
            users_with_progress_str=users_with_progress_str+rel3.intermediary_fname
            users_with_progress_str=users_with_progress_str+" "
            #users_with_progress_str=users_with_progress_str+rel3.intermediary_lname
            users_with_progress_str=users_with_progress_str+", Badge:"
            users_with_progress_str=users_with_progress_str+rel2.badgename
            users_with_progress_str=users_with_progress_str+"|"
            users_with_progress=users_with_progress+1
      
           
          for record in intermediaries_tuple.items():
               
               
               key,user =record
              
               if(user["D2"]=="None"):
                   continue
               else:
                    
                   
                    orig_emails.append(user["D1"]) #keep original email addresses
                    orig_email=user["D1"]
               
                    user["D1"]=user["D1"].replace("@","_at_")
                    user["D1"]=user["D1"].replace(".","_dot_")
                    
                    intermediaries_emails.append(user["D1"])
                    intermediary_names.append(user["D0"])
                    beneficiary_names.append(user["D2"][0:user["D2"].index('.')])# get the name only
                    beneficiary_relations.append(user["D3"][(user["D3"].index(':')+1):(len(user["D3"]))])
                    intermediary_mobiles.append(user["D5"][(user["D5"].index(':')+1):(len(user["D5"]))])
                    first_name=intermediary_names[posn][0:(intermediary_names[posn].index(' ')+1)] # 
                    
                    myjson={'Fname':'Dummy','Lname':'Dummy','Username':orig_email}
                    obj=RetrieveIntermediary(myjson)
                    result2=obj.isAssignedBeneficiary()
                    
                    beneficiary_tuple=json.loads(result2)
                    beneficiary_ids.append(beneficiary_tuple["Id"])
                    
                    
                  
                    file_path="django_facebook/images/garden/%s/%s_%s.jpeg"%(intermediaries_emails[posn],beneficiary_ids[posn],garden_label)
                    
                    file_name="%s_%s"%(beneficiary_ids[posn],garden_label)
                    urls.append(file_path)
                    
      
                  
                     
                    varmyjson={'Day':day}
                    
                                     
                    clickPointsObj=RetrievePoints(varmyjson,orig_email,1)
                    resclickpoints=clickPointsObj.retrieveIntermediaryClickPoints()
                    resclickpoints=json.loads(resclickpoints)
                   
                    #clickpoints=int(resclickpoints["points"]/resclickpoints["dates_counter"])
                    clickpoints=int(resclickpoints["points"])
                    if clickpoints>18:
                        clickpoints=18
  
                  
                     
                    usage_points.append(clickpoints)
                   
                    ressteps=clickPointsObj.getSteps(beneficiary_tuple["Id"])
                    ressteps=json.loads(ressteps)
                     
  
                    #stepspoints=int(ressteps["steps"]/(100*ressteps["dates_counter"]))
                    stepspoints=int(ressteps["steps"])
                    if stepspoints>70000:
                        stepspoints=70000
                    
                    bonus_points.append(stepspoints) 
                    
                       
                    
                    trees=int(stepspoints*100/70000)
                    flowers=int(clickpoints*67/18)
                    #print file_name,trees, flowers
                    tree_array.append(trees)
                    flower_array.append(flowers)
                    total=trees+flowers
                    total_plants.append(total)
                    

                   
                    
                    
                    #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
                    #engine=db
                    # create a Session
                    #Session = sessionmaker(bind=engine)
                    #session = Session()
                    
                    #check if there a new badge attained in last week
                    res2=session.query(AttainedUserBadges,Badges).filter(AttainedUserBadges.intermediary_id==orig_email).filter(AttainedUserBadges.status==1).filter(AttainedUserBadges.badge_id==Badges.rank).filter(AttainedUserBadges.date_attained>=previous_week_start_date).filter(AttainedUserBadges.date_attained<=previous_week_end_date).first()
                                      
                    
                    if res2 is None:
                    
                      
                        # select one message out of five messages
                        num=randint(0,4)
                        message_bank=[]
                        if users_with_progress>0: 
                          
                          
                          if users_with_progress>1:
          
                            feedback_message="Hi %s, "%first_name
                            feedback_message=feedback_message+"these are the people who got new badges last week, %s. If you and your %s work harder this week then you can also attain a new higher badge. To progrees on a new badge you need to login to the app every day and motivate your %s to walk more steps in each day"%(users_with_progress_str,beneficiary_relations[posn],beneficiary_relations[posn])
                          else:
                            feedback_message="Hi %s, "%first_name
                            feedback_message=feedback_message+"this is the only person who got a new badge last week, %s. If you and your %s work harder this week then you can also attain a new higher badge. To progrees on a new badge you need to login to the app every day and motivate your %s to walk more steps in each day"%(users_with_progress_str,beneficiary_relations[posn],beneficiary_relations[posn])
                          message_bank.append(feedback_message)
                          # select one message out of six messages NB: There one additional message from this if statement
                          num=randint(0,5)
                        
                        feedback_message="Hey %s "%first_name
                        feedback_message=feedback_message+"your team has not been promoted to a new badge for the past seven days. You and your %s need to work harder to progress to higher badges. You can only obtain higher badges if you keep on using the app everyday and motivate your %s to walk more steps everyday."%(beneficiary_relations[posn],beneficiary_relations[posn])
                        
                        
                        message_bank.append(feedback_message)                     
                        
                        
                        feedback_message="Hallo %s "%first_name
                        feedback_message=feedback_message+"your team has not progressed to a higher badge for a while. This week you have another chance to progress. You and your %s need to work harder to progress to higher badges. You can only obtain higher badges if you keep on using the app everyday and motivate your %s to walk more steps everyday."%(beneficiary_relations[posn],beneficiary_relations[posn])
                        
                        message_bank.append(feedback_message)
                        
                        
                        feedback_message="Molo %s "%first_name
                        feedback_message=feedback_message+" Your team never got any new badge for the all of last week. You and your %s can attain new higher badges if you keep on using the app everyday and motivate your %s to walk more steps everyday. Log on the app now to check your current badge"%(beneficiary_relations[posn],beneficiary_relations[posn])
                        message_bank.append(feedback_message)
                        
                        feedback_message="Kunjani %s ? "%first_name
                        feedback_message=feedback_message+" It is monday again. Last week your badge never changed. It is time your team get a new badge.  Keep on using the app every day and motivate  your %s to walk more steps this week so that your team gets higher badges. Log on the app now to check your progress"%beneficiary_relations[posn]
                        message_bank.append(feedback_message)
                        
                        feedback_message="Heita %s ? "%first_name
                        feedback_message=feedback_message+" Here is another monday, the week begins. You have been on the same badge for too long. It is time for a change. Keep on using the app every day and motivate  your %s to walk more steps this week so that your team gets higher badges. Log on the app now to check your progress"%beneficiary_relations[posn]
                        
                        message_bank.append(feedback_message)
                        
                        print message_bank[num]
                        
                
             
                        
                        myjson2={"recipient":intermediary_mobiles[posn],"message":message_bank[num]}
                        
                        obj=QueueFeedback(myjson2)
                        res=obj.saveFeedbackInDB()
                    else:
                      # select one message out of four messages
                      num=randint(0,3)
                      message_bank=[]
                      if users_with_progress>0: 
                        if users_with_progress>1:
                          feedback_message="Hi %s. "%first_name
                          feedback_message=feedback_message+"you are among the people who scored new badges last week.%s. Here is a another week and you have a chance to progress more.You can only obtain higher badges if you keep on using the app everyday and motivate your %s to walk more steps everyday. Login on the app to check steps walked by %s and increase your chance to score higher badges."%(users_with_progress_str,beneficiary_relations[posn],beneficiary_relations[posn])
                        else:
                          feedback_message="Hi %s,"%first_name
                          feedback_message=feedback_message+"you are the only person to attain a new in the past seven days. Big up for that. Here is a another week and you have a chance to progress more.You can only obtain higher badges if you keep on using the app everyday and motivate your %s to walk more steps everyday. Log on the app now to check your current badge "%beneficiary_relations[posn]
                        # select one message out of four messages
                        num=randint(0,4)
                        
                  
                      feedback_message="Holaa %s, "%first_name
                      feedback_message=feedback_message+" congratulations for achieving a new badge last week. Here is another week. You and your %s have chance to work together to progress to higher badges. You can only obtain higher badges if you keep on using the app everyday and motivate your %s to walk more steps everyday. Log on the app now to check your current badge"%(beneficiary_relations[posn],beneficiary_relations[posn])
                      
                      
                     
                      message_bank.append(feedback_message);
                      
                      
                      feedback_message="Molo %s, "%first_name
                      feedback_message=feedback_message+" big up for getting a new badge last week. It is the begining of a new week. You and your %s can attain higher badges if you keep on using the app everyday and motivate your %s to walk more steps everyday. Log on the app now to check your current badge"%(beneficiary_relations[posn],beneficiary_relations[posn])
                      message_bank.append(feedback_message)
                      
                      feedback_message="Kunjani %s ? "%first_name
                      feedback_message=feedback_message+"Kudos for achieving a new badge in the last week. It is another monday again. Keep on using the app every day and motivate  your %s to walk more steps this week so that your team gets higher badges. Log on the app now to check your progress"%(beneficiary_relations[posn])
                      message_bank.append(feedback_message)
                      
                      feedback_message="Heita %s ? "%first_name
                      feedback_message=feedback_message+"last week you nailed it by geting a new badge. Here is another monday, the week begins. Keep on using the app every day and motivate  your %s to walk more steps this week so that your team gets higher badges. Log on the app now to check your progress"%(beneficiary_relations[posn])
                      
                      
                      message_bank.append(feedback_message)
                      
                      

                      
                      
                      myjson2={"recipient":intermediary_mobiles[posn],"message":message_bank[num]}
                      
                      obj=QueueFeedback(myjson2)
                      res=obj.saveFeedbackInDB()
                      
                      
  
                    
                    '''
                    try:
                      
                      
                      old_badge=""
                        
                      #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
                      engine=db
                      # create a Session
                      Session = sessionmaker(bind=engine)
                      session = Session()
                      res=session.query(Badges).filter(Badges.badgename==badges[posn]).first()
                      
                      if res ==None:
                        rank=0
                      else:
                        old_badge=res.badgename
                        rank=res.rank
                        
                        
                      first_name=intermediary_names[posn][0:(intermediary_names[posn].index(' ')+1)] # 
                      #new_attained_badge
                      #first get the current badge of this
                      res=session.query(AttainedUserBadges).filter(AttainedUserBadges.intermediary_id==orig_email).filter(AttainedUserBadges.status==1).first()
                      if res is None:
                        #first promotion 
                          #insert a new badge into the database
                          new_attained_badge=AttainedUserBadges(orig_email,datetime.date.today(),rank)
                          session.add(new_attained_badge)
                          session.commit()# Commit this transaction
                          #first_name=intermediary_names[posn][0:(intermediary_names[posn].index(' ')+1)] #
                          print "First Promotion"
                          feedback_message="Hey %s "%first_name
                          feedback_message=feedback_message+"your team's first badge is %s . You and your %s need to work harder to progress to higher badges. You can only obtain higher badges if you keep on using the app everyday and motivate your %s to walk more steps everyday."%(badges[posn],beneficiary_relations[posn],beneficiary_relations[posn])
                          
                          myjson2={"recipient":intermediary_mobiles[posn],"message":feedback_message}
                          
                          obj=QueueFeedback(myjson2)
                          res=obj.saveFeedbackInDB()
                      
                      else:
                        #check if the current badge rank is less than the new badge rank
                        if rank<res.badge_id:
                          #promote to new higher badge
                          
                          res.status=0# make the current badge obsolete
                          session.commit()
                          session = Session()#create a new session
                          
                          #insert a new badge into the database
                          new_attained_badge=AttainedUserBadges(orig_email,datetime.date.today(),rank)
                          session.add(new_attained_badge)
                          session.commit()# Commit this transaction
                          print "Promoted to new rank"
                          feedback_message="Hey %s "%first_name
                          feedback_message=feedback_message+"your team has been promoted to a new badge. Your old badge was %s and now your new badge is %. Keep on using your app every day and keep on motivating your %s to walk more steps so that your team can continue to shine."%(old_badge,badges[posn],beneficiary_relations[posn])
                          
                          myjson2={"recipient":intermediary_mobiles[posn],"message":feedback_message}
                          obj=QueueFeedback(myjson2)
                          res=obj.saveFeedbackInDB()
                          print feedback_message
                          
                        else:
                          print "No new promotion"
                          pass# no new promotion
                        
              
                      
                        
                        
                    except Exception as e:
                      print "Exception thrown: %s"%e
                      return -1
                    '''    
                    
                        
  
                   
                    posn=posn+1
        except Exception as e:
          print "Exception thrown %s "%e 
          return -1
              
                
                  
        return 1         
      
         

              
     
     
     


highest_points=0
team=""
score_date=datetime.date.today()-datetime.timedelta(days=1)
score_date_str="%s"%score_date.strftime("%d/%m/%Y")
score_date_str2="%s"%score_date.strftime("%Y-%m-%d")
recommendation=""
url="0"
leaders_counter=0
team=[]
top_points=[]
level=[]
badge=[]
recommendations=[]

myjson={'Day':score_date_str2}
obj=RetrievePoints(myjson,'katulentwa@gmail.com',0)
result=obj.assignBadges()

if result==1:
  print "The progress has been scheduled"
else:
  print "The schedule of progress failed to complete"

