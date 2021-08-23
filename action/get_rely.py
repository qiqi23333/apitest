from config.public_data import REQUEST_DATA, RESPONSE_DATA
from utils.Md5_Encrypt import md5_encrypt

class GetRely(object):
    def __init__(self):
        pass

    @classmethod
    def get(self, dataSource, relyData):
        # 处理依赖数据
        dataS = dataSource.copy()
        for key, value in relyData.items():
            if key == "request":
                # 说明应该去REQUEST_DATA公共变量中获取数据
                for k, v in value.items():
                    interfaceName, case_id = v.split("->")
                    try:
                        val = REQUEST_DATA[interfaceName][case_id][k]
                        if k == "password":
                            # 需要对密码进行MD5加密处理
                            dataS[k] = md5_encrypt(val)
                        else:
                            dataS[k] = val
                    except Exception as err:
                        raise err
            elif key == "reponse":
                # 说明应该去RESPONSE_DATA公共变量中获取数据
                for k, v in value.items():
                    interfaceName, case_id = v.split("->")
                    try:
                        dataS[k] = RESPONSE_DATA[interfaceName][case_id][k]
                    except Exception as err:
                        raise err
        return dataS

if __name__ == "__main__":
    REQUEST_DATA = {"register":
                        {"1": {"username": "zhangsan", "password": "zhangsan01"}},
                        "2": {"username": "lisi", "password": "lisi01"}
                    }
    RESPONSE_DATA = {"register":{"1":{"userid":123}}}
    dataSource = {"username":"","password":"","userid":0}
    relyData = {"request":{"username":"register->1","password":"register->1"},
                "reponse":{"userid":"register->1"}}
    res = GetRely.get(dataSource, relyData)
    print(res)
    # -----------------------

    # gr = GetRely()
    # res = gr.get(dataSource, relyData)
    # print(res)

















