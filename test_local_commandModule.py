import json
from CommandModules import *
import unittest
# For display chinese characters
import io, sys, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class TestTool(unittest.TestCase):

    def initialize(self, message):
        snsRequestContent = json.load(open('/Users/jamesyeh/PentWork/test/AWS_SNS_Request_Content_v3.json', encoding="utf-8"))
        snsRequestContent["Records"][0]["Sns"]["Message"] = json.dumps({"default": message})
        arn = ":".join(((snsRequestContent["Records"][0]["Sns"]["TopicArn"]).split(":"))[:-1]) + ":"
        handler = CommandsHandler(arn)
        workflowRequestContent = dict({"queue": list(), "results": dict()})
        snsAttribute = snsRequestContent["Records"][0]["Sns"]["MessageAttributes"]
        potatoObject = {
            "toolId": "ptbd372662f43611e7a1d28c859066a326",
            "params": {},
            "conditions": {},
        }
        for key, value in snsAttribute.items():  # potatoObj is equal RequestContent Queue and params is from snsAttribute.
            potatoObject["params"][key] = value["Value"]
            if key == "chat_id":
                workflowRequestContent["chatId"] = value["Value"]
        handler.setPotatoListener(potatoObject)
        handler.setMessage(message)
        handler.setLogBody({"logAction": False})
        handler.getWorkflowsShow(incomingSource="potato")
        userId = potatoObject["params"]["user_id"]
        basePath = handler.apiAgent["token"]["url"]
        workflowRequestContent["token"] = handler.getToken("POST", basePath, userId)
        return handler, workflowRequestContent

    def test_getHelp(self):
        message = "help"
        handler, workflowRequestContent = self.initialize(message)
        responseMsg = getHelp(handler, workflowRequestContent, "")
        handler.messageHandler(responseMsg, message)
        self.assertEqual(responseMsg['statusCode'], 200)


if __name__ == '__main__':
    unittest.main()
