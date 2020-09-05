import json
import os
import subprocess
import sys
import glob
import shutil
import yaml

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

def getAppPipelineNamesUsingConfigFile():
    with open(r'./config.yaml') as file:
        documents = yaml.full_load(file)
        app_pipelines_names=[]
        for app, pipe in documents.items():
            for pipe in pipe:
                app_pipelines_names.append({'application': app, 'pipeline': pipe})
        return app_pipelines_names

def getAppPipelineJson():
    if os.path.exists("spin-existing-pipelines"):
        shutil.rmtree("spin-existing-pipelines")
    appPipelines = getAppPipelineNames()
    for pipe in appPipelines:
        cmd= f"spin pipeline get --name {pipe['pipeline']} --application {pipe['application']}"
        pipelineJson = json.loads(getProcessOutput(cmd))
        if not os.path.exists(f"spin-existing-pipelines/{pipe['application']}"):
            os.makedirs(f"spin-existing-pipelines/{pipe['application']}")
        with open(f"spin-existing-pipelines/{pipe['application']}/{pipe['pipeline']}.json", 'w') as outfile:
            json.dump(pipelineJson, outfile)

def getAppPipelineJsonUsingConfigFile():
    if os.path.exists("spin-existing-pipelines"):
        shutil.rmtree("spin-existing-pipelines")
    appPipelines = getAppPipelineNamesUsingConfigFile()
    for pipe in appPipelines:
        cmd = f"spin pipeline get --name {pipe['pipeline']} --application {pipe['application']}"
        pipelineJson = json.loads(getProcessOutput(cmd))
        if pipelineJson is not None:
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

def updateAppPipelineUsingConfigFile():
    pipeDirectory='spin-existing-pipelines/'
    if os.path.isdir(pipeDirectory):
        appPipelineNames = getAppPipelineNamesUsingConfigFile()
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
    if arg  == 'spin-get-all-pipelines':
        getAppPipelineJson()
    elif arg == 'spin-update-all-pipelines':
        updateAppPipeline()
    elif arg == 'spin-get-config-only-pipelines':
        getAppPipelineJsonUsingConfigFile()
    elif arg == 'spin-update-config-only-pipelines':
        updateAppPipelineUsingConfigFile()
    elif arg == 'help':
        print ('spin-get-all-pipelines or spin-update-all-pipelines   ||   spin-get-config-only-pipelines or spin-update-config-only-pipelines')
    elif arg == '':
        print ('missing argument, type `help` to know about valid args')
    else:
        print ('Invalid argument, type `help` to know about valid args')
