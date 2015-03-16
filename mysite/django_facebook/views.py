from django.http import HttpResponse
from django.contrib.auth import authenticate
from app.retrieve_meals_goal import RetrieveMealsGoal
from app.retrieve_activity_goal import RetrieveActivityGoal
from app.save_weight import SaveWeight
from app.save_meal import SaveMeal
from app.plot_activity_graph import PlotActivityGraph
from app.plot_weight_graph import PlotWeightGraph
from app.plot_meal_graph import PlotMealGraph
from app.retrieve_weight import RetrieveWeight
from app.sync_activity import SyncActivityModule
from app.save_points import SavePoints
from app.save_logs import SaveLogs
from app.authentication_module import Authentication
from app.retrieve_intermediary import RetrieveIntermediary
from app.save_meals_goal import SaveMealsGoal
from app.save_activity_goal import SaveActivityGoal
from app.save_comment import SaveComment
from app.retrieve_points import RetrievePoints
from app.queue_notifications import FacebookNotification
from app.manage_avatars import ManageAvatars
import os
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from collections import OrderedDict

from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import logging
import json,sys,urllib2
import datetime,calendar
from django.contrib.auth import logout
#content = urllib2.urlopen("https://graph.facebook.com/v2.1/?id=http://ict4d01.cs.uct.ac.za/wellness/facebook/example/").read()
#from open_facebook.api import OpenFacebook

#graph = OpenFacebook("my_access_token")

#if there is an error then check if an object is imported above before being used

#view for facebook authentication

logger = logging.getLogger(__name__)

# retrieve meals goals
def retrieveMealGoal(beneficiary_id):
    obj=RetrieveMealsGoal(beneficiary_id)
    goal=obj.getGoal() #the returned goal is an encoded json object    
    return goal
def retrieveActivityGoal(beneficiary_id):
    obj=RetrieveActivityGoal(beneficiary_id)
    goal=obj.getGoal() #the returned goal is an encoded json object
    return goal

def plotActivityGraph(myjson,beneficiary_id):
    obj=PlotActivityGraph(myjson,beneficiary_id)
    datapoints=obj.getDataPoints() #the returned goal is an encoded json object
    return datapoints
    
def plotMealGraph(myjson,beneficiary_id):
    obj=PlotMealGraph(myjson,beneficiary_id)
    datapoints=obj.getDataPoints() #the returned goal is an encoded json object 
    return datapoints
    
def retrieveWeight(myjson,beneficiary_id):
    obj=RetrieveWeight(myjson,beneficiary_id)
    weight=obj.getWeight() #the returned goal is an encoded json object
    return weight

def plotWeightGraph(myjson,beneficiary_id):
    obj=PlotWeightGraph(myjson,beneficiary_id)
    datapoints=obj.getDataPoints() #the returned goal is an encoded json object 
    return datapoints

def retrieveScoreBoard(myjson,intermediary_id):
    obj=RetrievePoints(myjson,intermediary_id,1)
    status=obj.retrieveScoreGardensUrls()
    return status
def retrieveScoreGardens(myjson,intermediary_id):
    result={}
    obj=RetrievePoints(myjson,intermediary_id,1)
    status=obj.retrieveScoreGardensUrls()
    return status
    #result["message"]="Got here"
    #return HttpResponse(json.JSONEncoder().encode(result), mimetype='application/json')
    
def retrieveScoreTanks(myjson,intermediary_id):
    result={}
    obj=RetrievePoints(myjson,intermediary_id,1)
    status=obj.retrieveScoreGardensUrls()
    return status


def retriveAllData(beneficiary_id,intermediary_id):
    
    #capture activities on different days
    activity_tuples={"Today":{},"This week":{},"Last week":{},"This month":{},"Last month":{},"Last three months":{}}
    meals_tuples={"Today":{},"This week":{},"Last week":{},"This month":{},"Last month":{},"Last three months":{}}
    weight_tuples={"This month":{},"Last month":{},"Last three months":{}}
    score_tuples={"Today":{}}
    meals_goal_tuple={"Goal":{}} 
    activity_goal_tuple={"Goal":{}} 
    name_tuple={"Name":{}}
    
    for day,activity_tuple in activity_tuples.iteritems():
        myjson={"Day":day}
        new_tuple=plotActivityGraph(myjson,beneficiary_id)
        temp=json.loads(new_tuple)
        activity_tuples[day]=OrderedDict(sorted(temp.items(), key=lambda t: t[0]))
    
        
    for day,meals_tuple in meals_tuples.iteritems():
        myjson={"Day":day}
        new_tuple=plotMealGraph(myjson,beneficiary_id)
        temp=json.loads(new_tuple)
        meals_tuples[day]=OrderedDict(sorted(temp.items(), key=lambda t: t[0]))
        
    for day,weight_tuple in weight_tuples.iteritems():
        myjson={"Day":day}
        new_tuple=plotWeightGraph(myjson,beneficiary_id)
        temp=json.loads(new_tuple)
        weight_tuples[day]=OrderedDict(sorted(temp.items(), key=lambda t: t[0]))        
        
      
    for day,score_tuple in score_tuples.iteritems():
        myjson={"Day":day}
        new_tuple=retrieveScoreBoard(myjson,intermediary_id)
        temp=json.loads(new_tuple)
        score_tuples[day]=OrderedDict(sorted(temp.items(), key=lambda t: t[0]))
        
        
    for goal,meals_goal in meals_goal_tuple.iteritems():
        new_tuple=retrieveMealGoal(beneficiary_id)
        temp=json.loads(new_tuple)
        meals_goal_tuple[goal]=OrderedDict(sorted(temp.items(), key=lambda t: t[0]))
    
    for goal,activity_goal in activity_goal_tuple.iteritems():
        new_tuple=retrieveActivityGoal(beneficiary_id)
        temp=json.loads(new_tuple)
        activity_goal_tuple[goal]=OrderedDict(sorted(temp.items(), key=lambda t: t[0]))
    
    alldata={}
    
    alldata["Activity"]=activity_tuples
    alldata["Meals"]=meals_tuples
    alldata["Weight"]=weight_tuples
    alldata["MealsGoal"]=meals_goal_tuple
    alldata["ActivityGoal"]=activity_goal_tuple
    alldata["ScoreBoard"]=score_tuples
    
    return(json.JSONEncoder().encode(OrderedDict(sorted(alldata.items(), key=lambda t: t[0]))))
    


@csrf_exempt
def fishtank(request,command_id):
    #myjsonpoints={"points":3}
    #myjsonclickscounter={"clickscounter":1}
    return example(request)

@csrf_exempt
def garden(request,command_id):
    #myjsonpoints={"points":3}
    #myjsonclickscounter={"clickscounter":1}
    return example(request)


@csrf_exempt
def dataloader(request,command_id):
    #myjsonpoints={"points":3}
    #myjsonclickscounter={"clickscounter":1}
    
     
    try:
        try:
            
            #intermediary_id=request.session['username']
            if request.user.is_authenticated():
                intermediary_id=request.user.username
                intermediary_id=intermediary_id.replace(".","")   
                #if intermediary_id=="ntwakatule":
                #    intermediary_id="katulentwa@gmail.com"
            else:
                raise Exception("Access denied")
                
                
        except Exception as e:
            result={}
            result["R00"]={'F1':-6,'F0':e}# a code used when a beneficiary doesn't exist
            status=json.JSONEncoder().encode(result)
            status=json.JSONEncoder().encode(result)
            return HttpResponse(status, mimetype='application/json')
            
        
        #myjson=json.loads(request.body)
        myjson={'Username':intermediary_id}
        obj=RetrieveIntermediary(myjson)
        status=obj.isAssignedBeneficiary()
        status=json.loads(status)
        beneficiary_id=status["Id"]
        #return HttpResponse(status, mimetype='application/json') 
        
    except Exception as e: 
        beneficiary_id=None 
        #result={}
        activity_tuples={"Today":{},"This week":{},"Last week":{},"This month":{},"Last month":{},"Last three months":{}}
        meals_tuples={"Today":{},"This week":{},"Last week":{},"This month":{},"Last month":{},"Last three months":{}}
        weight_tuples={"This month":{},"Last month":{},"Last three months":{}}
        score_tuples={"Today":{},"This week":{},"Last week":{},"This month":{},"Last month":{},"Last three months":{}}
        meals_goal_tuple={"Goal":{}} 
        activity_goal_tuple={"Goal":{}} 

        for day,activity_tuple in activity_tuples.iteritems():
            result={}
            result["R00"]={'F1':-5,'F0':"You don't have a family member assigned to your account"}
            temp=result
            activity_tuples[day]=OrderedDict(sorted(temp.items(), key=lambda t: t[0]))
        
            
        for day,meals_tuple in meals_tuples.iteritems():
            result={}
            myjson={"Day":day}
            result["P00"]={'D1':-5,'D0':"You don't have a family member assigned to your account"}
            temp=result
            meals_tuples[day]=OrderedDict(sorted(temp.items(), key=lambda t: t[0]))
            
        for day,weight_tuple in weight_tuples.iteritems():
            result={}
            myjson={"Day":day}
            result["R00"]={'F1':-5,'F0':"You don't have a family member assigned to your account"}
            temp=result
            weight_tuples[day]=OrderedDict(sorted(temp.items(), key=lambda t: t[0]))        
            
          
        for day,score_tuple in score_tuples.iteritems():
            result={}
            myjson={"Day":day}
            result["R00"]={'D1':-5,'D0':"You don't have any beneficiary assigned to you. You can't be part of this game"}
            temp=result
            score_tuples[day]=OrderedDict(sorted(temp.items(), key=lambda t: t[0]))
            
            
        for goal,meals_goal in meals_goal_tuple.iteritems():
            result={}
            result["Starch"]="None"
            result["Fruits"]="None"
            result["Fat"]="None"
            result["Protein"]="None"
            result["Dairy"]="None" 
            temp=result
            meals_goal_tuple[goal]=OrderedDict(sorted(temp.items(), key=lambda t: t[0]))
        
        for goal,activity_goal in activity_goal_tuple.iteritems():
            result={}
            result["Goal"]={'Steps':-5}
            temp=result
            activity_goal_tuple[goal]=OrderedDict(sorted(temp.items(), key=lambda t: t[0]))
        
        alldata={}
        
        alldata["Activity"]=activity_tuples
        alldata["Meals"]=meals_tuples
        alldata["Weight"]=weight_tuples
        alldata["MealsGoal"]=meals_goal_tuple
        alldata["ActivityGoal"]=activity_goal_tuple
        alldata["ScoreBoard"]=score_tuples
        
        status=(json.JSONEncoder().encode(OrderedDict(sorted(alldata.items(), key=lambda t: t[0]))))

        return HttpResponse(status, mimetype='application/json')
    
    
    

    try:
        myjson=json.loads(request.body)
        obj=SavePoints(myjson,intermediary_id)
        status=obj.savePointsInDB()
        
        obj=SaveLogs(myjson,intermediary_id)
        status=obj.saveLogsInDB()
        #return HttpResponse(status, mimetype='application/json')
    except Exception as e:
        #errorcode={}
        #errorcode["error"]=e.message
        #status=json.JSONEncoder().encode(errorcode)
        #return HttpResponse(status, mimetype='application/json')
        pass
    
    if command_id =="RAD":
        alldata=retriveAllData(beneficiary_id,intermediary_id)
        return HttpResponse(alldata, mimetype='application/json')
    
    elif command_id =="RMG":
        #RMG means retrieve meals goal
        goal=retrieveMealGoal(beneficiary_id)
        return HttpResponse(goal, mimetype='application/json')

    elif command_id =="RAG":
        #RAG means retrieve activity goal
        goal=retrieveActivityGoal(beneficiary_id)
        return HttpResponse(goal, mimetype='application/json') 
    
    elif command_id =="PAG":
        #PAG means plot activity graph
        myjson =json.loads(request.body)  
        datapoints=plotActivityGraph(myjson,beneficiary_id)
        return HttpResponse(datapoints, mimetype='application/json')
    
    elif command_id == "PMG":
        #PMG means plot meal graph or chart
        myjson =json.loads(request.body)  
        datapoints=plotMealGraph(myjson,beneficiary_id)
        return HttpResponse(datapoints, mimetype='application/json')        
    
    elif command_id =="RW":
        #RW means retrieve weight
        myjson =json.loads(request.body)  
        weight=retrieveWeight(myjson,beneficiary_id)
        return HttpResponse(weight, mimetype='application/json')
    
    elif command_id =="PWG":
        #WG means plot activity graph
        myjson =json.loads(request.body)  
        datapoints=plotWeightGraph(myjson,beneficiary_id)
        return HttpResponse(datapoints, mimetype='application/json')
    elif command_id=="RSB":
        #Retrieve score board
        #myjson={"Username":intermediary_id,"Day":"Last week"}
        myjson =json.loads(request.body) 
        status=retrieveScoreBoard(myjson,intermediary_id)
        return HttpResponse(status, mimetype='application/json')
    elif command_id=="RSG":
        #result={}
        #Retrieve score gardens
        #myjson={"Day":"Today"}

        #myjson =json.loads(request.body) 
        status=retrieveScoreGardens(myjson,intermediary_id)
        return HttpResponse(status, mimetype='application/json')
        #result["message"]="Got here%s"%intermediary_id
        #return HttpResponse(json.JSONEncoder().encode(result), mimetype='application/json')
    elif command_id=="RST":
        #result={}
        #Retrieve score gardens
        #myjson={"Day":"Today"}

        #myjson =json.loads(request.body) 
        status=retrieveScoreGardens(myjson,intermediary_id)
        return HttpResponse(status, mimetype='application/json')

    elif command_id=="GAAV":
        myjson={"IntermediaryId":intermediary_id}
        obj=ManageAvatars(myjson)
        status=obj.getAllAvatars()
        
        return HttpResponse(status, mimetype='application/json')

        
        


def saveWeight(myjson,beneficiary_id):
    obj=SaveWeight(myjson,beneficiary_id)
    status=obj.saveWeightInDB() #the returned status is an encoded json object  
    return status 

def saveMeal(myjson,beneficiary_id):
    obj=SaveMeal(myjson,beneficiary_id)
    status=obj.saveMealInDB()#the returned status is an encoded json object  
    return status

def uploadActivity(myjson):
    obj=SyncActivityModule(myjson)
    status=obj.uploadActivity()
    return status

def saveComment(myjson,beneficiary_id):
    obj=SaveComment(myjson,beneficiary_id)
    status=obj.saveCommentInDB()
    return status

def saveActivityGoal(myjson,beneficiary_id):
    obj=SaveActivityGoal(myjson,beneficiary_id)
    status=obj.saveGoal()
    return status

def saveMealsGoal(myjson,beneficiary_id):
    obj=SaveMealsGoal(myjson,beneficiary_id)
    status=obj.saveGoal()
    return status

def queueNotification(myjson,beneficiary_id):
    obj=FacebookNotification(myjson,beneficiary_id)
    status=obj.queueNotification()
    return status

def saveTeamName(myjson):
    obj=RetrieveIntermediary(myjson)
    status=obj.saveTeamName()
    return status

def saveAvatar(myjson):
    obj=ManageAvatars(myjson)
    status=obj.setAvatar()
    return status

    




@csrf_exempt
def dataupdate(request,command_id):
      
    try:
             
        
        #myjson=json.loads(request.body)
        if request.user.is_authenticated():
            intermediary_id=request.user.username
            intermediary_id=intermediary_id.replace(".","") 
            #if intermediary_id=="ntwakatule":
            #    intermediary_id="katulentwa@gmail.com"
        else:
            result={}
            result["R00"]={'F1':-6,'F0':"Access denied"}# a code used when an intermediary is not logged in
            status=json.JSONEncoder().encode(result)
            status=json.JSONEncoder().encode(result)
            if command_id =="SA":
                pass# This is an upload from a pedometer. 
            else:
                return HttpResponse(status, mimetype='application/json')   
         
        myjson={'Username':intermediary_id}
       
        obj=RetrieveIntermediary(myjson)
        status=obj.isAssignedBeneficiary()
        status=json.loads(status)
        beneficiary_id=status["Id"]
        #return HttpResponse(status, mimetype='application/json') 
        
    except Exception as e: 
        beneficiary_id=None 
        result={}
        message="iYou don't have a family member assigned to your account"
        #message=e.message
        result["R00"]={'F1':-5,'F0':message}# a code used when a beneficiary doesn't exist
        status=json.JSONEncoder().encode(result)
        status=json.JSONEncoder().encode(result)
        if command_id =="SA":
            pass# This is an upload from a pedometer.
        else:
            return HttpResponse(status, mimetype='application/json')
    
  
    try:
        myjson=json.loads(request.body)
        obj=SavePoints(myjson)
        status=obj.savePointsInDB()
        
        obj=SaveLogs(myjson)
        status=obj.saveLogsInDB()
        #return HttpResponse(status, mimetype='application/json')
    except Exception as e:
        #errorcode={}
        #errorcode["error"]=e.message
        #status=json.JSONEncoder().encode(errorcode)
        #return HttpResponse(status, mimetype='application/json')
        pass
    
          
    
    if command_id =="SW":
        #SW means retrieve save weight
        myjson =json.loads(request.body)
        status=saveWeight(myjson,beneficiary_id)
        return HttpResponse(status, mimetype='application/json')
    
    elif command_id == "SM":
        #result={}
        #SM means save meal
        myjson =json.loads(request.body)
        status=saveMeal(myjson,beneficiary_id) 
        return HttpResponse(status, mimetype='application/json') 

        #result["message"]="The food was recorded sucessfully"
        #return HttpResponse(json.JSONEncoder().encode(result), mimetype='application/json')
        
    elif command_id =="SA":
        
        myjson=json.loads(request.body)
        status=uploadActivity(myjson)
        return HttpResponse(status, content_type='application/json')
    
    elif command_id =="SC":
        
        myjson=json.loads(request.body)
        status=saveComment(myjson,beneficiary_id)
        return HttpResponse(status, content_type='application/json')
         
    
    elif command_id == "SAG":
        myjson=json.loads(request.body)
        status=saveActivityGoal(myjson,beneficiary_id)
        #errorcode={}
        #errorcode["message"]="gfgfgfg"
        #status=json.JSONEncoder().encode(errorcode)        
        return HttpResponse(status, content_type='application/json')
    
    elif command_id == "SMG":
        myjson=json.loads(request.body)
        status=saveMealsGoal(myjson,beneficiary_id)
        #errorcode={}
        #errorcode["message"]="gfgfgfg"
        #status=json.JSONEncoder().encode(errorcode)         
        return HttpResponse(status, content_type='application/json')      
    #Queue notification 
    elif command_id == "SN":
        myjson=json.loads(request.body)
        #myjson={"EventObject":"Aquarium","EventUrl":"http://ict4d01.cs.uct.ac.za/","DateDisplayed":"22nd September","ObjectOwner":"8"}

        status=queueNotification(myjson,beneficiary_id);
        #errorcode={}
        #errorcode["message"]="gfgfgfg"
        #status=json.JSONEncoder().encode(errorcode) 
        return HttpResponse(status, content_type='application/json')
    elif command_id == "CTN":
        myjson=json.loads(request.body)
        myjson["BeneficiaryID"]=beneficiary_id
        status=saveTeamName(myjson)
        return HttpResponse(status,content_type='application/json')
    elif command_id  == "CAV":
        myjson=json.loads(request.body)
        myjson["IntermediaryId"]=intermediary_id
        status=saveAvatar(myjson)
        return HttpResponse(status, content_type='application/json')


@login_required
def pagelogout(request):
    context = RequestContext(request)
    return render_to_response('django_facebook/pagelogout.html', context)        

@login_required
def index(request):
    
    beneficiaries_counter=0
    beneficiary_fname=""
    beneficiary_lname=""
    beneficiary_ids=""
    beneficiary_counter=0
    username=""
    context = RequestContext(request)
    invaliduser=0
    beneficiary_team=""
    beneficiary_relation=""
    
    intermediary_fname=""
    intermediary_lname=""
    context["exception"]="None"
    try:
         
        if request.user.is_authenticated():#get the beneficiary name
            username=request.user.username
            username=username.replace(".","") 
            context["exception"]=username
            #facebook_data = facebook.facebook_registration_data()
            #if username=="ntwakatule":
            #    username="katulentwa@gmail.com"
            #username=facebook_data['facebook_id']
            myjson={'Username':username}
            obj=RetrieveIntermediary(myjson)
            status2=obj.isAssignedBeneficiary()
            status3=obj.countIntermediaries()
            status2=json.loads(status2)
            status3=json.loads(status3)
            intermediary_fname=status2["Ifname"]
            intermediary_lname=status2["Ilname"] 
            beneficiary_fname=status2["Fname"]
            beneficiary_lname=status2["Lname"]
            beneficiary_relation=status2["Relation"]
            beneficiary_team=status2["TeamName"]
           
            beneficiary_ids=obj.retrieveIntermediaryInDB();
            beneficiary_ids=json.loads(beneficiary_ids)
            beneficiaries_counter=status3["counter"]
            
    except Exception as e:
        invaliduser=1
        pass
       # status={"Error":e}
       # status=json.JSONEncoder().encode(status) 
       # return HttpResponse(status, content_type='application/json')
        #context["exception"]="The following exception %s is thrown on %s "%(e,username)       
      
    #return HttpResponse(content)
    context['invaliduser']=invaliduser
    #context['username']=username
    if request.user.is_authenticated():
        context['fname']=beneficiary_fname
        context['lname']=beneficiary_lname
        context['ifname']=intermediary_fname
        context['ilname']=intermediary_lname
        context['relation']=beneficiary_relation
        context["teamname"]=beneficiary_team
        ben_num={}
        key="R"
        for x in range(0,beneficiaries_counter):
            ben_num["R%s"%x]=x
        
        context['users_counter']=OrderedDict(sorted(ben_num.items(), key=lambda t: t[0]))
      
        myjson={"Day":"Today"}
         
        context["beneficiary_ids"]=beneficiary_ids


        intermediary_id=request.user.username
        intermediary_id=intermediary_id.replace(".","")
        #if intermediary_id=="ntwakatule":
        #    intermediary_id="katulentwa@gmail.com"
        obj=RetrievePoints(myjson,intermediary_id,1)
        result=obj.retrieveIndividualBadge()
        result=json.loads(result)

        myjson={"IntermediaryId":intermediary_id}      
        obj=ManageAvatars(myjson) 
        result2=obj.getAvatarUrl()
        result2=json.loads(result2)
       
        todaysdate=datetime.date.today()   
        date_str=todaysdate.strftime('%d-%m-%Y')  
        date_str2=todaysdate.strftime("%m/%d/%Y")
        context["badge"]=result["R00"]["D1"]
        context["sound"]=result["R00"]["D2"] 
        context["scoredate"]=date_str    
        context["todaysdate"]=date_str2
              
        context["avatar"]=result2["AvatarUrl"]
        context["avatarId"]=result2["AvatarId"]
        context.push()
        
    #return HttpResponse(template.render(context))
    
    return render_to_response('django_facebook/index.html', context)
    '''
    if request.user.is_authenticated():
        username=request.user.username
    else:
        username="Helo"
    context = RequestContext(request)
    myjson ={"Data":username}
    status=json.JSONEncoder().encode(myjson)
    return HttpResponse(status, content_type='application/json')
    '''
'''
def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')
'''
