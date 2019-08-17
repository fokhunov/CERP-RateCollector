#!/usr/bin/env bash

set -e          # exit if any command fails
set -u          # prevent using an undefined variable
set -o pipefail # force pipelines to fail on the first non-zero status

step () {
  echo -e "\033[38;5;11m- $1\033[m"
}


COUNTRY=${1?country should be provided as the first parameter}
ENV=${2?env should be provided as the second parameter}
VERSION=${3?version should be provided as the third parameter}
LOGLEVEL=${4?log level should be provided as the third parameter}

BASE_DIR="$(dirname $0)"
PARAMS="Country=$COUNTRY LogLevel=$LOGLEVEL"

PROJECT_NAME="CurrencyExchangeRatePlatform"
SERVICE_NAME="CERP-RateCollector-${COUNTRY}"
STACK_NAME="${SERVICE_NAME}-${ENV}"

GLOBAL_TAGS="Owner=build4use \
    ProjectName=$PROJECT_NAME \
    ServiceName=$SERVICE_NAME \
    Env=$ENV \
    Version=$VERSION"

step "Begin deployment of ${STACK_NAME}"

step "Send resources to S3"
LAMBDA_DEPLOYMENT_BUCKET=$(echo "$STACK_NAME-lambda" | tr '[:upper:]' '[:lower:]')
EXISTING_BUCKETS=$(aws s3 ls --profile "$AWS_PROFILE")
if [[ "$EXISTING_BUCKETS" != *$LAMBDA_DEPLOYMENT_BUCKET* ]]; then
    echo "S3 bucket $LAMBDA_DEPLOYMENT_BUCKET does not exist. Creating..."
    aws s3 mb "s3://$LAMBDA_DEPLOYMENT_BUCKET" --profile "$AWS_PROFILE"
fi


step "Package SAM template"
PACKAGED_OUTPUT_FILE="${BASE_DIR}/${STACK_NAME}-${VERSION}.yml"
sam package \
    --template-file "${BASE_DIR}/template.yml" \
    --output-template-file "$PACKAGED_OUTPUT_FILE" \
    --s3-bucket "$LAMBDA_DEPLOYMENT_BUCKET"


step "Deploy to AWS"
sam deploy \
    --template-file $PACKAGED_OUTPUT_FILE \
    --stack-name $STACK_NAME \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides $PARAMS \
    --tags $GLOBAL_TAGS \
    --debug
step "Deploying complete"