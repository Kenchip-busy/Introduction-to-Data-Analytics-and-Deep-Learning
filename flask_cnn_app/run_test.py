from PIL import Image
import os
import numpy as np
from app import load_model, instantiate_arch_from_state_dict, predict_image_with_model, load_labels_for

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOADS = os.path.join(BASE, 'static', 'uploads')
MODELS = os.path.join(BASE, 'models')
os.makedirs(UPLOADS, exist_ok=True)

# Create a dummy test image (solid color)
img_path = os.path.join(UPLOADS, 'test_image.jpg')
if not os.path.exists(img_path):
    im = Image.new('RGB', (224,224), color=(120,200,150))
    im.save(img_path)
    print('Created test image:', img_path)
else:
    print('Using existing test image:', img_path)

model_name = 'garbage_classification_model.pt'
print('Loading model:', model_name)
loaded = load_model(model_name)

labels = load_labels_for(model_name)

if isinstance(loaded, tuple) and loaded[0] == 'state_dict':
    print('Model is a state_dict; showing debug info...')
    state_dict = loaded[1]
    print('Type:', type(state_dict))
    if isinstance(state_dict, dict):
        keys = list(state_dict.keys())
        print(f'Number of keys in state_dict: {len(keys)}')
        print('Sample keys:', keys[:40])
    # Try to infer num_classes from common classifier/fc keys
    inferred = None
    for k, v in state_dict.items():
        if k.endswith('fc.weight') or k.endswith('fc.bias') or 'classifier' in k and 'weight' in k:
            if hasattr(v, 'shape'):
                # weight typically shape (num_classes, in_features)
                if v.dim() >= 1:
                    inferred = v.shape[0]
                    break
    print('Labels file found:', bool(labels))
    print('Inferred num_classes from state_dict:', inferred)
    model_obj, err = instantiate_arch_from_state_dict('custom', state_dict, num_classes=len(labels) if labels else inferred)
    if err:
        print('Error instantiating model:', err)
        raise SystemExit(1)
    model = model_obj
else:
    model = loaded

print('Running prediction on test image...')
pred = predict_image_with_model(model, img_path, labels)
print('Prediction:', pred)
