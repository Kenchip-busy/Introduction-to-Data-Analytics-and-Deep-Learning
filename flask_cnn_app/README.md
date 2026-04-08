# Flask + PyTorch Image Classification Demo

Mục tiêu: tạo một giao diện web đơn giản bằng Flask để upload ảnh và dùng model PyTorch (.pt) đã train để phân loại ảnh.

Các file chính đã tạo:

- `app.py`: ứng dụng Flask chính, load model từ thư mục `models/`, nhận file upload, tiền xử lý và gọi model để dự đoán.
- `templates/index.html`: giao diện upload ảnh và hiển thị kết quả.
- `requirements.txt`: thư viện cần cài đặt.

Hướng dẫn nhanh:

1. Cài đặt thư viện:

```bash
pip install -r requirements.txt
```

2. Đặt file mô hình `.pt` vào thư mục `models/` (ví dụ `models/garbage_classification_model.pt`).
Screenshots
-----------

Add a screenshot of the running web UI to the repo to make the lab report clearer. Recommended path: `docs/screenshot.png` or `README_images/screenshot.png`.

How to capture and include a screenshot:

1. Run the server:

```bash
python app.py
```

2. Open `http://127.0.0.1:5000/` in your browser.
3. Select a model, upload an image (e.g. a photo of a dog), and take a screenshot of the result.
4. Save the image to `docs/screenshot.png` and commit it to the repository.

Labels file
-----------

If your model outputs class indices, provide a `.labels` file with one label per line in the `models/` folder using the same basename as the `.pt` file. Example:

```
models/garbage_classification_model.labels
cardboard
glass
metal
paper
plastic
trash
```

This repository already includes a sample labels file `models/garbage_classification_model.labels` as a placeholder — replace the contents with the real class names if needed.

3. Chạy server:

```bash
python app.py
```

4. Mở trình duyệt: `http://127.0.0.1:5000/` → chọn model → (nếu cần) chọn kiến trúc → upload ảnh → xem kết quả.

Ghi chú:
- Nếu bạn cung cấp `garbage_classification_model.pt`, hãy đặt nó vào `d:/lab10/flask_cnn_app/models/`.
- Nếu file là `state_dict`, chọn kiến trúc tương ứng trong dropdown (ResNet18 hoặc MobileNetV2). Nếu kiến trúc khác, tôi có thể thêm hỗ trợ nếu bạn cho biết tên kiến trúc.

