# Setup Instructions for IBM Cloud Account

In order to complete the Kubernetes 101 workshop at LISA you'll need
the ability to provision a Kubernetes Cluster. We are providing IBM
Cloud Accounts with Promo codes to do this. This is a detailed walk
through of that process.

## Step 1: Register for IBM Cloud with the LISA url

Go to https://ibm.biz/kube101-lisa to start the registration.

![registration page](images/regpage.png)

Fill out all the require information and the CAPTCHA and
submit. You'll get a confirmation page like:

![confirmation page](images/confirmemail.png)

## Step 2: Confirm Email

Check your email and confirm your account. This will take you to an
IBM coders site. You can ignore this.

## Step 3: IBM Cloud Console

Navigate to the [Dashboard](https://console.bluemix.net/dashboard/apps/)

It will ask you to login:

![login screen](images/login.png)

## Step 4: Add Promo Code

Click on the upper right icon that looks like a "person", and click on
the **Profile** link.

![edit profile](images/profile.png)

From the profile page click on the [Billing](https://console.bluemix.net/account/billing)

![billing screen](images/billing.png)

You will be getting a Promo Code from the Google Drive link specified
in the workshop. Take one from there. Add it with the Add Promo Code
Screen.

![promo code](images/promocode.png)

## Step 5: Provision Kube Cluster

First navigate to the [Catalog](https://console.bluemix.net/catalog/).

![IBM service catalog](images/catalog.png)

There are lots of services available here, so the best bet is to start
typing ``kube`` in the search field to find the IBM Kubernetes
Service.

![IBM kube service](images/catalog-kube.png)

Click on Create.

![IBM kube service](images/kube-create-1.png)

Create a cluster. Be sure to do the following things:

* Set the region to **US South**
* Select Free Cluster
* Name the cluster **kubelisa**

You can name it anything you want, but the commands examples use
kubelisa as the name for consistency.

Then click on create.

![IBM kube create](images/kube-create-2.png)

Afterwards you can see the status of the cluster here

![IBM kube status](images/kube-create-3.png)
