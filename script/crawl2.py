import requests
from bs4 import BeautifulSoup
import csv
import time
import json
from util.api import send_api
import schedule

URL = "http://127.0.0.1:8000/api/posts/receiver"

# URL của trang web
base_url = "https://phongtro123.com/tinh-thanh/ha-noi"
entry_url = "https://phongtro123.com"
# Ghi thông tin vào file JSON
def save_to_json(data, filename):
    print("Saving data to file...")
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print("Saved data to file...")

# Hàm lấy HTML từ trang web
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Báo lỗi nếu request không thành công
    return response.text

# Hàm lấy link chi tiết từ trang danh sách
def get_detail_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    menu = soup.find('ul', class_='post__listing')
    items = menu.find_all('li')
    links =  [entry_url + item.find('a', href=True)['href'] for item in items]
    return links

# Hàm crawl thông tin chi tiết từ từng link
def get_phongtro_detail(detail_url):
    html = get_html(detail_url)
    soup = BeautifulSoup(html, 'html.parser')
    try:
        header = soup.find('header', class_='border-bottom pb-4 mb-4')
        try:
            title = header.find('h1', class_='fs-5 fw-semibold lh-sm mb-2').get_text(strip=True)
        except AttributeError:
            title = ""
        try:
            rent_fee = header.find('span', class_='text-price').get_text(strip=True).replace("triệu/tháng", "").replace("đồng/tháng", "").strip()
            rent_fee = float(rent_fee)
        except AttributeError:
            rent_fee = None
        
        try:
            acreage = header.find('span', class_='').get_text(strip=True).strip()
        except AttributeError:
            acreage = ""
        
        try:
            detail_address = header.find('address').get_text(strip=True).replace("-Xem bản đồ", "").strip()
        except AttributeError:
            detail_address = ""
        try:
            description = soup.find('div', class_='border-bottom pb-3 mb-4').find_all('p')
            description = ' '.join([p.get_text(strip=True) for p in description])
        except AttributeError:  
            description = ""

        try:
            img_tag = soup.find('div', class_='carousel-item active').find('img')
            image_url =  img_tag['data-src'] if img_tag else ""
        except AttributeError:
            image_url = ""

        try:
            breadcrumbs = soup.find('ol', class_='breadcrumb')
            li_tags = breadcrumbs.find_all('li')
            district = li_tags[2].get_text(strip=True)
        except AttributeError:
            district = ""

        try:
            contact_tag = soup.find('a', class_='btn btn-green btn-lg text-white d-flex justify-content-center rounded-4')
            contact_phone = contact_tag['href'].replace("tel:", "") if contact_tag else ""
        except AttributeError:
            contact_phone = ""

        try:
            contact_name = soup.find('div', class_='fs-5-5 fw-medium me-2').get_text(strip=True)
        except AttributeError:
            contact_name = ""
        return {
            'title': title,
            'rent_fee': rent_fee,
            'acreage': acreage,
            'detail_address': detail_address,
            'description': description,
            'url': detail_url,
            "image_url": image_url,
            "room_type": "MOTEL",
            "city": "Hà Nội",
            "district": district,
            "contact_phone": contact_phone,
            "contact_name": contact_name

        }
    except AttributeError:
        print("not ok")
        return None

# Ghi thông tin vào file CSV
def save_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

# Crawl thông tin từ nhiều trang
def crawl_pages(base_url, pages=5):
    for page in range(1, pages + 1):
        page_data = []
        print(f"Đang crawl trang danh sách {page}...")
        page_url = f"{base_url}?orderby=mac-dinh&page={page}"
        html = get_html(page_url)
        detail_links = get_detail_links(html)

        print(f"Đã tìm thấy {len(detail_links)} link chi tiết ở trang {page}.")
        for link in detail_links:
            print(f"Đang crawl thông tin từ: {link}")
            detail_data = get_phongtro_detail(link)
            page_data.append(detail_data)   
            time.sleep(1)  # Thêm độ trễ để tránh bị chặn
        save_to_json(page_data, f"data/phongtro123/listings_details_{page}.json")
        # print("Sending data to API...")
        # send_api(URL, page_data)
        # print("Sent data to API...")

def task():
    print("Crawling data from phongtro123.com")
    crawl_pages(base_url, pages=2)
    print("Crawling data from phongtro123.com successfully")

if __name__ == '__main__':
    # 1 phut chay 1 lan
    schedule.every(1).minutes.do(task)

    # Vòng lặp chạy mãi mãi để kiểm tra và thực thi các công việc được lên lịch
    while True:
        print("Waiting for scheduled tasks to run...")
        schedule.run_pending()
        time.sleep(1)