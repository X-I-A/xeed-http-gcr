# XEED Agent : HTTP to Pubsub 
## Introduction
* This Xeed Agent can capture Xeed HTTP flow and publish the message of X-I protocol to Pubsub which is one of the entry point of Insight Module
* Please find the [protocol defintion here](https://github.com/X-I-A/X-I-Protocol/blob/main/HTTP_AGENT.md)
* As is described in the protocol, URI of GCP is defined as: `https://..../projects/<project_id>/topics/<topic_name>`

## Quick Start guide
### Preparation
The following steps will help you to build the HTTP to PubSub agent under Google Cloud Run
* All of the command should be executed in the Google Cloud Console or by using Google Cloud SDK
* You can change mannuelly the variables ${} by the required value of the following command
* It is also possible to fill the setenv.sh file and run `source setenv.sh`. You can run the command without change.
It is a good idea to keep this file because you will reuse part of it in other X-I-A applications.
## Service Account Preparation
1. Create Servcie account: 
```
gcloud iam service-accounts create cloud-run-xeed-http \
    --description="Xeed Http to Pubsub Agent" 
```
2. Grant Pubsub Publish Roles: 
```
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member=serviceAccount:cloud-run-xeed-http@${PROJECT_ID}.iam.gserviceaccount.com \
	--role=roles/pubsub.publisher
```
### Deployment of Cloud Run
1. Clone the repo 
```
git clone https://github.com/X-I-A/Xeed_http_pubsub
```
2. Go to the downloaded directory 
```
cd Xeed_http_pubsub
```
3. Build the solution
```
gcloud builds submit --tag gcr.io/${PROJECT_ID}/xeed-http-pubsub
```
4. Deploy the solution with created service account and provide user / password
```
gcloud run deploy xeed-http --image gcr.io/${PROJECT_ID}/xeed-http-pubsub \
    --service-account cloud-run-xeed-http@${PROJECT_ID}.iam.gserviceaccount.com \
	--region ${REGION_NAME} --platform managed --allow-unauthenticated \
	--update-env-vars XEED_USER=${XEED_USER},XEED_PASSWORD=${XEED_PASSWORD}
```
### Usage
* You can now post the HTTP Message into <url>/projects/<project_id>/topics/<topic_name>