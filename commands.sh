#!/bin/sh

# Full list of commands from Kube 101 LISA workshop.
#
# In order to ensure there is a complete list of commands that
# everyone has access to even if the screens have passed, this is
# listed below.
#
# The comment before each set of commands matches the slide title they
# were on.
#
# Note: some commands require a specific podname, those are listed as
# $podname in the below script.

# Step 2: Build Image

ibmcloud login --sso

ibmcloud cr namespace-add status_page

ibmcloud cr build --tag \
  registry.ng.bluemix.net/status_page/web:1 status_page

# Step 3: Connect to Kube Cluster

ibmcloud ks cluster-config kubelisa

# Step 4: Explore the Cluster

kubectl get all -o wide

# Step 5: Deploy the Application

kubectl apply -f deploy/status-deployment.yaml

kubectl get all -o wide

# Connect to Application

kubectl get nodes -o wide

kubectl get service -l app=status-web -o wide

# What's going on?

kubectl get all -o wide

kubectl describe pod/$podname

# Step 6: Deploy Datastore

kubectl apply -f deploy/redis-deployment.yaml

# Step 8: Pod Lifecycle

kubectl get pods -l app=status-web

kubectl delete pod/$podname

## Upgrade

# Step 1: Make a bad image

ibmcloud cr build --tag registry.ng.bluemix.net/status_page/web:2 status_page

# Step 2: Upgrade image

kubectl apply -f deploy/status-deployment.yaml

kubectl get pods -l app=status-web

# Step 3: Find out what's wrong - logs

kubectl logs $podname

# Fix it, watch the upgrade complete

ibmcloud cr build --tag registry.ng.bluemix.net/status_page/web:3 status_page

kubectl apply -f deploy/status-deployment.yaml

kubectl get pods -l app=status-web

# Interactive debug

kubectl -it exec $podname bash
