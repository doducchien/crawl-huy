import requests

# # URL API cần gửi tới
# url = "https://example.com/api"

# # Dữ liệu JSON cần gửi
# data = {
#     "name": "John Doe",
#     "age": 30,
#     "email": "johndoe@example.com"
# }

token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiN2NkY2I0NmE1ZWEzYWY4NTM0MTMwYWNkNGY5ZjdkNGMyNzZlYzE5YjE4MmVhODFmZTJiMTc5ZjA2Y2NhZjAzZDQ2N2MzMDhkYmNmZDRjOTkiLCJpYXQiOjE3MzcxMjMxNjUuNzk5MzU0LCJuYmYiOjE3MzcxMjMxNjUuNzk5MzU4LCJleHAiOjE3Njg2NTkxNjUuMjkxNTM2LCJzdWIiOiIxMSIsInNjb3BlcyI6W119.uYETs3nmPHqQHqVxKVTDex84vDibENu2JpbYTFKXvE9It980MiecxLH2REnKl259lbARbiWE7kn9aUhaHP_78MPEnbWnSdPgaQwqRTE7D-1uKINxy9tH_l-JiroiJtMoxXPHhkni_n0qeiN5kBUuzgpy33kchsotofnR_cV8HwwVrWyuPRB4YcT_Zbz_9larRF9w28W9dJxCJj86-DYMTw_YSE5MBHTrvTpujJPRTsMJn0Ki7Gtyk75K0UhL9vMqm5u9wIDpLXURK9MouJSBMQQ-Bk5ne23Sye32vPfEDArJ3EIXnt3mkqV7UxXteQr0UJVEc_Z-gNlNk9FSFrk0TTqjS2uKBGWFSVEiVZfXe5sOdu0AHgXA2niYIWh6oIvp_X8vsk3apcWRkEGyf4TapEy2d9F8f6uu4oKenyHAKbyPClLPGVsB4jtGDfTDS0h1jQjM1F8AsBhpN2TgmjcW2lz25CpaYDW6mMiT7xXBX68GNSyrZipFub6d9EOtoeit_Nw3CqQU1LkgdhHRc-uT6ySreqblOINZTRa7ybkpxIJIRLu-RoPVFclz75U2gKdcF3VxQGeYk10Y69hoKukxrV0OmL1C7tzY9DzeQyuTbYNc-oX03-os6zfOG0Atjb0locPdkeoNCEdUXNJZuyYZ1-45bf0Razw9-qg2db6ZYSU"

def send_api(url, data):
    # Gửi yêu cầu POST với JSON
    response = requests.post(url, json=data, headers={
        "Authorization": token
    })    

    # Kiểm tra phản hồi
    if response.status_code == 201:
        print("Success:", response.json())  # In phản hồi nếu trả về JSON
    else:
        print("Error:", response.status_code, response.text)  # In lỗi