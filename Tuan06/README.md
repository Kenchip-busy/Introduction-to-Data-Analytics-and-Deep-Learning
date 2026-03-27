Lab 6: Phân Loại Rác Thải Với Deep Learning
Công nghệ và Thư viện sử dụng
Ngôn ngữ: Python 3

Framework học sâu: PyTorch

Xử lý ảnh: Torchvision, Pillow (PIL)

Kiến trúc mô hình: ResNet-18 (Sử dụng kỹ thuật Transfer Learning với trọng số đã được huấn luyện sẵn từ ImageNet).

Tối ưu hóa (Optimizer): Adam với tốc độ học (learning rate) là 0.0001.

Hàm mất mát (Loss Function): CrossEntropyLoss.

Quản lý Dataset: kagglehub (Tự động tải dữ liệu trực tiếp từ Kaggle).

Tập dữ liệu (Dataset)
Mô hình được huấn luyện trên tập dữ liệu Garbage Classification V2, bao gồm 7 lớp đối tượng:

Biodegradable: Rác hữu cơ dễ phân hủy.

Cardboard: Thùng giấy, bìa các-tông.

Glass: Chai lọ thủy tinh.

Metal: Lon nhôm, đồ kim loại.

Paper: Giấy vụn, báo chí.

Plastic: Chai nhựa, túi nilon.

Trash: Các loại rác khác.
Cấu trúc mã nguồn & Cách vận hành
1. Tiền xử lý dữ liệu (Data Preprocessing)
Ảnh được resize về kích thước 224x224 để phù hợp với đầu vào của ResNet.

Áp dụng RandomHorizontalFlip (Lật ảnh ngẫu nhiên) để tăng cường dữ liệu (Data Augmentation), giúp mô hình không bị quá khớp (overfitting).

Chuẩn hóa ảnh theo thông số của ImageNet để tối ưu hóa quá trình hội tụ.

2. Xây dựng mô hình
Sử dụng mô hình ResNet18 làm khung xương (backbone).

Thay đổi lớp cuối cùng (fc layer) từ 1000 lớp mặc định thành 7 lớp tương ứng với các loại rác thải trong bài tập.

3. Quy trình huấn luyện (Training Pipeline)
Dữ liệu được chia thành các Batch (kích thước 32).

Mô hình được huấn luyện qua 5 Epochs trên thiết bị GPU (CUDA) để đạt tốc độ cao nhất.

Mã nguồn bao gồm hàm tính toán độ chính xác (Accuracy) sau mỗi vòng lặp để theo dõi hiệu năng.

Cách chạy dự án
Cài đặt thư viện:

Bash
pip install torch torchvision numpy matplotlib pillow kagglehub
Chạy Notebook:

Mở file .ipynb trên Google Colab hoặc Jupyter Notebook.

Chạy Cell đầu tiên để tải dữ liệu (Yêu cầu kết nối Internet).

Tiếp tục chạy các Cell huấn luyện. Đồ thị Loss và Accuracy sẽ tự động hiển thị ở cuối trang.

Kết quả đạt được
Mô hình đạt độ chính xác trên tập Validation (Validation Accuracy) lên đến ~93% chỉ sau 5 lần huấn luyện.

Độ lỗi (Loss) giảm mạnh và ổn định, cho thấy mô hình học rất tốt các đặc trưng của ảnh rác thải.
