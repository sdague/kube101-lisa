#!/bin/sh

# Full list of commands from Kube 101 LISA workshop.
#
# In order to ensure there is a complete list of commands that
# everyone has access to even if the screens have passed, this is
# listed below.
#
# Note: some commands require a specific podname, those are listed as
# $podname in the below script.

ibmcloud cr namespace-add status_page

ibmcloud cr build --tag \
  registry.ng.bluemix.net/status_page/web:1 status_page

ibmcloud ks cluster-config kubelisa

kubectl get all -o wide

kubectl apply -f deploy/status-deployment.yaml

kubectl get all -o wide

kubectl get nodes -o wide

kubectl get service -l app=status-web -o wide

kubectl get all -o wide

kubectl describe pod/$podname

kubectl apply -f deploy/redis-deployment.yaml

kubectl get pods -l app=status-web

kubectl delete pod/$podname

## Upgrade

ibmcloud cr build --tag registry.ng.bluemix.net/status_page/web:2 status_page

kubectl apply -f deploy/status-deployment.yaml

kubectl get pods -l app=status-web

kubectl logs $podname

ibmcloud cr build --tag registry.ng.bluemix.net/status_page/web:3 status_page

kubectl apply -f deploy/status-deployment.yaml

kubectl get pods -l app=status-web

## Debug

kubectl -it exec $podname bash
