import cv2
import numpy as np
import torch
import torch.nn.functional as F

class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        # PyTorch forward ve backward hook'larını güvenli bir şekilde bağlıyoruz
        self.target_layer.register_forward_hook(self.save_activation)
        self.target_layer.register_full_backward_hook(self.save_gradient)

    def save_activation(self, module, input, output):
        self.activations = output.detach()

    def save_gradient(self, module, grad_input, grad_output):
        # Gradyanları güvenli bir şekilde yakala
        self.gradients = grad_output[0].detach()

    def generate_heatmap(self, input_tensor, class_idx=None):
        self.model.eval()
        
        # Giriş tensörünün gradyan gerektirdiğinden emin olalım
        input_tensor = input_tensor.clone().detach().requires_grad_(True)
        
        # İleri yayılım (Forward pass)
        output = self.model(input_tensor)
        
        if class_idx is None:
            class_idx = torch.argmax(output, dim=1).item()
            
        # Sadece tahmin edilen sınıfın skorunu baz alarak geriye yayılım (Backward pass)
        self.model.zero_grad()
        score = output[0, class_idx]
        score.backward()
        
        if self.gradients is None or self.activations is None:
            # Güvenlik önlemi: Gradyanlar yakalanamazsa boş matris dönmesin
            return np.zeros((224, 224), dtype=np.float32)
            
        # Global Average Pooling ile gradyan ağırlıklarını hesapla (Alpha katsayıları)
        weights = torch.mean(self.gradients, dim=(2, 3))[0, :]
        activations = self.activations[0, ...]
        
        # Ağırlıklı kombinasyon (Linear combination of maps)
        heatmap = torch.zeros(activations.shape[1:], dtype=torch.float32, device=activations.device)
        for i, w in enumerate(weights):
            heatmap += w * activations[i, ...]
            
        # ReLU aktivasyonu (Sadece pozitif katkı veren pikselleri filtrele)
        heatmap = F.relu(heatmap)
        
        # Normalize et [0, 1] aralığına çek
        max_val = torch.max(heatmap)
        if max_val > 0:
            heatmap /= max_val
            
        return heatmap.cpu().numpy()

def apply_gradcam_on_image(img_array, heatmap, alpha=0.5, colormap=cv2.COLORMAP_JET):
    # Isı haritasını orijinal görselin piksel boyutuna yeniden boyutlandır
    heatmap = cv2.resize(heatmap, (img_array.shape[1], img_array.shape[0]))
    
    # 0-255 aralığına uint8 formatına dönüştür
    heatmap = np.uint8(255 * heatmap)
    
    # OpenCV JET renk haritasını (Mavi -> Sarı -> Kırmızı) uygula
    heatmap_colored = cv2.applyColorMap(heatmap, colormap)
    
    if len(img_array.shape) == 2 or img_array.shape[2] == 1:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
        
    # Isı haritasını orijinal MR üzerine şeffaf bir şekilde harmanla (Overlay)
    superimposed_img = cv2.addWeighted(img_array, 1.0 - alpha, heatmap_colored, alpha, 0)
    
    return superimposed_img