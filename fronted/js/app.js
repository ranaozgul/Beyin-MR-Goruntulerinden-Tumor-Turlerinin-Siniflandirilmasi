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

        btnAnalyze.innerText = "Analiz Ediliyor...";
        btnAnalyze.disabled = true;

        try {
            /* 
               Rana Backend API'yi tamamladığında bura açılacak:
               const response = await fetch('http://localhost:8000/api/predict', {
                   method: 'POST',
                   body: formData
               });
               const data = await response.json();
            */

            // SIMÜLASYON / MOCK VERİ (Backend hazır olana kadar test için):
            setTimeout(() => {
                // Mock Geçerlilik Kontrolü Testi:
                const isBrainMR = true; // Yanıt backend'den gelecek

                if (!isBrainMR) {
                    showError("Yüklenen görsel beyin MR niteliği taşımamaktadır.");
                    btnAnalyze.innerText = "Analizi Başlat";
                    btnAnalyze.disabled = false;
                    return;
                }

                // Mock Sonuçlar (Glioma, Meningioma, Pituitary veya No tumor)
                const mockResult = {
                    class: "Glioma",
                    confidence: 94.2,
                    original_url: rawImagePreview.src,
                    gradcam_url: rawImagePreview.src, // Normalde Grad-CAM ısı haritası URL'si gelecek
                    info: "Glioma, beyin ve omurilikteki glial hücrelerden kaynaklanan bir tümör türüdür. Düzenli uzman hekim kontrolü önerilir."
                };

                // Arayüzü Güncelle (FR-2, FR-3, FR-5)
                displayOriginal.src = mockResult.original_url;
                displayGradcam.src = mockResult.gradcam_url;
                predictedClass.innerText = mockResult.class;
                confidenceScore.innerText = `%${mockResult.confidence}`;
                medicalInfoText.innerText = mockResult.info;
                
                btnDownloadPdf.classList.remove('hidden');
                btnAnalyze.innerText = "Analiz Tamamlandı";
                btnAnalyze.disabled = false;
            }, 1500);

        } catch (error) {
            showError("Backend API ile bağlantı kurulamadı.");
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