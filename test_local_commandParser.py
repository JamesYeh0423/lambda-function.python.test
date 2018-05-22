import unittest
import json
from CommandsParser import lambdaHandler
from CommandModules import *
import boto3
# For display chinese characters
import io, sys, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class TestCommandParser(unittest.TestCase):

    message_list = ["help", "/portal", "/portal mgJj6vG4uYm9ZK5AbDTDr7", "/yuacc yp2", "/yuacc yp2 -t 10m",
                    "/yuacc yp2 -t -1", "/dntime dns2 -i n:google.com", "onr Liho", "whoami", "/domain_bne",
                    "/ip -add ip:11.／11.11.254 port:99 dn:www.test.edu acc:admin rg:RR ft:RRR note:note desc:desc name:tttt123 os:centos6, envType:local",
                    "/ip -del name:tttt123", "pbg"]

    def local_lambda_req(self, message):
        snsRequestContent = json.load(open('/Users/jamesyeh/PentWork/test/AWS_SNS_Request_Content_v3.json', encoding="utf-8"))
        snsRequestContent["Records"][0]["Sns"]["Message"] = json.dumps({"default": message})
        try:
            r = lambdaHandler(snsRequestContent, "")
            return r
        except Exception as err:
            pass

    def test_cmd(self):
        cmd_success = dict()
        cmd_fail = dict()
        for message in self.message_list:
            r = self.local_lambda_req(message)
            try:
                self.assertEqual(r['statusCode'], 200)
                cmd_success[message] = r['statusCode']
            except (AssertionError, TypeError) as err:
                try:
                    cmd_fail[message] = r['statusCode'] + "; " + r['message']
                except TypeError:
                    pass
        print("cmd {} has tested successfully.".format(cmd_success))
        print("cmd {} are fail.".format(cmd_fail))


if __name__ == '__main__':
    unittest.main()



