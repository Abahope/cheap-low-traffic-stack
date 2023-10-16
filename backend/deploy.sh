#! /usr/bin/env bash
# exit when any command fails
set -e
# Avoid pagination of AWS CLI output
export AWS_PAGER=""

dt=$(date '+%d-%m-%Y-%H-%M-%S')
DEPLOY_HISTORY_FILE="deploy_history.txt"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
LAMBDA_ROLE_NAME="cheap_demo_lambda"
AWS_REGION="us-east-1"

# Login to ECR
echo "Logging into ECR"
(aws ecr get-login-password \
    --region $AWS_REGION | docker login \
    --username AWS \
    --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com)

# Create the ECR repository if it doesn't exist
ecr_repo_name="cheap_backend"
if [ -z "$(aws ecr describe-repositories | grep $ecr_repo_name)" ]
then
    echo "Creating ECR repository"
    aws ecr create-repository --repository-name $ecr_repo_name
    echo "Created ECCR repository"
fi

# Build docker image and push to ECR
docker_image_name="cheap_backend"
docker build -t $docker_image_name .
ecr_image=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ecr_repo_name:$dt
docker tag $docker_image_name:latest $ecr_image
docker push $ecr_image


# Create/update the lambda
function_key="cheap_backend"
function_name=$(aws lambda list-functions | grep FunctionName | grep $function_key | cut -d '"' -f 4)
if [ -z "$function_name" ]
then
    echo "Creating lambda function"
    (aws lambda create-function \
        --function-name $function_key \
        --code ImageUri=$ecr_image \
        --package-type Image \
        --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/${LAMBDA_ROLE_NAME} \
        --timeout 30 \
        --memory-size 128 \
        --architecture arm64)
else
    echo "Updating lambda function"
    (aws lambda update-function-code \
        --function-name $function_name \
        --image-uri $ecr_image)
fi

# Create a function url if it doesn't exist
set +e
aws lambda get-function-url-config --function-name $function_key --query FunctionUrl --output text
exit_code=$?
set -e
if [ $exit_code -ne 0 ]
then
    echo "Creating function url"
    (aws lambda create-function-url-config \
        --function-name $function_key \
        --auth-type NONE)
else
    echo "Function url already exists"
fi

# Allow function to be invoked by anyone if not already allowed
set +e
aws lambda get-policy --function-name $function_key --query Policy --output text
exit_code=$?
set -e
if [ $exit_code -ne 0 ]
then
    echo "Allowing lambda function to be invoked by anyone"
    (aws lambda add-permission \
        --function-name $function_key \
        --action lambda:InvokeFunctionUrl \
        --statement-id FunctionURLAllowPublicAccess \
        --function-url-auth-type NONE \
        --principal "*")
else
    echo "Lambda function already has a policy"
fi

# Update the deployment history file
function_url=$(aws lambda get-function-url-config --function-name $function_key --query FunctionUrl --output text)
echo "On $dt, deployed commit $(git rev-parse --short HEAD) at $function_url" >> $DEPLOY_HISTORY_FILE

# Update the frontend with the new backend url
cd ../frontend
sed -i.bak "s|NEXT_PUBLIC_API_HOST=.*|NEXT_PUBLIC_API_HOST=$function_url|g" .env.production
rm .env.production.bak