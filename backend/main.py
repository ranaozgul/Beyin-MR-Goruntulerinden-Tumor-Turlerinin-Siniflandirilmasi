import os
import io
import base64
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
import cv2

from xai import GradCAM, apply_gradcam_on_image
from supabase import create_client, Client

SUPABASE_URL = "https://yrhihxvsgzhlcwhtiipo.supabase.co"
SUPABASE_KEY = "sb_publishable_fR2bqYWSsyqjeR40jHFOgA_IeMH3H4a"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
# ----------------------------------------------------

app = FastAPI(title="N3uro - XAI ve Veritabanı API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CLASSES = ["Glioma", "Meningioma", "No Tumor", "Pituitary"]
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pth")

# Modeli Yükle
model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, len(CLASSES))

if os.path.exists(MODEL_PATH):
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
    model.eval()

target_layer = model.layer4[-1]
grad_cam = GradCAM(model, target_layer)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

@app.post("/predict")
async def predict_mri(file: UploadFile = File(...)):
    # 1. Fotoğrafı Al ve Model Tahmini Yap
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor_img = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        outputs = model(tensor_img)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        confidence, predicted_idx = torch.max(probabilities, 0)
        
    tahmin_sonucu = CLASSES[predicted_idx.item()]
    guven = float(confidence.item())

    # 2. XAI / Grad-CAM Isı Haritası 
    tensor_img_grad = tensor_img.clone().detach().requires_grad_(True)
    heatmap = grad_cam.generate_heatmap(tensor_img_grad, predicted_idx.item())
    
    img_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gradcam_img = apply_gradcam_on_image(img_cv2, heatmap)
    
    _, buffer = cv2.imencode('.jpg', gradcam_img)
    gradcam_base64 = base64.b64encode(buffer).decode('utf-8')
    gradcam_url = f"data:image/jpeg;base64,{gradcam_base64}"
    
    # app.js dosyasındaki data.gradcam_url için Base64 formatına çevir
    _, buffer = cv2.imencode('.jpg', gradcam_img)
    gradcam_base64 = base64.b64encode(buffer).decode('utf-8')
    gradcam_url = f"data:image/jpeg;base64,{gradcam_base64}"

    # 3. Supabase Veritabanına Kayıt 
    try:
        supabase.table("mr_analysis").insert({
            "dosya_adi": file.filename,
            "tahmin": tahmin_sonucu,
            "guven_orani": round(guven * 100, 2)
        }).execute()
    except Exception as e:
        print(f"Supabase Kayıt Hatası: {e}")
        
    return {
        "tahmin": tahmin_sonucu,
        "guven_orani": guven,
        "gradcam_url": gradcam_url 
    }

@app.get("/history")
async def get_history():
    try:
        response = supabase.table("mr_analysis").select("*").order("tarih", desc=True).execute()
        
        history_data = response.data
        for item in history_data:
            item["created_at"] = item.get("tarih")
            
        return history_data
    except Exception as e:
        return {"error": str(e)}
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)    