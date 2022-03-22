import json
import requests

url = "https://apigw.qa.91dev.tw/ec/V1/SalePage/GetStock"

# 情境
request_body = {
   "id": 371499,
   "skuId": 751324
}
request_body_onlymust = {
   "id": 371499
}
request_body_Error_errorskuid = {
   "id": 371499,
   "skuId": 751366
}
request_body_Error_errorid = {
   "id": 370000
}
request_body_Error_errorFormatid = {
   "id": "ccc"
}
request_body_Error_noid = {
   "skuId": 751324
}

# x-api-key
headers = {
   "x-api-key": "3nEI05nlnq9XaZ9mJBuSK827ktigIU9N2manKnfd"
}
headers_Error_errorkey = {
   "x-api-key": "3nEI05nlnq9XaZ9mJBuSK827ktigIU9N2manKn00"
}
headers_Error_nokey = {
   "x-api-key": ""
}

# response = requests.post(url, headers=headers, json=request_body)
session = requests.session()

# Happy Path Pass
response = session.post(url, headers=headers, json=request_body)
print(f"Status Code: {response.status_code}")
print(f'Request Json body: {json.dumps(response.json(), indent=4, ensure_ascii=False)}')
assert response.status_code == 200, f"[Status Code] Expected: 200, but Actual: {response.status_code}"
for item in response.json()["Data"]:
   assert item["Id"] == request_body["id"], f"[ID] Expected: {request_body['id']}, but Actual: {item['Id']}"
   assert item["SkuId"] == request_body["skuId"], f"[SkuId] Expected: {request_body['skuId']}, but Actual: {item['SkuId']}"

# 僅有必填欄位 Pass
response = session.post(url, headers=headers, json=request_body_onlymust)
assert response.status_code == 200, f"[Status Code] Expected: 200, but Actual: {response.status_code}"
for item in response.json()["Data"]:
   assert item["Id"] == request_body["id"], f"[ID] Expected: {request_body['id']}, but Actual: {item['Id']}"

# skuid 錯誤
response = session.post(url, headers=headers, json=request_body_Error_errorskuid)
assert response.status_code == 500, f"[Status Code] Expected: 500, but Actual: {response.status_code}"
assert response.json()["ErrorMessage"] == "Id Or SkuId => 不存在", \
   f"[ErrorMessage] Expected: Id Or SkuId => 不存在, but Actual: {response.json()['ErrorMessage']}"

# id 錯誤
response = session.post(url, headers=headers, json=request_body_Error_errorid)
assert response.status_code == 500, f"[Status Code] Expected: 500, but Actual: {response.status_code}"
assert response.json()["ErrorMessage"] == "Id Or SkuId => 不存在", \
   f"[ErrorMessage] Expected: Id Or SkuId => 不存在, but Actual: {response.json()['ErrorMessage']}"

# id 錯誤 - 格式有誤
response = session.post(url, headers=headers, json=request_body_Error_errorFormatid)
assert response.status_code == 500, f"[Status Code] Expected: 500, but Actual: {response.status_code}"
assert response.json()["ErrorMessage"] == "請確認傳入資料型別是否符合規範!Invalid type. Expected Integer but got String. Line 1, position 12.", \
   f"[ErrorMessage] Expected: 請確認傳入資料型別是否符合規範!Invalid type. Expected Integer but got String. Line 1, position 12., but Actual: {response.json()['ErrorMessage']}"

# id 必填未填
response = session.post(url, headers=headers, json=request_body_Error_noid)
assert response.status_code == 500, f"[Status Code] Expected: 500, but Actual: {response.status_code}"
assert response.json()["ErrorMessage"] == "id => 不得為空", \
   f"[ErrorMessage] Expected: id => 不得為空, but Actual: {response.json()['ErrorMessage']}"

# x-api-key 錯誤
response = session.post(url, headers=headers_Error_errorkey, json=request_body)
assert response.status_code == 403, f"[Status Code] Expected: 403, but Actual: {response.status_code}"
assert response.json()["message"] == "User is not authorized to access this resource with an explicit deny", \
   f"[message] Expected: User is not authorized to access this resource with an explicit deny, but Actual: {response.json()['message']}"

# x-api-key 未填
response = session.post(url, headers=headers_Error_nokey, json=request_body)
assert response.status_code == 401, f"[Status Code] Expected: 401, but Actual: {response.status_code}"
assert response.json()["message"] == "尚未套用 API Key", \
   f"[message] Expected: 尚未套用 API Key, but Actual: {response.json()['message']}"


