#!/usr/bin/env python
import datetime,calendar
import sys,json
from sqlalchemy import create_engine,distinct,func,asc
from sqlalchemy.orm import sessionmaker
from wellness.applogic.points_module import Points,db
from retrieve_intermediary import RetrieveIntermediary
from collections import OrderedDict
from save_factors import ManageFactors
import os

def bubblesort(A,X,Y,Z,U,V):
  
  for i in range( len( A ) ):
    for k in range( len( A ) - 1, i, -1 ):
      if ( A[k]> A[k - 1] ):
        swap( A, k, k - 1 )
        swap(X, k, k - 1 )
        swap(Y, k, k - 1 )
        swap(Z, k, k - 1 )
        swap(U, k, k - 1 )
        swap(V, k, k - 1 )
  return A
 
def swap( A, x, y ):
  tmp = A[x]
  A[x] = A[y]
  A[y] = tmp
  

class RetrievePoints:
    def __init__(self,myjson,intermediary_id):
         self.myjson=myjson
         self.intermediary_id=intermediary_id
   
   
    def first_day_of_month(self,d):
       return datetime.date(d.year, d.month, 1)
    def last_day_of_month(self,d):
       t=(calendar.monthrange(d.year,d.month))
       return datetime.date(d.year,d.month,t[1])
       

    def retriveIndividualScore(self):
         result={}
         try:
             
              day=self.myjson["Day"]
                                 
         except Exception as e:
              #print "Content-type: text/html\n" 
              result["message"]="Error%s"%e.message
              return (json.JSONEncoder().encode(result))


         #day="Today"
         #startdate="2013-12-06"
         #enddate="2013-12-06"
         #intermediary_id=self.sessionvar['username']
         #self.b_id='KTLNTW001'
         
         if day=="Today":
              startdate = datetime.date.today()
              enddate = datetime.date.today()              
              
         elif day=="This week":
              #from monday up to sunday. 
              day_of_week = datetime.datetime.today().weekday()
              startdate=datetime.date.today()-datetime.timedelta(days=day_of_week)#monday
              enddate=startdate+datetime.timedelta(days=6)#sunday
    
             
         elif day=="Last week":
              day_of_week = datetime.datetime.today().weekday()
              enddate = datetime.date.today()-datetime.timedelta(days=(day_of_week+1))#last sunday. Subtract today from the number of days that have passed since sunday
              startdate = enddate-datetime.timedelta(days=6)# Monday of the previous week.
                        
              
         elif day=="This month":
              #from 1st of this month to end of last month
              startdate=self.first_day_of_month(datetime.date.today())
              enddate=self.last_day_of_month(datetime.date.today())
         
              
         elif day=="Last month":
              #from 1st of last month to end of last month
              #startdate=self.first_day_of_month(first_day_of_month(datetime.date.today())-datetime.timedelta(days=1))
              startdate=self.first_day_of_month(self.first_day_of_month(datetime.date.today())-datetime.timedelta(days=1))               
              enddate=self.last_day_of_month(startdate)
              
         
         elif day=="Last three months":
              # go two months back
              first_day_last_month=self.first_day_of_month(self.first_day_of_month(datetime.date.today())-datetime.timedelta(days=1))
              startdate=self.first_day_of_month(first_day_last_month-datetime.timedelta(days=1))# subract 1 day to get to the end of a previous month before last month and get the first day of that month
              enddate=self.last_day_of_month(datetime.date.today())#



         
         
         try:
              #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
              engine=db
              # create a Session
              Session = sessionmaker(bind=engine)
              session = Session()
                                  
              # querying for a record in the physical_activity pattern table
              res= session.query(func.sum(Points.scoredpoints).label("sum_points")).filter(Points.intermediary_id==self.intermediary_id).filter(Points.datecaptured>=startdate).filter(Points.datecaptured<=enddate).first()
              retrieved_points_sum=0# initialize how many distinct dates are in the database
              for retrieved_points_sum in res:
                   break
               
              result["points"]="%s"%retrieved_points_sum
              
              if res.sum_points is None:
                   
                   retrieved_points_sum="0"
                   result["message"]="You have no points from '%s'"%day
                   result["points"]="%s"%retrieved_points_sum
              else: 
                   result["message"]="You have scored some points  from '%s'"%day

              
              session.close()
              engine.dispose()
                   
              return (json.JSONEncoder().encode(result))                   
                                  
         except Exception as e:
                        
              #print "Content-type: text/html\n" 
              session.close()
              engine.dispose() 
                                  
              result["message"]="Error: %s"%e
              #print      
              return (json.JSONEncoder().encode(result))
              #sys.exit()    
              
              
    def retrieveScoreBoard(self):
         result={}
         try:
             
              day=self.myjson["Day"]
                                 
         except Exception as e:
              #print "Content-type: text/html\n" 
              result["message"]="Error%s"%e.message
              return (json.JSONEncoder().encode(result))


         #day="Today"
         #startdate="2013-12-06"
         #enddate="2013-12-06"
         #intermediary_id=self.sessionvar['username']
         #self.b_id='KTLNTW001'
         
         if day=="Today":
              startdate = datetime.date.today()
              enddate = datetime.date.today()              
              
         elif day=="This week":
              #from monday up to sunday. 
              day_of_week = datetime.datetime.today().weekday()
              startdate=datetime.date.today()-datetime.timedelta(days=day_of_week)#monday
              enddate=startdate+datetime.timedelta(days=6)#sunday
    
             
         elif day=="Last week":
              day_of_week = datetime.datetime.today().weekday()
              enddate = datetime.date.today()-datetime.timedelta(days=(day_of_week+1))#last sunday. Subtract today from the number of days that have passed since sunday
              startdate = enddate-datetime.timedelta(days=6)# Monday of the previous week.
              print startdate,enddate              
              
         elif day=="This month":
              #from 1st of this month to end of last month
              startdate=self.first_day_of_month(datetime.date.today())
              enddate=self.last_day_of_month(datetime.date.today())
         
              
         elif day=="Last month":
              #from 1st of last month to end of last month
              #startdate=self.first_day_of_month(first_day_of_month(datetime.date.today())-datetime.timedelta(days=1))
              startdate=self.first_day_of_month(self.first_day_of_month(datetime.date.today())-datetime.timedelta(days=1))               
              enddate=self.last_day_of_month(startdate)
              
         
         elif day=="Last three months":
              # go two months back
              first_day_last_month=self.first_day_of_month(self.first_day_of_month(datetime.date.today())-datetime.timedelta(days=1))
              startdate=self.first_day_of_month(first_day_last_month-datetime.timedelta(days=1))# subract 1 day to get to the end of a previous month before last month and get the first day of that month
              enddate=self.last_day_of_month(datetime.date.today())#



         
         
         try:
              #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
              engine=db
              # create a Session
              Session = sessionmaker(bind=engine)
              session = Session()
              record_not_exist=True                   
              # querying for a record in the physical_activity pattern table
              res= session.query(func.sum(Points.scoredpoints).label("sum_score"),Points.intermediary_id).filter(Points.datecaptured>=startdate).filter(Points.datecaptured<=enddate).group_by(Points.intermediary_id).order_by(asc("sum_score")).all()
              retrieved_points_sum=0# initialize how many distinct dates are in the database
              
              first_posn=0
              second_posn=0
              point_tuples={}
              key2="D"
              for retrieved_points_sum,intermediary_id in res:
                   point_tuple={}
                   if first_posn<10:
                        key1="R0"
                   else:
                        key1="R"
                   record_not_exist=False
                        
                   point_tuple[key2+"%s"%second_posn]=intermediary_id
                   second_posn=second_posn+1
                   
                   point_tuple[key2+"%s"%second_posn]="%s"%retrieved_points_sum
                   second_posn=second_posn+1
                   
                   second_posn=0
                   result[key1+"%s"%first_posn]=point_tuple
                   first_posn=first_posn+1
              
              if record_not_exist:
                   result["R00"]={"D0":"No points available for that specified period of time","D1":-4}
                   #result["R00"]["D1"]="-4"
   
       
              session.close()
              engine.dispose()
                   
              return (json.JSONEncoder().encode(result))                   
                                  
         except Exception as e:
              
              session.close()
              engine.dispose() 
              point_tuple={} 
              point_tuple["D0"]=e.message
              point_tuple["D1"]="-1"
              result["R00"]=point_tuple  
              return (json.JSONEncoder().encode(result))
          
    def retrieveScoreGardensUrls(self):
        result={}
        try:
            
             day=self.myjson["Day"]
                                
        except Exception as e:
             #print "Content-type: text/html\n" 
             result["message"]="Error%s"%e.message
             return (json.JSONEncoder().encode(result))


        #day="Today"
        #startdate="2013-12-06"
        #enddate="2013-12-06"
        #intermediary_id=self.sessionvar['username']
        #self.b_id='KTLNTW001'
        
        if day=="Today":
             date_int=datetime.date.today()
             date_str ="%s"%date_int             
             
        elif day=="Yesterday":
             #Yesterday
             date_int=datetime.date.today()-datetime.timedelta(days=1)
        else:
             result["message"]="Error: The option '%s' is invalid"%day
             return (json.JSONEncoder().encode(result))
             
             
             
        date_str ="%s"%date_int
        
        myjson={'Fname':'Dummy','Lname':'Dummy','Username':'dummy'}
        obj=RetrieveIntermediary(myjson)
        res=obj.retrieveIntermediaryInDB()
        
        intermediaries_tuple=json.loads(res)
        intermediaries_emails=[]
        intermediary_names=[]
        orig_emails=[]
        beneficiary_ids=[]
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
                  
                  myjson={'Fname':'Dummy','Lname':'Dummy','Username':orig_email}
                  obj=RetrieveIntermediary(myjson)
                  result2=obj.isAssignedBeneficiary()
                  
                  beneficiary_tuple=json.loads(result2)
                  beneficiary_ids.append(beneficiary_tuple["Id"])
                  
                  #image_path="/static/wellnessapp/images/garden/%s/%s_%s.jpeg"%(intermediaries_emails[posn],beneficiary_ids[posn],garden_label)
                  #file_path=os.path.dirname(os.path.abspath(__file__))
                  #if not os.path.isfile(image_path):
   
                  #  file_path="wellnessapp/images/garden/%s/blank.jpeg"%intermediaries_emails[posn]
                  #else:
                
                  file_path="wellnessapp/images/garden/%s/%s_%s.jpeg"%(intermediaries_emails[posn],beneficiary_ids[posn],garden_label)
                  file_path_alt="wellnessapp/images/garden/blank.jpeg"
                  file_name="%s_%s"%(beneficiary_ids[posn],garden_label)
                  urls.append(file_path)
                  
    
                  myjson={'FactorId':file_name}
                  obj=ManageFactors(myjson)
                  res=obj.retrieveFactorsFromDB()
                  res=json.loads(res)
                  trees=int(res["R00"]["TreeFactor"]*100.0)
                  flowers=int(res["R00"]["FlowerFactor"]*67.0)
                  
                  tree_array.append(trees)
                  flower_array.append(flowers)
                  total=trees+flowers
                  total_plants.append(total)
                  
                  posn=posn+1
                  
                 
        posn=0

         

        '''
        for beneficiary in beneficiary_ids:
          
            
            file_path="{{STATIC_URL}}wellnessapp/images/garden/%s/%s_%s"%(intermediaries_emails[posn],beneficiary_ids[posn],garden_label)
            file_name="%s_%s"%(beneficiary_ids[posn],garden_label)
            urls.append(file_path)
            

            myjson={'FactorId':file_name}
            obj=ManageFactors(myjson)
            res=obj.retrieveFactorsFromDB()
            res=json.loads(res)
            trees=int(res["R00"]["TreeFactor"]*100.0)
            flowers=int(res["R00"]["FlowerFactor"]*67.0)
            
            tree_array.append(trees)
            flower_array.append(flowers)
            total=trees+flowers
            total_plants.append(total)
            posn=posn+1
        '''
             
           
        bubblesort(total_plants,urls,beneficiary_ids,tree_array,flower_array,intermediary_names)
        posn=0
        file_path_alt="wellnessapp/images/garden/blank.jpeg"
        for beneficiary in beneficiary_ids:
            urls_tuple={}
            if first_posn<10:
              key1="R0"
            else:
              key1="R"     
            urls_tuple[key2+"%s"%second_posn]=urls[posn]
            second_posn=second_posn+1
            
            
            urls_tuple[key2+"%s"%second_posn]=file_path_alt
            second_posn=second_posn+1
            

            urls_tuple[key2+"%s"%second_posn]="%s"%tree_array[posn]
            second_posn=second_posn+1
            
            urls_tuple[key2+"%s"%second_posn]="%s"%flower_array[posn]
            second_posn=second_posn+1
            
            urls_tuple[key2+"%s"%second_posn]="%s"%intermediary_names[posn]
            second_posn=second_posn+1
            
            second_posn=0
            result[key1+"%s"%first_posn]=urls_tuple
            
            first_posn=first_posn+1
            posn=posn+1
        
             
        return (json.JSONEncoder().encode(OrderedDict(sorted(result.items(), key=lambda t: t[0]))))
         

              
     
     
#myjson={'Fname':'Lucas','Lname':'Katule','Username':'katulentwa@gmail.com'}
#obj=RetrieveIntermediary(myjson)
#result=obj.retrieveIntermediaryInDB()
#print result

#myjson={'Day':'Yesterday'}
#obj=RetrievePoints(myjson,'katulentwa@gmail.com')
#result=obj.retrieveScoreGardensUrls()
#print result

#myjson={'Day':'Today'}
#obj=RetrievePoints(myjson,'katulentwa@gmail.com')
#print result
