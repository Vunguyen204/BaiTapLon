import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time
from datetime import datetime

def scrape_news():
    response = requests.get("https://kenh14.vn/sport/bong-da.chn/")
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        news = soup.find_all("h3", class_="ktncli-title")
        
        links=[]
        for link in news:
            try:
                url = link.find('a').attrs['href']
                if url.startswith("/"):
                    url = "https://kenh14.vn" + url
                links.append(url)
            except:
                continue
        
        data =  []
        for link in links:
            try:
                news = requests.get(link)
                soup = BeautifulSoup(news.content, "html.parser")
                title = soup.find("h1", class_="kbwc-title").text.strip()
                summary = soup.find("h2", class_="knc-sapo").text.strip()
                body = soup.find("div", class_="knc-content")
                try:
                    content = body.decode_contents()
                except:
                    content = ""
                    
                try:
                    image = soup.find("img", class_="VCSortableInPreviewMode")
                    if image:
                        image = image.get('data-original') or image.get('src')
                    else:
                        image = ""
                except:
                    image = ""
                    
                item = [title, summary, content, image]
                data.append(item)
            except Exception as e:
                print(f"Lỗi khi xử lý bài: {link} | {e}")
                continue
            
        df = pd.DataFrame(data, columns=["Title", "Summary", "Content", "Image"])
        fileName = f"kenh14_bongda_{datetime.now().strftime('%Y%m%d')}.xlsx"
        df.to_excel(fileName, index=False, encoding='utf-8-sig')
        print("Đã lưu dữ liệu vào file: outputKenh14.xlsx")
        
schedule.every().day.at("06:00").do(scrape_news)

print("Đang đợi để scrape tin tức...")
while True:
    schedule.run_pending()
    time.sleep(60)
