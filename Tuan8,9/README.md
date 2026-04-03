
Lab 8,9: Phân Tích Dữ Liệu Văn Bản Với Thư Viện NLTK
 Mô Tả Dự Án
Kho lưu trữ này chứa toàn bộ mã nguồn thực hiện Lab 7: Phân tích dữ liệu văn bản. Dự án tập trung vào việc áp dụng các kỹ thuật Xử lý Ngôn ngữ Tự nhiên (NLP) cơ bản, hướng dẫn cách trích xuất, làm sạch và phân tích dữ liệu văn bản bằng thư viện NLTK (Natural Language Toolkit) trong Python.

 Các Nội Dung Thực Hiện
Dự án bao gồm các tác vụ NLP chính sau:

Quản lý Kho ngữ liệu: Tải và khám phá các tập dữ liệu văn bản mẫu (Gutenberg, Names).

Tìm kiếm Ngữ cảnh: Tìm kiếm từ khóa và xem cách từ đó xuất hiện trong văn bản.

Thống kê Tần suất (FreqDist): Đếm số lần xuất hiện của từ để xác định các thuật ngữ quan trọng.

Tiền xử lý Dữ liệu: Loại bỏ từ dừng (Stopwords) và dấu câu để làm sạch dữ liệu.

Phân tích N-grams: Rút trích các cụm 2 từ (Bigrams) và 3 từ (Trigrams) thường đi cùng nhau.

Thu thập dữ liệu Web: Lấy và phân tích nội dung văn bản thô hoặc HTML từ internet bằng urllib và BeautifulSoup.

Từ điển Ngữ nghĩa (WordNet): Tra cứu định nghĩa, từ đồng nghĩa, trái nghĩa và tính toán độ tương đồng giữa các từ.

Phân tích Cảm xúc: Xây dựng mô hình phân loại Naïve Bayes để dự đoán đánh giá phim là tích cực hay tiêu cực.

 Công Nghệ Sử Dụng
Ngôn ngữ: Python 3.x

Thư viện chính:

nltk: Thư viện xử lý ngôn ngữ tự nhiên.

bs4 (BeautifulSoup4): Phân tích cú pháp HTML.

urllib: Truy cập dữ liệu qua URL.

random, os, string: Các thư viện chuẩn của Python.

 Hướng Dẫn Cài Đặt
1. Cài đặt các thư viện cần thiết:
Mở terminal (hoặc command prompt) và chạy lệnh:

Bash
pip install nltk beautifulsoup4 lxml
2. Tải dữ liệu bổ trợ cho NLTK:
Chạy đoạn mã sau trong Python để tải các gói dữ liệu cần thiết:

Python
import nltk
nltk.download(['gutenberg', 'punkt', 'stopwords', 'wordnet', 'omw-1.4', 'tagsets', 'names', 'movie_reviews'])
 Cách Sử Dụng
Nếu dùng Jupyter Notebook / Google Colab: Mở file .ipynb và chạy từng ô (cell) từ trên xuống dưới.

Nếu dùng script Python (.py): Chạy trực tiếp qua terminal:

Bash
python lab7_nltk.py
 Kiến Thức Tích Lũy
Thực hành quy trình Tiền xử lý dữ liệu (tokenization, loại bỏ stopwords), đây là bước then chốt trong mọi dự án Machine Learning.

Hiểu cách khai thác các mối quan hệ ngữ nghĩa thông qua WordNet.

Tự huấn luyện một mô hình học máy cơ bản (Naïve Bayes) để phân loại văn bản, tạo nền tảng vững chắc về trí tuệ nhân tạo
