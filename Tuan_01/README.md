
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



### Phiên bản 2: Tiếng Anh (English Version)



Dành cho mục tiêu học tập của bạn. Hãy chú ý các từ khóa chuyên ngành (mình đã in đậm).



```markdown

# University Admission Data Analysis and Processing



This project creates a data processing pipeline using Python and Pandas to analyze university admission datasets. It handles data cleaning, feature engineering, and admission result prediction based on high school academic records.



##  Table of Contents

- [Overview](#overview)

- [Prerequisites](#prerequisites)

- [Key Features](#key-features)

- [Logic & Formulas](#logic--formulas)

- [Usage](#usage)



##  Overview

The notebook processes raw student score data to perform **missing value imputation**, calculate **Weighted GPA**, classify academic performance, standardize scores to the **US 4.0 scale**, and determine the final **admission status** (Pass/Fail).



## Prerequisites

Ensure you have the following libraries installed:

* Python 3.x

* Pandas (for data manipulation)

* NumPy (for numerical operations)



Installation:

```bash

pip install pandas numpy

⚙️ Key Features & Steps

Data Loading: Imports the dataset dulieuxettuyendaihoc.csv.

Handling Missing Values:

Column DT (Ethnicity): Filled with 0.

Column T1 (Math Grade 10): Filled with the mean value.

Other score columns: Filled with 0.

Feature Engineering:

GPA Calculation (TBM): Calculates weighted average scores for Grade 10, 11, and 12.

Classification (XL): Categorizes students into levels: Weak, Average, Fair, Good, Excellent.

Min-Max Normalization (US_TBM): Converts the Vietnamese 10-point scale to the US 4.0 scale.

Admission Result (KQXT): Predicts admission results based on exam blocks (A, A1, B, etc.).

Logic & Formulas

The admission result (KQXT) is determined as follows:



Block A, A1: (DH1*2 + DH2 + DH3) / 4

Block B: (DH1 + DH2*2 + DH3) / 4

Other Blocks: (DH1 + DH2 + DH3) / 3

Condition: Pass if Score >= 5.0, otherwise Fail.

 Usage

Place the dulieuxettuyendaihoc.csv file in the same directory.

Run the Jupyter Notebook cells sequentially.

The processed data will be exported to processed_dulieuxettuyendaihoc.csv.
