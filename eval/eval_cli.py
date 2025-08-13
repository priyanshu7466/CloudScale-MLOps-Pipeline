# eval/eval_cli.py
# Computes FID (using pytorch-fid) and CLIP similarity between two folders of images.
import torch
import clip
from PIL import Image
from pytorch_fid.fid_score import calculate_fid_given_paths
import numpy as np
import os

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load('ViT-B/32', device=device)

def clip_similarity(real_dir, gen_dir):
    real_imgs = sorted([os.path.join(real_dir, f) for f in os.listdir(real_dir)])
    gen_imgs = sorted([os.path.join(gen_dir, f) for f in os.listdir(gen_dir)])
    def encode(paths):
        toks = []
        for p in paths:
            img = preprocess(Image.open(p).convert('RGB')).unsqueeze(0).to(device)
            with torch.no_grad():
                toks.append(model.encode_image(img).cpu().numpy())
        return np.vstack(toks)
    r = encode(real_imgs)
    g = encode(gen_imgs)
    r_norm = r / np.linalg.norm(r, axis=1, keepdims=True)
    g_norm = g / np.linalg.norm(g, axis=1, keepdims=True)
    sims = np.dot(r_norm, g_norm.T)
    return float(np.mean(np.max(sims, axis=1)))

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--real', required=True)
    p.add_argument('--gen', required=True)
    args = p.parse_args()
    fid = calculate_fid_given_paths([args.real, args.gen], batch_size=50, device=device)
    clip_sim = clip_similarity(args.real, args.gen)
    print('FID:', fid)
    print('CLIP similarity:', clip_sim)
