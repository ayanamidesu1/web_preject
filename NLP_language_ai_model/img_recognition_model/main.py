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

# 检查是否使用 GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

###########################################
# 定义CBAM模块
###########################################
class ChannelAttention(nn.Module):
    def __init__(self, in_planes, reduction=16):
        super(ChannelAttention, self).__init__()
        # 定义自适应平均池化层
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        # 定义自适应最大池化层
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        # 定义全连接层
        self.fc = nn.Sequential(
            nn.Conv2d(in_planes, in_planes // reduction, 1, bias=False),
            nn.ReLU(),
            nn.Conv2d(in_planes // reduction, in_planes, 1, bias=False)
        )
        # 定义Sigmoid激活函数
        self.sigmoid = nn.Sigmoid()
    def forward(self, x):
        # 对输入进行自适应平均池化
        avg_out = self.fc(self.avg_pool(x))
        # 对输入进行自适应最大池化
        max_out = self.fc(self.max_pool(x))
        # 将平均池化和最大池化的结果相加
        out = avg_out + max_out
        # 对结果进行Sigmoid激活
        return self.sigmoid(out)

class SpatialAttention(nn.Module):
    def __init__(self, kernel_size=7):
        super(SpatialAttention, self).__init__()
        # 计算卷积核的padding大小
        padding = (kernel_size - 1) // 2
        # 定义卷积层，输入通道数为2，输出通道数为1，卷积核大小为kernel_size，padding大小为padding，不使用偏置
        self.conv = nn.Conv2d(2, 1, kernel_size, padding=padding, bias=False)
        # 定义sigmoid激活函数
        self.sigmoid = nn.Sigmoid()
    def forward(self, x):
        # 计算输入x的平均值，保持维度不变
        avg_out = torch.mean(x, dim=1, keepdim=True)
        # 计算输入x的最大值，保持维度不变
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        # 将平均值和最大值在通道维度上拼接
        x_cat = torch.cat([avg_out, max_out], dim=1)
        # 对拼接后的结果进行卷积操作
        out = self.conv(x_cat)
        # 对卷积结果进行sigmoid激活
        return self.sigmoid(out)

class CBAM(nn.Module):
    # 定义CBAM类，继承自nn.Module
    def __init__(self, in_planes, reduction=16, kernel_size=7):
        # 初始化函数，接收输入通道数、通道注意力模块的降维比例、空间注意力模块的卷积核大小
        super(CBAM, self).__init__()
        # 调用父类的初始化函数
        self.channel_attention = ChannelAttention(in_planes, reduction)
        # 定义通道注意力模块，传入输入通道数和降维比例
        self.spatial_attention = SpatialAttention(kernel_size)
        # 定义空间注意力模块，传入卷积核大小
    def forward(self, x):
        # 定义前向传播函数，接收输入x
        out = x * self.channel_attention(x)
        # 将输入x与通道注意力模块的输出相乘
        out = out * self.spatial_attention(out)
        # 将上一步的输出与空间注意力模块的输出相乘
        return out

###########################################
# 定义数据预处理流程
###########################################
train_transform = transforms.Compose([
    transforms.Resize((1024, 1024)),  # ResNet输入尺寸
    transforms.RandomHorizontalFlip(p=0.5),  # 随机水平翻转
    transforms.RandomVerticalFlip(p=0.5),  # 随机垂直翻转
    transforms.RandomRotation(5),  # 随机旋转
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),  # 随机颜色变换
    #画面小幅度形变
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.9, 1.1), shear=0.1),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                         std=[0.229, 0.224, 0.225]),
    
])
eval_transform = transforms.Compose([
    transforms.Resize((1024, 1024)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                         std=[0.229, 0.224, 0.225])
])

###########################################
# 自定义图像加载器，加入异常处理
###########################################
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

# 在构造数据集时直接传入 loader 参数，避免全局重写
train_dataset = datasets.ImageFolder(root=train_set, transform=train_transform, loader=pil_loader)
validation_dataset = datasets.ImageFolder(root=validation_set, transform=eval_transform, loader=pil_loader)
test_dataset = datasets.ImageFolder(root=test_set, transform=eval_transform, loader=pil_loader)

def safe_loader(dataset, batch_size=15, num_workers=0):
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

train_loader = safe_loader(train_dataset, batch_size=15, num_workers=4)
validation_loader = safe_loader(validation_dataset, batch_size=15, num_workers=4)
test_loader = safe_loader(test_dataset, batch_size=15, num_workers=4)

###########################################
# 定义包含CBAM的ResNet-18模型
###########################################
class ResNet18_CBAM(nn.Module):
    def __init__(self, pretrained=True, num_classes=2):
        super(ResNet18_CBAM, self).__init__()
        self.resnet = models.resnet18(pretrained=pretrained)
        # 替换全连接层
        self.resnet.fc = nn.Linear(self.resnet.fc.in_features, num_classes)
        # 在layer4后加入CBAM模块，layer4输出通道为1024
        self.cbam = CBAM(512)
    def forward(self, x):
        # ResNet-18 前几层
        x = self.resnet.conv1(x)
        x = self.resnet.bn1(x)
        x = self.resnet.relu(x)
        x = self.resnet.maxpool(x)
        x = self.resnet.layer1(x)
        x = self.resnet.layer2(x)
        x = self.resnet.layer3(x)
        x = self.resnet.layer4(x)
        x = self.cbam(x)  # 应用注意力机制
        x = self.resnet.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.resnet.fc(x)
        return x

model = ResNet18_CBAM(pretrained=True, num_classes=2).to(device)
print("Using ResNet-18 with CBAM for fine-tuning.")

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3, verbose=True)
scaler = torch.cuda.amp.GradScaler()

train_losses = []
validation_losses = []

# 如果存在之前训练的模型，则加载以继续训练
if os.path.exists(target_model_path):
    model.load_state_dict(torch.load(target_model_path, map_location=device))
    print(f"Loaded model from {target_model_path} for further training.")
else:
    print("No pre-trained model found. Training a new model from scratch.")

###########################################
# 训练过程
###########################################
if __name__ == '__main__':
    mp.set_start_method('spawn', force=True)
    best_accuracy = 0.0  # 记录最佳准确率
    with open(os.path.join(model_temp_path, 'loss_and_accuracy.txt'), 'w') as loss_file:
        for epoch in range(50):  # 总epoch数设为50
            # ... 训练阶段代码保持不变 ...
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
            # ========== 验证阶段 ==========
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
                    #打印损失和正确率
                    print(f'Validation Loss: {loss.item()}, Validation Accuracy: {(predicted == labels).sum().item() / labels.size(0)}')
                    

            avg_validation_loss = validation_loss / len(validation_loader)
            validation_accuracy = correct / total
            validation_losses.append(avg_validation_loss)

            # ====== 新增：保存准确率>75%的模型 ======
            if validation_accuracy >= 0.70:
                # 格式化准确率为4位小数（例如0.7523）
                accuracy_str = "{:.4f}".format(validation_accuracy).replace(".", "_")
                model_name = f"model_{accuracy_str}.pth"
                save_path = os.path.join(model_temp_path, model_name)
                torch.save(model.state_dict(), save_path)
                print(f">>> Saved model with accuracy {validation_accuracy:.2%} at {save_path}")

                # 更新最佳准确率（可选：只保存最佳模型时启用）
                # if validation_accuracy > best_accuracy:
                #     best_accuracy = validation_accuracy
                #     torch.save(model.state_dict(), os.path.join(model_temp_path, "best_model.pth"))

            # ====== 日志记录 ======
            loss_file.write(f'Epoch [{epoch+1}/50], Avg Validation Loss: {avg_validation_loss:.4f}, '
                           f'Accuracy: {validation_accuracy:.4f}\n')
            print(f'Epoch [{epoch+1}/50] Validation Loss: {avg_validation_loss:.4f}, Accuracy: {validation_accuracy:.2%}')

            # 学习率调整
            scheduler.step(avg_validation_loss)

        # 最终模型保存（无论准确率是否达标）
        torch.save(model.state_dict(), os.path.join(model_temp_path, 'final_model.pth'))
        print(f'Final model saved to {os.path.join(model_temp_path, "final_model.pth")}')
        
    # 绘制训练和验证Loss曲线
    plt.plot(train_losses, label='Training Loss')
    plt.plot(validation_losses, label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig(os.path.join(model_temp_path, 'loss_curve.png'))
    plt.show()
