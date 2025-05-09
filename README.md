<!--  9. Viết file README.md hướng dẫn cài đặt cho project github đầy đủ rõ ràng. -->
# Crawler Kenh14.vn - Chuyên mục Đời Sống

Đây là một chương trình web scraper sử dụng **Selenium** và **BeautifulSoup** để thu thập tin tức theo từ khóa "Việt Nam" của trang web **Kenh14.vn**. Các bài viết được thu thập bao gồm tiêu đề, tóm tắt, nội dung và ảnh. Dữ liệu sau đó sẽ được lưu vào file **CSV**.

## Các tính năng:
- Tự động tải trang, cuộn xuống và click vào nút "Xem thêm" để tải tối đa 100 bài viết.
- Trích xuất dữ liệu bao gồm:
  - Tiêu đề bài viết
  - Tóm tắt bài viết
  - Nội dung bài viết
  - Hình ảnh (nếu có)
- Lưu dữ liệu vào file CSV với encoding đúng để hỗ trợ tiếng Việt (UTF-8-SIG).
- Lịch trình tự động chạy mỗi ngày lúc **6h sáng** để thu thập tin tức mới.

## Các bước cài đặt

### 1. Cài đặt thư viện
Bạn cần cài đặt các thư viện Python sau:

```bash
pip install selenium beautifulsoup4 pandas schedule
```

### 2. Clone repo
```bash
git clone https://github.com/Vunguyen204/BaiTapLon.git
```
