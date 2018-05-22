# lambda-function.python.test

## workflow的整合測試：
當程式收到toolId時，會先到dynamodb找出對應的workflowName，之後將workflowName做test case產生出一連串的commands，之後依序將這些command發布給sns，最後判斷sns的response是否正常，如果不正常可以透過ELK API去做查詢。

## CommandsParser lambda function本地端unittest：
### 本地端workflow的整合測試：
透過test case產生的指令，將指令傳給本地端的lambda function後判斷是否成功發送到potato測試群組並回傳２００，如果不正常可以透過ELK API去做查詢。
### 本地端測試CommandMoudle：
需要先初始化一個lambdaHandler物件以及workflowRequestContent，將commandModule所需要的參數傳入後，即可對各個ComandModule做測試。


