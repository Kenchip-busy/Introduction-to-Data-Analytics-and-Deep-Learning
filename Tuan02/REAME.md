#Lab 2: Phân tích & Trực quan hóa Dữ liệu (EDA) 

Tiếp nối Lab 1 (đã clean data), Lab 2 này là bước mình "lặn sâu" vào dữ liệu (Deep Dive). Mục tiêu không chỉ là tính toán con số mà còn là vẽ biểu đồ để tìm ra quy luật (Insights) của bộ dữ liệu tuyển sinh.

Notebook này bao gồm các kỹ thuật từ cơ bản đến nâng cao trong Data Analysis.

## 🛠 Tech Stack
- **Pandas:** Để nhào nặn dữ liệu (Filter, Sort, Pivot).
- **Matplotlib & Seaborn:** Bộ đôi "thần thánh" để vẽ biểu đồ (Visualization).
- **Scipy:** Để tính các chỉ số thống kê chuyên sâu.

## Chi tiết các bước thực hiện

### 1. Data Manipulation (Xào nấu dữ liệu)
Trước khi vẽ vời thì mình phải sắp xếp lại data cho gọn:
- **Sorting:** Sắp xếp bảng điểm theo thứ tự tăng dần của `DH1` (Điểm ĐH môn 1), rồi sắp xếp theo nhóm Giới tính (`GT`).
- **Filtering (Lọc):**
  - Lấy list các bạn Nam, Dân tộc Kinh.
  - Lấy các bạn học sinh Khu vực `2NT` có điểm 3 môn `DH1, DH2, DH3` đều >= 5.0 (đội này là "con ngoan trò giỏi" nè).

### 2. Descriptive Statistics (Thống kê mô tả)
Bước này để trả lời câu hỏi: "Phổ điểm chung nó như thế nào?"
- Dùng `describe()` cho các cột điểm hệ Mỹ (`US_TBM1`, `US_TBM2`...) để xem Mean, Min, Max.
- **Pivot Table:** Tạo bảng thống kê tổng hợp (như Excel pivot) để tính `Count`, `Sum`, `Mean`, `Median`, `Std`, `Q1`, `Q2`, `Q3` của điểm `DH1` theo từng Khối thi (`KT`).
  -> *Mục đích: Xem khối nào có điểm thi môn 1 cao nhất/thấp nhất.*

### 3. Feature Engineering (Tạo biến mới - Part 2)
Trong Lab 2 mình có tạo thêm cột `phanlopt1` dựa trên điểm Toán năm lớp 10 (`T1`):
- `< 5`: Kém
- `5 - 7`: Trung bình
- `7 - 8`: Khá
- `>= 8`: Giỏi
-> *Mục đích: Để lát nữa vẽ biểu đồ so sánh xem nhóm "Giỏi Toán" đi thi ĐH điểm có cao hơn nhóm "Kém" không.*

### 4. Data Visualization (Trực quan hóa - Phần quan trọng nhất) 📈
Code vẽ rất nhiều loại biểu đồ để nhìn data dưới nhiều góc độ:

- **Line Plot (Biểu đồ đường):**
  - Vẽ phân phối điểm `T1`.
  - **Multiple Line Plot:** So sánh biến động điểm `T1` giữa các nhóm xếp loại (Giỏi/Khá/TB...).
  - **Drop-line Plot:** Một dạng biểu đồ nâng cao để highlight các điểm dữ liệu cụ thể.

- **Boxplot (Biểu đồ hộp):**
  - Dùng để soi **Outliers** (điểm ngoại lai) và phân phối điểm `T1` trên từng nhóm phân lớp. Nhìn cái này là biết nhóm nào học đều, nhóm nào học lệch.

- **Scatter Plot & Correlation (Biểu đồ tương quan):**
  - Vẽ `T1` (trục X) vs `DH1` (trục Y) và nhóm theo Khu vực (`KV`).
  - **Insight:** Xem thử *Điểm học bạ* có phản ánh đúng *Điểm thi Đại học* không? (Nếu các điểm nằm trên 1 đường thẳng đi lên -> Tương quan thuận).

### 5. Correlation Matrix (Ma trận tương quan)
- Tính hệ số tương quan (Correlation Coefficient) giữa 3 môn `DH1`, `DH2`, `DH3`.
- In ra ma trận để xem các môn này có liên quan mật thiết với nhau không.

## Cách chạy (How to run)
1. Đảm bảo file `processed_dulieuxettuyendaihoc.csv` (đầu ra của Lab 1) đã nằm trong folder.
2. Cài thư viện visualization nếu chưa có:
   ```bash
   pip install seaborn matplotlib
