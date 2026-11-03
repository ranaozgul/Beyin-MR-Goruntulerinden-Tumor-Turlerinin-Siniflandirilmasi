document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const imageInput = document.getElementById('image-input');
    const previewContainer = document.getElementById('preview-container');
    const rawImagePreview = document.getElementById('raw-image-preview');
    const btnAnalyze = document.getElementById('btn-analyze');
    const errorBanner = document.getElementById('error-banner');
    
    const displayOriginal = document.getElementById('display-original');
    const displayGradcam = document.getElementById('display-gradcam');
    const predictedClass = document.getElementById('predicted-class');
    const confidenceScore = document.getElementById('confidence-score');
    const medicalInfoText = document.getElementById('medical-info-text');
    const btnDownloadPdf = document.getElementById('btn-download-pdf');

    let selectedFile = null;

    // 1. Görsel Seçimi ve Otomatik Buton Sıfırlama
    dropZone.addEventListener('click', () => imageInput.click());

    imageInput.addEventListener('change', (e) => {
        handleFileSelect(e.target.files[0]);
    });

    function handleFileSelect(file) {
        if (!file) return;
        
        if (!file.type.startsWith('image/')) {
            showError("Lütfen geçerli bir görsel dosyası (PNG, JPG, JPEG) seçin.");
            return;
        }

        selectedFile = file;
        errorBanner.classList.add('hidden');
        
        const reader = new FileReader();
        reader.onload = (e) => {
            rawImagePreview.src = e.target.result;
            previewContainer.classList.remove('hidden');

            // Yeni bir resim seçildiği an butonu anında 'Analizi Başlat' durumuna getiriyoruz
            btnAnalyze.innerText = "🚀 Analizi Başlat";
            btnAnalyze.disabled = false;
            btnAnalyze.classList.remove('btn-success'); // Varsa yeşil/tamamlandı stilini kaldır
        };
        reader.readAsDataURL(file);
    }

    // 2. Analiz Butonu ve Durum Yönetimi
    btnAnalyze.addEventListener('click', async () => {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('file', selectedFile);

        // Yüklenme Durumu (Loading State)
        btnAnalyze.innerText = "⏳ Yapay Zekâ Analiz Ediyor...";
        btnAnalyze.disabled = true;

        try {
            const response = await fetch('http://127.0.0.1:8000/predict', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) throw new Error("API hatası");
            
            const data = await response.json();

            // Arayüzü Güncelleme
            displayOriginal.src = rawImagePreview.src;

            // --- 5. HAFTA HAFTA GÜNCELLEMESİ (Gerçek Grad-CAM Bağlantısı) ---
            // Backend'den 'gradcam_url' veya base64 formatında 'gradcam_image' gelecek
            if (data.gradcam_url) {
                displayGradcam.src = data.gradcam_url;
            } else if (data.gradcam_image) {
            displayGradcam.src = `data:image/jpeg;base64,${data.gradcam_image}`;
            } else {
                displayGradcam.src = rawImagePreview.src; // Fallback (Yedek)
            }

            predictedClass.innerText = data.tahmin || data.predicted_class;
            confidenceScore.innerText = `%${((data.guven_orani || data.confidence_score) * 100).toFixed(1)}`;
            
            // Hastalık Bilgilendirmesi
            if (data.tahmin === "Glioma") {
                medicalInfoText.innerText = "Glioma, glial hücrelerden kaynaklanan bir tümör türüdür. Uzman değerlendirmesi şarttır.";
            } else if (data.tahmin === "Meningioma") {
                medicalInfoText.innerText = "Meningioma, genellikle iyi huylu olan ve beyin zarlarında oluşan tümördür.";
            } else if (data.tahmin === "Pituitary") {
                medicalInfoText.innerText = "Hipofiz bezi tümörüdür. Hormonal dengesizliklere yol açabilir.";
            } else {
                medicalInfoText.innerText = "Tümör bulgusuna rastlanmamıştır. Sağlıklı MR görüntüsü.";
            }
            
            btnDownloadPdf.classList.remove('hidden');

            // Analiz bittiğinde butonu kilitli bırakmak yerine 'Yeniden Analiz Et' yapıp AKTİF tutuyoruz
            btnAnalyze.innerText = "🔄 Yeniden Analiz Et";
            btnAnalyze.disabled = false;
            btnAnalyze.classList.add('btn-success');

        } catch (error) {
            showError("Backend API ile bağlantı kurulamadı. Sunucunun çalıştığından emin olun.");
            btnAnalyze.innerText = "🚀 Analizi Başlat";
            btnAnalyze.disabled = false;
        }
    });

    // 3. PDF Raporu Oluşturma
    btnDownloadPdf.addEventListener('click', () => {
        const element = document.getElementById('report-content');
        const opt = {
            margin:       0.5,
            filename:     `N3uro_MR_Analiz_Raporu.pdf`,
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2 },
            jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
        };
        html2pdf().set(opt).from(element).save();
    });

    function showError(message) {
        errorBanner.innerText = `⚠️ ${message}`;
        errorBanner.classList.remove('hidden');
    }
});