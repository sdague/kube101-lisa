# Kube 101 Workshop

<style>
    img {
        border: 2px #445588 solid;
    }
    section {
        width: 800px;
    }
    #banner {
        width: 100%;
    }
    nav {
        text-align: left;
    }
    li.tag-h3 {
        padding-left: 8px;
    }
    pre {
        background-color: #eee;
    }
    pre.highlight {
        background-color: #333333;
    }
    code.language-command:before {
        content: "> ";
    }
    code.language-command,
    code.language-output {
        background-color: inherit;
        color: inherit;
        text-shadow: inherit;
    }
    code.language-command {
        font-weight: bold;
        color: black;
    }
</style>

This is the workflow for the Kubernetes 101 Workshop.

## Learning Objectives

During this workshop you'll do the following things

- Create an IBM Cloud Account and Kubernetes Cluster
- Learn basic Conceptual Model of common Kubernetes Resources
- Build an application image
- Deploy application image to Kubernetes
- Explore lifecycle of pods
- Debug when things go wrong / break things to see common debug steps
- Upgrade application

## Sample Application

The sample application is a status page application that lets you
record system status.

## Prep-Work

Before completing the interactive portion of the workshop you'll need
to create an IBM Cloud Account using the [instructions provided](index.html).

# Deploying Your First App

## Step 1: Clone Repo

```command
git clone https://github.com/sdague/kube101-lisa
```
```command
cd kube101-lisa
```

This contains the application code for the python app, as well as all
the kubernetes configurations you'll need.

## Step 2: Build Image

First, we have to login to our environment:

```command
ibmcloud login --sso
```

After doing that we need to create an image registry. In IBM Cloud you
can have your own private image registry to build and store container
images. This prevents anyone outside of your account from seeing
these.

You must select a name for your image namespace, as these are globally
unique. Once you have selected it replace the `$namespace` in all
commands below with that value.

```command
ibmcloud cr namespace-add $namespace
```

Next we build the image using IBM Cloud's Image build farm. Remember
to replace `$namespace` with your chosen namespace.

```command
ibmcloud cr build --tag registry.ng.bluemix.net/$namespace/web:1 status_page
```

```output
Sending build context to Docker daemon   22.2MB
Step 1/11 : FROM ubuntu:18.04
18.04: Pulling from library/ubuntu
473ede7ed136: Pull complete
c46b5fa4d940: Pull complete
93ae3df89c92: Pull complete
6b1eed27cade: Pull complete
Digest: sha256:29934af957c53004d7fb6340139880d23fb1952505a15d69a03af0d1418878cb
Status: Downloaded newer image for ubuntu:18.04

...

Step 11/11 : CMD flask run -h 0.0.0.0
 ---> Running in 6c6b234b3af5
 ---> 0fafed49d891
Removing intermediate container 6c6b234b3af5
Successfully built 0fafed49d891
Successfully tagged registry.ng.bluemix.net/status_page/web:1
The push refers to a repository [registry.ng.bluemix.net/status_page/web]
54084949a5fc: Pushed
1b7b005ebbd4: Pushed
cdfea8cbb4bd: Pushed
76c033092e10: Layer already exists
2146d867acf3: Layer already exists
ae1f631f14b7: Layer already exists
102645f1cf72: Layer already exists
1: digest: sha256:bf0e91c99df7a67b8c83c4eea2d37bad65bca1ad7454812a068fbbe051a89851 size: 1785

OK

```

### The Application Image

The following is the image file that we're building.

```docker
FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV FLASK_APP status_page
ENV STATUS_PAGE_SETTINGS ../settings.cfg

RUN apt-get update && apt-get install -y python3 python3-dev python3-pip && apt-get clean

COPY ./ /var/www/status_page
WORKDIR /var/www/status_page

RUN pip3 install -U .

CMD flask run -h 0.0.0.0
```

This has a few basic container image stanzas:

- FROM - specify a base image, in our case a dockerhub ubuntu 18.04
  minimal image
-  ENV - specify environment variables. Many are needed for apt to run
   cleanly
- RUN - run a command. We do an apt install, as well as a pip install
  later
- COPY - copy files from the local directory into the image. This is
  how we load in our application.
- WORKDIR - set the working directory for the image
- CMD - what command should we run if nothing else is specified via
  kubernetes.

It is important that `flask` is passed the `-h 0.0.0.0`
argument. Without that, it would bind to localhost (i.e. 127.0.0.1),
which would not allow inbound connections.

## Step 3: Connect to Kube Cluster

```command
ibmcloud ks cluster-config kubelisa
```

Which returns something like

```output
OK

The configuration for kubelisa was downloaded successfully. Export
environment variables to start using Kubernetes.

export KUBECONFIG=/home/sdague/.bluemix/plugins/container-service/clusters/kubelisa/kube-config-wdc06-kubelisa.yml
```

You must then run the `export` command to enable `kubectl` to access
your cluster. For the rest of this exercise we'll be using `kubectl`
for almost all actions.


## Step 4: Explore the cluster

A good starting point for the cluster is to look at all the resources:

```command
kubectl get all -o wide
```

```output
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE       SELECTOR
service/kubernetes   ClusterIP   172.21.0.1   <none>        443/TCP   10d       <none>
```

A kuberenetes cluster starts with very little in it's default namespace. There is just a
single service for the kubernetes API itself.

## Step 5: Deploying the Application

**Note:** you have to change your image url in the files to match you
chosen `$namespace` above.

Edit the `deploy/status-deployment.yaml` file and replace
`status_page` with your chosen `$namespace`:

```yaml
...
    spec:
      containers:
      - name: status-web
        image: registry.ng.bluemix.net/status_page/web:1
        imagePullPolicy: Always
...
```

Then you can deploy the application:

```command
kubectl apply -f deploy/status-deployment.yaml
```

```output
deployment.apps "status-web" created
service "status-web" created
```

Then look at what happened:

```command
kubectl get all -o wide
```

```output
NAME                              READY     STATUS    RESTARTS   AGE       IP              NODE
pod/status-web-64474bccd5-btmn5   0/1       Running   0          33s       172.30.112.86   10.190.15.245
pod/status-web-64474bccd5-fwt5h   0/1       Running   0          33s       172.30.112.87   10.190.15.245
pod/status-web-64474bccd5-rjq44   0/1       Running   0          33s       172.30.112.85   10.190.15.245

NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE       SELECTOR
service/kubernetes   ClusterIP   172.21.0.1       <none>        443/TCP          10d       <none>
service/status-web   NodePort    172.21.161.127   <none>        5000:32101/TCP   33s       app=status-web

NAME                         DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE       CONTAINERS   IMAGES                                      SELECTOR
deployment.apps/status-web   3         3         3            0           33s       status-web   registry.ng.bluemix.net/status_page/web:1   app=status-web

NAME                                    DESIRED   CURRENT   READY     AGE       CONTAINERS   IMAGES                                      SELECTOR
replicaset.apps/status-web-64474bccd5   3         3         0         33s       status-web   registry.ng.bluemix.net/status_page/web:1   app=status-web,pod-template-hash=2003067781

```

### Connect to Application

Once the application is deployed, we can connect to it. Because we are
using a **NodePort** we need to run a couple of commands to determine
the url for the application.

```command
kubectl get nodes -o wide
```

```output
NAME            STATUS    ROLES     AGE       VERSION       EXTERNAL-IP    OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
10.190.15.245   Ready     <none>    10d       v1.10.8+IKS   169.61.97.62   Ubuntu 16.04.5 LTS   4.4.0-137-generic   docker://17.6.2
```

The import information here is the `EXTERNAL-IP`.

```command
kubectl get service -l app=status-web -o wide
```

```output
NAME         TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE       SELECTOR
status-web   NodePort   172.21.161.127   <none>        5000:32101/TCP   13m       app=status-web
```

Here we need the 2nd port listed under ports. That's what's exposed to
the outside world.

The above would give us a URL of **http://169.61.97.62:32101**.

Did it work?

### Discovering what's going on

Run the following command again:

```command
kubectl get pod -l app=status-web -o wide
```

```output
NAME                          READY     STATUS    RESTARTS   AGE       IP              NODE
status-web-64474bccd5-btmn5   0/1       Running   0          18m       172.30.112.86   10.190.15.245
status-web-64474bccd5-fwt5h   0/1       Running   0          18m       172.30.112.87   10.190.15.245
status-web-64474bccd5-rjq44   0/1       Running   0          18m       172.30.112.85   10.190.15.245
```

What's going on in that `READY` field? Why aren't any of our services
ready?

Let's start with looking at one of the pods and see if we can see:

```command
kubectl describe pod/status-web-64474bccd5-rjq44
```

```output
...
Events:
  Type     Reason                 Age                 From                    Message
  ----     ------                 ----                ----                    -------
  Normal   Scheduled              21m                 default-scheduler       Successfully assigned status-web-64474bccd5-rjq44 to 10.190.15.245
  Normal   SuccessfulMountVolume  21m                 kubelet, 10.190.15.245  MountVolume.SetUp succeeded for volume "default-token-hsk5t"
  Normal   Pulling                21m                 kubelet, 10.190.15.245  pulling image "registry.ng.bluemix.net/status_page/web:1"
  Normal   Pulled                 21m                 kubelet, 10.190.15.245  Successfully pulled image "registry.ng.bluemix.net/status_page/web:1"
  Normal   Created                21m                 kubelet, 10.190.15.245  Created container
  Normal   Started                21m                 kubelet, 10.190.15.245  Started container
  Warning  Unhealthy              1m (x119 over 21m)  kubelet, 10.190.15.245  Readiness probe failed: HTTP probe failed with statuscode: 500
```

Ah, we're failing a readiness probe. Because we're failing readiness,
the pods in question aren't being added to the service pool, and thus
there is nothing to answer the incoming requests.

If we look at our deployment yaml we'll see that we included a
readiness check

```yaml
...
    spec:
      containers:
      - name: status-web
        image: registry.ng.bluemix.net/status_page/web:1
        imagePullPolicy: Always
        env:
          - name: REDIS_HOST
            value: "redis-leader"
        ports:
        - name: http
          containerPort: 5000
          protocol: TCP
        readinessProbe:
          httpGet:
            path: /readiness
            port: 5000
```

The reason the readiness probe is failing is that the redis datastore
that's needed for the application hasn't been deployed. We can fix
that in our next step.
