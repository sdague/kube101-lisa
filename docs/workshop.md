# Kube 101 Workshop

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

```
git clone https://github.com/sdague/kube101-lisa
```

This contains the application code for the python app, as well as all
the kubernetes configurations you'll need.

## Step 2: Build Image

First, select a name for your image namespace. These must be globally
unique. Replace `$namespace` below with whatever you have chosen.

```
cd kube101-lisa
ibmcloud login --sso
ibmcloud cr namespace-add $namespace
ibmcloud cr build --tag registry.ng.bluemix.net/$namespace/web:1 status_page

```
