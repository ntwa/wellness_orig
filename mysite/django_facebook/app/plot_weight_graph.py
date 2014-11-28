#!/usr/bin/env python
import datetime,calendar
import sys,json
from sqlalchemy import create_engine,func
from sqlalchemy.orm import sessionmaker
from wellness.applogic.weight_module import Weight,db,dbconn
from collections import OrderedDict






class PlotWeightGraph:     
     
     def __init__(self,myjson,b_id):
          self.myjson=myjson
          self.b_id=b_id
          
     def first_day_of_month(self,d):
               return datetime.date(d.year, d.month, 1)
     
     def last_day_of_month(self,d):
               t=(calendar.monthrange(d.year,d.month))
               return datetime.date(d.year,d.month,t[1])     
          
          
          
     def getMonthlyWeight(self,startdate,enddate):
          
          errorcode={}
          try:
               
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False)
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               
               session = Session()
               
               day_of_week = startdate.weekday()
               week_start_date=startdate
               week_end_date=(startdate-datetime.timedelta(days=day_of_week))+datetime.timedelta(days=6)
               
               temp_start_date=startdate             
               
                            
               
               weight_ids=[]
               weight_dates=[]
               weight_start_times=[]
               weight_end_times=[]
               
               key1="R"
               key2="F"
               first_posn=0
               second_posn=0
               counter=0
               dates=[]
               previousdate_string=None
               current_date_string=""
               next_date_string=""
               days_iterator=0
               week_iterator=1
               total_week_weight=0
               average_weekly_weight=0
               
               weight_by_date=0
               weight_tuples={} 
               dates_counter=0# for keeping track of the number of dates
               
               
               # count the number of dates in the databases.
               num_dates=session.query(func.count(Weight.datecaptured)).filter(Weight.beneficiary_id==self.b_id).filter(Weight.datecaptured>=startdate).filter(Weight.datecaptured<=enddate).order_by(Weight.datecaptured).first()
               
               
               retrieved_dates_counter=0# initialize how many  dates records have meet the above query
               for retrieved_dates_counter in num_dates:
                    break
          
               weekly_weight_tuple={}
               if retrieved_dates_counter==0:
                    
                    weekly_weight_tuple[key2+"%d"%second_posn]="There is not weight recorded at the specified period of time"
                    second_posn=second_posn+1
                                                                                                                                                                                  
                                                                                                                                                                                  
                    weekly_weight_tuple[key2+"%d"%second_posn]=-4
                    second_posn=0 
                    if first_posn<10:
                         key1="R0"
                    else:
                         key1="R"
                                                                                                                                                 
                    weight_tuples[key1+"%d"%first_posn]=weekly_weight_tuple
                                                                                                                                               
                    first_posn=first_posn+1 
                    weekly_weight_tuple={}
                    return(json.JSONEncoder().encode(weight_tuples))                
               
               #print retrieved_dates_counter
               
     
               
               
               
               
               
               
               res = session.query(Weight).filter(Weight.beneficiary_id==self.b_id).filter(Weight.datecaptured>=startdate).filter(Weight.datecaptured<=enddate).order_by(Weight.datecaptured).all()
        
               
               for weight in res:
                    
                    
                    #current_date_string=weight.datecaptured.strftime("%d/%m/%Y")
                    current_date=weight.datecaptured
                    #current_date_string=weight.datecaptured.strftime("%d/%m")
                    current_date_string=current_date.strftime("%d/%m")
                    
                    dates.append(weight.datecaptured.strftime("%d/%m/%Y"))
                    counter=counter+1
                    weight_by_date=weight.weight 
                    
                    dates_counter=dates_counter+1
                                 
                    
                    
                   
                    
                    if((current_date>=week_start_date) and (current_date<=week_end_date)):
                         weight_tuple={}
                         total_week_weight=total_week_weight+weight_by_date
                         days_iterator=days_iterator+1
                         
                         #print "Current= %s, Week_start = %s, and Week end=%s"%(current_date_string,week_start_date,week_end_date)
                         if dates_counter==retrieved_dates_counter:
                              average_weekly_weight=total_week_weight/days_iterator
                                                            
                              weight_tuple[key2+"%d"%second_posn]="Week %s"%week_iterator
                              second_posn=second_posn+1
                                                                                                                 
                              weight_tuple[key2+"%d"%second_posn]=float("{0:.2f}".format(average_weekly_weight))
                              second_posn=0 
                              if first_posn<10:
                                   key1="R0"
                              else:
                                   key1="R"
                                                                                
                              weight_tuples[key1+"%d"%first_posn]=weight_tuple
                              first_posn=first_posn+1
                              
                              week_start_date=week_end_date+datetime.timedelta(days=1)# move to next monday
                              week_end_date=week_start_date+datetime.timedelta(days=6)# move to next sunday 
                                                       
                              week_iterator=week_iterator+1
                              total_week_weight=0 #initialize the total weight of that week to zero
                              days_iterator=0                               
                              
                         
                    else:
                         #compute the average weight accumulated in the week before moving to next week
                         #first check if the total_weight is greater than 0 before moving to next week
                         
                         if total_week_weight > 0:
                              weight_tuple={}
                              average_weekly_weight=total_week_weight/days_iterator
                              
                              weight_tuple[key2+"%d"%second_posn]="Week %s"%week_iterator
                              second_posn=second_posn+1
                                                                                   
                              weight_tuple[key2+"%d"%second_posn]=float("{0:.2f}".format(average_weekly_weight))
                              second_posn=0 
                              if first_posn<10:
                                   key1="R0"
                              else:
                                   key1="R"
                                                  
                              weight_tuples[key1+"%d"%first_posn]=weight_tuple
                              first_posn=first_posn+1 
                              
                              
                         
                              
                         week_start_date=week_end_date+datetime.timedelta(days=1)# move to next monday
                         week_end_date=week_start_date+datetime.timedelta(days=6)# move to next sunday 
                         week_iterator=week_iterator+1
                         total_week_weight=0 #initialize the total weight of that week to zero
                         days_iterator=0 
                         
                         
                         if week_end_date>enddate:
                              week_end_date=enddate #ensure that the last week of the month is within the range of days within the month.                    
                                         
                         while((current_date>week_end_date)):#keep on incrementing
                              week_start_date=week_end_date+datetime.timedelta(days=1)# move to next monday
                              week_end_date=week_start_date+datetime.timedelta(days=6)# move to next sunday
                              week_iterator=week_iterator+1# move the iterator by 1 week
                         
                         
                         if((current_date>=week_start_date) and (current_date<=week_end_date)):
                              weight_tuple={}
                              total_week_weight=total_week_weight+weight_by_date
                              days_iterator=days_iterator+1
                              #print "--Current= %s, Week_start = %s, and Week end=%s"%(current_date_string,week_start_date,week_end_date)
                              #if we have reached the end then compute the average
                              if dates_counter==retrieved_dates_counter:
                                   average_weekly_weight=total_week_weight/days_iterator
                                                                 
                                   weight_tuple[key2+"%d"%second_posn]="Week %s"%week_iterator
                                   second_posn=second_posn+1
                                                                                                                      
                                   weight_tuple[key2+"%d"%second_posn]=float("{0:.2f}".format(average_weekly_weight))
                                   second_posn=0 
                                   if first_posn<10:
                                        key1="R0"
                                   else:
                                        key1="R"
                                                                                     
                                   weight_tuples[key1+"%d"%first_posn]=weight_tuple
                                   first_posn=first_posn+1 
                                   week_start_date=week_end_date+datetime.timedelta(days=1)# move to next monday
                                   week_end_date=week_start_date+datetime.timedelta(days=6)# move to next sunday 
                                                            
                                   week_iterator=week_iterator+1
                                   total_week_weight=0 #initialize the total weight of that week to zero
                                   days_iterator=0 

                              
                         

                    
                    
                    
               
                        
                                          
                        
               session.close()
               engine.dispose()     
               dbconn.close()

               return(json.JSONEncoder().encode(OrderedDict(sorted(weight_tuples.items(), key=lambda t: t[0]))))
               
          except Exception as e:
               session.close()
               engine.dispose() 
               dbconn.close()

               second_posn=0
               weekly_weight_tuple[key2+"%d"%second_posn]="%s"%e
               second_posn=second_posn+1
                                                                                                                                                                             
                                                                                                                                                                             
               weekly_weight_tuple[key2+"%d"%second_posn]=-1
               second_posn=0 
               if first_posn<10:
                    key1="R0"
               else:
                    key1="R"
                                                                                                                                            
               weight_tuples[key1+"%d"%first_posn]=weekly_weight_tuple
                                                                                                                                          
               first_posn=first_posn+1 
               weekly_weight_tuple={}
               return(json.JSONEncoder().encode(weight_tuples))                     
         

     def getThreeMonthsWeight(self,startdate,enddate):
          errorcode={}
          
          monthly_weight_tuple={}
          weekly_weight_tuple=None
          weight_tuples={}
          
          try:
               
               month_start_date=startdate
               month_end_date=self.last_day_of_month(startdate)
               
               key1="R"
               key2="F"
               first_posn=0
               second_posn=0

               weeks_iterator=0
               months_iterator=1
               
               total_monthly_weight=0
            
               weight_tuples={} 
               found_data=0
               
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               
               session = Session()
               
               while ((month_start_date>=startdate) and (month_start_date<=enddate)):
                    
                    monthly_weight_tuple={}
                    weekly_weight_tuple=None
                    total_monthly_weight=0
                    weeks_iterator=0

                    #weekly_weight_tuple=json.loads(self.getMonthlyWeight(month_start_date,month_end_date))
                    #weight=0
                    res = session.query(func.sum(Weight.weight).label("sum_weight")).filter(Weight.beneficiary_id==self.b_id).filter(Weight.datecaptured>=month_start_date).filter(Weight.datecaptured<=month_end_date).order_by(Weight.datecaptured).first()
                    
                    if res.sum_weight==None:
                         pass
                    else:
                         total_monthly_weight=res.sum_weight 
                         
                    
                    res = session.query(func.count(Weight.weight).label("counter")).filter(Weight.beneficiary_id==self.b_id).filter(Weight.datecaptured>=month_start_date).filter(Weight.datecaptured<=month_end_date).order_by(Weight.datecaptured).first()
                    if res.counter==None:
                         pass
                    else:
                         weeks_iterator=res.counter 
                    

                         
                         

                         
                    if total_monthly_weight > 0.0:
                         found_data=found_data+1
                    
                    
                    
                    
                 
                    
                         
                    #weekly_weight_tuple[key2+"%d"%second_posn]="Week %s"%weeks_iterator
                    monthly_weight_tuple[key2+"%d"%second_posn]="%s"%month_start_date.strftime("%m/%Y")
                    second_posn=second_posn+1
                    months_iterator=months_iterator+1
                                                                                                                                                                                  
                                                                                                                                                                                  
                    if(weeks_iterator>0):
                         monthly_weight_tuple[key2+"%d"%second_posn]=total_monthly_weight/weeks_iterator
                         second_posn=0
                    else:
                         monthly_weight_tuple[key2+"%d"%second_posn]=0 
                    
                    
                    if first_posn<10:
                         key1="R0"
                    else:
                         key1="R"
                                                                                                                                                 
                    if weeks_iterator>0:
                         weight_tuples[key1+"%d"%first_posn]=monthly_weight_tuple
                    
                         first_posn=first_posn+1
                         
                    
                    month_start_date=month_end_date+datetime.timedelta(days=1)# move to the begining of next month
                    month_end_date=self.last_day_of_month(month_start_date)# move to the end of next month 
                    
 
                    
                    #if(month_end_date>enddate):
                    #     week_end_date=enddate#for the next iteration     
                    
                    

               session.close()
               engine.dispose()
               dbconn.close()

               if(found_data>0):
                    return(json.JSONEncoder().encode(OrderedDict(sorted(weight_tuples.items(), key=lambda t: t[0]))))
               else:
               
                    #errorcode["error"]=-4
                    weight_tuples={}
                    first_posn=0
                    monthly_weight_tuple[key2+"%d"%second_posn]="There is no weight recorded in a specified period of time"
                    second_posn=second_posn+1
                                                                                                                                                                                  
                                                                                                                                                                                  
                    monthly_weight_tuple[key2+"%d"%second_posn]=-4
                    second_posn=0 
                    if first_posn<10:
                         key1="R0"
                    else:
                         key1="R"
                                                                                                                                                 
                    weight_tuples[key1+"%d"%first_posn]=monthly_weight_tuple
                                                                                                                                               
                    first_posn=first_posn+1 
                    weight_tuple={}
                    return(json.JSONEncoder().encode(OrderedDict(sorted(weight_tuples.items(), key=lambda t: t[0]))))
                    
               
          except Exception as e:
               session.close()
               engine.dispose() 
               dbconn.close()

               
               monthly_weight_tuple[key2+"%d"%second_posn]="%s"%e
               second_posn=second_posn+1
                                                                                                                                                                             
                                                                                                                                                                             
               monthly_weight_tuple[key2+"%d"%second_posn]=-1
               second_posn=0 
               if first_posn<10:
                    key1="R0"
               else:
                    key1="R"
                                                                                                                                            
               weight_tuples[key1+"%d"%first_posn]=monthly_weight_tuple
                                                                                                                                          
               first_posn=first_posn+1 
               monthly_weight_tuple={}
               return(json.JSONEncoder().encode(weight_tuples))          
                 

     
     def getDataPoints(self):
          errorcode={}

          
          # Get data from fields
          try:
               day=self.myjson["Day"] 
               #day="By date"
               #if day=="By date":
                    #startdate=self.myjson["Date1"]
                    #enddate=self.myjson["Date2"]
                    #startdate='2014-02-13'
                    #enddate='2014-02-20' 
               pass
          #except Exception as e:
               #print "Content-Type: text/html\n"
               #print e
               #sys.exit()
          except Exception as e:
               
               weight_tuples={}
               first_posn=0
               monthly_weight_tuple[key2+"%d"%second_posn]=e.message
               second_posn=second_posn+1
                                                                                                                                                                             
                                                                                                                                                                             
               monthly_weight_tuple[key2+"%d"%second_posn]=-1
               second_posn=0 
               if first_posn<10:
                    key1="R0"
               else:
                    key1="R"
                                                                                                                                            
               weight_tuples[key1+"%d"%first_posn]=monthly_weight_tuple
                                                                                                                                          
               first_posn=first_posn+1 
               weight_tuple={}
               return(json.JSONEncoder().encode(OrderedDict(sorted(weight_tuples.items(), key=lambda t: t[0]))))        
               
          
          
          
          #day="This month"
          #startdate="2013-10-01"
          #enddate="2013-10-16"
          
          if day=="This month":
               #from 1st of this month to end of last month
               startdate=self.first_day_of_month(datetime.date.today())
               enddate=self.last_day_of_month(datetime.date.today())
               return self.getMonthlyWeight(startdate,enddate)
               
          elif day=="Last month":
               #from 1st of last month to end of last month
               startdate=self.first_day_of_month(self.first_day_of_month(datetime.date.today())-datetime.timedelta(days=1))
               enddate=self.last_day_of_month(startdate)
               return self.getMonthlyWeight(startdate,enddate)
               
          elif day=="Last three months":
               # go two months back
               first_day_last_month=self.first_day_of_month(self.first_day_of_month(datetime.date.today())-datetime.timedelta(days=1))
               startdate=self.first_day_of_month(first_day_last_month-datetime.timedelta(days=1))# subract 1 day to get to the end of a previous month before last month and get the first day of that month
               enddate=self.last_day_of_month(datetime.date.today())#
               return self.getThreeMonthsWeight(startdate,enddate)
    
               
          
     

#myjson={"Day":"Last three months"}
#obj=PlotWeightGraph(myjson,8)
#result=obj.getDataPoints()
#print result
