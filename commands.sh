#!/bin/sh

ibmcloud cr namespace-add status_page

ibmcloud cr build --tag \
  registry.ng.bluemix.net/status_page/web:1 status_page

ibmcloud ks cluster-config kubelisa

kubectl get all -o wide

kubectl apply -f deploy/status-deployment.yaml

kubectl get all -o wide

kubectl get nodes -o wide

kubectl get service -l app=status-web -o wide

kubectl describe pod/status-web-5c47b9b67b-57ksk


kubectl apply -f deploy/redis-deployment.yaml

kubectl get pods -l app=status-web

kubectl delete

## Upgrade

ibmcloud cr build --tag registry.ng.bluemix.net/status_page/web:2 status_page

kubectl apply -f deploy/status-deployment.yaml

kubectl get pods -l app=status-web

kubectl logs status-web-5d6b4665dc-5t7c5

ibmcloud cr build --tag registry.ng.bluemix.net/status_page/web:3 status_page

kubectl apply -f deploy/status-deployment.yaml

kubectl get pods -l app=status-web

## Debug

kubectl -it exec status-web-5c47b9b67b-cxk8c bash
