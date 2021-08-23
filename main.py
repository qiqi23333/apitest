from utils.ParseExcel import ParseExcel
from config.public_data import *
from action.get_rely import GetRely
from utils.HttpClient import HttpClient
from action.data_store import RelyDataStore
from action.check_result import CheckResult
from action.write_result import WriteTestResult

# 框架的入口方法
def main():
    # 新建一个解析excel工具类的实例对象
    parseE = ParseExcel()
    parseE.loadWorkBook(FILEPATH)
    sheetObj = parseE.getSheetByName("API")

    # 获取active列的列对象
    activeList = parseE.getColumn(sheetObj, API_active)
    for idx, cell in enumerate(activeList[1:], 2):
        if cell.value == "y":
            # 需要执行的接口所在的行的对象
            rowObj = parseE.getRow(sheetObj, idx)
            apiName = rowObj[API_apiName - 1].value
            requestUrl = rowObj[API_requestUrl - 1].value
            requestMethed = rowObj[API_requestMothod - 1].value
            paramsType = rowObj[API_paramsType - 1].value
            apiTestCaseFileName = rowObj[API_apiTestCaseFileName - 1].value

            # 下一步需要读取接口用例表，获取接口的测试用例
            caseSheetObj = parseE.getSheetByName(apiTestCaseFileName) # obj类型
            caseActiveObj = parseE.getColumn(caseSheetObj, CASE_active) # tuple类型
            for c_idx, c_cell in enumerate(caseActiveObj[1:], 2):
                if c_cell.value == "y":
                    # 说明此case需要被执行
                    caseRowObj = parseE.getRow(caseSheetObj, c_idx)
                    requestData = caseRowObj[CASE_requestData - 1].value
                    requestData = eval(requestData) if requestData else {}
                    relyData = caseRowObj[CASE_relyData - 1].value
                    responseCode = caseRowObj[CASE_responseCode - 1].value
                    dataStore = caseRowObj[CASE_dataStore - 1].value
                    checkPoint = caseRowObj[CASE_checkPoint - 1].value

                    # 接口发送请求之前需要先做数据依赖的处理
                    if relyData:
                        requestData = GetRely.get(requestData, eval(relyData))
                    # 构造接口请求需要的数据，并调用HttpClient类中的方法发送接口情况，并获取响应结果
                    hc = HttpClient()
                    response = hc.request(requestUrl, requestMethed, paramsType, requestData)
                    if response.status_code == responseCode:
                        responseBody = response.json()

                        # 获取到接口的响应body后，接下来就是处理依赖数据的存储问题
                        if dataStore:
                            RelyDataStore.do(eval(dataStore), apiName, c_idx - 1, requestData, responseBody)
                        else:
                            print("第%s个接口的第%s条用例不需要依赖数据存储！" %(idx - 1, c_idx - 1))

                        # 接下来进行接口响应结果的结果校验
                        if checkPoint:
                            errorInfo = CheckResult.check(responseBody, eval(checkPoint))
                            WriteTestResult.write(parseE, caseSheetObj, responseBody, errorInfo, c_idx)
                        else:
                            print("第%s个接口的第%s条测试用例未设置校验点！")
                    else:
                        print("第%s个接口的第%s条用例所调用的接口响应失败，接口响应code=%s, 而预期接口响应code=%s"
                              %(idx - 1, c_idx - 1, response.status_code, responseCode))
                else:
                    print("第%s个接口的第%s条用例被忽略执行！" %(idx - 1, c_idx - 1))
        else:
            print("第%s个接口被设置忽略执行！" %(idx - 1))


if __name__ == "__main__":
    main()