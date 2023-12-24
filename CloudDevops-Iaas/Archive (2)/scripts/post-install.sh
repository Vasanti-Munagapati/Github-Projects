#!/bin/bash

HOME_PATH="/opt/codedeploy-agent/deployment-root"
SUFFIX="deployment-archive"

SERVICE="backend/service"
SERVICE_PATH="/RawDatavm"
LOCAL_PREFIX="$HOME_PATH/$DEPLOYMENT_GROUP_ID/$DEPLOYMENT_ID/$SUFFIX"
CODE_PATH="$LOCAL_PREFIX/$SERVICE"

# COPY_FILES="$CODE_PATH/."

SOURCE_FILE="rawdatatask-2.py"
REQ_FILE="requirements.txt"

SOURCE_PATH="$CODE_PATH/$SOURCE_FILE"
REQ_PATH="$CODE_PATH/$REQ_FILE"
FRESH_REQ_PATH="$SERVICE_PATH/$REQ_FILE"

ARTIFACT="backend.zip"
ARTIFACT_PATH="$HOME_PATH/$DEPLOYMENT_GROUP_ID/$DEPLOYMENT_ID/$SUFFIX/$ARTIFACT"

if [ ! -d "/RawDatavm" ]
then
	sudo mkdir /RawDatavm
fi

sudo pwd
sudo unzip -o $ARTIFACT_PATH -d $LOCAL_PREFIX

sudo cp  $SOURCE_PATH $SERVICE_PATH
sudo cp  $REQ_PATH $SERVICE_PATH

sudo pip3 install -r $FRESH_REQ_PATH
