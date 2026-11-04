
import cv2
import numpy as np
import torch
import torch.nn.functional as F


class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.activations = None
        self.gradients = None

        self.target_layer.register_forward_hook(
            self.save_activation
        )

    def save_activation(self, module, inputs, output):
        self.activations = output.detach()

        if output.requires_grad:
            output.register_hook(self.save_gradient)

    def save_gradient(self, gradient):
        self.gradients = gradient.detach()

    def generate_heatmap(self, input_tensor, class_idx=None):
        self.model.eval()

        self.activations = None
        self.gradients = None

        with torch.enable_grad():
            input_tensor = input_tensor.detach()

            output = self.model(input_tensor)

            if class_idx is None:
                class_idx = output.argmax(dim=1).item()

            self.model.zero_grad(set_to_none=True)

            score = output[:, class_idx].sum()
            score.backward()

            if self.gradients is None or self.activations is None:
                raise RuntimeError("Grad-CAM gradyanları yakalanamadı!")

            weights = self.gradients.mean(
                dim=(2, 3),
                keepdim=True
            )

            heatmap = (
                weights * self.activations
            ).sum(dim=1, keepdim=True)

            heatmap = F.relu(heatmap)

            heatmap = F.interpolate(
                heatmap,
                size=(224, 224),
                mode="bilinear",
                align_corners=False
            )

            heatmap = heatmap[0, 0]

            heatmap = heatmap - heatmap.min()

            max_value = heatmap.max()

            if max_value.item() < 1e-8:
                raise RuntimeError("Grad-CAM haritası sıfır oluştu!")

            heatmap = heatmap / max_value

            return heatmap.cpu().numpy()


def apply_gradcam_on_image(
    img_array,
    heatmap,
    alpha=0.45,
    colormap=cv2.COLORMAP_JET
):
    if len(img_array.shape) == 2:
        img_array = cv2.cvtColor(
            img_array, cv2.COLOR_GRAY2BGR
        )

    heatmap = cv2.resize(
        heatmap,
        (img_array.shape[1], img_array.shape[0])
    )

    heatmap = np.clip(heatmap, 0, 1)

    heatmap_uint8 = np.uint8(255 * heatmap)

    heatmap_colored = cv2.applyColorMap(
        heatmap_uint8,
        colormap
    )

    return cv2.addWeighted(
        img_array,
        1 - alpha,
        heatmap_colored,
        alpha,
        0
    )
