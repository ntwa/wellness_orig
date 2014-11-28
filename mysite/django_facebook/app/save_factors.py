#!/usr/bin/env python
import datetime
import sys,json
#sys.path.insert(0, 'C:\\workspace\\test\\helloword\\sqlalchemy.zip')
#sys.path.insert(0, 'sqlalchemy.zip')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wellness.applogic.factor_module import Factors,db,dbconn
from collections import OrderedDict


class ManageFactors:
     def __init__(self,myjson):
          self.myjson=myjson
     def retrieveFactorsFromDB(self):
          result={}
          allow_insert=1
          # Get data from fields
          try:
              
               factor_id=self.myjson["FactorId"] 
               e="Error"
                        
                             
          except Exception as e:
               factors_tuples={}
               factors_tuple={}
     
               key1="R"
               key2="F"
               first_posn=0
               second_posn=0
               factors_tuple[key2+"%d"%second_posn]=e
               second_posn=second_posn+1
                                                                                                                                                                             
                                                                                                                                                                             
               factors_tuple[key2+"%d"%second_posn]=-1
               second_posn=0 
               if first_posn<10:
                    key1="R0"
               else:
                    key1="R"
                                                                                                                                            
               factors_tuples[key1+"%d"%first_posn]=factors_tuple
                                                                                                                                          
               first_posn=first_posn+1 
               factors_tuple={}
               return(json.JSONEncoder().encode(OrderedDict(sorted(factors_tuples.items(), key=lambda t: t[0]))))
          


               
          
          
          
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
                                   
               # querying for a record in the physical_activity pattern table
               res= session.query(Factors).filter(Factors.factor_id==factor_id).first()
               
               factors_tuple={}
               key1="R"
               key2="F"
               first_posn=0
               second_posn=0
               
               if res is None:
                    factors_tuple["TreeFactor"]=0.0
                    second_posn=second_posn+1
                    
                    factors_tuple["FlowerFactor"]=0.0
                    second_posn=0 
                    
               else:

                    factorsrecord=res
                    factors_tuple["TreeFactor"]=factorsrecord.tree_factor
                    second_posn=second_posn+1
                                                                                                                                                                                  
                                                                                                                                                                                  
                    factors_tuple["FlowerFactor"]=factorsrecord.flower_factor
                    second_posn=0 
               
                    

                    first_posn=first_posn+1
                    
               result["R00"]=factors_tuple
                               
                                             
               
                    #result["message"]="The factors arleady existed and they were updated"
                                  
                                   
          except Exception as e:
               session.close()
               engine.dispose()         
               dbconn.close()

               #print "Content-type: text/html\n" 
                                   
               result["R00"]={"D0":"Error: %s"%e,"D1":'-1'}
               #print      
               #sys.exit()
               
          return (json.JSONEncoder().encode(result))
     

     def saveFactorsInDB(self):
          
         
          result={}
          allow_insert=1
          # Get data from fields
          try:
              
               factor_id=self.myjson["FactorId"] 
               tree_factor=self.myjson["TreeFactor"]
               flower_factor=self.myjson["FlowerFactor"]
               e="Error"
                        
                             
          except Exception as e:
               factors_tuples={}
               factors_tuple={}
     
               key1="R"
               key2="F"
               first_posn=0
               second_posn=0
               factors_tuple[key2+"%d"%second_posn]=e
               second_posn=second_posn+1
                                                                                                                                                                             
                                                                                                                                                                             
               factors_tuple[key2+"%d"%second_posn]=-1
               second_posn=0 
               if first_posn<10:
                    key1="R0"
               else:
                    key1="R"
                                                                                                                                            
               factors_tuples[key1+"%d"%first_posn]=factors_tuple
                                                                                                                                          
               first_posn=first_posn+1 
               factors_tuple={}
               return(json.JSONEncoder().encode(OrderedDict(sorted(factors_tuples.items(), key=lambda t: t[0]))))
          


               
          
          
          
          try:
               #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False) 
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
                                   
               # querying for a record in the physical_activity pattern table
               res= session.query(Factors).filter(Factors.factor_id==factor_id).first()
               if res is None:
                    pass
               else:
                    factorsrecord=res
                    if(factorsrecord.tree_factor!=tree_factor):
                         factorsrecord.tree_factor=tree_factor
                    if factorsrecord.flower_factor!=flower_factor:
                         factorsrecord.flower_factor=flower_factor
                                
                                             
                    allow_insert=0
                    
                    session.commit()
                    result["message"]="The factors arleady existed and they were updated"
                                  
                                   
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
                    new_factors=Factors(factor_id,tree_factor,flower_factor)
                         
                    session.add(new_factors)
               
               
                    # commit the record the database
               
               
                    session.commit()
                    result["message"]="The factors were recorded successfully"
                    
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
     
#obj=SavePoints(1)
#result=obj.savePointsInDB()
#print result
