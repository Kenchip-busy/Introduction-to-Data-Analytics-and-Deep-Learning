import os
import torch
import torch.nn.functional as F
from PIL import Image

from app import load_model, load_labels_for, auto_instantiate_from_state_dict, transform, device

MODEL = 'garbage_classification_model.pt'
IMG = os.path.join('static', 'uploads', 'test_image.jpg')
K = 5


def main():
    loaded = load_model(MODEL)
    labels = load_labels_for(MODEL)

    if isinstance(loaded, tuple):
        if loaded[0] == 'state_dict':
            state_dict = loaded[1]
            model_obj, arch, err = auto_instantiate_from_state_dict(state_dict, labels=labels)
            if err:
                print('Auto instantiate error:', err)
                return
            model = model_obj
            print('Auto-detected arch:', arch)
        elif loaded[0] == 'error':
            print('Error loading model:', loaded[1])
            return
    else:
        model = loaded
        print('Full model loaded')

    if not os.path.exists(IMG):
        print('Image not found:', IMG)
        return

    img = Image.open(IMG).convert('RGB')
    t = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        out = model(t)
        if isinstance(out, (list, tuple)):
            out = out[0]
        if out.dim() == 1:
            out = out.unsqueeze(0)
        probs = F.softmax(out, dim=1)[0]
        topv, topi = torch.topk(probs, K)

        print('Top-{} predictions for {}:'.format(K, IMG))
        for p, idx in zip(topv.tolist(), topi.tolist()):
            lbl = labels[idx] if labels and idx < len(labels) else f'Class_{idx}'
            print(f'  idx={idx:2d}  prob={p:.4f}  label={lbl}')


if __name__ == '__main__':
    main()
