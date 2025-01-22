from selenium.webdriver.common.by import By
import time
import json
import re
from tqdm import tqdm
from selenium import webdriver
import schedule
import time
import random

from util.api import send_api

URL = "http://127.0.0.1:8000/api/posts/receiver"

def get_data(i, link, district_, driver):
    # link = f"https://batdongsan.com.vn/cho-thue-nha-tro-phong-tro-ha-noi/p{i}"
    link = link + f'/p{i}'

    try:
        # Mở trang danh sách
        driver.get(link)
        time.sleep(3)  # Đợi trang tải

        # Lấy danh sách các liên kết chi tiết (URLs)
        listings = driver.find_elements(By.CSS_SELECTOR, "a.js__product-link-for-product-id")
        links = [listing.get_attribute("href") for listing in listings]

        all_data = []  # Danh sách lưu dữ liệu các mục

        for link in tqdm(links, desc=f"Link: {link}", unit="link"):
            # Mở liên kết trong cùng tab
            driver.get(link)
            time.sleep(5)  # Đợi trang chi tiết tải

            # Lấy thông tin từ trang chi tiết
            try:
                title = driver.find_element(By.CSS_SELECTOR, "h1.re__pr-title").text
            except:
                title = ""

            try:
                rent_fee = driver.find_element(By.CSS_SELECTOR, "div.re__pr-short-info-item span.value").text.replace("triệu/tháng", "").replace(",", ".")
                rent_fee = float(rent_fee)
            except:
                rent_fee = ""

            try:
                detail_address = driver.find_element(By.CSS_SELECTOR, "span.js__pr-address").text
            except:
                detail_address = ""

            try:
                description = driver.find_element(By.CSS_SELECTOR, "div.re__detail-content").text
            except:
                description = ""

            try:
                acreage = driver.find_element(By.CSS_SELECTOR, "div.re__pr-short-info-item:nth-of-type(2) span.value").text
            except:
                acreage = ""

            try:
                contact_phone = driver.find_element(By.CSS_SELECTOR, "span.hidden-mobile").text.replace(" ", "").replace("***", f"{random.randint(100, 999)}")
            except:
                contact_phone = ""
            try:
                contact_name = driver.find_element(By.CSS_SELECTOR, "span.hidden-mobile").get_attribute("data-kyc-name")
            except:
                contact_name = ""
            
            try:
                image_div = driver.find_element(By.CSS_SELECTOR, "div.re__pr-image-cover")
                style_attribute = image_div.get_attribute("style")
                image_url = re.search(r'url\("(.*?)"\)', style_attribute).group(1)
            except:
                image_url = ""
            try:
                bread_crumb = driver.find_elements(By.CSS_SELECTOR, "div.re__breadcrumb a")
                city = bread_crumb[1].text
                district = bread_crumb[2].text
            except:
                city = ""
                district = ""



            # Thêm dữ liệu vào danh sách
            data = {
                "title": title,
                "rent_fee": rent_fee,
                "detail_address": detail_address,
                "description": description,
                "room_type": "MOTEL",
                "acreage": acreage,
                "url": link,
                "contact_phone": contact_phone,
                "contact_name": contact_name,
                "image_url": image_url,
                "city": city,
                "district": district
            }
            all_data.append(data)
            print("Getting data successfully at: ", title)


        # Lưu dữ liệu dưới dạng JSON
        with open(f"data/batdongsan_com_vn/{district_}/listings_details_{i}.json", "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)

        print(f"Hoàn thành việc crawl và lưu dữ liệu tại page thứ {i}")
        print("Sending data to API...")
        # send_api(URL, all_data)
        print("sent data to API...")


    except Exception as e:
        print(e)
        pass

def task_crawl_cau_giay():
    link = "https://batdongsan.com.vn/cho-thue-nha-tro-phong-tro-cau-giay"
    print("Crawling data from batdongsan.com.vn in Cau Giay")
    driver = webdriver.Chrome()
    for i in tqdm(range(3), desc="Crawling first 8 pages", unit="page"):
             get_data(i + 1, link, "cau_giay", driver)
    driver.quit()
    print("Crawling data from batdongsan.com.vn in Cau Giay successfully")

def task_crawl_ba_dinh():
    link = "https://batdongsan.com.vn/cho-thue-nha-tro-phong-tro-ba-dinh"
    print("Crawling data from batdongsan.com.vn in Ba Dinh")
    driver = webdriver.Chrome()
    for i in tqdm(range(3), desc="Crawling first 8 pages", unit="page"):
             get_data(i + 1, link, "ba_dinh", driver)
    driver.quit()
    print("Crawling data from batdongsan.com.vn in Ba Dinh successfully")

def task_crawl_bac_tu_liem():
    link = "https://batdongsan.com.vn/cho-thue-nha-tro-phong-tro-bac-tu-liem"
    print("Crawling data from batdongsan.com.vn in Bac Tu Liem")
    driver = webdriver.Chrome()
    for i in tqdm(range(3), desc="Crawling first 8 pages", unit="page"):
             get_data(i + 1, link, "bac_tu_liem", driver)
    driver.quit()
    print("Crawling data from batdongsan.com.vn in Bac Tu Liem successfully")

def task_crawl_dong_da():
    link = "https://batdongsan.com.vn/cho-thue-nha-tro-phong-tro-dong-da"
    print("Crawling data from batdongsan.com.vn in Dong Da")
    driver = webdriver.Chrome()
    for i in tqdm(range(3), desc="Crawling first 8 pages", unit="page"):
             get_data(i + 1, link, "dong_da", driver)
    driver.quit()
    print("Crawling data from batdongsan.com.vn in Dong Da successfully")

def task_crawl_ha_dong():
    link = "https://batdongsan.com.vn/cho-thue-nha-tro-phong-tro-ha-dong"
    print("Crawling data from batdongsan.com.vn in Ha Dong")
    driver = webdriver.Chrome()
    for i in tqdm(range(3), desc="Crawling first 8 pages", unit="page"):
             get_data(i + 1, link, "ha_dong", driver)
    driver.quit()
    print("Crawling data from batdongsan.com.vn in Ha Dong successfully")


def task_crawl_hai_ba_trung():
    link = "https://batdongsan.com.vn/cho-thue-nha-tro-phong-tro-hai-ba-trung"
    print("Crawling data from batdongsan.com.vn in Hai Ba Trung")
    driver = webdriver.Chrome()
    for i in tqdm(range(3), desc="Crawling first 8 pages", unit="page"):
             get_data(i + 1, link, "hai_ba_trung", driver)
    driver.quit()
    print("Crawling data from batdongsan.com.vn in Hai Ba Trung successfully")


def task_crawl_hoang_mai():
    link = "https://batdongsan.com.vn/cho-thue-nha-tro-phong-tro-hoang-mai"
    print("Crawling data from batdongsan.com.vn in Hoang Mai")
    driver = webdriver.Chrome()
    for i in tqdm(range(3), desc="Crawling first 8 pages", unit="page"):
             get_data(i + 1, link, "hoang_mai", driver)
    driver.quit()
    print("Crawling data from batdongsan.com.vn in Hoang Mai successfully")

def task_crawl_hoan_kiem():
    link = "https://batdongsan.com.vn/cho-thue-nha-tro-phong-tro-hoan-kiem"
    print("Crawling data from batdongsan.com.vn in Hoan Kiem")
    driver = webdriver.Chrome()
    for i in tqdm(range(3), desc="Crawling first 8 pages", unit="page"):
             get_data(i + 1, link, "hoan_kiem", driver)
    driver.quit()
    print("Crawling data from batdongsan.com.vn in Hoan Kiem successfully")


def task_crawl_long_bien():
    link = "https://batdongsan.com.vn/cho-thue-nha-tro-phong-tro-long-bien"
    print("Crawling data from batdongsan.com.vn in Long Bien")
    driver = webdriver.Chrome()
    for i in tqdm(range(3), desc="Crawling first 8 pages", unit="page"):
             get_data(i + 1, link, "long_bien", driver)
    driver.quit()
    print("Crawling data from batdongsan.com.vn in Long Bien successfully")

def task_crawl_nam_tu_liem():
    link = "https://batdongsan.com.vn/cho-thue-nha-tro-phong-tro-nam-tu-liem"
    print("Crawling data from batdongsan.com.vn in Nam Tu Liem")
    driver = webdriver.Chrome()
    for i in tqdm(range(3), desc="Crawling first 8 pages", unit="page"):
             get_data(i + 1, link, "nam_tu_liem", driver)
    driver.quit()
    print("Crawling data from batdongsan.com.vn in Nam Tu Liem successfully")


def task_crawl_tay_ho():
    link = "https://batdongsan.com.vn/cho-thue-nha-tro-phong-tro-tay-ho"
    print("Crawling data from batdongsan.com.vn in Tay Ho")
    driver = webdriver.Chrome()
    for i in tqdm(range(3), desc="Crawling first 8 pages", unit="page"):
             get_data(i + 1, link, "tay_ho", driver)
    driver.quit()
    print("Crawling data from batdongsan.com.vn in Tay Ho successfully")


def task_crawl_thanh_xuan():
    link = "https://batdongsan.com.vn/cho-thue-nha-tro-phong-tro-thanh-xuan"
    print("Crawling data from batdongsan.com.vn in Thanh Xuan")
    driver = webdriver.Chrome()
    for i in tqdm(range(3), desc="Crawling first 8 pages", unit="page"):
             get_data(i + 1, link, "thanh_xuan", driver)
    driver.quit()
    print("Crawling data from batdongsan.com.vn in Thanh Xuan successfully")


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