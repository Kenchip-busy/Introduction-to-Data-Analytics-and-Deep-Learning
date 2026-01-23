
Quy trình xử lý

Notebook thực hiện các bước chính sau:



Tải dữ liệu: Đọc file dulieuxettuyendaihoc.csv.

Xử lý dữ liệu thiếu (Data Imputation):

Điền giá trị 0 cho cột Dân tộc (DT).

Điền giá trị trung bình (Mean) cho cột điểm T1.

Điền giá trị 0 cho các cột điểm số còn lại nếu bị thiếu.

Feature Engineering (Tạo biến mới):

TBM1, TBM2, TBM3: Tính điểm trung bình các năm lớp 10, 11, 12 theo công thức trọng số.

XL1, XL2, XL3: Xếp loại học lực (Yếu, Trung bình, Khá, Giỏi, Xuất sắc) dựa trên điểm trung bình.

US_TBM1, US_TBM2, US_TBM3: Chuyển đổi điểm sang thang điểm 4 bằng phương pháp Min-Max Normalization.

KQXT (Kết quả xét tuyển): Xác định Đậu (1) hoặc Rớt (0) dựa trên tổ hợp môn (Khối A, A1, B, C, D...).

 Cấu trúc dữ liệu

Input: dulieuxettuyendaihoc.csv - Chứa điểm các môn T (Toán), L (Lý), H (Hóa), S (Sinh), V (Văn), X (Sử), D (Địa), N (Ngoại ngữ) qua các kỳ.

Output: processed_dulieuxettuyendaihoc.csv - File dữ liệu đã được làm sạch và bổ sung các cột tính toán mới.

 Cách sử dụng

Mở file .ipynb bằng Jupyter Notebook hoặc Google Colab và chạy lần lượt các cell từ trên xuống dưới.





---





The processed data will be exported to processed_dulieuxettuyendaihoc.csv.
