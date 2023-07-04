# MSCONF project
for more general environment variables go [here](https://github.com/amiriry/Devops/tree/main/Kubernetes/Microservices/msconf).<br><br>
This is an example project for very simple microservice that environment variables.<br>
It also defines one, which makes the tests much easier to understand. Its name is MY_ENVIRONMENT_VARIABLE.<br>
It is first defined with configmap named `myconfigfile.yaml` with the value: ```vvvvv```<br>
<br>


## Steps to make it work
### Install minikube
You can run this project on any kubernetes infratructure you want, I used ```minikube```<br>
because its very easy and its on your local machine.<br>

```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```
## Clone the project
You need to clone the project<br>
` git clone https://github.com/amiriry/msconf.git`

## Make minikube work with local docker images
`eval $(minikube -p minikube docker-env)`<br>
This command will define all the variabes needed for ```kubectl``` to point to the docker engine
inside minikube which is on port 2376 on the node that minikube starts.<br>
You can see this ip with the command:<br>
`kubectl get nodes -owide`<br><br>
The environment variables that should be defined:<br>
`export | grep DOCKER`<br><br>
You should see all of these with values:
```
DOCKER_CERT_PATH
DOCKER_HOST
DOCKER_TLS_VERIFY
MINIKUBE_ACTIVE_DOCKERD
```
##### &nbsp;&nbsp;&nbsp; back to original docker deamon:
If you want to go back to original docker configuration do:<br>
`unset $(export | grep DOCKER | awk -F'[ =]' '{print $3}' | xargs)`
<hr>

## Build the container image
Go into `build/` dir, where all the application code is.<br>
Run:<br>
```docker build -t confms .```
###### &nbsp;&nbsp;&nbsp;&nbsp;<u>Notice</u> the dot in the end,  very important for context of the build

We need to check that the image does exist in minikube registry:<br>
`minikube image ls | grep confms`<br>
The output should contain something like this:<br>
```
docker.io/library/confms:latest
```

## Install Helm Chart
Go to the base folder `msconf`<br> 
`cd ../`<br>
Do the command:<br>
```helm install myconfapp myconfapp/ --values myconfapp/values.yaml```

Now you should see all charts resources up:<br>
`kubectl get all --show-labels | egrep -v "NAME|^$" | awk '{print $1}'`<br>
output:
```
pod/ms-demo-5c6fffd499-pp6rm
pod/ms-test-6b5c8996b-z7xmp
service/kubernetes
service/microservice
deployment.apps/ms-demo
deployment.apps/ms-test
replicaset.apps/ms-demo-5c6fffd499
replicaset.apps/ms-test-6b5c8996b
```
Notice: <br>
There are 2 deployments<br>
<b>ms-demo</b> - Where the actual code is running<br>
<b>ms-test</b> - Tests to the ms api are going to be done from the pod in this deployment

## Test the MS

##### Define pods as variables
For you to tests this ms more easily, you need to define env vars for the pods.<br>
Use these commands:<br>
```
MS_TEST_POD=$(kubectl get pod | grep "ms-test" | awk '{print $1}')
MS_DEMO_POD=$(kubectl get pod | grep "ms-demo" | awk '{print $1}')
```
#### -- Do the API test --
###### &nbsp;&nbsp;&nbsp;<u>test /healthy</u>
`kubectl exec $MS_TEST_POD -- curl -s http://microservice:5000/healthy`
###### &nbsp;&nbsp;&nbsp;<u>test /get_variable</u>
```
# Get value from configmap
kubectl get configmap myconfig -o jsonpath='{.data}{"\n"}'

# Get the environment variable from the api, using os.environ['MY_ENVIRONMENT_VARIABLE']
kubectl exec $MS_TEST_POD -- curl -s http://microservice:5000/get_variable
```
###### &nbsp;&nbsp;&nbsp;<u>test /set_variable</u>
```
# First set the variable
kubectl exec $MS_TEST_POD -- curl -s -X POST http://microservice:5000/set_variable?new=aaaaa

# Check that it is different from before (what was defined as 'new' in set_variable request)
kubectl exec $MS_TEST_POD -- curl -s http://microservice:5000/get_variable
```
#### -- Do the PYTEST tests --
You can look in the file `myconfapp/test_api.py`, it defines all the tests.<br>
The way to run it is from is from where the code is, meaning from the ms pod.<br>
That's the reason we defined <b>MS_DEMO_POD</b> variable.<br>

To see the results:<br>
```kubectl exec $MS_DEMO_POD -- pytest -rA```

The result should be:<br>
```
==================================== PASSES ====================================
=========================== short test summary info ============================
PASSED test_api.py::test_healthy
PASSED test_api.py::test_get_var
PASSED test_api.py::test_set_var
============================== 3 passed in 0.07s ===============================
```
The tests names are self explanatory.
