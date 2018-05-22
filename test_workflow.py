import boto3
import json
import time
from botocore.exceptions import ClientError
import requests

region = "us-east-1"
dbResource = boto3.resource("dynamodb", region_name=region)
snsClient = boto3.client("sns", region_name=region)
attrs = {"message_source":
                {
                    "DataType": "String",
                    "StringValue": "potato"
                  },
                  "first_name": {
                    "DataType": "String",
                    "StringValue": "test_user"
                  },
                  "last_name": {
                    "DataType": "String",
                    "StringValue": "HaHa"
                  },
                  "user_id": {
                    "DataType": "String",
                    "StringValue": "20041626"
                  },
                  "uuid": {
                    "DataType": "String",
                    "StringValue": "1debb975-ea07-4fab-88b1-bbe6fb414ec4"
                  },
                  "chat_Type": {
                    "DataType": "String",
                    "StringValue": "2"
                  },
                  "chat_id": {
                    "DataType": "String",
                    "StringValue": "10012105"
                  },
                  "message_id": {
                    "DataType": "String",
                    "StringValue": "284"
                  },
                  "chat_title":{
                    "DataType": "String",
                    "StringValue": "hahahaChat"}
            }


def fetch_workflow_name(tool_id):
    fetch_workflow_start = time.time()
    table = dbResource.Table("WorkflowDetail")
    response = table.scan()
    workflow_name_list = list()
    for item in response['Items']:
        if tool_id in item['configuration']:
            workflow_name_list.append(item['workflowName'])
    fetch_workflow_end = time.time()
    print("fetch_workflow time spend {} sec.".format(fetch_workflow_end-fetch_workflow_start))
    return workflow_name_list


def create_test_case(workflow_name_list):
    cmd_list = workflow_name_list  # list()
    return cmd_list


def elk_api(sns_response_log, sns_response, message):
    if sns_response['ResponseMetadata']['HTTPStatusCode'] == 200:
        log = requests.get(url='https://api.github.com/events').text
        sns_response_log[message] = log
        return sns_response_log
    else:
        sns_response_log[message] = 'http request error.'
        return sns_response_log


def trigger_cmd_parser(tool_id):
    workflow_name_list = ['dntime', 'help']#fetch_workflow_name(tool_id)
    print(workflow_name_list)
    cmd_list = create_test_case(workflow_name_list)
    sns_topic = "arn:aws:sns:us-east-1:657315558120:potato-msg"
    sns_response_log = dict()
    if cmd_list:
        for message in cmd_list:
            try:
                sns_response = snsClient.publish(
                    TopicArn=sns_topic,
                    Message="default: /{} dns2 -i n:google.com".format(message),
                    MessageStructure="string",
                    MessageAttributes=attrs
                )
            except ClientError as ce:
                request_body = "Something wrong about workflows configuration. Detail as following: \n" + ce.response["Error"]["Message"]
                sns_response = snsClient.publish(
                    TopicArn=sns_topic,
                    Message=json.dumps({"default": request_body}),
                    MessageStructure="string"
                )
            print(sns_response)
            sns_response_log = elk_api(sns_response_log, sns_response, message)
        return sns_response_log


def main():
    tool_id = "pt15dc1868f43711e7853d8c859066a326"
    sns_response = trigger_cmd_parser(tool_id)
    print(sns_response)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print("Time spend {} sec.".format(end-start))

