#  University Admission Data Processing Pipeline

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Library-Pandas-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

Dự án này xây dựng quy trình xử lý dữ liệu (Data Pipeline) tự động cho bộ dữ liệu xét tuyển đại học. Mục tiêu là chuyển đổi dữ liệu thô, thiếu sót thành dữ liệu sạch, chuẩn hóa để phục vụ cho các mô hình phân tích và dự báo sau này.

##  Mục lục
1. [Tổng quan dự án](#tổng-quan-dự-án)
2. [Cấu trúc dữ liệu](#cấu-trúc-dữ-liệu)
3. [Quy trình xử lý (Pipeline)](#quy-trình-xử-lý-pipeline)
4. [Logic nghiệp vụ (Business Logic)](#logic-nghiệp-vụ-business-logic)
5. [Hướng dẫn cài đặt](#hướng-dẫn-cài-đặt)
6. [Kết quả](#kết-quả)

## 1.  Tổng quan dự án
Dữ liệu điểm thi và học bạ thường gặp các vấn đề: thiếu thông tin dân tộc, điểm số bị trống, và thang điểm không đồng nhất. Script này giải quyết các vấn đề trên thông qua 4 giai đoạn: **Cleaning -> Imputation -> Feature Engineering -> Normalization**.

## 2.  Cấu trúc dữ liệu
* **Input:** `dulieuxettuyendaihoc.csv` (100 dòng, 55 cột) - Bao gồm điểm trung bình các môn Toán (T), Lý (L), Hóa (H), Sinh (S), Văn (V), Sử (X), Địa (D), Ngoại ngữ (N) của 3 năm lớp 10, 11, 12 và điểm thi đại học (DH1, DH2, DH3).
* **Output:** `processed_dulieuxettuyendaihoc.csv` - Dữ liệu đã làm sạch và thêm các trường tính toán.

## 3.  Quy trình xử lý (Pipeline)

### Bước 1: Xử lý dữ liệu thiếu (Data Imputation)
Dữ liệu thiếu được xử lý dựa trên tính chất của từng trường:
* **Dân tộc (`DT`):** Các giá trị `NaN` được điền là `0` (Giả định là dân tộc Kinh/Đa số).
* **Điểm Toán lớp 10 (`T1`):** Sử dụng phương pháp **Mean Imputation** (thay thế bằng giá trị trung bình của cả lớp) để không làm lệch phân phối dữ liệu.
* **Các điểm số khác:** Điền giá trị mặc định là `0` để đảm bảo tính toán không bị lỗi.

### Bước 2: Feature Engineering (Tạo đặc trưng mới)
Tính toán điểm trung bình môn (GPA) cho từng năm học với trọng số:
* Công thức: `(Toán*2 + Văn*2 + Các môn khác) / 10`
* Biến tạo mới: `TBM1` (Lớp 10), `TBM2` (Lớp 11), `TBM3` (Lớp 12).

### Bước 3: Phân loại học lực (Classification)
Hệ thống tự động xếp loại học sinh dựa trên điểm TBM:
* **Yếu (Y):** < 5.0
* **Trung bình (TB):** 5.0 - 6.5
* **Khá (K):** 6.5 - 8.0
* **Giỏi (G):** 8.0 - 9.0
* **Xuất sắc (XS):** >= 9.0

### Bước 4: Chuẩn hóa dữ liệu (Normalization)
Chuyển đổi điểm TBM từ thang 10 (Việt Nam) sang thang 4.0 (Hệ Mỹ) sử dụng kỹ thuật **Min-Max Scaling**:
$$Score_{US} = \frac{Score_{VN} - Min}{Max - Min} \times 4$$

## 4.  Logic nghiệp vụ (Business Logic)
Quy tắc xét tuyển đậu/rớt (`KQXT`) được lập trình dựa trên Khối thi (`KT`):

| Khối thi | Môn chính (Hệ số 2) | Công thức xét tuyển |
| :--- | :--- | :--- |
| **A, A1** | Toán (`DH1`) | `(DH1*2 + DH2 + DH3) / 4` |
| **B** | Hóa (`DH2`) | `(DH1 + DH2*2 + DH3) / 4` |
| **Khác (C, D1...)** | Không có | `(DH1 + DH2 + DH3) / 3` |

*Điều kiện đỗ:* Điểm tổng kết >= 5.0.

## 5.  Hướng dẫn cài đặt
Yêu cầu hệ thống: Python 3.7+

1. Cài đặt thư viện:
   ```bash
   pip install pandas numpy
