[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) 
[![codecov](https://codecov.io/gh/X-I-A/xeed-http-gcr/branch/master/graph/badge.svg)](https://codecov.io/gh/X-I-A/xeed-http-gcr) 
[![master-check](https://github.com/x-i-a/xeed-http-gcr/workflows/master-check/badge.svg)](https://github.com/X-I-A/xeed-http-gcr/actions?query=workflow%3Amaster-check) 
# XEED: HTTP End point on Google Cloud Run
## Introduction
* This HTTP application can capture Xeed Http flow and publish the message to google cloud (Pubsub actually supported)
* Please find the [protocol defintion here](https://github.com/X-I-A/X-I-Protocol/blob/main/HTTP_AGENT.md)
* As is described in the protocol, URI of GCP is defined as: 
`https://..../publisher/pubsub/destinations/<project_id>/topics/<topic_name>/tables/<table_name>`

## Quick Start guide
Download the source code:
```
git clone https://github.com/X-I-A/xeed-http-gcr
cd xeed-http-gcr
```
Please using Google Cloud Console or by using Google Cloud SDK
* `make init` Activation of API, creation of service account with publisher roles
* `make build` Build and upload Cloud Run Image
* `make deploy` Deploy Cloud Run Image by using the last built image

### Usage
* You can now post the [XEED HTTP Message](https://github.com/X-I-A/X-I-Protocol/blob/main/HTTP_AGENT.md) to <url>/publishers/pubsub/destinations/<project_id>
