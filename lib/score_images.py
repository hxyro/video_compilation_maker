import os
import glob
import torch
from PIL import Image
import torchvision.models
import torchvision.transforms as transforms

def score_images(model_path,thumbnail_cache_dir):
    files = list(glob.glob(os.path.join(thumbnail_cache_dir,'*.png')))
    best_images = {}
    thumb = []
    model = torchvision.models.resnet50()
    model.fc = torch.nn.Linear(in_features=2048, out_features=1)
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'))) 
    model.eval()
    for x in files:
        image = Image.open(x)
        a = predict(image, model, x)
        best_images[a['score']] = a['path']
    sorted_dict = dict(sorted(best_images.items()))
    last_three_items = dict(list(sorted_dict.items())[-3:])
    for i in last_three_items.items():
        thumb.append(i[1])
    return thumb

def predict(image, model, x):
    if image.mode != 'RGB': image = image.convert("RGB")
    Transform = transforms.Compose([transforms.Resize([256,256]), transforms.ToTensor()])
    image = Transform(image).unsqueeze(0)   
    with torch.no_grad():
        preds = model(image)
    score = preds.detach().numpy().item()
    return { "score": round(score,2), "path": str(x)}
