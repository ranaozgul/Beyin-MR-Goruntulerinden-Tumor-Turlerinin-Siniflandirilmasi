import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def preprocess_image(image_path, target_size=(224, 224)):
    # 1. Görüntüyü Türkçe karakter destekli (numpy) şekilde oku
    image_stream = np.fromfile(image_path, np.uint8)
    img = cv2.imdecode(image_stream, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError(f"Görsel okunamadı: {image_path}")
    
    # 2. BGR'den RGB'ye çevir
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 3. Gürültü temizleme (Gaussian Blur)
    img_blur = cv2.GaussianBlur(img, (3, 3), 0)
    
    # 4. 224x224 piksel standart boyutlandırma
    img_resized = cv2.resize(img_blur, target_size, interpolation=cv2.INTER_AREA)
    
    # 5. [0, 1] aralığına normalizasyon
    img_normalized = img_resized.astype(np.float32) / 255.0
    
    return img_normalized, img_resized

# --- KODU TEST ETME BÖLÜMÜ ---
if __name__ == "__main__":
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
    
    test_dir = os.path.join(PROJECT_ROOT, "dataset", "train", "glioma")
    
    if os.path.exists(test_dir):
        sample_images = os.listdir(test_dir)
        if len(sample_images) > 0:
            sample_image_path = os.path.join(test_dir, sample_images[0])
            
            print(f"Test edilen görsel: {sample_image_path}")
            
            processed_img_norm, processed_img_display = preprocess_image(sample_image_path)
            
            print(f"İşlem Başarılı! Yeni boyut: {processed_img_norm.shape}")
            print(f"Maksimum piksel değeri (Normalizasyon testi, 1.0 olmalı): {processed_img_norm.max():.2f}")
            
            plt.imshow(processed_img_display)
            plt.title("On Isleme Tamamlandi (224x224 - Blur Etkili)")
            plt.axis("off")
            plt.show()
        else:
            print("Test için resim bulunamadı.")
    else:
        print(f"Dataset klasörü bulunamadı: {test_dir}")