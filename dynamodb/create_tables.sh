#! /usr/bin/env bash

# Avoid pagination of AWS CLI output
export AWS_PAGER=""

(aws dynamodb create-table \
    --table-name items \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST)