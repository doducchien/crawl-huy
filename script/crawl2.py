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
def crawl_pages(base_url, district, pages=5):
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
        save_to_json(page_data, f"data/phongtro123/{district}/listings_details_{page}.json")
        # print("Sending data to API...")
        # send_api(URL, page_data)
        # print("Sent data to API...")



def task_crawl_cau_giay():
    url = base_url + "/quan-cau-giay"
    print("Crawling data from phongtro123.com in Cau Giay")
    crawl_pages(url, district="cau_giay", pages=2)
    print("Crawling data from phongtro123.com successfully in Cau Giay")

def task_crawl_ba_dinh():
    url = base_url + "/quan-ba-dinh"
    print("Crawling data from phongtro123.com in Ba Dinh")
    crawl_pages(url, district="ba_dinh", pages=2)
    print("Crawling data from phongtro123.com successfully in Ba Dinh")

def task_crawl_bac_tu_liem():
    url = base_url + "/quan-bac-tu-liem"
    print("Crawling data from phongtro123.com in Bac Tu Liem")
    crawl_pages(url, district="bac_tu_liem", pages=2)
    print("Crawling data from phongtro123.com successfully in Bac Tu Liem")

def task_crawl_dong_da():
    url = base_url + "/quan-dong-da"
    print("Crawling data from phongtro123.com in Dong Da")
    crawl_pages(url, district="dong_da", pages=2)
    print("Crawling data from phongtro123.com successfully in Dong Da")

def task_crawl_ha_dong():
    url = base_url + "/quan-ha-dong"
    print("Crawling data from phongtro123.com in Ha Dong")
    crawl_pages(url, district="ha_dong", pages=2)
    print("Crawling data from phongtro123.com successfully in Ha Dong")

def task_crawl_hai_ba_trung():
    url = base_url + "/quan-hai-ba-trung"
    print("Crawling data from phongtro123.com in Hai Ba Trung")
    crawl_pages(url, district="hai_ba_trung", pages=2)
    print("Crawling data from phongtro123.com successfully in Hai Ba Trung")

def task_crawl_hoang_mai():
    url = base_url + "/quan-hoang-mai"
    print("Crawling data from phongtro123.com in Hoang Mai")
    crawl_pages(url, district="hoang_mai", pages=2)
    print("Crawling data from phongtro123.com successfully in Hoang Mai")

def task_crawl_hoan_kiem():
    url = base_url + "/quan-hoan-kiem"
    print("Crawling data from phongtro123.com in Hoan Kiem")
    crawl_pages(url, district="hoan_kiem", pages=2)
    print("Crawling data from phongtro123.com successfully in Hoan Kiem")

def task_crawl_long_bien():
    url = base_url + "/quan-long-bien"
    print("Crawling data from phongtro123.com in Long Bien")
    crawl_pages(url, district="long_bien", pages=2)
    print("Crawling data from phongtro123.com successfully in Long Bien")

def task_crawl_nam_tu_liem():
    url = base_url + "/quan-nam-tu-liem"
    print("Crawling data from phongtro123.com in Nam Tu Liem")
    crawl_pages(url, district="nam_tu_liem", pages=2)
    print("Crawling data from phongtro123.com successfully in Nam Tu Liem")

def task_crawl_tay_ho():
    url = base_url + "/quan-tay-ho"
    print("Crawling data from phongtro123.com in Tay Ho")
    crawl_pages(url, district="tay_ho", pages=2)
    print("Crawling data from phongtro123.com successfully in Cau Giay")

def task_crawl_thanh_xuan():
    url = base_url + "/quan-thanh-xuan"
    print("Crawling data from phongtro123.com in Thanh Xuan")
    crawl_pages(url, district="thanh_xuan", pages=2)
    print("Crawling data from phongtro123.com successfully in Thanh Xuan")



if __name__ == '__main__':
    # 1 phut chay 1 lan
    schedule.every(1).minutes.do(task_crawl_cau_giay)
    schedule.every(1).minutes.do(task_crawl_ba_dinh)
    schedule.every(1).minutes.do(task_crawl_bac_tu_liem)
    schedule.every(1).minutes.do(task_crawl_dong_da)
    schedule.every(1).minutes.do(task_crawl_ha_dong)
    schedule.every(1).minutes.do(task_crawl_hai_ba_trung)
    schedule.every(1).minutes.do(task_crawl_hoang_mai)
    schedule.every(1).minutes.do(task_crawl_hoan_kiem)
    schedule.every(1).minutes.do(task_crawl_long_bien)
    schedule.every(1).minutes.do(task_crawl_nam_tu_liem)
    schedule.every(1).minutes.do(task_crawl_tay_ho)
    schedule.every(1).minutes.do(task_crawl_thanh_xuan)

    # Vòng lặp chạy mãi mãi để kiểm tra và thực thi các công việc được lên lịch
    while True:
        print("Waiting for scheduled tasks to run...")
        schedule.run_pending()
        time.sleep(1)