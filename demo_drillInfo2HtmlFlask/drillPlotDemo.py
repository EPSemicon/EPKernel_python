from epkernel import Configuration,Input,GUI
from epkernel.Action import Information
from matplotlib import collections
import json,webbrowser,flask
import pandas as pd

markers = ['.',',','x','+']
colorsList = ['b','g','y','k']
htmlstr=''
Configuration.init(r'')
Input.open_eps('this',r'34224396.eps')
GUI.show_layer('this','prepare','l1')
drlInfoList=[]
drlList = Information.get_layer_info('this','board',['drill'])
profilePolyStr = Information.get_profile('this','prepare')
profilePolyDict = json.loads(profilePolyStr)
profilePolyList = profilePolyDict['points']
polygonList = []
for i in range(0,len(profilePolyList)):
    pointDict = profilePolyList[i]
    polygonList.append((pointDict['ix']*(1e-6),pointDict['iy']*(1e-6)))
for drl in drlList:
    drlLayer = drl['name']
    collection_1=collections.LineCollection([polygonList], color=["red"])
    listInfo = Information.get_drill_info('this','prepare',drlLayer)
    jsonInfo = json.dumps(listInfo)
    df = pd.read_json(jsonInfo,encoding='utf-8')
    htmlstr += '<fieldset> <legend>'+drlLayer+'    strat from '+drl['start_name']+'   end at '+drl['end_name']+'</legend>'
    htmlstr += df.to_html()
    drillPointList = df['vLocations'].iloc[0]
    drillPointJson = json.dumps(drillPointList)
    dfPoint = pd.read_json(drillPointJson,encoding='utf-8')
    dfPoint = dfPoint*(1e-6)
    ax = dfPoint.plot.scatter(x = 'X',y = 'Y',use_index = False,xlabel = 'X(Unit:MM)',ylabel = 'Y(Unit:MM)',marker = markers[0],color = colorsList[0])
    for i in range(1,len(df)):
        drillPointList = df['vLocations'].iloc[i]
        drillPointJson = json.dumps(drillPointList)
        dfPoint = pd.read_json(drillPointJson,encoding = 'utf-8')
        dfPoint = dfPoint*(1e-6)
        ax = dfPoint.plot.scatter(x = 'X',y = 'Y',use_index = False,xlabel = 'X(Unit:MM)',ylabel = 'Y(Unit:MM)',ax = ax,marker = markers[i],color = colorsList[i])
    ax.add_collection(collection_1)
    fig=ax.get_figure()
    fig.savefig(fname='./static/'+'svg'+drlLayer+'.svg',format='svg')
    ax.clear()
    fig.clear()
    htmlstr += '<img src='+'"static/svg'+drlLayer+'.svg"'+' width="800" height="600">'
    htmlstr += ' </fieldset>'

flaskData = flask.Flask(__name__)

@flaskData.route('/drillInfo')
def flaskDataFunc():
    return flask.render_template_string(htmlstr.replace('<td>','<td contenteditable="true">'))

if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:4396/drillInfo')
    flaskData.run(port=4396)
