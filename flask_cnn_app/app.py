import os
import uuid
from flask import Flask, request, render_template, url_for
import torch
import torchvision.transforms as transforms
import torchvision.models as tv_models
from PIL import Image

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
MODELS_FOLDER = os.path.join(BASE_DIR, 'models')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODELS_FOLDER, exist_ok=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Simple cache for loaded models
model_cache = {}

# Image preprocessing (adjust to match your training transforms)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


def available_models():
    """Return list of .pt files in models/"""
    files = [f for f in os.listdir(MODELS_FOLDER) if f.lower().endswith('.pt')]
    return files


def load_labels_for(model_name):
    base = os.path.splitext(model_name)[0]
    labels_path = os.path.join(MODELS_FOLDER, base + '.labels')
    if os.path.exists(labels_path):
        with open(labels_path, 'r', encoding='utf-8') as fh:
            labels = [line.strip() for line in fh if line.strip()]
        return labels
    return None


def infer_num_classes_from_state_dict(state_dict):
    """Try to infer number of output classes from common classifier/fc keys in a state_dict."""
    for k, v in state_dict.items():
        if k.endswith('fc.weight') or k.endswith('fc.bias') or ('classifier' in k and 'weight' in k):
            if hasattr(v, 'shape'):
                # weight typically shape (num_classes, in_features)
                if len(v.shape) >= 1:
                    return v.shape[0]
    return None


def auto_instantiate_from_state_dict(state_dict, labels=None):
    """Attempt to instantiate a model from state_dict by trying common architectures.

    Returns (model_obj, arch_name, error_str) where error_str is None on success.
    """
    num_classes_inferred = infer_num_classes_from_state_dict(state_dict)
    num_classes = num_classes_inferred if num_classes_inferred else (len(labels) if labels else None)

    archs_to_try = ['resnet18', 'mobilenet_v2', 'custom']
    last_err = None
    for arch in archs_to_try:
        model_obj, err = instantiate_arch_from_state_dict(arch, state_dict, num_classes=num_classes)
        if err is None:
            return model_obj, arch, None
        last_err = err

    return None, None, last_err


def load_model(model_name):
    path = os.path.join(MODELS_FOLDER, model_name)
    if model_name in model_cache:
        return model_cache[model_name]

    try:
        obj = torch.load(path, map_location=device)
        # If the saved object is a state_dict (dict of tensors), return marker for caller to reconstruct
        if isinstance(obj, dict) and not any(hasattr(v, 'parameters') for v in [obj]):
            model_cache[model_name] = ('state_dict', obj)
            return ('state_dict', obj)

        # Otherwise assume full model object
        model = obj
        model.to(device)
        model.eval()
        model_cache[model_name] = model
        return model
    except Exception as e:
        return ('error', str(e))


def instantiate_arch_from_state_dict(arch_name, state_dict, num_classes=None):
    arch = arch_name.lower() if arch_name else ''
    model = None
    try:
        # Custom CNN architecture matching the notebook's CustomCNN
        class CustomCNN(torch.nn.Module):
            def __init__(self, num_classes):
                super(CustomCNN, self).__init__()
                self.features = torch.nn.Sequential(
                    torch.nn.Conv2d(3, 32, kernel_size=3, padding=1),
                    torch.nn.BatchNorm2d(32),
                    torch.nn.ReLU(),
                    torch.nn.MaxPool2d(2),

                    torch.nn.Conv2d(32, 64, kernel_size=3, padding=1),
                    torch.nn.BatchNorm2d(64),
                    torch.nn.ReLU(),
                    torch.nn.MaxPool2d(2),

                    torch.nn.Conv2d(64, 128, kernel_size=3, padding=1),
                    torch.nn.BatchNorm2d(128),
                    torch.nn.ReLU(),
                    torch.nn.MaxPool2d(2),

                    torch.nn.Conv2d(128, 256, kernel_size=3, padding=1),
                    torch.nn.BatchNorm2d(256),
                    torch.nn.ReLU(),
                    torch.nn.MaxPool2d(2)
                )
                self.classifier = torch.nn.Sequential(
                    torch.nn.Flatten(),
                    torch.nn.Linear(256 * 14 * 14, 512),
                    torch.nn.ReLU(),
                    torch.nn.Dropout(0.5),
                    torch.nn.Linear(512, num_classes)
                )

            def forward(self, x):
                x = self.features(x)
                x = self.classifier(x)
                return x

        if arch in ('resnet18', 'resnet'):
            model = tv_models.resnet18(pretrained=False)
            # infer num_classes if not provided
            if not num_classes:
                key = 'fc.weight'
                if key in state_dict:
                    num_classes = state_dict[key].shape[0]
            if num_classes:
                model.fc = torch.nn.Linear(model.fc.in_features, num_classes)

        elif arch in ('mobilenet_v2', 'mobilenet'):
            model = tv_models.mobilenet_v2(pretrained=False)
            if not num_classes:
                for k in ('classifier.1.weight', 'classifier.1.bias'):
                    if k in state_dict:
                        num_classes = state_dict[k].shape[0] if state_dict[k].dim() > 0 else None
                        break
            if num_classes:
                model.classifier[1] = torch.nn.Linear(model.last_channel, num_classes)

        elif arch in ('custom', 'customcnn'):
            # If num_classes not provided, try to infer from classifier weights in state_dict
            if not num_classes:
                for k, v in state_dict.items():
                    if 'classifier' in k and k.endswith('weight') and v.dim() >= 2:
                        num_classes = v.shape[0]
                        break
            if not num_classes:
                return None, 'Không xác định được số lớp cho CustomCNN; vui lòng cung cấp file .labels'
            model = CustomCNN(num_classes)
        else:
            return None, f'Kiến trúc {arch_name} chưa được hỗ trợ tự động.'

        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()
        return model, None
    except Exception as e:
        return None, str(e)


def predict_image_with_model(model, image_path, labels=None):
    image = Image.open(image_path).convert('RGB')
    tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(tensor)
        if isinstance(outputs, (list, tuple)):
            outputs = outputs[0]
        if outputs.dim() == 1:
            outputs = outputs.unsqueeze(0)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        _, pred = torch.max(probs, 1)
        idx = pred.item()
        if labels and idx < len(labels):
            return labels[idx]
        return f'Class {idx}'


def predict_topk_with_model(model, image_path, labels=None, k=3):
    image = Image.open(image_path).convert('RGB')
    tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(tensor)
        if isinstance(outputs, (list, tuple)):
            outputs = outputs[0]
        if outputs.dim() == 1:
            outputs = outputs.unsqueeze(0)
        probs = torch.nn.functional.softmax(outputs, dim=1)[0]
        topv, topi = torch.topk(probs, k)

        results = []
        for p, idx in zip(topv.tolist(), topi.tolist()):
            lbl = labels[idx] if labels and idx < len(labels) else f'Class {idx}'
            results.append({'idx': int(idx), 'label': lbl, 'prob': float(p)})
        return results


def predict_multilabel_with_model(model, image_path, labels=None, threshold=0.5):
    image = Image.open(image_path).convert('RGB')
    tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(tensor)
        if isinstance(outputs, (list, tuple)):
            outputs = outputs[0]
        if outputs.dim() == 1:
            outputs = outputs.unsqueeze(0)
        probs = torch.sigmoid(outputs)[0]

        results = []
        for idx, p in enumerate(probs.tolist()):
            lbl = labels[idx] if labels and idx < len(labels) else f'Class {idx}'
            if p >= threshold:
                results.append({'idx': int(idx), 'label': lbl, 'prob': float(p)})

        # If nothing passed the threshold, return top-3 as fallback
        if not results:
            topv, topi = torch.topk(probs, min(3, probs.shape[0]))
            for p, idx in zip(topv.tolist(), topi.tolist()):
                lbl = labels[idx] if labels and idx < len(labels) else f'Class {idx}'
                results.append({'idx': int(idx), 'label': lbl, 'prob': float(p)})

        return results


@app.route('/', methods=['GET', 'POST'])
def index():
    models = available_models()
    prediction = None
    image_url = None
    error = None

    if request.method == 'POST':
        # Selected model
        sel_model = request.form.get('model')
        sel_arch = request.form.get('arch')
        multilabel = bool(request.form.get('multilabel'))
        try:
            threshold = float(request.form.get('threshold', '0.5'))
        except Exception:
            threshold = 0.5

        if 'file' not in request.files:
            error = 'Không tìm thấy file upload.'
            return render_template('index.html', models=models, error=error)

        file = request.files['file']
        if file.filename == '':
            error = 'Chưa chọn ảnh.'
            return render_template('index.html', models=models, error=error)

        # Save uploaded image
        ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        image_url = url_for('static', filename=f'uploads/{filename}')

        if not sel_model:
            error = 'Vui lòng chọn mô hình (.pt) từ dropdown.'
            return render_template('index.html', models=models, error=error, image_url=image_url)

        loaded = load_model(sel_model)
        if isinstance(loaded, tuple) and loaded[0] == 'error':
            error = f'Không load được mô hình: {loaded[1]}'
            return render_template('index.html', models=models, error=error, image_url=image_url)

        # If state_dict, try to instantiate architecture (auto-detect if not provided)
        if isinstance(loaded, tuple) and loaded[0] == 'state_dict':
            state_dict = loaded[1]
            labels = load_labels_for(sel_model)

            # Try to auto-instantiate model using common architectures when user
            # didn't specify `arch` in the form.
            if not sel_arch:
                model_obj, detected_arch, err = auto_instantiate_from_state_dict(state_dict, labels=labels)
                if err:
                    error = f'Mô hình được lưu dưới dạng state_dict và không thể tự động nhận diện kiến trúc. Lỗi: {err}. Vui lòng chọn kiến trúc ở dropdown.'
                    return render_template('index.html', models=models, error=error, image_url=image_url)
                sel_arch = detected_arch
            else:
                # If user selected an arch, try to use it (but prefer num_classes from state_dict)
                inferred = infer_num_classes_from_state_dict(state_dict)
                num_classes = inferred if inferred else (len(labels) if labels else None)
                model_obj, err = instantiate_arch_from_state_dict(sel_arch, state_dict, num_classes=num_classes)
                if err:
                    error = f'Không thể khởi tạo kiến trúc: {err}'
                    return render_template('index.html', models=models, error=error, image_url=image_url)

            try:
                if multilabel:
                    topk = predict_multilabel_with_model(model_obj, filepath, labels, threshold=threshold)
                    prediction = ', '.join([it['label'] for it in topk]) if topk else None
                else:
                    topk = predict_topk_with_model(model_obj, filepath, labels, k=3)
                    prediction = topk[0]['label'] if topk else None
            except Exception as e:
                topk = None
                prediction = None
                error = f'Lỗi khi dự đoán: {str(e)}'

            return render_template('index.html', models=models, prediction=prediction, image_url=image_url, error=error, used_arch=sel_arch, topk=topk, multilabel=multilabel, threshold=threshold)

        # Otherwise model is a full object
        labels = load_labels_for(sel_model)
        try:
            if multilabel:
                topk = predict_multilabel_with_model(loaded, filepath, labels, threshold=threshold)
                prediction = ', '.join([it['label'] for it in topk]) if topk else None
            else:
                topk = predict_topk_with_model(loaded, filepath, labels, k=3)
                prediction = topk[0]['label'] if topk else None
        except Exception as e:
            topk = None
            prediction = None
            error = f'Lỗi khi dự đoán: {str(e)}'
        return render_template('index.html', models=models, prediction=prediction, image_url=image_url, error=error, used_arch='full_model', topk=topk, multilabel=multilabel, threshold=threshold)

    return render_template('index.html', models=models, prediction=prediction, image_url=image_url, error=error, used_arch=None, topk=None, multilabel=False, threshold=0.5)


if __name__ == '__main__':
    app.run(debug=True)
