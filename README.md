# spinnaker-spin-cli

### Problem Statement:
How to update multiple spinnaker pipelines at a time using spin-cli ?

### Framework design:
 - Connect to spinnaker and automatically download pipeline json files
     - Note: If run-time argument passed for `config.yaml` file, then it will GET/UPDATE for only pipelines present in config.yaml file
 - Update files in local machine
 - Upload files again to spinnaker to update pipelines


### Pre-requisite:

1. Install spin-cli: https://spinnaker.io/setup/spin/
2. Update `gate_api_url` endpoint as require. I am using localhost now and my config.yaml looks like below without auth key.

```
# path: cat ~/.spin/config.yaml
gate:
  endpoint: http://localhost:9000
```



3. Install `python3` in your local machine

```
python3 --version
```

## GET/UPDATE ALL pipelines:
1. Clone this repo
2. Navigate to the downloaded folder in terminal or command prompt
3. To know about required run-time arguments
```
python3 spin-cli.py help
```

4. To get `ALL` spinnaker pipelines to your local machine.  Folder `spin-existing-pipelines` will get create upon successful execution.
```
python3 spin-cli.py spin-get-all-pipelines
```

5. Update spinnaker pipelines config field in files as required and save it

6. To update `ALL` pipelines into spinnaker application
```
python3 spin-cli.py spin-update-all-pipelines
```


## GET/UPDATE ONLY selected pipelines:

1. Update `config.yaml` present in root folder with application & pipeline details

2. To get above `step-1` config defined pipelines to your local machine.  Folder `spin-existing-pipelines` will get create upon successful execution.
```
python3 spin-cli.py spin-get-config-only-pipelines
```

3. Update spinnaker pipelines config field in files as required and save it

4. To update as per above `step-2` config defined pipelines into spinnaker application
```
python3 spin-cli.py spin-update-config-only-pipelines
```


## Execution video:

### ALL pipelines:

[![spinnaker spin-cli](http://img.youtube.com/vi/h1k3tLguu78/0.jpg)](http://www.youtube.com/watch?v=h1k3tLguu78 "https://img.youtube.com/vi/h1k3tLguu78/0.jpg")
