import os
import shutil
from sklearn.model_selection import train_test_split

# Kodu nereden çalıştırırsanız çalıştırın doğru ana dizini bulmasını sağlayan sistem:
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) # notebooks klasörünü bulur
PROJECT_ROOT = os.path.dirname(CURRENT_DIR) # Ana proje klasörünü bulur

RAW_DIR = os.path.join(PROJECT_ROOT, "dataset_raw")
OUT_DIR = os.path.join(PROJECT_ROOT, "dataset")
CLASSES = ["glioma", "meningioma", "notumor", "pituitary"]

# 1. Bütün resimleri sınıflarına göre tek bir listede toplayalım
all_images = {cls: [] for cls in CLASSES}

# İçerideki Training ve Testing klasörlerini gez
for root_folder in os.listdir(RAW_DIR):
    root_path = os.path.join(RAW_DIR, root_folder)
    if os.path.isdir(root_path):
        # Her bir alt sınıf klasörünü gez
        for cls in CLASSES:
            cls_path = os.path.join(root_path, cls)
            if os.path.exists(cls_path):
                # Bulunan resimleri ilgili sınıfın listesine ekle
                images = [os.path.join(cls_path, img) for img in os.listdir(cls_path)]
                all_images[cls].extend(images)

# 2. Şimdi bu toplanan resimleri 80-10-10 oranında bölelim
for cls in CLASSES:
    images = all_images[cls]
    if len(images) == 0:
        continue
        
    # %80 Train, %20 Geriye Kalanlar
    train_imgs, test_val_imgs = train_test_split(images, test_size=0.2, random_state=42)
    
    # Kalan %20'yi -> %10 Validation, %10 Test olarak ikiye böl
    val_imgs, test_imgs = train_test_split(test_val_imgs, test_size=0.5, random_state=42)
    
    splits = {'train': train_imgs, 'val': val_imgs, 'test': test_imgs}
    
    # Resimleri oluşturulan yeni dataset klasörüne kopyala
    for split_name, split_files in splits.items():
        split_dir = os.path.join(OUT_DIR, split_name, cls)
        os.makedirs(split_dir, exist_ok=True)
        for f in split_files:
            shutil.copy(f, split_dir)

print("İşlem Tamamlandı! Training ve Testing klasörleri birleştirilip %80 Eğitim, %10 Validation, %10 Test olarak başarıyla ayrıldı.")