#!/usr/bin/env python
import datetime,calendar
import sys,json
from sqlalchemy import create_engine,distinct,func
from sqlalchemy.orm import sessionmaker
from wellness.applogic.activity_module import PhysicalActivity,db,dbconn
from collections import OrderedDict


class PlotActivityGraph:
     def __init__(self,myjson,b_id):
          self.myjson=myjson
          self.b_id=b_id
     
     
     def timeDiff(self,time1,time2):
          timeA = datetime.datetime.strptime(time1, "%H:%M")
          timeB = datetime.datetime.strptime(time2, "%H:%M")
          newTime = timeA - timeB
          return newTime.seconds/3600 
     
     def first_day_of_month(self,d):
          return datetime.date(d.year, d.month, 1)
     def last_day_of_month(self,d):
          t=(calendar.monthrange(d.year,d.month))
          return datetime.date(d.year,d.month,t[1])
     
     def month_num_days(self,d):
          t=(calendar.monthrange(d.year,d.month))
          return t[1]    
     
     


     def get_daily_steps(self,startdate,enddate):
          
          errorcode={}
          activity_tuple={}
          activity_tuples={}
         
          engine=db
          #create a Session
          Session = sessionmaker(bind=engine)
          session = Session()          

          key1="R"
          key2="F"
          first_posn=0
          second_posn=0 


          try:
               
               #engine=db
               #create a Session
               #Session = sessionmaker(bind=engine)
               #session = Session()
               
               
              # key1="R"
              # key2="F"
              # first_posn=0
               #second_posn=0
               
               counted_dates=0
               
            
               
               
               step_sum_by_date=0
               #activity_tuple={}
              # activity_tuples={} 
               
               # count if there are distinct dates.
               counted_dates=session.query(func.count(distinct(PhysicalActivity.datecaptured))).filter(PhysicalActivity.beneficiary_id==self.b_id).filter(PhysicalActivity.datecaptured>=startdate).filter(PhysicalActivity.datecaptured<=enddate).order_by(PhysicalActivity.datecaptured).first()
               
               
               
               
               retrieved_dates_counter=0# initialize how many distinct dates are in the database
               for retrieved_dates_counter in counted_dates:
                    break
          
               
               if retrieved_dates_counter==0:
                    #errorcode["error"]=-4
                    activity_tuple[key2+"%d"%second_posn]="12AM-12AM"
                    second_posn=second_posn+1
                                                                                                                                                                                  
                                                                                                                                                                                  
                    activity_tuple[key2+"%d"%second_posn]=-4
                    second_posn=0
                    if first_posn<10:
                         key1="R0"
                    else:
                         key1="R"
                                                                                                                                                 
                    activity_tuples[key1+"%d"%first_posn]=activity_tuple
                                                                                                                                               
                    first_posn=first_posn+1 
                    activity_tuple={}
                    return(json.JSONEncoder().encode(activity_tuples))               
                    
               
               

               res = session.query(PhysicalActivity).filter(PhysicalActivity.beneficiary_id==self.b_id).filter(PhysicalActivity.datecaptured>=startdate).filter(PhysicalActivity.datecaptured<=enddate).order_by(PhysicalActivity.datecaptured).order_by(PhysicalActivity.starttimecaptured).all()
               
               
               #query result within time clusters of one date
               if retrieved_dates_counter<2 and retrieved_dates_counter>0 and startdate==enddate: #The condition startdate==enddate prevents a weeks with only one day of activities to be splitted into time intervals.
                    time_clusters_str=['12AM-6AM','6AM-12PM','12PM-6PM','6PM-12AM']
                              
                    steps_on_time_clusters=[0,0,0,0]
                              
                    #time_clusters=[['00:00','03:59'],['04:00','07:59'],['08:00','11:59'],['12:00','15:59'],['16:00','19:59'],['20:00','23:59']]
                              
                    end_time_clusters=['05:59','11:59','17:59','23:59']
                              
                    time_clusters_counter=0
                    time_space_counter=0# for keeping track of time clustera                      
                                       
                    
                    # find which activity falls under a particular time cluster and add them together
                    for end_time_cluster in end_time_clusters:
                         activity_tuple={}                     
                         for activity in res:
                              initial_time=datetime.datetime.strptime(end_time_cluster, "%H:%M")-datetime.timedelta(hours=6)+datetime.timedelta(minutes=1)# get start time for time cluster. We add one minute at the end becuase we want start time to begin with 0 minutes
                              final_time=datetime.datetime.strptime(end_time_cluster, "%H:%M")
                              
                              # now lets get the time from the database and compare if it is within range of start time and end time
                              
                              activity_time=datetime.datetime.strptime(activity.starttimecaptured, "%H:%M")
                              
                              
                              #comparing if start time of an activity is within a specific time cluster 
                              if activity_time>=initial_time and activity_time<final_time:
                                   steps_on_time_clusters[time_space_counter]=steps_on_time_clusters[time_space_counter]+activity.stepscounter #add all the time that belong to one cluster
                                   
                         #print steps_on_time_clusters[time_space_counter]
                         
                         activity_tuple[key2+"%d"%second_posn]=time_clusters_str[time_space_counter]
                         second_posn=second_posn+1
                                                                                                                                                                                       
                         #activity_tuple[key2+"%d"%second_posn]=activity.starttimecaptured
                         #second_posn=second_posn+1
                                                                                                                                                                                  
                         #activity_tuple[key2+"%d"%second_posn]=activity.endtimecaptured
                         #second_posn=second_posn+1  
                                                                                                                                                                                       
                         activity_tuple[key2+"%d"%second_posn]=steps_on_time_clusters[time_space_counter]
                         second_posn=0 
                         if first_posn<10:
                              key1="R0"
                         else:
                              key1="R"
                                                                                                                                                      
                         activity_tuples[key1+"%d"%first_posn]=activity_tuple
                                                                                                                                                    
                         first_posn=first_posn+1                                
                                              
                         
                         time_space_counter=time_space_counter+1
         
                         
                         
                                      
               session.close() 
               engine.dispose()
               dbconn.close()
               return(json.JSONEncoder().encode(OrderedDict(sorted(activity_tuples.items(), key=lambda t: t[0]))))
               
          except Exception as e:
               session.close()
               engine.dispose()
               dbconn.close() 
               second_posn=0
               #errorcode["error"]=e     
               #return (json.JSONEncoder().encode(errorcode))
               #return errorcode
               activity_tuple[key2+"%d"%second_posn]="%s"%e
               second_posn=second_posn+1
                                                                                                                                                                             
                                                                                                                                                                             
               activity_tuple[key2+"%d"%second_posn]=-1
               second_posn=0 
               if first_posn<10:
                    key1="R0"
               else:
                    key1="R"
                                                                                                                                            
               activity_tuples[key1+"%d"%first_posn]=activity_tuple
                                                                                                                                          
               first_posn=first_posn+1 
               activity_tuple={}
               return(json.JSONEncoder().encode(activity_tuples)) 
     
     
     
     
     def get_weekly_steps(self,startdate,enddate):
          
          errorcode={}
          daily_activity_tuple={}
          first_posn=0
          second_posn=0
          key1="R"
          key2="F"
          activity_tuples={} 
          
          engine=db
          #create a Session
          Session = sessionmaker(bind=engine)
          session = Session()

          try:
               
          
               #first_posn=0
               #second_posn=0
               #previousdate_string=None
               current_retrieved_date_string=""
               
               
               step_sum_by_date=0
               
        
               #activity_tuples={} 
               #current_date_searched=startdate
               #number_of_tuples_counted=0
               #week_num_of_days=7 # the week has seven days. We will use this variable to determine if the total number of dates counted from the database is less than number of days in week
               num_of_weekdays_iterated=0# keeping track of the positiion within a seven days week.          
               weekdays_clusters=['Mon','Tue','Wed','Thur','Frid','Sat','Sun']
               
               #weekday=enddate.weekday()# is for checking if a week is shorter when this function is used by get_manth_data
               
               found_data=0
               day=""
               #engine=db
               #create a Session
               #Session = sessionmaker(bind=engine)
               #session = Session()
               
               #new code
               daily_activity_tuple={}
               while(startdate<=enddate):
                        
                    day_of_week=startdate.weekday()     
                          
                    day=weekdays_clusters[day_of_week]
               
               #for week_day in weekdays_clusters:
                    #activity_tuple=json.loads(self.get_daily_steps(startdate, startdate))
                    daily_activity_tuple={}
                    hourly_activity_tuple=None
                    total_daily_steps=0
                    
                              
                    #activity_tuple=json.JSONDecoder.decode(self.get_daily_steps(startdate, startdate))
                    #activity_tuple=json.JSONDecoder.decode(self.get_daily_steps(startdate, startdate), _w=WHITESPACE.match)
                    #hourly_activity_tuple=json.loads(self.get_daily_steps(startdate, startdate))
                    
                    
                    
                    
                    
                    
                    #exception_info=""
                    
                    #steps=0
                    
                    res=session.query(func.sum(PhysicalActivity.stepscounter).label("sum_steps")).filter(PhysicalActivity.beneficiary_id==self.b_id).filter(PhysicalActivity.datecaptured==startdate).order_by(PhysicalActivity.datecaptured).first()
                    if res.sum_steps==None:
                         pass
                    else:
                         total_daily_steps=int(res.sum_steps)
                         
                         
                    startdate=startdate+datetime.timedelta(days=1)#move to the next day
                    

                         
                    if total_daily_steps > 0:
                         found_data=found_data+1
                    
                         
                         
                    daily_activity_tuple[key2+"%d"%second_posn]=day
                    second_posn=second_posn+1
                    
                                                                                                                                                                                  
                                                                                                                                                                                  
                    daily_activity_tuple[key2+"%d"%second_posn]=total_daily_steps
                    second_posn=0
                    
                    
                    if first_posn<10:
                         key1="R0"
                    else:
                         key1="R"
                                                                                                                                                 
                    activity_tuples[key1+"%d"%first_posn]=daily_activity_tuple
                    
                    first_posn=first_posn+1
                    total_daily_steps=0
                    
                    #if(num_of_weekdays_iterated==weekday):# we have encontered the end of the week. This is for shorter weeks within the month
                    #     break
                    #num_of_weekdays_iterated=num_of_weekdays_iterated+1     
               
               
               
               
               #end of new code
               
               session.close()
               engine.dispose()
               dbconn.close()
                 
               if(found_data > 0):
                    return(json.JSONEncoder().encode(OrderedDict(sorted(activity_tuples.items(), key=lambda t: t[0]))))
               else:
                    #errorcode["error"]=-4
                    activity_tuples={}
                    first_posn=0
                    daily_activity_tuple[key2+"%d"%second_posn]="No day"
                    second_posn=second_posn+1
                                                                                                                                                                                  
                                                                                                                                                                                  
                    daily_activity_tuple[key2+"%d"%second_posn]=-4
                    second_posn=0 
                    if first_posn<10:
                         key1="R0"
                    else:
                         key1="R"
                                                                                                                                                 
                    activity_tuples[key1+"%d"%first_posn]=daily_activity_tuple
                                                                                                                                               
                    first_posn=first_posn+1 
                    activity_tuple={}
                    return(json.JSONEncoder().encode(OrderedDict(sorted(activity_tuples.items(), key=lambda t: t[0]))))  

                    #return (json.JSONEncoder().encode(errorcode))                    
                                     
               
               
          except Exception as e:
               session.close()
               engine.dispose()
               dbconn.close() 
               second_posn=0
                    
               daily_activity_tuple[key2+"%d"%second_posn]="%s"%e
               second_posn=second_posn+1
                                                                                                                                                                             
                                                                                                                                                                             
               daily_activity_tuple[key2+"%d"%second_posn]=-1
               second_posn=0 
               if first_posn<10:
                    key1="R0"
               else:
                    key1="R"
                                                                                                                                            
               activity_tuples[key1+"%d"%first_posn]=daily_activity_tuple
                                                                                                                                          
               first_posn=first_posn+1 
               daily_activity_tuple={}
               return(json.JSONEncoder().encode(activity_tuples)) 
     
     
     
     
     def get_monthly_steps(self,startdate,enddate):
          errorcode={}
          key1="R"
          key2="F"
          first_posn=0
          second_posn=0
          weekly_activity_tuple={}
          activity_tuples={} 

          engine=db
          #create a Session
          Session = sessionmaker(bind=engine)
          session = Session()

          print startdate,enddate

          try:
               
               day_of_week = startdate.weekday()
               week_start_date=startdate    
               #week_end_date=(startdate-datetime.timedelta(days=day_of_week))+datetime.timedelta(days=6)
               week_end_date=startdate+datetime.timedelta(days=6)
             
               
                         
                            
               
               #key1="R"
               #key2="F"
               #first_posn=0
               #second_posn=0

               days_iterator=0
               weeks_iterator=1
               
               total_weekly_steps=0
               
               
               
               #activity_tuples={} 
               found_data=0
               
               


               if(week_end_date>enddate): # make sure week end date is not greater than the current end date 
                    week_end_date=enddate
               
               daily_activity_tuple=None
               weekly_activity_tuple={}
               
                
               engine=db
               #create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               
               while((week_start_date>=startdate) and (week_start_date<=enddate)):
                        
                    weekly_activity_tuple={}
                    daily_activity_tuple=None
                    total_weekly_steps=0
                    
                    if week_end_date<enddate:
                        days_iterator=7
                    else:
                        diff=week_end_date-week_start_date
                        days_iterator=diff.days+1
                    
                    

                   # daily_activity_tuple=json.loads(self.get_weekly_steps(week_start_date,week_end_date))
                    #steps=0
                    res=session.query(func.sum(PhysicalActivity.stepscounter).label("sum_steps")).filter(PhysicalActivity.beneficiary_id==self.b_id).filter(PhysicalActivity.datecaptured>=week_start_date).filter(PhysicalActivity.datecaptured<=week_end_date).order_by(PhysicalActivity.datecaptured).first()
                    if res.sum_steps==None:
                         pass
                    else:
                         total_weekly_steps=int(res.sum_steps)
                         
                    
                         
                    if total_weekly_steps > 0:
                         found_data=found_data+1                     
              
                    
                 
                    
                         
                    #weekly_activity_tuple[key2+"%d"%second_posn]="Week %s"%weeks_iterator
                    weekly_activity_tuple[key2+"%d"%second_posn]="%s-%s"%(week_start_date.strftime("%d"),week_end_date.strftime("%d"))
                    second_posn=second_posn+1
                    weeks_iterator=weeks_iterator+1
                                                                                                                                                                                  
                                                                                                                                                                                  
                    if(days_iterator>0):
                         weekly_activity_tuple[key2+"%d"%second_posn]=total_weekly_steps/days_iterator
                         second_posn=0
                    else:
                         weekly_activity_tuple[key2+"%d"%second_posn]=0 
                         second_posn=0
                    
                    
                    if first_posn<10:
                         key1="R0"
                    else:
                         key1="R"
                                                                                                                                                 
                    activity_tuples[key1+"%d"%first_posn]=weekly_activity_tuple
                    
                    first_posn=first_posn+1
                    
                    
                    week_start_date=week_end_date+datetime.timedelta(days=1)# move to next monday
                    week_end_date=week_start_date+datetime.timedelta(days=6)# move to next sunday 
                    
 
                    
                    if(week_end_date>enddate):
                         week_end_date=enddate#for the next iteration     
                    
              

    
               session.close()
               engine.dispose()
               dbconn.close()

               if(found_data>0):
                    return(json.JSONEncoder().encode(OrderedDict(sorted(activity_tuples.items(), key=lambda t: t[0]))))
               
       
               
                    #errorcode["error"]=-4
               activity_tuples={}
               first_posn=0
               weekly_activity_tuple[key2+"%d"%second_posn]="No week"
               second_posn=second_posn+1
                                                                                                                                                                                  
                                                                                                                                                                                  
               weekly_activity_tuple[key2+"%d"%second_posn]=-4
               second_posn=0 
               if first_posn<10:
                    key1="R0"
               else:
                    key1="R"
                                                                                                                                                 
               activity_tuples[key1+"%d"%first_posn]=weekly_activity_tuple
                                                                                                                                               
               first_posn=first_posn+1 
               activity_tuple={}
               return(json.JSONEncoder().encode(OrderedDict(sorted(activity_tuples.items(), key=lambda t: t[0]))))  

              
          except Exception as e:
               session.close()
               engine.dispose()
               dbconn.close()
               
               second_posn=0 
               weekly_activity_tuple[key2+"%d"%second_posn]="%s"%e
               second_posn=second_posn+1
                                                                                                                                                                             
                                                                                                                                                                             
               weekly_activity_tuple[key2+"%d"%second_posn]=-1
               second_posn=0 
               if first_posn<10:
                    key1="R0"
               else:
                    key1="R"
                                                                                                                                            
               activity_tuples[key1+"%d"%first_posn]=weekly_activity_tuple
                                                                                                                                          
               first_posn=first_posn+1 
               weekly_activity_tuple={}
               return(json.JSONEncoder().encode(activity_tuples))
                    
               
      
     
     def getDataPoints(self):
          
          errorcode={}
          
          
          # Get data from form fields
          try:
              #day=self.myjson["Day"] 
               startdate=self.myjson["StartDate"]
               enddate=self.myjson["EndDate"]
               interval=self.myjson["TimeInterval"]

               startdate=datetime.datetime.strptime(startdate , '%Y-%m-%d').date()
               enddate=datetime.datetime.strptime(enddate , '%Y-%m-%d').date()

            
               #pass
               
          #except Exception as e:
               #print "Content-Type: text/html\n"
               #print e
               #sys.exit()
          except Exception as e:
               activity_tuples={}
               activity_tuple={}
     
               key1="R"
               key2="F"
               first_posn=0
               second_posn=0
               activity_tuple[key2+"%d"%second_posn]=e.message
               second_posn=second_posn+1
                                                                                                                                                                             
                                                                                                                                                                             
               activity_tuple[key2+"%d"%second_posn]=-1
               second_posn=0 
               if first_posn<10:
                    key1="R0"
               else:
                    key1="R"
                                                                                                                                            
               activity_tuples[key1+"%d"%first_posn]=activity_tuple
                                                                                                                                          
               first_posn=first_posn+1 
               activity_tuple={}
               return(json.JSONEncoder().encode(OrderedDict(sorted(activity_tuples.items(), key=lambda t: t[0]))))                       
               
          
          
          #day="Today"
          #startdate="2013-12-06"
          #enddate="2013-12-06"
          #intermediary_id=self.sessionvar['username']
          #self.b_id='KTLNTW001'
          
          if   interval=="Daily":
               #startdate = datetime.date.today()
               #enddate = datetime.date.today()
               return self.get_daily_steps(startdate, enddate)               
               
          elif interval=="Weekly":

               return self.get_weekly_steps(startdate, enddate)
     
          elif interval=="Monthly":
           
               return self.get_monthly_steps(startdate,enddate)
     
                  
          activity_tuples={}
          activity_tuple={}

          key1="R"
          key2="F"
          first_posn=0
          second_posn=0
          activity_tuple[key2+"%d"%second_posn]="No data"
          second_posn=second_posn+1
                                                                                                                                                                        
                                                                                                                                                                        
          activity_tuple[key2+"%d"%second_posn]=-4
          second_posn=0 
          if first_posn<10:
               key1="R0"
          else:
               key1="R"
                                                                                                                                       
          activity_tuples[key1+"%d"%first_posn]=activity_tuple
                                                                                                                                     
          first_posn=first_posn+1 
          activity_tuple={}
          return(json.JSONEncoder().encode(OrderedDict(sorted(activity_tuples.items(), key=lambda t: t[0]))))
          
          
                              
          
          
#obj=PlotActivityGraph({"StartDate":"2014-08-31","EndDate":"2014-09-06","TimeInterval":"Weekly"},8)
#res=obj.getDataPoints()
#print res


#obj=PlotActivityGraph({"StartDate":"2014-9-1","EndDate":"2014-9-1","TimeInterval":"Daily"},8)
#res=obj.getDataPoints()
#print res

#obj=PlotActivityGraph({"StartDate":"2015-03-01","EndDate":"2015-03-31","TimeInterval":"Monthly"},1)
#res=obj.getDataPoints()
#print res

