document.addEventListener('DOMContentLoaded', async () => {
    const timelineContainer = document.getElementById('timeline-container');

    try {
        // Rana'nın Supabase ile bağladığı FastAPI uç noktası
        const response = await fetch('http://127.0.0.1:8000/history');
        
        if (!response.ok) {
            throw new Error("Veritabanı geçmiş verileri alınamadı.");
        }

        const historyData = await response.json();

        // Veritabanında henüz hiç kayıt yoksa
        if (!historyData || historyData.length === 0) {
            timelineContainer.innerHTML = `
                <p style="color: var(--text-muted); text-align: center; padding: 2rem 0;">
                    Henüz veritabanına kaydedilmiş geçmiş bir analiz bulunmamaktadır.
                </p>
            `;
            return;
        }

        // Yükleniyor yazısını temizle
        timelineContainer.innerHTML = '';

        // Supabase'den dönen tüm analiz kayıtlarını döngüye alarak kart oluşturma
        historyData.forEach(item => {
            const dateFormatted = item.created_at 
                ? new Date(item.created_at).toLocaleString('tr-TR') 
                : 'Tarih Belirtilmedi';

            const predictedClass = item.predicted_class || item.tahmin || 'Bilinmiyor';
            const confidenceRaw = item.confidence_score || item.guven_orani || 0;
            const confidenceFormatted = (confidenceRaw > 1 ? confidenceRaw : confidenceRaw * 100).toFixed(1);

            const itemCard = document.createElement('div');
            itemCard.className = 'timeline-item';
            itemCard.style.cssText = `
                border-left: 4px solid var(--accent);
                background: rgba(255, 255, 255, 0.03);
                padding: 1.2rem;
                margin-bottom: 1rem;
                border-radius: 0 8px 8px 0;
                border-top: 1px solid var(--border-color);
                border-right: 1px solid var(--border-color);
                border-bottom: 1px solid var(--border-color);
            `;

            itemCard.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <h4 style="margin: 0; color: var(--text-main);">Kayıt ID: #${item.id || 'N/A'}</h4>
                    <span style="font-size: 0.85rem; color: var(--text-muted);">${dateFormatted}</span>
                </div>
                <p style="margin: 0.25rem 0;">
                    Teşhis / Sınıf: <strong style="color: var(--accent);">${predictedClass}</strong>
                </p>
                <p style="margin: 0.25rem 0; font-size: 0.9rem; color: var(--text-muted);">
                    Model Güven Skoru: <strong>%${confidenceFormatted}</strong>
                </p>
            `;

            timelineContainer.appendChild(itemCard);
        });

    } catch (error) {
        console.error("Timeline veri yükleme hatası:", error);
        timelineContainer.innerHTML = `
            <div style="color: var(--danger); background: rgba(239, 68, 68, 0.1); padding: 1rem; border-radius: 6px;">
                ⚠️ Geçmiş analiz verileri Supabase veritabanından çekilirken bir hata oluştu. Backend (/history) sunucusunun açık olduğundan emin olun.
            </div>
        `;
    }
});