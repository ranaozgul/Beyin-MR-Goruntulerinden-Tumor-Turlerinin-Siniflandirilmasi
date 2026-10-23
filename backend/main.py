import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="N3uro - Beyin MR Sınıflandırma API")

# Frontend'in (Esma'nın yapacağı arayüzün) bu sunucuya erişebilmesi için güvenlik (CORS) ayarı
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"mesaj": "N3uro FastAPI Sunucusu Başarıyla Çalışıyor!"}

@app.post("/predict")
async def predict_mri(file: UploadFile = File(...)):
    # NOT: 4. Hafta Firdevs modeli eğittiğinde, model buraya entegre edilecek.
    # Şimdilik frontend testleri için prototip (sahte) bir sonuç dönüyoruz.
    return {
        "dosya_adi": file.filename,
        "tahmin": "Meningioma",
        "guven_orani": 0.95,
        "mesaj": "Model entegrasyonu bekleniyor."
    }

if __name__ == "__main__":
    # Sunucuyu 8000 portunda başlat
    uvicorn.run(app, host="127.0.0.1", port=8000)