SHELL:=/bin/bash

all: say_hello

say_hello:
	@echo "Hello World"

input_test:
	@TMP_PROJECT=$(shell gcloud config list --format 'value(core.project)'); \
	read -e -p "Enter Your Project Name: " -i $${TMP_PROJECT} PROJECT_ID; \
	read -e -p "Enter Desired Cloud Run Region: " -i "europe-west1" CLOUD_RUN_REGION; \
	echo $${PROJECT_ID}; \
	echo $${CLOUD_RUN_REGION}; \
	gcloud config set project $${PROJECT_ID}; \
	echo $(shell gcloud projects list --filter=$(shell gcloud config list --format 'value(core.project)') --format="value(PROJECT_NUMBER)");