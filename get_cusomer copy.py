import requests             # 發出請求的模組, 非常實用, 強烈建議納入你的工具包。
import json                 # 關於json檔案的轉換, 能夠將python內部的資料型態dict轉換成json檔案, 或者反之。

# 原理概論: 
# 我們(client)透過發出request, 也就是請求給"華南銀行"的伺服器(server), 
# 華南銀行的server會將我的們請求(也就是那一串url, 網址)辨別, 透過我們給予的參數(也就是)api_key, uiid等等
# 辨識出我們需要甚麼回應(response), 回應就是資料, 只是有各種不同形式, 有的時候是網頁(也就是平常我們上網的時候, 那就是一個例子)
# 有的時候是pdf, 大家應該有用過goole開過瀏覽器吧, 那也是一種response
# 然而, 我們這次的例子response是json檔案。
# json檔案是網路傳輸資料一種標準格式, 因為資料規則簡單, 需要的容量少, 因此常常用以傳遞大量資料。


# 發出request, 並將response存在response這個變數中
# 也就是透過API直接得到資料。
# get是一種函式, 是requests這個類別(class)的函式, 這個例子我們輸入兩個參數, 一個是url(地址), 另一個是headers(標頭, 你用什麼東西發出請求, 大概懂概念就好))
response = requests.get(url='https://www.fintechersapi.com/bank/huanan/getUUIDs?api_key=cef5e50c-c6df-46c0-86a8-69fa2fdc0fe1', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                 'AppleWebKit/537.36 (KHTML, like Gecko)'
                                 'Chrome/75.0.3770.100 Safari/537.36'})
# 上面的response大概長這樣
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
# json是一個類別, 我們利用其函式loads, 將response.text內容轉換成python內部的dict資料型態
# 而response.text則是將回應轉化成text(可以被轉化成python的檔案), 這一行不是太重要, 固定用法
response = json.loads(response.text)        
# print(response)                             # dict 資料呈現
# print(type(response))                       # dict

# 銀行客戶帳戶API
# 下面是一個範例, 根據他們的結構進行解析。
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
    i = 1                                   # 只是用來記數
    for uuid in response['uuid_list']:
        # 下面這個是保險資料的取得, 若要查看這方面資料將其下面三行解除comment
        resp_insurance = requests.get(url='https://www.fintechersapi.com/bank/huanan/insurance/record?uuid={}&api_key=cef5e50c-c6df-46c0-86a8-69fa2fdc0fe1'.format(uuid), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'            
                            'AppleWebKit/537.36 (KHTML, like Gecko)'
                            'Chrome/75.0.3770.100 Safari/537.36'})
        # input(resp_insurance.encoding), 得到ISO-8859-1編碼
        # 下面這行是處理編碼問題, 不太重要, 有需要再跟大家講解。
        resp_insurance = resp_insurance.text.encode('ISO-8859-1').decode('utf-8')
        
        # 下面這個是客戶基本資訊的取得, 若要查看將其下面三行解除comment
        resp_client = requests.get(url='https://www.fintechersapi.com/bank/huanan/digitalfin/customers?uuid={}&api_key=cef5e50c-c6df-46c0-86a8-69fa2fdc0fe1'.format(uuid), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'            
                            'AppleWebKit/537.36 (KHTML, like Gecko)'
                            'Chrome/75.0.3770.100 Safari/537.36'})
        # 下面這個是客戶資料近10筆交易資訊的取得, 若要查看將其下面三行解除comment
        resp_recent_10 = requests.get(url='https://www.fintechersapi.com/bank/huanan/digitalfin/account_records?uuid={}&api_key=cef5e50c-c6df-46c0-86a8-69fa2fdc0fe1'.format(uuid), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                    'AppleWebKit/537.36 (KHTML, like Gecko)'
                                    'Chrome/75.0.3770.100 Safari/537.36'})                                  
        print('第{}筆資料, '.format(i))                                  # 這個地方只是用來標註第幾筆
        i += 1
        print(f'uuid: {uuid}')                    # 只是輸出uuid給我們看一下
        # 下面三行都是將資料json轉乘python的dict。
        resp_insurance = json.loads(resp_insurance)
        resp_client = json.loads(resp_client.text)
        resp_recent_10 = json.loads(resp_recent_10.text)
        
        print('保險資料如下: \n', resp_insurance)                      # 這會直接呈現dict型態, 如果需要更進一步應用(通常需要), 就再把欄位分解出來
        for column in resp_insurance['insurance_record'][0]:     # 陽春分解
            print(column, resp_insurance['insurance_record'][0][column], sep='\t')
        
        print('客戶資料如下: \n', resp_client)                         # dict型態
        for column in resp_client:                               # 陽春分解
            print(column, resp_client[column], sep='\t')

        print('客戶近10筆交易資料如下: \n', resp_recent_10)
        for column in resp_recent_10['trans_record'][0]:
            print(column, resp_recent_10['trans_record'][0][column], sep='\t')

        answer = input('下一筆請按enter, 離開則隨便輸入再按enter: ')
        if answer == '':
            continue
        else:
            break

    leave_or_not_text = input('按enter繼續下個十筆, 其於輸入皆會離開(程式結束)')
    if leave_or_not_text == '':
        continue
    else:
        break