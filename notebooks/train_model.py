import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
import os

# Yollar
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "dataset")
MODEL_SAVE_PATH = os.path.join(PROJECT_ROOT, "backend", "model.pth")

data_transforms = {
    'train': transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

image_datasets = {x: datasets.ImageFolder(os.path.join(DATA_DIR, x), data_transforms[x]) for x in ['train', 'val']}
dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=16, shuffle=True) for x in ['train', 'val']}
class_names = image_datasets['train'].classes

# ResNet18 Transfer Learning
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model.fc = nn.Linear(model.fc.in_features, len(class_names))

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

print("Model eğitimi başlıyor (Tahmini süre: 2-5 dk)...")
for epoch in range(2): # Prototip için 2 epok
    for phase in ['train', 'val']:
        if phase == 'train': model.train()
        else: model.eval()

        running_corrects = 0
        for inputs, labels in dataloaders[phase]:
            optimizer.zero_grad()
            with torch.set_grad_enabled(phase == 'train'):
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)
                if phase == 'train':
                    loss.backward()
                    optimizer.step()
            running_corrects += torch.sum(preds == labels.data)
        
        acc = running_corrects.double() / len(image_datasets[phase])
        print(f'Epoch {epoch+1} - {phase} Başarımı: {acc:.4f}')

torch.save(model.state_dict(), MODEL_SAVE_PATH)
print("Eğitim bitti! model.pth backend klasörüne kaydedildi.")