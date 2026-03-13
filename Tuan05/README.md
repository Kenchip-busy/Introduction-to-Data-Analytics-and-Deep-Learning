Về phần dữ liệu, em sử dụng tập FashionMNIST. Nếu mọi người đã từng làm qua tập MNIST nhận diện chữ số viết tay thì tập này cũng tương tự, nhưng thay vì các con số thì nó chứa hình ảnh của các loại quần áo và phụ kiện. Dữ liệu bao gồm các bức ảnh đen trắng kích thước nhỏ gọn 28x28 pixel. Mục tiêu của em là huấn luyện máy tính nhìn vào ảnh và phân loại chính xác nó vào 1 trong 10 nhóm đồ vật, ví dụ như áo thun, quần dài, áo khoác, giày thể thao, túi xách...

Dưới đây là chi tiết các bước em đã thực hiện trong file notebook này:

Bước đầu tiên luôn là chuẩn bị dữ liệu. Em dùng luôn thư viện torchvision để tự động tải tập FashionMNIST về. Sau khi tải xong, em trích xuất dữ liệu ảnh và nhãn ra các biến tensor riêng biệt để dễ kiểm tra. Nhìn vào kích thước tensor thì tập huấn luyện có tổng cộng 60.000 mẫu ảnh.

Để đảm bảo dữ liệu tải về chuẩn xác và dễ hình dung hơn, em dùng thư viện Matplotlib để vẽ hẳn một lưới ảnh 10x10. Trong lưới này, em sắp xếp sao cho mỗi hàng hiển thị một loại trang phục cụ thể, mỗi cột là một ảnh ngẫu nhiên lấy từ lớp đó. Nhìn vào đồ thị trực quan này sẽ dễ dàng nhận thấy sự đa dạng của tập dữ liệu trước khi đem đi huấn luyện.

Tiếp theo là phần tiền xử lý. Em tự định nghĩa một cấu trúc Custom Dataset và dùng DataLoader của PyTorch để chia dữ liệu thành các lô nhỏ (batch) nhằm đưa dữ liệu vào bộ nhớ GPU hiệu quả hơn.

Đến phần quan trọng nhất là xây dựng kiến trúc mạng nơ-ron. Em dùng module nn.Sequential để lắp ráp các lớp lại với nhau. Vì ảnh đầu vào có kích thước 28x28 nên đầu tiên em phải duỗi phẳng nó ra thành một vector 784 chiều. Dữ liệu này sau đó đi qua một lớp ẩn khá lớn với 1000 nơ-ron, đi kèm với hàm kích hoạt phi tuyến ReLU để giúp mạng có khả năng học các đặc trưng phức tạp. Cuối cùng, dữ liệu đi qua lớp đầu ra gồm 10 nơ-ron, đại diện cho 10 loại trang phục cần dự đoán.

Quá trình huấn luyện mô hình diễn ra trong một vòng lặp. Em thiết lập hàm mất mát là CrossEntropyLoss vì đây là bài toán phân loại đa lớp, và dùng thuật toán tối ưu SGD để liên tục cập nhật trọng số. Trong lúc chạy vòng lặp, đoạn code cũng sẽ tự động tính toán loss và hiển thị luôn độ chính xác (accuracy) để em theo dõi quá trình học của mô hình qua từng chu kỳ.

Nếu mọi người muốn chạy thử code của em, chỉ cần clone repo này về và mở file bằng Jupyter Notebook hoặc tốt nhất là đưa lên Google Colab. Em đã tối ưu để code chạy tốt trên môi trường có GPU (như GPU T4 của Colab) nên chạy sẽ khá nhanh. Các thư viện bắt buộc phải có là torch, torchvision, matplotlib và numpy.
