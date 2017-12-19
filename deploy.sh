#!/bin/bash

# Exit on any error
set -e

export IMG_TAG=$(echo $CIRCLE_SHA1 | cut -c -7)
# install kubectl
#  set key and authenticate gcloud
# configure gcloud
# I need to build the image
# then push the new image to gcp
# deploy with kubectl

DOCKER_SOURCE=$HOME/docker-src

DEPLOYMENT_ENVIRONMENT="staging"
GCLOUD_SERVICE_KEY=$GCLOUD_SERVICE_KEY_STAGING

if [ "$CIRCLE_BRANCH" == 'master' ]; then
  DEPLOYMENT_ENVIRONMENT="production"
  GCLOUD_SERVICE_KEY=$GCLOUD_SERVICE_KEY_PROD
  PROJECT_NAME=$PROJECT_NAME_PROD
  CLUSTER_NAME=$CLUSTER_NAME_PROD
  CLOUDSDK_COMPUTE_ZONE=$CLOUDSDK_COMPUTE_ZONE_PROD
fi

echo " Deploying to ${DEPLOYMENT_ENVIRONMENT}"

# set key and authenticate gcloud
echo $GCLOUD_SERVICE_KEY | base64 --decode > ${HOME}/gcloud-service-key.json
gcloud auth activate-service-account --key-file ${HOME}/gcloud-service-key.json

# configure gcloud
gcloud --quiet config set project $PROJECT_NAME
gcloud --quiet config set container/cluster $CLUSTER_NAME
gcloud --quiet config set compute/zone ${CLOUDSDK_COMPUTE_ZONE}
gcloud --quiet container clusters get-credentials $CLUSTER_NAME

rm -rf ${DOCKER_SOURCE}
mkdir -p ${DOCKER_SOURCE}
echo "Docker source , ${DOCKER_SOURCE}"

# Pull docker repo
echo " Pulling docker image source from git "
/usr/bin/git clone --depth=1 git@github.com:andela-skanyi/bucketlist_api.git ${DOCKER_SOURCE}
echo " Successfully pulled "

echo " Building image"
gcloud docker -- build -t gcr.io/${PROJECT_NAME}/${IMAGE}:$IMG_TAG  ${DOCKER_SOURCE} > /dev/null
docker tag gcr.io/${PROJECT_NAME}/${IMAGE}:${IMG_TAG} gcr.io/${PROJECT_NAME}/${IMAGE}:latest
echo " Successfully built"

echo " Pushing image"
gcloud docker -- push gcr.io/${PROJECT_NAME}/${IMAGE}:$IMG_TAG
gcloud docker -- push gcr.io/${PROJECT_NAME}/${IMAGE}:latest
echo " Successfully pushed"

echo " Deploying to ${DEPLOYMENT_ENVIRONMENT}"
kubectl config current-context
kubectl set image deployment/${DEPLOYMENT} ${CONTAINER_NAME}=gcr.io/${PROJECT_NAME}/${IMAGE}:$IMG_TAG
echo " Successfully deployed to ${DEPLOYMENT_ENVIRONMENT} :)"
