#!/bin/bash

# Exit on any error
set -e

# install kubectl
#  set key and authenticate gcloud
# configure gcloud
# I need to build the image
# then push the new image to gcp
# deploy with kubectl

DOCKER_SOURCE=$HOME/docker-src

DEPLOYMENT_ENVIRONMENT="staging"
if [ "$CIRCLE_BRANCH" == 'master']; then
  DEPLOYMENT_ENVIRONMENT="production"
  GCLOUD_SERVICE_KEY=$GCLOUD_SERVICE_KEY_PROD
  PROJECT_NAME=$PROJECT_NAME_PROD
  CLUSTER_NAME=$CLUSTER_NAME_PROD
  CLOUDSDK_COMPUTE_ZONE=$CLOUDSDK_COMPUTE_ZONE_PROD
fi

echo " Deploying to ${DEPLOYMENT_ENVIRONMENT}"
# install kubectl and gcloud
  echo " Installing and configuring google cloud"
  sudo /opt/google-cloud-sdk/bin/gcloud --quiet version
  sudo /opt/google-cloud-sdk/bin/gcloud --quiet components update --version 120.0.0
  sudo /opt/google-cloud-sdk/bin/gcloud --quiet components update --version 120.0.0 kubectl

# set key and authenticate gcloud
echo $GCLOUD_SERVICE_KEY | base64 --decode > ${HOME}/gcloud-service-key.json
sudo /opt/google-cloud-sdk/bin/gcloud auth activate-service-account --key-file ${HOME}/gcloud-service-key.json

# configure gcloud
sudo /opt/google-cloud-sdk/bin/gcloud --quiet config set project $PROJECT_NAME
sudo /opt/google-cloud-sdk/bin/gcloud --quiet config set container/cluster $CLUSTER_NAME
sudo /opt/google-cloud-sdk/bin/gcloud --quiet config set compute/zone ${CLOUDSDK_COMPUTE_ZONE}
sudo /opt/google-cloud-sdk/bin/gcloud --quiet container clusters get-credentials $CLUSTER_NAME

rm -rf ${DOCKER_SOURCE}
mkdir -p ${DOCKER_SOURCE}

# Pull docker repo
echo " Pulling docker image source from git "
/usr/bin/git clone --depth=1 -b git@github.com/andela-skanyi/bucketlist_api.git ${DOCKER_SOURCE}
ecjo " Successfully pulled "

echo " Building image"
sudo /opt/google-cloud-sdk/bin/gcloud docker -- build -t gcr.io/${PROJECT_NAME}/${IMAGE}:$IMG_TAG  ${DOCKER_SOURCE} > /dev/null
sudo docker tag -f gcr.io/${PROJECT_NAME}/${IMAGE}:${IMG_TAG} gcr.io/${PROJECT_NAME}/${IMAGE}:latest
echo " Successfully built"

echo " Pushing image"
sudo /opt/google-cloud-sdk/bin/gcloud docker push gcr.io/${PROJECT_NAME}/${IMAGE}:$IMG_TAG
sudo /opt/google-cloud-sdk/bin/gcloud docker push gcr.io/${PROJECT_NAME}/${IMAGE}:latest
echo " Successfully pushed"

echo " Deploying to ${DEPLOYMENT_ENVIRONMENT}"
/opt/google-cloud-sdk/bin/kubectl config current-context
/opt/google-cloud-sdk/bin/kubectl set image deployment/${DEPLOYMENT} ${CONTAINER_NAME}=gcr.io/${PROJECT_NAME}/${IMAGE}:$IMG_TAG
echo " Successfully deployed to ${DEPLOYMENT_ENVIRONMENT} :)"
