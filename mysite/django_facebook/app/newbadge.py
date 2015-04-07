#!/usr/bin/env python
#This script runs every evening at 8 PM
import datetime,calendar
import sys,json
from sqlalchemy import create_engine,distinct,func,asc
from sqlalchemy.orm import sessionmaker
from wellness.applogic.points_module import Points,db
from wellness.applogic.badges_module import Badges,AttainedUserBadges
from retrieve_intermediary import RetrieveIntermediary
from collections import OrderedDict
from save_factors import ManageFactors
from save_sms_feedback import QueueFeedback
import os
from wellness.applogic.activity_module import PhysicalActivity,dbconn
#from wellness.applogic.intermediary_module import Beneficiary
from random import randint
from wellness.applogic.pilot_start import PilotCommencement

 

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

    #get average steps
    def getSteps(self,beneficiary_id):
        

        try:
            engine=db
            #create a Session
            Session = sessionmaker(bind=engine)
            session = Session()
            pilotdateres=session.query(PilotCommencement).first()

            if pilotdateres is None:
                sys.exit
            else:
                datestarted=pilotdateres.datestarted


            if self.last_date_specified==1:
                day=self.myjson["Day"]
            
                res=session.query(func.sum(PhysicalActivity.stepscounter).label("sum_steps")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).filter(PhysicalActivity.datecaptured>=datestarted).filter(PhysicalActivity.datecaptured<=day).first()
         
            else:
 
                res=session.query(func.sum(PhysicalActivity.stepscounter).label("sum_steps")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).first()
            
            if res.sum_steps==None:
                sum_steps=0
            else:
                sum_steps=int(res.sum_steps)
            result={}
            result["steps"]=sum_steps
            
            if self.last_date_specified==1:
                res=session.query(func.min(PhysicalActivity.datecaptured).label("min_date")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).filter(PhysicalActivity.datecaptured<=day).filter(PhysicalActivity.datecaptured>=datestarted).first()
            else: 
                res=session.query(func.min(PhysicalActivity.datecaptured).label("min_date")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).filter(PhysicalActivity.datecaptured>=datestarted).first()
            
            min_date=res.min_date 

            

            if self.last_date_specified==1:
                max_date=self.myjson["Day"]
           
                max_date=datetime.datetime.strptime(max_date , '%Y-%m-%d').date()
            else:
                max_date=datetime.date.today()

            
            if min_date is None:
                dates_difference=1
            else:
                delta=max_date-min_date
                dates_difference=delta.days+1
                if min_date>max_date:
                    dates_difference=1
        
            result["dates_counter"]=dates_difference
        

        except Exception as e:
            print "Exception thrown in function getSteps(): %s"%e 
            result["steps"]=0
            result["dates_counter"]=1
          
        
        #self.steps=sum_steps
        session.close()
        engine.dispose()
        dbconn.close()
        result["steps"]=result["steps"]/result["dates_counter"]

        return (json.JSONEncoder().encode(result))
        

       
    
    def retrieveIntermediaryClickPoints(self):
        result={}       
        try:
                         
            #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
            engine=db
            # create a Session
            Session = sessionmaker(bind=engine)
            session = Session()
                                

            if self.last_date_specified==1:
                day=self.myjson["Day"]
                if day=="Today":
                   day=datetime.date.today()

                res=session.query(func.count(distinct(Points.datecaptured)).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).filter(Points.datecaptured<=day).first()        
                 #res= session.query(func.sum(Points.scoredpoints).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).filter(Points.datecaptured<=day).first()
            #get points by number of days an application has been used.
            #res=session.query(func.count(distinct(Points.datecaptured)).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).filter(Points.datecaptured<=day).first()
            else:
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
                    
                       
                                          
                    #trees=int(stepspoints*100/70000)
                    
                    #flowers=int(clickpoints*67/18)


                    #print file_name,trees, flowers
                    
                    #tree_array.append(trees)
                    #flower_array.append(flowers)
                    #total=trees+flowers
                    #total_plants.append(total)

                    #Get the current badge of this individual
                     
                    engine=db
                    # create a Session
                    Session = sessionmaker(bind=engine)
                    session = Session()
                   

                    #get the current badge 
                    res=session.query(AttainedUserBadges).filter(AttainedUserBadges.intermediary_id==orig_email).filter(AttainedUserBadges.status==1).first()

                    if res is None:
                        #this user is not assigned a bagde 
                        currentbadge=0 #start with slave badge
                       
                    else:
                        currentbadge=res.badge_id
                    
                    old_badge=currentbadge                    
                    if stepspoints>=10000 and currentbadge==2:
                        if clickpoints>=18:
                            
                            badges.append("Queen/King")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/queen.jpeg")
                        else:
                            badges.append("No promotion")
                           
                    elif stepspoints>=9000 and currentbadge==3:
                        if clickpoints>=16:
                            badges.append("Princess/Prince")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/princess.jpeg")
                        else:
                            badges.append("No promotion") 
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/duchess.jpeg")
                    elif stepspoints>=8000 and currentbadge==4:
                        if clickpoints>=14:
                            badges.append("Duchess/Duke")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/duchess.jpeg")
                        else:
                           badges.append("No promotion")
                           badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/grandmaster.jpeg")
                    elif stepspoints>=7000 and currentbadge==5:
                        if clickpoints>=12:
                            badges.append("Grand Master")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/grandmaster.jpeg")
                        else:
                            badges.append("No promotion")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniormaster.jpeg")
  
                    elif stepspoints>=6000 and currentbadge==6:
                        if clickpoints>=10:
                            badges.append("Senior Master")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniormaster.jpeg")
                        else:
                            badges.append("No promotion")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/master.jpeg")
                    elif stepspoints>=5000 and currentbadge==7:
                        if clickpoints>=8:
                            badges.append("Master")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/master.jpeg")
                        else:
                            badges.append("No promotion")               
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/juniormaster.jpeg")
                    if stepspoints>=4000 and currentbadge==8:
                        if clickpoints>=4:
                            badges.append("Junior Master")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/juniormaster.jpeg")
                        else:
                            badges.append("No promotion")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniorservant.jpeg")
                    elif stepspoints>=3000 and currentbadge==9:
                        if clickpoints>=2:
                            badges.append("Senior Servant")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniorservant.jpeg")
                        else:
                            badges.append("No Promotion") 
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/servant.jpeg")
                    elif stepspoints>=2500 and currentbadge==10:
                        if clickpoints>=1:
                            badges.append("Servant")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/servant.jpeg")
                        else:
                            badges.append("No promotion")
                            badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/slave.jpeg")
                    else:
                     
                        badges.append("Slave")
                        
                        badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/slave.jpeg")
                   
                   
                    try:
  
                   
                        #get the rank of the badge
                        if badges[posn] == "No promotion":
                            print "No Promotion"
                        else:
                            
                            #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
                            engine=db
                            # create a Session
                            Session = sessionmaker(bind=engine)
                            session = Session()
                            res=session.query(Badges).filter(Badges.badgename==badges[posn]).first()
                            
                            if res ==None:
                                rank=0
                            else:
                                
                                rank=res.rank #new acquired rank
                              
                             
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
                                    
                                    feedback_message=feedback_message+"your team has been promoted to a new badge. Your old badge was %s and now your new badge is %s. Keep on using your app every day and keep on motivating your %s to walk more steps so that your team can continue to shine."%(old_badge,badges[posn],beneficiary_relations[posn])
                                                                        
                                    myjson2={"recipient":intermediary_mobiles[posn],"message":feedback_message}
                                    obj=QueueFeedback(myjson2)
                                    res=obj.saveFeedbackInDB()
                                  
                                
                                #else:
                                #    print "No new promotion"
                                #    #pass# no new promotion
                        
              
                      
                        
                        
                    except Exception as e:
                        print "Exception thrown: %s"%e
                        return -1
                        
                    
                        
  
                   
                    posn=posn+1
        except Exception as e:
            print "Exception thrown %s "%e
            return -1
              
                
                  
        return 1         
      
         

              
     
     
     


score_date=datetime.date.today()-datetime.timedelta(days=1)
score_date_str="%s"%score_date.strftime("%d/%m/%Y")
score_date_str2="%s"%score_date.strftime("%Y-%m-%d")


myjson={'Day':score_date_str2}
obj=RetrievePoints(myjson,'katulentwa@gmail.com',1)
result=obj.assignBadges()

if result==1:
    print "The badge assignment completed successfully"
else:
    print "Badge assignment failed to complete"

