from cryptography.fernet import Fernet

# 生成和保存密钥（首次运行时生成一次并安全存储密钥）
key = Fernet.generate_key()
# 保存密钥时，建议放在环境变量或配置文件中
with open('secret.key', 'wb') as key_file:
     key_file.write(key)