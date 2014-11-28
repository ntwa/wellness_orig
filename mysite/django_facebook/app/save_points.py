#!/usr/bin/env python
import datetime
import sys,json
#sys.path.insert(0, 'C:\\workspace\\test\\helloword\\sqlalchemy.zip')
#sys.path.insert(0, 'sqlalchemy.zip')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.points_module import Points,db,dbconn
from collections import OrderedDict


class SavePoints:
     def __init__(self,myjson,intermediary_id):
          self.myjson=myjson
          self.intermediary_id=intermediary_id
     def savePointsInDB(self):
          
          datecaptured=""
          points=0
          result={}
          allow_insert=1
          # Get data from fields
          try:
              
               points=self.myjson["Points"] #every data update or data retrieval is awarded three extra bonus points. 
               #points=40
               datecaptured = datetime.date.today()
               e="Error"
                        
                             
          except Exception as e:
               points_tuples={}
               points_tuple={}
     
               key1="R"
               key2="F"
               first_posn=0
               second_posn=0
               points_tuple[key2+"%d"%second_posn]=e
               second_posn=second_posn+1
                                                                                                                                                                             
                                                                                                                                                                             
               points_tuple[key2+"%d"%second_posn]=-1
               second_posn=0 
               if first_posn<10:
                    key1="R0"
               else:
                    key1="R"
                                                                                                                                            
               points_tuples[key1+"%d"%first_posn]=points_tuple
                                                                                                                                          
               first_posn=first_posn+1 
               points_tuple={}
               return(json.JSONEncoder().encode(OrderedDict(sorted(points_tuples.items(), key=lambda t: t[0]))))
          


               
          
          
          
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
                                   
               # querying for a record in the physical_activity pattern table
               res= session.query(Points).filter(Points.intermediary_id==self.intermediary_id).filter(Points.datecaptured==datecaptured).first()
               if res is None:
                    pass
               else:
                    pointsrecord=res
                    previouspoints=pointsrecord.scoredpoints
                    pointsrecord.scoredpoints=previouspoints+points#increment existing points
                                
                                             
                    allow_insert=0
                    
                    session.commit()
                    result["message"]="The points for this date existed and it was updated from %s points to %s points"%(previouspoints,(points+previouspoints))
                                  
                                   
          except Exception as e:
               session.close()
               engine.dispose()         
               dbconn.close()
               #print "Content-type: text/html\n" 
                                   
               result["message"]="Error: %s"%e
               #print      
               return (json.JSONEncoder().encode(result))
               #sys.exit()
                                         
                         
                         
          if allow_insert==1:
               try:
                    #print "Content-Type: text/html\n"
                    #engine=db
                    # create a Session
                    #Session = sessionmaker(bind=engine)
               
                    #session = Session()
               
                    # Create weight
                    #new_food=FoodAndBeverage('KTLNTW00',datetime.date(1988,12,01))
                    new_points=Points(self.intermediary_id,points,datecaptured)
                         
                    session.add(new_points)
               
               
                    # commit the record the database
               
               
                    session.commit()
                    result["message"]="The points were recorded successfully"
                    
               except Exception as e:
                    session.close()
                    engine.dispose()
                    dbconn.close()
                    result["message"]=e
                    return (json.JSONEncoder().encode(result)) 
          
          session.close()
          engine.dispose()        
          dbconn.close()  
          return (json.JSONEncoder().encode(result))
     
#myjson={"Points":4}
#obj=SavePoints(myjson,"katulentwa@gmail.com")
#result=obj.savePointsInDB()
#print result
     
#obj=SavePoints(1)
#result=obj.savePointsInDB()
#print result
