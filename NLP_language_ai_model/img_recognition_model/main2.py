import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
import torch.nn.functional as F
from PIL import Image, UnidentifiedImageError
import os
import time
import psutil
import torch.cuda as cuda
import matplotlib.pyplot as plt
import multiprocessing as mp

# 设置路径
train_set = 'H:/img_data_set/result_set/'
validation_set = 'H:/img_data_set/validation_set/'
test_set = 'H:/img_data_set/test_set/'
model_temp_path = "G:/ai_model/"
target_model_path = os.path.join(model_temp_path, "final_model.pth")
#r18文件夹
r18_folder='r-18/'
#正常文件夹
normal_folder='normal/'

# 检查是否使用 GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

# 定义数据预处理流程
# 注意：此处数据增强策略参照您给出的要求，其中随机水平翻转和颜色扰动（brightness, contrast）适用于对称性图像 [cite[6]]
train_transform = transforms.Compose([
    transforms.Resize((512, 512)),  # ResNet输入尺寸
    transforms.RandomHorizontalFlip(),  # 水平翻转
    #transforms.ColorJitter(brightness=0.2, contrast=0.2),  # 颜色扰动
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                         std=[0.229, 0.224, 0.225])  # ImageNet归一化参数
])

# 验证和测试集不采用数据增强，只进行Resize和归一化
eval_transform = transforms.Compose([
    transforms.Resize((512, 512)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                         std=[0.229, 0.224, 0.225])
])

# 自定义图像加载器，加入异常处理
def pil_loader(path):
    try:
        with open(path, 'rb') as f:
            img = Image.open(f)
            return img.convert('RGB')
    except (UnidentifiedImageError, FileNotFoundError) as e:
        print(f"Error loading image {path}: {e}")
        return None
    except Exception as e:
        print(f"Error loading image file {path}: {e}")
        return None

# 重写 ImageFolder 的 default_loader
from torchvision.datasets.folder import default_loader
datasets.folder.default_loader = pil_loader

# 数据加载函数
def safe_loader(dataset, batch_size=35, num_workers=0):
    try:
        loader = torch.utils.data.DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=num_workers,
            pin_memory=True,
            prefetch_factor=None if num_workers == 0 else 2
        )
        return loader
    except Exception as e:
        print(f"Error creating data loader: {e}")
        return None

train_dataset = datasets.ImageFolder(root=train_set, transform=train_transform, loader=pil_loader)
train_loader = safe_loader(train_dataset, batch_size=35, num_workers=4)

validation_dataset = datasets.ImageFolder(root=validation_set, transform=eval_transform, loader=pil_loader)
validation_loader = safe_loader(validation_dataset, batch_size=35, num_workers=4)

test_dataset = datasets.ImageFolder(root=test_set, transform=eval_transform, loader=pil_loader)
test_loader = safe_loader(test_dataset, batch_size=35, num_workers=4)

# 使用torchvision预训练的ResNet-18模型，并修改最后的全连接层输出二分类
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, 2)
model = model.to(device)
print("Using pretrained ResNet-18 model for fine-tuning.")

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)

# 使用 ReduceLROnPlateau，根据验证集 loss 自动降低学习率
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3, verbose=True)
scaler = torch.cuda.amp.GradScaler()

train_losses = []
validation_losses = []

# 如果存在第一轮训练的模型，则加载该模型进行二次训练
if os.path.exists(target_model_path):
    model.load_state_dict(torch.load(target_model_path, map_location=device))
    print(f"Loaded model from {target_model_path} for further training.")
else:
    print("No pre-trained model found. Training a new model from scratch.")

if __name__ == '__main__':
    mp.set_start_method('spawn', force=True)
    with open(os.path.join(model_temp_path, 'loss_and_accuracy.txt'), 'w') as loss_file:
        for epoch in range(20):
            model.train()
            epoch_loss = 0.0
            epoch_start_time = time.time()
            
            for batch_idx, (images, labels) in enumerate(train_loader):
                batch_start_time = time.time()
                try:
                    images, labels = images.to(device), labels.to(device)
                    optimizer.zero_grad()
                    
                    with torch.autocast(device_type='cuda'):
                        outputs = model(images)
                        loss = criterion(outputs, labels)
                    
                    scaler.scale(loss).backward()
                    scaler.step(optimizer)
                    scaler.update()
                    
                    epoch_loss += loss.item()
                    
                    print(f'Epoch [{epoch+1}/20], Batch [{batch_idx+1}/{len(train_loader)}], '
                          f'Loss: {loss.item():.4f}, Time per batch: {time.time()-batch_start_time:.2f}s')
                    
                    if device.type == 'cuda':
                        print(f'GPU Memory Allocated: {cuda.memory_allocated()/1024**3:.2f} GB, '
                              f'GPU Memory Cached: {cuda.memory_reserved()/1024**3:.2f} GB')
                except Exception as e:
                    print(f"Error processing batch {batch_idx+1}: {e}")
                    continue
            
            avg_train_loss = epoch_loss / len(train_loader)
            train_losses.append(avg_train_loss)
            loss_file.write(f'Epoch [{epoch+1}/20], Avg Train Loss: {avg_train_loss:.4f}, '
                           f'Time: {time.time()-epoch_start_time:.2f}s\n')
            print(f'Epoch [{epoch+1}/20] completed in {time.time()-epoch_start_time:.2f}s')
            
            # 验证模型
            model.eval()
            validation_loss = 0.0
            correct = 0
            total = 0
            with torch.no_grad():
                for images, labels in validation_loader:
                    images, labels = images.to(device), labels.to(device)
                    with torch.autocast(device_type='cuda'):
                        outputs = model(images)
                        loss = criterion(outputs, labels)
                    validation_loss += loss.item()
                    _, predicted = torch.max(outputs, 1)
                    total += labels.size(0)
                    correct += (predicted == labels).sum().item()
            
            avg_validation_loss = validation_loss / len(validation_loader)
            validation_accuracy = correct / total
            validation_losses.append(avg_validation_loss)
            loss_file.write(f'Epoch [{epoch+1}/20], Avg Validation Loss: {avg_validation_loss:.4f}, '
                           f'Accuracy: {validation_accuracy:.4f}\n')
            print(f'Validation Loss: {avg_validation_loss:.4f}, Accuracy: {validation_accuracy:.4f}')
            
            # 调整学习率：根据验证 loss 进行调整
            scheduler.step(avg_validation_loss)
        
        # 保存最终模型
        torch.save(model.state_dict(), os.path.join(model_temp_path, 'final_model.pth'))
        print(f'Model saved to {os.path.join(model_temp_path, "final_model.pth")}')
        
    # 绘制训练和验证 Loss 曲线
    plt.plot(train_losses, label='Training Loss')
    plt.plot(validation_losses, label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig(os.path.join(model_temp_path, 'loss_curve.png'))
    plt.show()
