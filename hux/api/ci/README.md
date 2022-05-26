# CI/CD Pipelines With Variables File

## Codefresh Variables File
In Codefresh there are many ways to handle variables. Documentation can be found here: https://codefresh.io/docs/docs/codefresh-yaml/variables/.

In order to make variable management easier and in code, a variables file named `codefresh_vars.yml` can be maintained along side the pipeline yaml named `codefresh.yml`.
To top of the file is a global section that has all variables that can be used across pipelines (CI, CD, Promotion, security scan, etc) and across pipeline triggers. A step early in the pipeline will use the yq command to set all values under the global section and append them to a file name `env_vars_to_export`, which is exported with each Codefresh step.

The global section of the codefresh_vars.yml would be in the following format.

```
global:
  APP_NAME: customer-application
  DEV_REGISTRY: cdm-docker-dev-local
  STG_REGISTRY: cdm-docker-qa-local
  PROD_REGISTRY: cdm-docker-prod-local
  DEPLOY_REPO: hxp-ms-deploy
  CHART_PATH: k8s/charts
  APP_REPO: hxp-customer-application
```

The step including the `yq` command would look like the below:

```
  set_global_vars:
    stage: set_env
    title: Set environment variables
    type: freestyle
    image: huxhub.repo.mgnt.in/yq
    working_directory: "${{CF_REPO_NAME}}/ci"
    commands:
      # Set Global vars
      - yq r $VARS_FILE 'global' | sed -e 's/:\ /=/g' >> ${{CF_VOLUME_PATH}}/env_vars_to_export
    environment:
      - VARS_FILE=codefresh_vars.yml
```
Adding a new variable into the yaml file under the global section is the suggested way to manage variables used throughout the pipeline.

At the lower part of the file is a section that lists important environment values that are used during the CD pipeline. For example, a CI build will deploy to all dev environments so the pipeline will search for values set for the variables "DEV_VALUES", which could be one or more names for elm chart values files.

## Pre-reqs Before Adding a New Delivery
Adding environment related variables to the codefesh-vars.yml is actually the last step to enable deployment though pipelines, using GitOps. The pre-requisites to have a fully prepared environment include:
1. A functional cloud account provisioned.
2. A Kubernetes cluster created using TechOps automation, which configures the cluster with a set of standard Kubernetes applications.
3. ArgoCD installed on the cluster, which should be a part of the standard Kubernetes bootstrap.
4. ArgoCD configured to a top-level repository that has an Argo Application yaml file created to manage all applications on the cluster (commonly called App of Apps).
5. A functional Helm chart for an application and checked in to a deployment repository that is referenced in the Argo Application yaml file.
6. A values file with the application to manage environment specific settings and named after the cluster in the new cloud account.
7. A defined development delivery for a promoted application. For example, is there a dev, stg, and rc? Maybe just a dev? What other development stacks make up the delivery?

Pre-req number 7 above is very key. Not all deliveries will have an RC environment, for example, or even a stage. Because of these differences in the typical pattern for a development promotion delivery, each stack needs to be accounted for in our codefresh_vars.yml file. 

A full development delivery with dev, stg, and rc should be represented like this in the vars file.

```
delivery:
  aws1:
    DEV_VALUES: values-aws-dev1.yml
    STG_VALUES: values-aws-stg1.yml
    RC_VALUES: values-aws-rc1.yml
```
The delivery name "aws1" is an arbitrary name but should be recognizable to the cloud platform. 

Once all the pre-reqs are in place, the values file names can be added to the codefresh_vars.yml file and future pipeline runs will make the necessary changes to the values files in the deploy repo and ArgoCD, following GitOps principles, will orchestrate the application deploy to the new environment.

## CD and Promotion Pipeline
The CD pipeline will update the values file in the deploy repository. In addition, a promotion will deploy from the dev to the stg environment in the delivery if the particular trigger is called.

In the CD pipeline in Codefresh, there are triggers named for the delivery appended by "_promote". Each trigger has a unique ID that can be called as a post step from the environment. For example, a deploy to dev is successful in Azure (azure1) so a post step calls the pipeline with the trigger named `azure1_promote`. The same CD pipeline will get variables from the `codefresh_vars.yml` for the DEV_VALUES file (which will have the latest image.tag set) and update the values file STG_VALUES with the same image.tag value. The pipeline will also copy the image tag from the dev-local Artifactory repo to the stg-local (or equivalent) repo.

