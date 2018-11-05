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
