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

    // 1. Görsel Sürükle / Bırak ve Seçme
    dropZone.addEventListener('click', () => imageInput.click());

    imageInput.addEventListener('change', (e) => {
        handleFileSelect(e.target.files[0]);
    });

    function handleFileSelect(file) {
        if (!file) return;
        
        // Basit Frontend Ön Kontrolü (FR-1)
        if (!file.type.startsWith('image/')) {
            showError("Lütfen geçerli bir görsel dosyası seçin.");
            return;
        }

        selectedFile = file;
        errorBanner.classList.add('hidden');
        
        const reader = new FileReader();
        reader.onload = (e) => {
            rawImagePreview.src = e.target.result;
            previewContainer.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }

    // 2. Backend API Entegrasyonu (İş Paketi 6 & FR-2, FR-3)
    btnAnalyze.addEventListener('click', async () => {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('file', selectedFile);

        btnAnalyze.innerText = "Yapay Zeka Analiz Ediyor...";
        btnAnalyze.disabled = true;

        try {
            // 4. HAFTA: Rana'nın Backend API'sine gerçek bağlantı
            const response = await fetch('http://127.0.0.1:8000/predict', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) throw new Error("API hatası");
            
            const data = await response.json();

            // Arayüzü backend'den gelen gerçek verilerle güncelle
            displayOriginal.src = rawImagePreview.src;
            displayGradcam.src = rawImagePreview.src; // 5. hafta Grad-CAM gelene kadar orijinali koyuyoruz
            
            predictedClass.innerText = data.tahmin;
            confidenceScore.innerText = `%${(data.guven_orani * 100).toFixed(1)}`;
            
            // Hastalık bilgilendirmesi
            if (data.tahmin === "Glioma") medicalInfoText.innerText = "Glioma, glial hücrelerden kaynaklanan bir tümör türüdür. Uzman değerlendirmesi şarttır.";
            else if (data.tahmin === "Meningioma") medicalInfoText.innerText = "Meningioma, genellikle iyi huylu olan ve beyin zarlarında oluşan tümördür.";
            else if (data.tahmin === "Pituitary") medicalInfoText.innerText = "Hipofiz bezi tümörüdür. Hormonal dengesizliklere yol açabilir.";
            else medicalInfoText.innerText = "Tümör bulgusuna rastlanmamıştır. Sağlıklı MR görüntüsü.";
            
            btnDownloadPdf.classList.remove('hidden');
            btnAnalyze.innerText = "Analiz Tamamlandı";
            btnAnalyze.disabled = false;

        } catch (error) {
            showError("Backend API ile bağlantı kurulamadı. Sunucunun terminalde çalıştığından emin olun.");
            btnAnalyze.innerText = "Analizi Başlat";
            btnAnalyze.disabled = false;
        }
    });

    // 3. PDF Raporu Oluşturma (FR-6)
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