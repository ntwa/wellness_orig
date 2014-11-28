from django.http import HttpResponse
import os
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader,Context
#from django.shortcuts import render_to_response
#from django.conf import settings
#from django.contrib import messages
#from django.http import Http404
from django.shortcuts import render_to_response
#from django.utils.translation import ugettext as _
#from django.views.decorators.http import require_POST
import logging
import json,sys
from app.authentication_module import Authentication 
#from django.template import Context, loader
from django import forms
from django.core.context_processors import csrf
from django.contrib.sessions.backends.db import SessionStore
from app.save_intermediary import SaveIntermediary
from app.retrieve_intermediary import RetrieveIntermediary
from app.save_beneficiary import SaveBeneficiary
from django.views.decorators.csrf import csrf_exempt
from collections import OrderedDict

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    passwd = forms.CharField(max_length=50)
    #sender = forms.EmailField()
    #cc_myself = forms.BooleanField(required=False)

# Create your views here.
def index(request):
    c = {}
    c.update(csrf(request))    
    status=0
    username=""
    password=""
    session_set=0

    try:
        username=request.session['username']
        password=request.session['passwd']
        session_set=1
        pass
    except Exception as e:
        pass
        #authenticated=e
        #return render_to_response('adminapp/index.htm', {'authenticated':authenticated,'username':username})

    if request.method == 'POST' or session_set==1: # If the form has been submitted...
        # ContactForm was defined in the the previous section
        form = LoginForm(request.POST) # A form bound to the POST data

        
        if form.is_valid() or session_set==1:
            # All validation rules pass
            # Process the data in form.cleaned_data
            if session_set == 0:
                username=form.cleaned_data['username']
                password=form.cleaned_data['passwd']
            else:
                pass
            
            myjson={'Username':username,'Password':password}
            obj=Authentication(myjson,request)
            status=obj.authenticateAdmin() 
            myjson=json.loads(status)
            status=myjson["authentication"]
            
            
            #return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = LoginForm() # An unbound form
        
    
    intermediary_tuples=None
    if status == 1:
        #retrieve intermediaries
        myjson={'Empty':''}
        obj=RetrieveIntermediary(myjson)
        intermediary_tuples=obj.retrieveIntermediaryInDB()
        
        intermediary_tuples=json.loads(intermediary_tuples)
        #intermediary_tuples=OrderedDict(sorted(intermediary_tuples.items(), key=lambda t: t[0]))
        #return HttpResponse(status, mimetype='application/json')        

    #return render_to_response('adminapp/index.htm', {'authenticated': status,'username':username})
    template = loader.get_template('adminapp/index.htm')
    context = RequestContext(request)
    context['authenticated']=status
    context['username']=username
    context['intermediaries']=intermediary_tuples
    context.push()
    return HttpResponse(template.render(context)) 

@csrf_exempt
def commands(request,command_id):
    c = {}
    c.update(csrf(request))
    
    if command_id=="LG":
        
        myjson={'Username':'..','Password':'..'}
        obj=Authentication(myjson,request)
        obj.resetSession()
        status=0
        #template = loader.get_template('adminapp/authenticate.htm')
        #c = Context({'var': varuu,})
        #return render_to_response('adminapp/index.htm', {'authenticated': status})
        #context = RequestContext(request)
        #return HttpResponse(template.render())
        #return HttpResponse(template.render(context))
        template = loader.get_template('adminapp/index.htm')
        context = RequestContext(request)
        context['authenticated']=status
        context['username']=""
        context.push()
        return HttpResponse(template.render(context)) 
    
    elif command_id=="SI":
        myjson=json.loads(request.body)
        obj=SaveIntermediary(myjson)
        status=obj.saveIntermediaryInDB()
        return HttpResponse(status, mimetype='application/json')
    elif command_id=="SB":
        myjson=json.loads(request.body)
        obj=SaveBeneficiary(myjson)
        status=obj.saveBeneficiaryInDB()
        return HttpResponse(status, mimetype='application/json')
    
    elif command_id=="CAB":
        #check if an intermediary has been assigned a beneficiary
        myjson=json.loads(request.body)
        obj=RetrieveIntermediary(myjson)
        status=obj.isAssignedBeneficiary()
        return HttpResponse(status, mimetype='application/json') 
    
    elif command_id=="DB":
        #check if an intermediary has been assigned a beneficiary
        myjson=json.loads(request.body)
        obj=SaveBeneficiary(myjson)
        status=obj.removeBeneficiary()
        return HttpResponse(status, mimetype='application/json') 
        

    
        