import requests
import json               # 將python內部的資料型態dict轉換成json檔案，或者反之

# 原理:
# 我們(client)發出request給華南銀行的伺服器(server)，
# 華南銀行的server會辨別我們的request(也就是那一串url, 網址)，透過我們給的參數(也就是api_key、uiid等)
# 辨識我們要什麼回應(response)，回應就是回傳給我們的資料(有各種不同形式，有時候是網頁，有時候是pdf)
# 在這個case裡面的response是json檔。(json檔是網路傳輸資料的一種標準資料格式，很輕量所以常常用以傳遞大量資料)


# 發出request，將華南銀行server的response存在response這個變數(這一步就是透過API得到資料)
response = requests.get(url="https://www.fintechersapi.com/bank/huanan/getUUIDs?api_key=cef5e50c-c6df-46c0-86a8-69fa2fdc0fe1", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"})

# response印出來大概長這樣
# {
#   "uuid_list": [
#     "2bef6593954b43bcb6bc93260e4ec25f",
#     "b66410d666b946989c4d42423041edbd",
#     "eb28013699de437f97bf7d7195abe2b9",
#     "e8e8a73a6a244c42880128a9e0bdb060",
#     "2b9ddc16bd0048c9935528ed9c14a697",
#     "1827e418bbe746a18c6a2701ba1fbc16",
#     "0747308e74ca4aa3bc4a4d498d52c557",
#     "fc05790459ca442db697d191f4bc245f",
#     "9a2c250157354020a0f31de622f15713",
#     "184f70b3fb054157b7e797f1e7f68035"
#   ]
# }

                                
# uuid_list 取得, 一次10筆
# 用response.text把response轉成text(這樣才能在python裡面做處理)
# 再用json.loads把response.text的內容轉換成dict資料型態
response = json.loads(response.text)        
# print(response)            # 印出dict    
# print(type(response))      # dict的資料型態

# 銀行客戶帳戶API
# 根據這個範例的結構解析
# {
#   "trans_record": [
#     {
#       "account_num": "160345191470",
#       "trans_date": "2015-10-01",
#       "amount": 2000,
#       "balance": 4282299,
#       "trans_channel": "臨櫃",
#       "id": 25827,
#       "trans_type": "台幣轉帳"
#     }
#   ],
#   "uuid": "833ecc53b7064974a0abaeb986da9c7a"
# }
while True:
    i = 1         # 用來記數
    for uuid in response["uuid_list"]:
        # 取得保險資料
        resp_insurance = requests.get(url="https://www.fintechersapi.com/bank/huanan/insurance/record?uuid={}&api_key=cef5e50c-c6df-46c0-86a8-69fa2fdc0fe1".format(uuid), headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"})
        # 處理編碼問題，先記起來!
        resp_insurance = resp_insurance.text.encode('ISO-8859-1').decode('utf-8')
        
        # 取得客戶基本資訊
        resp_client = requests.get(url="https://www.fintechersapi.com/bank/huanan/digitalfin/customers?uuid={}&api_key=cef5e50c-c6df-46c0-86a8-69fa2fdc0fe1".format(uuid), headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"})
        # 取得客戶資料內近10筆交易資訊
        resp_recent_10 = requests.get(url="https://www.fintechersapi.com/bank/huanan/digitalfin/account_records?uuid={}&api_key=cef5e50c-c6df-46c0-86a8-69fa2fdc0fe1".format(uuid), headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"})                              
        print("第{}筆資料, ".format(i))   # 標註是第幾筆資料
        i += 1
        print(f'uuid: {uuid}')           # 印出uuid來看一下
        # 這三行都是把json檔案的資料轉成python的dict
        resp_insurance = json.loads(resp_insurance)
        resp_client = json.loads(resp_client.text)
        resp_recent_10 = json.loads(resp_recent_10.text)
        
        print("保險資料如下: \n", resp_insurance)                                    # dict型態，如果需要更進一步應用(通常需要), 就再把欄位分解出來
        for column in resp_insurance["insurance_record"][0]:                        # 分解
            print(column, resp_insurance["insurance_record"][0][column], sep="\t")  # "\t"代表每筆資料用tab隔開
        
        print("客戶資料如下: \n", resp_client)                                       # dict型態
        for column in resp_client:                                                  # 分解
            print(column, resp_client[column], sep="\t")

        print("客戶近10筆交易資料如下: \n", resp_recent_10)                           # dict型態
        for column in resp_recent_10["trans_record"][0]:                            # 分解
            print(column, resp_recent_10["trans_record"][0][column], sep="\t")

        answer = input("下一筆請按enter, 離開則隨便輸入再按enter: ")
        if answer == "":
            continue
        else:
            break

    leave_or_not_text = input("按enter繼續下個十筆，其於輸入皆會離開(程式結束)")
    if leave_or_not_text == "":
        continue
    else:
        break
