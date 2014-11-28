#!/usr/bin/env python
import datetime
import sys,json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections import OrderedDict
import md5
from wellness.applogic.intermediary_module import Intermediary,db
#from django.contrib.sessions.backends.db import SessionStore

class Authentication:
                 
          def __init__(self,myjson,request):
                    self.myjson=myjson
                    self.sessionvar=request.session
                    
                    
          def resetSession(self):
                    try:
                              del self.sessionvar['username']
                              del self.sessionvar['passwd']
                    except Exception as e:
                              pass
                    #s=SessionStore(session_key='uno-such-session-here')
                    #s=SessionStore(session_key='username')
                    #s.save()
                    #s.flush()
                    
                    
                    #s['passwd']
                    #if((s['passwd']) and (s['username'])):
                    #          pass
                    #          del s['username']
                    #          del s['passwd']
                    #pass
                    
                   
          def authenticateAdmin(self):
          
                    errorcode={}
                    result={}
                    
                    #u = SessionStore(session_key='username')
                    #p = SessionStore(session_key='passwd')
                    #u.save()
                    #p.save()
                    #s=SessionStore(session_key='uno-such-session-here')
                    #s.save()
                    
                    # Get data from fields
                    try:
                              username=self.myjson["Username"]
                              passwd=self.myjson["Password"]
                              #recordeddate=datetime.date(2014,02,13)
                    except Exception as e:
                              errorcode["error"]=e.message
                              return(json.JSONEncoder().encode(errorcode))         
               
         
               
                    try:
                                             
                              #engine=create_engine('mysql://root:ugnkat@localhost/wellness', echo=False)
                              engine=db
                              # create a Session
                              Session = sessionmaker(bind=engine)
                                                  
                              session = Session()
                              
                              m=md5.new(passwd)
                              passwd=m.hexdigest()
                              
                              
                              prevusername=username
                              prevpasswd=passwd
                           
                              try:
                                        
                                        #if(self.sessionvar['username'])
                                        #del self.sessionvar['username']
                                        #del self.sessionvar['passwd']                                        
                                        username=self.sessionvar['username']
                                        passwd=self.sessionvar['passwd']
                                        #pass
                              except Exception as e:
                                        username=prevusername
                                        passwd=prevpasswd

                                                  
                             
                              res = session.query(Intermediary).filter(Intermediary.intermediary_id==username).filter(Intermediary.passwd==passwd).first()
                              #res = session.query(UserAdmin).filter(UserAdmin.username==username).first()
                              
                              
                              if res is None:
                                        result["authentication"]=0
                                        
                              else:
                                        result["authentication"]=1
                                        try:
                                                  
                                        
                                                  #pass

                                                  self.sessionvar['username']=username
                                                  self.sessionvar['passwd']=passwd
                                        except Exception as e:
                                                  pass
                                                  
                                                  
                                                        
                                                          
                                                                             
                                     
                              session.close() 
                              engine.dispose()
                              return(json.JSONEncoder().encode(result))
                                                  
                    except Exception as e:
                              session.close()
                              engine.dispose()  
                              result["authentication"]=e 
                              return (json.JSONEncoder().encode(result))                      


#myjson={"Username":"admin","Password":"ugnkat"}
#obj=Authentication(myjson)
#msg=obj.authenticateAdmin()
#print msg
