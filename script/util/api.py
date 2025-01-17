import requests

# # URL API cần gửi tới
# url = "https://example.com/api"

# # Dữ liệu JSON cần gửi
# data = {
#     "name": "John Doe",
#     "age": 30,
#     "email": "johndoe@example.com"
# }

def send_api(url, data):
    # Gửi yêu cầu POST với JSON
    response = requests.post(url, json=data)    

    # Kiểm tra phản hồi
    if response.status_code == 200:
        print("Success:", response.json())  # In phản hồi nếu trả về JSON
    else:
        print("Error:", response.status_code, response.text)  # In lỗi