# 🧠 N3uro | Beyin MR Görüntülerinden Tümör Türlerinin Sınıflandırılması

**N3uro**, Fırat Üniversitesi Bilgisayar Mühendisliği Bölümü Tasarım Dersi kapsamında geliştirilen, beyin MR görüntülerinin derin öğrenme yöntemleriyle analiz edilmesini amaçlayan web tabanlı bir karar destek sistemi projesidir.

Projenin temel amacı, beyin MR görüntülerinden tümör sınıflandırması yapmak ve modelin tahminlerini **Grad-CAM (Gradient-weighted Class Activation Mapping)** ısı haritalarıyla görselleştirerek Açıklanabilir Yapay Zekâ (Explainable AI - XAI) yaklaşımını sisteme entegre etmektir.

Transfer Learning yaklaşımıyla eğitilmesi planlanan derin öğrenme modelleri sayesinde görüntü sınıflandırma performansının değerlendirilmesi ve modelin tahminlerinde etkili olan görüntü bölgelerinin görsel olarak incelenmesi hedeflenmektedir.

> **Proje türü:** Akademik Tasarım Dersi Projesi  
> **Takım:** N3uro  
> **Geliştirme alanları:** Derin Öğrenme, Bilgisayarlı Görü, Açıklanabilir Yapay Zekâ ve Web Tabanlı Karar Destek Sistemleri

---

## 🎯 Projenin Amaçları

- Beyin MR görüntülerini derin öğrenme yöntemleriyle sınıflandırmak.
- Transfer Learning kullanarak önceden eğitilmiş CNN modellerinin performansını değerlendirmek.
- Grad-CAM ile modelin tahminlerinde etkili olan görüntü bölgelerini görselleştirmek.
- Modeli web tabanlı bir arayüz üzerinden kullanılabilir hâle getirmek.
- Analiz sonuçlarının kaydedilmesi ve raporlanması için uygun bir altyapı oluşturmak.
- Sınıflandırma performansını standart makine öğrenmesi metrikleriyle ölçmek.

## 🔍 Temel Özellikler

### 1. Görüntü Ön İşleme
- MR görüntülerinin modele uygun formata dönüştürülmesi.
- OpenCV ve NumPy ile görüntü işleme adımlarının uygulanması.
- Görüntülerin modelin giriş boyutuna göre yeniden boyutlandırılması.
- Eğitim aşamasında uygun veri artırma (Data Augmentation) tekniklerinin değerlendirilmesi.

### 2. Derin Öğrenme ile Sınıflandırma
- ResNet ve EfficientNet gibi önceden eğitilmiş CNN mimarilerinin değerlendirilmesi.
- Transfer Learning yaklaşımıyla model eğitimi.
- Sınıflandırma sonuçlarının Accuracy, Precision, Recall ve F1-Score metrikleriyle değerlendirilmesi.

### 3. Açıklanabilir Yapay Zekâ (XAI)
- Grad-CAM yöntemiyle modelin tahminlerinde etkili olan görüntü bölgelerinin ısı haritası olarak gösterilmesi.
- Tahmin sonuçlarının görsel olarak yorumlanmasının desteklenmesi.

### 4. Web Tabanlı Kullanıcı Arayüzü
- MR görüntülerinin arayüz üzerinden yüklenmesi.
- Backend API aracılığıyla görüntülerin analiz edilmesi.
- Tahmin sonuçlarının ve Grad-CAM görsellerinin kullanıcıya sunulması.

### 5. Analiz Geçmişi ve Raporlama
- Supabase üzerinden analiz kayıtlarının yönetilmesine yönelik altyapı.
- Önceki analiz sonuçlarının görüntülenebilmesi.
- ReportLab kullanılarak PDF formatında rapor oluşturulması.

*Not: Özelliklerin kullanılabilirliği, ilgili geliştirme ve entegrasyon çalışmalarının tamamlanma durumuna bağlıdır.*

---

## 🏗️ Sistem Mimarisi

Proje, birbirinden bağımsız geliştirilebilen modüller üzerinden yapılandırılmıştır.

```text
MR Görüntüsü
     │
     ▼
Görüntü Ön İşleme
     │
     ▼
Derin Öğrenme Modeli
(Transfer Learning)
     │
     ├──────────────► Sınıflandırma Sonucu
     │
     ▼
Grad-CAM Görselleştirme
     │
     ▼
FastAPI Backend
     │
     ▼
Web Arayüzü
     │
     ├──────────────► Analiz Sonuçları
     ├──────────────► Görsel Isı Haritası
     └──────────────► Raporlama ve Geçmiş
```

Veritabanı ve PDF raporlama modülleri, ilgili analiz ve kayıt iş akışlarıyla entegre edilecek şekilde tasarlanmıştır.

## 📂 Proje Dizin Yapısı

```text
Beyin-MR-Goruntulerinden-Tumor-Turlerinin-Siniflandirilmasi/
│
├── docs/
│   └── Proje dokümanları ve gereksinim analizi
│
├── notebooks/
│   └── Veri analizi, ön işleme ve model eğitimi
│
├── backend/
│   └── FastAPI, API uç noktaları ve sunucu işlemleri
│
├── frontend/
│   └── Kullanıcı arayüzü ve sonuç görüntüleme
│
├── requirements.txt
│   └── Python bağımlılıkları
│
├── .gitignore
│
└── README.md
```

*Dizin yapısı, depodaki gerçek dosya ve klasör adlarıyla uyumlu tutulmalıdır.*

## 🛠️ Teknolojiler

| Kategori | Teknolojiler |
|---|---|
| Programlama Dili | Python |
| Derin Öğrenme | PyTorch, Torchvision |
| Görüntü İşleme | OpenCV, NumPy |
| Model Değerlendirme | Scikit-learn |
| Backend ve API | FastAPI, Uvicorn |
| Veritabanı | Supabase |
| PDF Raporlama | ReportLab |
| Veri Seti | Brain Tumor MRI Dataset |

### Kullanılan Veri Seti

Projede, Kaggle üzerinde yayımlanan **Brain Tumor MRI Dataset** veri setinin kullanılması planlanmaktadır.

- **Kaynak:** Masoud Nickparvar
- **Platform:** Kaggle
- **Görüntü sayısı:** Yaklaşık 7.200 görüntü

Veri setinin güncel sürümü, sınıf dağılımları ve lisans koşulları model eğitimi öncesinde doğrulanmalıdır.

## 🚀 Kurulum

### Gereksinimler

- Python 3.10 veya proje bağımlılıklarıyla uyumlu bir Python sürümü
- Git
- Gerekli Python kütüphaneleri
- Model eğitimi için tercihen GPU destekli bir ortam

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/ranaozgul/Beyin-MR-Goruntulerinden-Tumor-Turlerinin-Siniflandirilmasi.git
cd Beyin-MR-Goruntulerinden-Tumor-Turlerinin-Siniflandirilmasi
```

### 2. Sanal Ortam Oluşturun

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 4. Backend Sunucusunu Başlatın

Projenin `backend` dizininde `main.py` dosyası bulunduğu ve uygulama bu dosya üzerinden başlatılacak şekilde yapılandırıldığı takdirde:

```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

API dokümantasyonu, FastAPI'nin varsayılan yapılandırması kullanılıyorsa aşağıdaki adreste görüntülenebilir:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### 5. Frontend'i Çalıştırın

Frontend dosyalarını, kullanılan mimariye uygun bir yerel web sunucusu üzerinden çalıştırın. Backend API adresinin frontend yapılandırmasıyla eşleştiğinden emin olun.

> **Önemli:** Kurulum komutları, gerçek dosya adları ve uygulama giriş noktaları doğrulandıktan sonra kesinleştirilmelidir. `main.py`, model ağırlıkları ve gerekli ortam değişkenleri henüz mevcut değilse uygulama doğrudan çalışmayabilir.

## 📊 Model Değerlendirme

Model performansının yalnızca doğruluk oranıyla değerlendirilmesi yerine aşağıdaki metriklerin birlikte incelenmesi hedeflenmektedir:

- **Accuracy:** Doğru sınıflandırılan örneklerin tüm örneklere oranı.
- **Precision:** Tahmin edilen bir sınıftaki örneklerin ne kadarının doğru olduğu.
- **Recall:** Gerçek sınıfa ait örneklerin ne kadarının doğru tespit edildiği.
- **F1-Score:** Precision ve Recall değerlerinin harmonik ortalaması.
- **Confusion Matrix:** Sınıflar arasındaki doğru ve yanlış tahminlerin dağılımı.

Model sonuçları, test veri seti üzerinde elde edilen gerçek ölçümlerle raporlanacaktır.

## 👥 Takım Üyeleri

**Takım Adı:** N3uro

| Takım Üyesi | Sorumluluk Alanı |
|---|---|
| **Rana ÖZGÜL** — | Backend mimarisi, FastAPI, veritabanı entegrasyonu, API geliştirme ve raporlama |
| **Firdevs KARA** | Veri seti analizi, görüntü ön işleme, veri artırma, CNN model eğitimi ve Grad-CAM |
| **Esma AÇARLAR** | Frontend tasarımı, API-arayüz entegrasyonu ve sistem entegrasyonu |

## 🔮 Gelecek Geliştirmeler

- Farklı CNN mimarilerinin performans karşılaştırmalarının yapılması.
- Modelin farklı veri setleri üzerindeki genelleme performansının incelenmesi.
- Grad-CAM görselleştirmelerinin kullanıcı arayüzüne entegre edilmesi.
- Analiz geçmişi ve PDF raporlama modüllerinin tamamlanması.
- Model performansının farklı metrikler ve hata analizleriyle ayrıntılı biçimde raporlanması.

## ⚠️ Akademik ve Tıbbi Kullanım Uyarısı

Bu proje, Fırat Üniversitesi Bilgisayar Mühendisliği Bölümü Tasarım Dersi kapsamında eğitim ve araştırma amacıyla geliştirilmektedir.

Sistem tarafından üretilen sınıflandırma sonuçları deneysel niteliktedir. Bu proje klinik olarak doğrulanmış bir tıbbi cihaz değildir ve **doktor değerlendirmesinin, tıbbi teşhisin veya profesyonel sağlık hizmetlerinin yerine kullanılamaz.** Grad-CAM görselleri de tek başına bir tümörün varlığını, konumunu veya türünü kesin olarak kanıtlamaz.

## 📄 Lisans ve Veri Kullanımı

Proje kapsamında kullanılan veri setinin lisans koşulları ve kullanım hakları, veri kaynağının belirlediği şartlara tabidir. Projenin açık kaynak olarak dağıtılması planlanıyorsa uygun bir yazılım lisansı ayrıca belirtilmelidir.

---

**N3uro Team**  
Fırat Üniversitesi — Bilgisayar Mühendisliği
