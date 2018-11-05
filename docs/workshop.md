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

    code.language-command:before {
    content: "> ";
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

### The Application Image

The following is the image file that we're building.

```docker
ROM ubuntu:18.04

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
