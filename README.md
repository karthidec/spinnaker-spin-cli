# spinnaker-spin-cli

### Problem Statement:
How to update multiple spinnaker pipelines at a time using spin-cli ?

### Framework design:
 - Connect to spinnaker and automatic download pipeline json files
 - Update files in your local machine
 - Upload files again to spinnaker to update pipelines


### Pre-requisite:

1. Install spin-cli: https://spinnaker.io/setup/spin/
2. Update `gate_api_url` endpoint as require. I am using localhost now and my config.yaml looks like below without auth key.

```
# path: cat ~/.spin/config.yaml
gate:
  endpoint: http://localhost:9000
```



3. Have `python3` in your local machine

```
python3 --version
```

### How to execute:
1. Clone this repo
2. Navigate to the downloaded folder in terminal or command prompt
3. To know about required run-time arguments
```
python3 spin-cli.py help
```

4. To get all spinnaker pipelines to your local machine.  Folder `spin-existing-pipelines` will get create upon successful execution.
```
python3 spin-cli.py spin-get-pipelines
```

5. Update spinnaker pipeline files as require and save it
6. To update pipelines into spinnaker application
```
python3 spin-cli.py spin-update-pipelines
```





Execution video:

[![spinnaker spin-cli](http://img.youtube.com/vi/h1k3tLguu78/0.jpg)](http://www.youtube.com/watch?v=h1k3tLguu78 "https://img.youtube.com/vi/h1k3tLguu78/0.jpg")
