import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import torchvision.transforms as transforms

# Raporda belirtilen veri artırma (Data Augmentation) adımları
augmentation_transforms = transforms.Compose([
    transforms.ToPILImage(),
    transforms.RandomRotation(15),                           # 15 dereceye kadar rastgele döndürme
    transforms.RandomHorizontalFlip(p=0.5),                  # %50 ihtimalle yatay çevirme
    transforms.RandomVerticalFlip(p=0.5),                    # %50 ihtimalle dikey çevirme
    transforms.ColorJitter(brightness=0.2, contrast=0.2),    # Parlaklık ve kontrast ayarı
    # Not: Model eğitimi aşamasında buraya ToTensor() ve Normalize() eklenecek
])

# --- KODU TEST ETME BÖLÜMÜ ---
if __name__ == "__main__":
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
    
    # Test için yine veri setimizden bir resim alıyoruz
    test_dir = os.path.join(PROJECT_ROOT, "dataset", "train", "glioma")
    
    if os.path.exists(test_dir):
        sample_images = os.listdir(test_dir)
        if len(sample_images) > 0:
            sample_image_path = os.path.join(test_dir, sample_images[0])
            
            # Türkçe karakter destekli okuma (Az önceki çözümümüz)
            image_stream = np.fromfile(sample_image_path, np.uint8)
            img = cv2.imdecode(image_stream, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Aynı resme farklı veri artırma işlemleri uygulayıp yan yana gösterelim
            fig, axes = plt.subplots(1, 4, figsize=(15, 5))
            axes[0].imshow(img)
            axes[0].set_title("Orijinal")
            axes[0].axis("off")
            
            for i in range(1, 4):
                augmented_img = augmentation_transforms(img)
                axes[i].imshow(augmented_img)
                axes[i].set_title(f"Artırılmış {i}")
                axes[i].axis("off")
                
            plt.suptitle("N3uro - Veri Artirma (Data Augmentation) Testi")
            plt.show()
        else:
            print("Test için resim bulunamadı.")
    else:
        print("Dataset klasörü bulunamadı.")