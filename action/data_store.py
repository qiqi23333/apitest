from config.public_data import REQUEST_DATA, RESPONSE_DATA

class RelyDataStore(object):
    def __init__(self):
        pass

    @classmethod
    def do(self, storePoint, apiName, caseId, request_source, response_source):
        type_map = {"request":REQUEST_DATA, "response":RESPONSE_DATA}
        r_map = {"request": request_source, "response": response_source}
        for key, value in storePoint.items():
            # 说明应该存入公共变量REQUEST_DATA中
            for i in value:
                # 说明：此处默认传入的数据源都是一层dict数据类型
                tmp = r_map[key].get(i, "")
                if tmp:
                    # REQUEST_DATA[apiName][str(caseId)][i] = tmp
                    if apiName not in type_map[key]:
                        # 说明存储数据的结构还未生成，需要指明数据存储结构
                        type_map[key][apiName] = {str(caseId): {i: tmp}}
                    else:
                        # 说明存储数据结构中最外层结构是完整的
                        if str(caseId) in type_map[key][apiName]:
                            type_map[key][apiName][str(caseId)][i] = tmp
                        else:
                            type_map[key][apiName][str(caseId)] = {i: tmp}
                else:
                    print("请求参数中不存在字段" + i)


if __name__ == "__main__":
    storePoint = {"request":["username","password"],"response":["code"]}
    apiName = "register"
    caseId = 1
    request_source = {"username":"lisi1231","password":"wcx123wac1","email":"wcx@qq.com"}
    response_source = {'username': 'zhwu1231', 'code': '01'}
    RelyDataStore.do(storePoint, apiName, caseId, request_source, response_source)
    print(REQUEST_DATA)
    print(RESPONSE_DATA)