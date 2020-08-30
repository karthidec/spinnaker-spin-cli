import json
import os
import subprocess
import sys
import glob

def getProcessOutput(cmd):
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE)
    process.wait()
    data, err = process.communicate()
    if process.returncode == 0:
        return data.decode('utf-8')
    else:
        print("Error:", err)
    return ""

def getAppNames():
    cmd = "spin application list"
    apps = json.loads(getProcessOutput(cmd))
    app_names=[]
    for app in apps:
        app_names.append(app['name'])
    return app_names

def getAppPipelineNames():
    appNameList=getAppNames()
    pipelines=[]
    for app in appNameList:
        cmd = f"spin pipeline list --application {app}"
        pipes = json.loads(getProcessOutput(cmd))
        if len(pipes):
            for pipe in pipes:
                pipelines.append({'application': app, 'pipeline': pipe['name']})
    return pipelines

def getAppPipelineJson():
    appPipelines = getAppPipelineNames()
    for pipe in appPipelines:
        cmd= f"spin pipeline get --name {pipe['pipeline']} --application {pipe['application']}"
        pipelineJson = json.loads(getProcessOutput(cmd))
        if not os.path.exists(f"spin-existing-pipelines/{pipe['application']}"):
            os.makedirs(f"spin-existing-pipelines/{pipe['application']}")
        with open(f"spin-existing-pipelines/{pipe['application']}/{pipe['pipeline']}.json", 'w') as outfile:
            json.dump(pipelineJson, outfile)

def updateAppPipeline():
    pipeDirectory='spin-existing-pipelines/'

    if os.path.isdir(pipeDirectory):
        appPipelineNames = getAppPipelineNames()
        appNames=[]

        for app in appPipelineNames:
            appNames.append(app['application'])
        filterAppNames =  list(set(appNames))

        for app in filterAppNames:
            fileList = glob.glob(f"spin-existing-pipelines/{app}/*.json")
            for file in fileList:
                print (f'application:{app} - pipeline:{file}',  getProcessOutput(f"spin pipeline save --file {file}"))
    else:
        print ('Pipeline files are missing. First get files and try again. Type `help` to know about details')

arg = sys.argv[1]

if arg:
    if arg  == 'spin-get-pipelines':
        getAppPipelineJson()
    elif arg == 'spin-update-pipelines':
        updateAppPipeline()
    elif arg == 'help':
        print ('spin-get-pipelines or spin-update-pipelines')
    elif arg == '':
        print ('missing argument, type `help` to know about valid args')
    else:
        print ('Invalid argument, type `help` to know about valid args')
