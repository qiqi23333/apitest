import os

# 当前项目的根目录绝对路径
BASEDIR = os.path.dirname(os.path.dirname(__file__))

# 测试数据文件的绝对路径
FILEPATH = BASEDIR + "\\TestData\\inter_test_data.xlsx"

# 测试用例数据表中列数字映射
API_apiName = 2
API_requestUrl = 3
API_requestMothod = 4
API_paramsType = 5
API_apiTestCaseFileName = 6
API_active = 7

CASE_requestData = 1
CASE_relyData = 2
CASE_responseCode = 3
CASE_responseData = 4
CASE_dataStore = 5
CASE_checkPoint = 6
CASE_active = 7
CASE_status = 8
CASE_errorInfo = 9

# 依赖数据存储公共变量
REQUEST_DATA = {} # request data
RESPONSE_DATA = {} # response data

















