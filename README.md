# Kenh14.vn Bóng Đá Crawler

Một trình crawler siêu nhẹ giúp tự động thu thập tin tức bóng đá từ chuyên mục `https://kenh14.vn/sport/bong-da.chn/` mỗi ngày vào lúc 6h sáng và lưu vào file Excel.

---

## Tính năng

- Tự động truy cập Kenh14 chuyên mục Bóng Đá
- Lấy thông tin: **Tiêu đề**, **Mô tả**, **Hình ảnh**, **Nội dung bài viết**
- Lưu dữ liệu vào file `.xlsx` với tên dạng `kenh14_bongda_YYYYMMDD.xlsx`
- Tự động chạy lúc **06:00 sáng mỗi ngày**

---

## Cài đặt

1. **Clone repo**

```bash
git clone https://github.com/Vunguyen204/BaiTapLon.git
cd kenh14-bongda-crawler
