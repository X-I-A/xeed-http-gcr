SHELL:=/bin/bash

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

config: ## Setting deploy configuration
	@TMP_PROJECT=$(shell gcloud config list --format 'value(core.project)'); \
	read -e -p "Enter Your Project Name: " -i $${TMP_PROJECT} PROJECT_ID; \
	gcloud config set project $${PROJECT_ID}; \
	read -e -p "Enter Desired Cloud Run Region: " -i 'europe-west1' CLOUD_RUN_REGION; \
	gcloud config set run/region $${CLOUD_RUN_REGION}; \
	read -e -p "Enter Desired Cloud Run Platform: " -i 'managed' CLOUD_RUN_PLATFORM; \
	gcloud config set run/platform $${CLOUD_RUN_PLATFORM};

init: ## Activation of API, creation of service account with publisher role
	@PROJECT_ID=$(shell gcloud config list --format 'value(core.project)'); \
	gcloud iam service-accounts create cloud-run-xeed-http \
		--display-name "Cloud Run Xeed Http Endpoint"
	gcloud projects add-iam-policy-binding $${PROJECT_ID} \
		--member=serviceAccount:cloud-run-xeed-http@$${PROJECT_ID}.iam.gserviceaccount.com \
		--role=roles/pubsub.publisher

build: ## Build and upload Cloud Run Image
	@PROJECT_ID=$(shell gcloud config list --format 'value(core.project)'); \
	gcloud builds submit --tag gcr.io/$${PROJECT_ID}/xeed-http-gcr;

deploy: ## Deploy Cloud Run Image by using the last built image
	@PROJECT_ID=$(shell gcloud config list --format 'value(core.project)'); \
	CLOUD_RUN_REGION=$(shell gcloud config list --format 'value(run.region)'); \
	CLOUD_RUN_PLATFORM=$(shell gcloud config list --format 'value(run.platform)'); \
	read -e -p "Enter Desired Username: " -i "user" XEED_USER; \
	read -e -p "Enter Desired Password: " -i "La_vie_est_belle" XEED_PASSWORD; \
	gcloud run deploy xeed-http \
		--image gcr.io/$${PROJECT_ID}/xeed-http-gcr \
    	--service-account cloud-run-xeed-http@$${PROJECT_ID}.iam.gserviceaccount.com \
		--region $${CLOUD_RUN_REGION} \
		--platform managed \
		--allow-unauthenticated \
		--update-env-vars XEED_USER=$${XEED_USER},XEED_PASSWORD=$${XEED_PASSWORD};

update: ## Update User/Password
	@PROJECT_ID=$(shell gcloud config list --format 'value(core.project)'); \
	CLOUD_RUN_REGION=$(shell gcloud config list --format 'value(run.region)'); \
	CLOUD_RUN_PLATFORM=$(shell gcloud config list --format 'value(run.platform)'); \
	read -e -p "Enter Desired Username: " -i "user" XEED_USER; \
	read -e -p "Enter Desired Password: " -i "La_vie_est_belle" XEED_PASSWORD; \
	gcloud run services update xeed-http \
		--region $${CLOUD_RUN_REGION} \
		--platform managed \
		--update-env-vars XEED_USER=$${XEED_USER},XEED_PASSWORD=$${XEED_PASSWORD};
