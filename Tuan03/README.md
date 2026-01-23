Lab 3: Data Wrangling - Xử lý dữ liệu Nhịp tim bệnh nhân 

Trong dự án Data Science, 80% thời gian là dành cho việc làm sạch dữ liệu. Bài Lab 3 này tập trung vào việc xử lý bộ dữ liệu `patient_heart_rate.csv` cực kỳ lộn xộn để đưa về dạng chuẩn (Tidy Data) sẵn sàng cho việc phân tích.

## Vấn đề của dữ liệu đầu vào
File dữ liệu gốc gặp hàng loạt vấn đề "nhức đầu" thường thấy trong thực tế:
1. **Header không chuẩn:** File không có header rõ ràng, phải tự định nghĩa.
2. **Thông tin bị gộp:** Cột `Name` chứa cả Họ và Tên.
3. **Đơn vị đo lường không nhất quán:** Cột `Weight` lẫn lộn giữa `kgs` và `lbs`.
4. **Dữ liệu trùng lặp & Rác:** Nhiều dòng null hoặc duplicate.
5. **Lỗi Font chữ:** Tên người chứa các ký tự lạ (non-ASCII).
6. **Sai cấu trúc (Untidy Data):** Các cột `m0006`, `m0612`... thực chất là giá trị của biến `Time` và `Sex`, chứ không phải là biến độc lập.

## Quy trình xử lý (Step-by-Step)

Notebook này giải quyết từng vấn đề theo quy trình sau:

### 1. Load & Định danh dữ liệu
- Đọc file CSV với tham số `names=...` để gán lại header chuẩn: `Id`, `Name`, `Age`, `Weight`, `m0006`, `m0612`, `m1218`, `f0006`, `f0612`, `f1218`.
- *Note:* Các cột `m0006` đại diện cho "Male, 00h-06h", `f` là "Female".

### 2. Tách thông tin (String Manipulation)
- **Problem:** Cột `Name` dính chùm (VD: "Mickie Mouse").
- **Solution:** Dùng `str.split()` để tách thành 2 cột `Firstname` và `Lastname`. Drop cột `Name` thừa.

### 3. Chuẩn hóa đơn vị (Unit Conversion)
- **Problem:** Cột `Weight` có dòng là "78kgs", có dòng là "172lbs".
- **Solution:** Duyệt qua từng dòng, nếu thấy đuôi `lbs` thì:
  - Cắt bỏ chuỗi "lbs".
  - Chuyển sang float, chia cho `2.2` để ra `kgs`.
  - Chuyển về kiểu string thêm đuôi "kgs" (hoặc giữ số int tùy mục đích).

### 4. Làm sạch cơ bản (Basic Cleaning)
- **Drop Null:** Xóa các dòng rỗng toàn bộ (`dropna(how='all')`).
- **Drop Duplicates:** Loại bỏ các dòng trùng lặp dựa trên tập thuộc tính định danh (`Firstname`, `Lastname`, `Age`, `Weight`).
- **Xử lý ký tự lạ:** Dùng **Regex** `r'[^\x00-\x7F]+'` để lọc bỏ các ký tự không phải bảng mã ASCII trong tên.

### 5. Xử lý dữ liệu thiếu (Imputation)
- **Problem:** Cột `Age` có giá trị bị thiếu.
- **Solution:** Điền các giá trị `NaN` bằng **Mean** (trung bình cộng) của cả cột tuổi.

### 6. Tái cấu trúc dữ liệu (Reshaping / Melting) *Quan trọng*
Đây là bước biến đổi **Wide Form** -> **Long Form**:
- **Problem:** Các cột `m0006`, `m0612`... đang chứa thông tin về *Giới tính* và *Thời gian* ngay trên tiêu đề cột.
- **Solution:** Dùng `pd.melt()` để "xoay" bảng dữ liệu:
  - Giữ nguyên `Id`, `Age`, `Weight`, `Name`.
  - Gom các cột `m0006`, `f0006`... vào một cột mới tên là `sex_and_time`.
  - Giá trị nhịp tim đưa vào cột `PulseRate`.

### 7. Trích xuất thông tin từ biến gộp
- Từ cột `sex_and_time` (VD: `m0006`), dùng Regex trích xuất ra:
  - **Sex:** `m` hoặc `f`.
  - **Time:** `00-06` (khoảng thời gian đo).

### 8. Final Polish
- Convert cột `PulseRate` sang kiểu số (`pd.to_numeric`), xử lý các lỗi phát sinh.
- Sắp xếp lại dữ liệu theo `Id` và `Time` cho đẹp đội hình.
- Lưu kết quả ra file `patient_heart_rate_clean.csv`.

## Kết quả đầu ra (Output)
File `patient_heart_rate_clean.csv` sẽ có cấu trúc Tidy Data chuẩn:
- Mỗi hàng là một lần đo duy nhất.
- Các cột rõ ràng: `Id`, `Age`, `Weight`, `Firstname`, `Lastname`, `Sex`, `Time`, `PulseRate`.

## Hướng dẫn chạy
```bash
# Cài đặt thư viện cần thiết
pip install pandas numpy
