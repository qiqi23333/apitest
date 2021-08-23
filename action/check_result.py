import re

class CheckResult(object):
    def __init__(self):
        pass

    @classmethod
    def check(self, responseObj, checkPoint):
        errorKey = {}
        for key, value in checkPoint.items():
            s_data = responseObj.get(key, None)
            if not s_data:
                errorKey[key] = "not exists"
                continue
            if isinstance(value, (str, int)):
                # 说明是等值校验
                if s_data != value:
                    errorKey[key] = s_data
            elif isinstance(value, dict):
                # 说明是需要通过正则校验或数据类型校验
                if "type" in value:
                    # 说明是数据类型校验
                    typeS = value["type"]
                    if typeS == "N":
                        # 说明是整形
                        if not isinstance(s_data, int):
                            errorKey[key] = s_data
                    elif typeS == "S":
                        # 说明是字符类型
                        if not isinstance(s_data, str):
                            errorKey[key] = s_data
                    elif typeS == "xxx":
                        pass
                elif "value" in value:
                    # 说明是正则表达式校验
                    regStr = value["value"]
                    rg = re.match(regStr, "%s" %s_data)
                    if not rg:
                        errorKey[key] = s_data
        return errorKey

if __name__ == "__main__":
    checkPoint = {"code":"00","userid":{"type":"N"}, "id":{"value":"^\d+$"}, "password":"\w+"}
    responseData = {"code":"01", "userid":123, "id":"dfg","usename":"zhangsan"}
    errorInfo = CheckResult.check(responseData, checkPoint)
    print(errorInfo)

















