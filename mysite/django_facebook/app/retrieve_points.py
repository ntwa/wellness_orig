#!/usr/bin/env python
import datetime,calendar
import sys,json
from sqlalchemy import create_engine,distinct,func,asc
from sqlalchemy.orm import sessionmaker
from wellness.applogic.points_module import Points,db
from retrieve_sound import RetrieveSound
from retrieve_intermediary import RetrieveIntermediary
from collections import OrderedDict
from save_factors import ManageFactors
import os
from wellness.applogic.activity_module import PhysicalActivity,db,dbconn
#from wellness.applogic.intermediary_module import Beneficiary
from random import randint
from wellness.applogic.pilot_start import PilotCommencement
from wellness.applogic.food_beverage_module import FoodAndBeverage,Meal,MealComposition,db,dbconn

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
                if day == "Today":
                    day=datetime.date.today()
                res=session.query(func.sum(PhysicalActivity.stepscounter).label("sum_steps")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).filter(PhysicalActivity.datecaptured>=datestarted).filter(PhysicalActivity.datecaptured<=day).first()
         
            else:
 
                res=session.query(func.sum(PhysicalActivity.stepscounter).label("sum_steps")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).filter(PhysicalActivity.datecaptured>=datestarted).first()
            
            if res.sum_steps==None:
                sum_steps=0
            else:
                sum_steps=int(res.sum_steps)
            result={}
            result["steps"]=sum_steps
            
            if self.last_date_specified==1:
                res=session.query(func.min(PhysicalActivity.datecaptured).label("min_date")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).filter(PhysicalActivity.datecaptured<=day).first()
            else: 
                res=session.query(func.min(PhysicalActivity.datecaptured).label("min_date")).filter(PhysicalActivity.beneficiary_id==beneficiary_id).first()
            
            min_date=res.min_date 

            

            if self.last_date_specified==1:
                max_date=self.myjson["Day"]
                if max_date=="Today":
                    max_date=datetime.date.today()
                else:
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

        return (json.JSONEncoder().encode(result))

    def countRecordedMeals(self):
      result={}
      try:
        beneficiary_id=self.myjson["BeneficiaryID"]
      except Exception as e:
        sys.exit



      try:
        
        engine=db
        #create a Session
        Session = sessionmaker(bind=engine)
        session = Session()
        res = session.query(func.count(FoodAndBeverage.id).label("mealscounter")).filter(FoodAndBeverage.beneficiary_id==beneficiary_id).first()
        if res.mealscounter is None:
          awarded_points=0;
        else:
          awarded_points=res.mealscounter



        result["NumberOfMeals"]=awarded_points
        result["Message"]="Meals count obtained successfully"


      except Exception as e:
        result["NumberOfMeals"]=-1
        result["Message"]=e

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
                                


            res=session.query(func.count(distinct(Points.datecaptured)).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).first()


            
            retrieved_points_sum=0# initialize how many distinct dates are in the database
                      
            
            
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



   
              
    def retrieveIndividualBadge(self):

         result={}

         try:


              varmyjson={'Day':"Today"}
              myjson={'Fname':'Dummy','Lname':'Dummy','Username':self.intermediary_id}
              obj=RetrieveIntermediary(myjson)
              res=obj.isAssignedBeneficiary()

              beneficiary_tuple=json.loads(res)
              b_id=beneficiary_tuple["Id"]
              if b_id==None :
                  raise ValueError('This individual is not assigned a beneficiary')

        
              clickPointsObj=RetrievePoints(varmyjson,self.intermediary_id,1)
              resclickpoints=clickPointsObj.retrieveIntermediaryClickPoints()
              resclickpoints=json.loads(resclickpoints)
        
              clickpoints=int(resclickpoints["points"]/resclickpoints["dates_counter"])
        
              if clickpoints>60:
                  clickpoints=60
        
        
              ressteps=clickPointsObj.getSteps(b_id)
              ressteps=json.loads(ressteps)
        
        
              stepspoints=int(ressteps["steps"]/(100*ressteps["dates_counter"]))
        
        
        
        
              if stepspoints>100:
                  stepspoints=100
        
              badges_urls=[]
        
        
              if stepspoints>=100:
                  if clickpoints>=6:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/queen.jpeg")
                  else:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/princess.jpeg")
              elif stepspoints>=90:
                  if clickpoints>=12:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/princess.jpeg")
                  else:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/duchess.jpeg")
              elif stepspoints>=80:
                  if clickpoints>=18:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/duchess.jpeg")
                  else:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/grandmaster.jpeg")
              elif stepspoints>=70:
                  if clickpoints>=24:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/grandmaster.jpeg")
                  else:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniormaster.jpeg")
        
              elif stepspoints>=60:
                  if clickpoints>=30:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniormaster.jpeg")
                  else:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/master.jpeg")
              elif stepspoints>=45:
                  if clickpoints>=36:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/master.jpeg")
                  else:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/juniormaster.jpeg")
              elif stepspoints>=30:
                  if clickpoints>=42:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/juniormaster.jpeg")
                  else:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniorservant.jpeg")
              elif stepspoints>=20:
                  if clickpoints>=48:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniorservant.jpeg")
                  else:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/servant.jpeg")
              elif stepspoints>=10:
                  if clickpoints>=54:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/servant.jpeg")
                  else:
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/slave.jpeg")
              else:
                  badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/slave.jpeg")
                       

              num=randint(2,49)
              obj=RetrieveSound(num)
              res=obj.retrieveSoundUrl()
              res=json.loads(res)
                
              sound_url=res["url"]              
              result={"R00":{"D0":"Badge Acquired","D1":badges_urls[0],"D2":sound_url}}

              
              

         except Exception as e:
              message="An exception was thrown in function retrieveIndividualScore(): %s"%e
              result={"R00":{"D0":message,"D1":"http://ict4d01.cs.uct.ac.za/static/django_facebook/images/nobadge.jpeg","D2":"Error"}}
















    
         return (json.JSONEncoder().encode(result))



    def retrieveScoreGardensUrls(self):
        result={}
        try:
            
             day=self.myjson["Day"]
                                 
        except Exception as e:
             #print "Content-type: text/html\n" 
             result["message"]="Error%s"%e.message
             return (json.JSONEncoder().encode(result))

        
        if day is not None:
            if day=="Today":
                today_date=datetime.date.today()
                date_str="%s"%today_date 
            else:
                date_str="%s"%day
        else:
             result["message"]="Error: The option '%s' is invalid"%day
             return (json.JSONEncoder().encode(result))
             
             
             
        
        
        myjson={'Fname':'Dummy','Lname':'Dummy','Username':'dummy'}
        obj=RetrieveIntermediary(myjson)
        res=obj.retrieveIntermediaryInDB()
        
        intermediaries_tuple=json.loads(res)
        intermediaries_emails=[]
        intermediary_names=[]
        orig_emails=[]
        beneficiary_ids=[]
        beneficiary_names=[]
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
                  myjson={'Fname':'Dummy','Lname':'Dummy','Username':orig_email}
                  obj=RetrieveIntermediary(myjson)
                  result2=obj.isAssignedBeneficiary()
                  
                  beneficiary_tuple=json.loads(result2)
                  #beneficiary_ids.append(beneficiary_tuple["Id"])
                  
                  team_identifier="%s_%s"%(beneficiary_tuple["Id"],garden_label)
                  beneficiary_ids.append(team_identifier)

                
                  file_path="django_facebook/images/garden/%s/%s_%s.jpeg"%(intermediaries_emails[posn],beneficiary_tuple["Id"],garden_label)
                  
                  file_name="%s_%s"%(beneficiary_ids[posn],garden_label)
                  urls.append(file_path)
                  #beneficiary_ids.append(beneficiary_tuple["Id"])

                 
                
                   
                  varmyjson={'Day':day}
		  
                                   
                  clickPointsObj=RetrievePoints(varmyjson,orig_email,1)
                  resclickpoints=clickPointsObj.retrieveIntermediaryClickPoints()
                  resclickpoints=json.loads(resclickpoints)
                 
                  clickpoints=int(resclickpoints["points"]/resclickpoints["dates_counter"])
                  
                  if clickpoints>60:
                      clickpoints=60

                
                   
                  usage_points.append(clickpoints)
                 
                  ressteps=clickPointsObj.getSteps(beneficiary_tuple["Id"])
                  ressteps=json.loads(ressteps)
                   

                  stepspoints=int(ressteps["steps"]/(100*ressteps["dates_counter"]))
                 
                  if stepspoints>100:
                      stepspoints=100
                  
                  bonus_points.append(stepspoints) 
                  
                     

                  trees=int(stepspoints*100.0/100)
                  flowers=int(clickpoints*67.0/60)
                  #print file_name,trees, flowers
                  tree_array.append(trees)
                  flower_array.append(flowers)
                  total=trees+flowers
                  total_plants.append(total)
                  
                  if stepspoints>=100:
                      if clickpoints>=6:
                         badges.append("Queen/King")
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/queen.jpeg")
                      else:
                         badges.append("Princess/Prince")
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/princess.jpeg")
                  elif stepspoints>=90:
                      if clickpoints>=12:
                         badges.append("Princess/Prince")
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/princess.jpeg")
                      else:
                         badges.append("Duchess/Duke") 
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/duchess.jpeg")
                  elif stepspoints>=80:
                      if clickpoints>=18:
                         badges.append("Duchess/Duke")
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/duchess.jpeg")
                      else:
                         badges.append("Grand Master")
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/grandmaster.jpeg")
                  elif stepspoints>=70:
                      if clickpoints>=24:
                         badges.append("Grand Master")
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/grandmaster.jpeg")
                      else:
                         badges.append("Senior Master")
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniormaster.jpeg")

                  elif stepspoints>=60:
                      if clickpoints>=30:
                         badges.append("Senior Master")
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniormaster.jpeg")
                      else:
                         badges.append("Master")
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/master.jpeg")
                  elif stepspoints>=45:
                      if clickpoints>=36:
                         badges.append("Master")
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/master.jpeg")
                      else:
                         badges.append("Junior Master")               
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/juniormaster.jpeg")
                  elif stepspoints>=30:
                      if clickpoints>=42:
                         badges.append("Junior Master")
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/juniormaster.jpeg")
                      else:
                      
                         badges.append("Senior Servant")
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniorservant.jpeg")
                  elif stepspoints>=20:

                      if clickpoints>=48:
                         badges.append("Senior Servant")
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/seniorservant.jpeg")
                      else:
                         badges.append("Servant") 
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/servant.jpeg")
                  elif stepspoints>=10:
                      if clickpoints>=54:
                         badges.append("Servant")
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/servant.jpeg")
                      else:
                         badges.append("Lowest Badge")
                         badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/slave.jpeg")
                  else:
                      badges.append("Lowest Badge")
                      badges_urls.append("http://ict4d01.cs.uct.ac.za/static/django_facebook/images/badges/slave.jpeg")
                     

                   
                  posn=posn+1
                  
                 
        posn=0      
      
    
           
        bubblesort(total_plants,urls,beneficiary_ids,tree_array,flower_array,intermediary_names,beneficiary_names,usage_points,bonus_points,badges,badges_urls)
        posn=0
        file_path_alt="django_facebook/images/garden/blank.jpg"
        for beneficiary in beneficiary_ids:
            urls_tuple={}
            if first_posn<10:
              key1="R0"
            else:
              key1="R"     
              
            urls_tuple[key2+"%s"%second_posn]="(%s, %s)"%(intermediary_names[posn],beneficiary_names[posn])
            second_posn=second_posn+1  
            
            urls_tuple[key2+"%s"%second_posn]=urls[posn]
            if total_plants[posn]==0:
              urls_tuple[key2+"%s"%second_posn]=file_path_alt
              
            second_posn=second_posn+1
            
            

            urls_tuple[key2+"%s"%second_posn]="%s"%tree_array[posn]
            second_posn=second_posn+1
            
            urls_tuple[key2+"%s"%second_posn]="%s"%flower_array[posn]
            second_posn=second_posn+1
            
            urls_tuple[key2+"%s"%second_posn]="%s"%total_plants[posn]
            second_posn=second_posn+1
            

            urls_tuple[key2+"%s"%second_posn]="%s"%usage_points[posn]
            second_posn=second_posn+1
 
 
            urls_tuple[key2+"%s"%second_posn]="%s"%bonus_points[posn]
            second_posn=second_posn+1

            urls_tuple[key2+"%s"%second_posn]="%s"%badges[posn]
            second_posn=second_posn+1
            
            urls_tuple[key2+"%s"%second_posn]="%s"%badges_urls[posn]
            second_posn=second_posn+1


            urls_tuple[key2+"%s"%second_posn]="%s"%beneficiary
            second_posn=second_posn+1
            

            
            second_posn=0
            result[key1+"%s"%first_posn]=(OrderedDict(sorted(urls_tuple.items(), key=lambda t: t[0])))
            first_posn=first_posn+1
            posn=posn+1
        
             
        return (json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))
         

              
     
     
#myjson={'Day':'Today',"BeneficiaryID":1}
#obj=RetrievePoints(myjson,'katulentwa@gmail.com',1)

#result=obj.countRecordedMeals()
#print result

#print result

#myjson={'Day':'Today'}
#obj=RetrievePoints(myjson,'katulentwa@gmail.com')
#print resulti
