from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import os

def scrape_news():
    # 1. Vào website đã chọn.
    driver = webdriver.Chrome()
    driver.get("https://kenh14.vn")
    
    # 2. Click chọn một mục tin tức bất kì(Đời sống).
    a_selector = '#k14-main-menu-wrapper > div > div > ul > li:nth-child(6) > a'
    element_a = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, a_selector))
    )
    element_a.click()
    
    # 3. Bấm tìm kiếm(nếu trang web tin tức không có Button tìm kiếm thì có thể bỏ qua).
    search_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "toolbar-search-wrapper"))
    )
    search_icon.click() #Click vào icon tìm kiếm

    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "searchinput"))
    )
    search_input.clear()
    search_input.send_keys("Việt Nam") #Điền từ khóa tìm kiếm
    time.sleep(1)
    
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "t-search-submit-btn"))
    )
    search_button.click() #Click vào nút tìm kiếm
    time.sleep(2)
    
    # 5. Lấy tất cả dữ liệu của các trang.
    links=set()
    while len(links) < 100:    # Vì trang Kênh 14 xem thêm vô hạn nên chỉ lấy giới hạn 100 bài viết
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        try:
            while True:
                moreButton = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#lastPage > div.view-more-detail.clearboth > a"))
                )
                moreButton.click()
                time.sleep(3)
        except:
            print("Không tìm thấy nút 'Xem thêm' hoặc đã load hết bài viết!")
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        news = soup.find_all("h3", class_="ktncli-title") + soup.find_all("h3", class_="knswli-title")
        for link in news:
            try:
                url = link.find('a').attrs['href']
                if url.startswith("/"):
                    url = "https://kenh14.vn" + url
                links.add(url)
                if len(links) >= 100:
                    break
            except:
                continue
            
    # 4. Lấy tất cả dữ liệu(Tiêu đề, Mô tả, Hình ảnh, Nội dung bài viết) hiển thị ở bài viết.
    data =  []
    for link in links:
        try:
            driver.get(link)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "kbwc-title"))
            )
            soup = BeautifulSoup(driver.page_source, "html.parser")
            title = soup.find("h1", class_="kbwc-title").text.strip()
            summary = soup.find("h2", class_="knc-sapo").text.strip()
            body = soup.find("div", class_="knc-content")
            try:
                content = body.decode_contents()
            except:
                content = ""
                
            try:
                figure = soup.find("figure", class_="VCSortableInPreviewMode")
                if figure:
                    img_tag = figure.find("img")
                    if img_tag:
                        image = img_tag.get("data-original") or img_tag.get("src") or ""
                    else:
                        image = ""
                else:
                    image = ""
            except:
                image = ""

                
            item = [title, summary, content, image]
            data.append(item)
        except Exception as e:
            print(f"Lỗi khi xử lý bài: {link} | {e}")
            continue
        
    driver.quit()
    
    # 6. Lưu dữ liệu đã lấy được vào file excel hoặc csv.
    folder = "dataKenh14"
    os.makedirs(folder, exist_ok=True)    
    fileName = os.path.join(folder, f"kenh14_VietNam_{datetime.now().strftime('%Y%m%d')}.csv")
    df = pd.DataFrame(data, columns=["Title", "Summary", "Content", "Image"])
    df.to_csv(fileName, index=False, encoding='utf-8-sig')
    print(f"Đã lưu dữ liệu vào file: {fileName}")

# 7. Set lịch chạy vào lúc 6h sáng hằng ngày.
schedule.every().day.at("06:00").do(scrape_news)

print("Đang đợi để scrape tin tức...")
while True:
    schedule.run_pending()
    time.sleep(60)

# 8. Tạo project github chế độ public.
    # https://github.com/Vunguyen204/BaiTapLon.git
# 10. Push(file code, README.md, requirements.txt) lên project và nộp link project github vào classroom.
    # Git init
    # Git remote add origin https://github.com/Vunguyen204/BaiTapLon.git
    # Git add .
    # Git commit -m "Thông điệp commit"
    # Git push -u origin main

    