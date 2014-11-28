import sys,json
from plot_activity_graph import PlotActivityGraph


def plotActivityGraph(myjson,beneficiary_id):
    obj=PlotActivityGraph(myjson,beneficiary_id)
    datapoints=obj.getDataPoints() #the returned goal is an encoded json object
    return datapoints  
    
activity_tuples={"Today":{},"This week":{},"Last week":{},"This month":{},"Last month":{},"Last three months":{}}
        
    
for day,activity_tuple in activity_tuples.iteritems():
    myjson={"Day":day}
    new_tuple=plotActivityGraph(myjson,8)
    activity_tuples[day]=json.loads(new_tuple)
    
print json.JSONEncoder().encode((activity_tuples))