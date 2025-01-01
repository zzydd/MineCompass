import base64
import hashlib
from cryptography.fernet import Fernet
'''
【程序说明】
本程序可以相对安全地将您的API密钥加密并存储到代码之中。
本程序可以提高反编译API密钥的难度，但不能保证绝对安全！
对于大量发行或者密钥非常重要的场景，更推荐不要保存密钥！

【警告】
本程序不能100%保证密钥安全！只能相对提高破解难度！
若使用本程序后密钥仍遭泄露，我(程序作者)不负任何责任！

【使用说明】
1：修改变量”pwd“为任意字符串，做为密码
2：修改变量”API_Key“你的API密钥
3：运行程序
4：程序会输出二进制的主密码，复制它。(例：b'123456abcdef')
5：程序会生成包含加密API密钥数据的"api_key.py"
6：在你的主代码中创建一个二进制变量来保存主密码
7：在你的主代码中 import api_key
8：根据下面的源码或者仿照"加密密钥加载解密测试"中的示例来编写解用的密代码
'''
print("")
print("")

# 【计算主密码】
'''
1: 设置 密码
2: 进行 UTF-32 编码
3: 进行 SHA256 编码
4: 进行 Base64 编码
'''
pwd = ("Replac Your Passworld Here") # 这里填写你的密码
pwd_sha256 = hashlib.sha256(pwd.encode('utf-32')) # UTF-32+SHA256
Main_Pwd = base64.urlsafe_b64encode(pwd_sha256.digest()) # Base64
print(f"主密码(保存到主代码): {Main_Pwd}")
print("")


# 【加密API】
'''
1: 以 UTF-16 编码 API密钥
2: 根据 主密码 生成 Fernet 主密钥
3: 根据 主密钥 加密 API密钥
'''
API_Key = ("Replac Your API KEY Here") # API
print(f"API密钥: {API_Key}")
Main_Key = Fernet(Main_Pwd) # 主密钥
Encode_Api_Key = API_Key.encode("utf-16") # 编码API密钥
Encrypt_API_Key = Main_Key.encrypt(Encode_Api_Key) # 加密API密钥
print(f"加密API密钥(二进制): {Encrypt_API_Key}")



#【生成数据文件】
'''
1: 写入文件头
2: 进行 Base64 编码
3: 写入 编码数据
4: 写入 文件结尾
'''
# 生成数据文件头
with open("api_key.py", "w") as file:
    file.write('class API_Key_Data(object):\n')
    file.write('\tdef __init__(self):\n')
    file.write("\t\tself.key='")
# Base64 编码 加密API密钥
Base64Data = base64.b64encode(Encrypt_API_Key)
# 将 Base64 编码的 加密API密钥 二进制数据 追加写入到 数据文件
with open("api_key.py", "ab+") as file:
    file.write(Base64Data)
# 追加写入 数据文件尾
with open("api_key.py", "a") as file:
    file.write("'")
print("加密API密钥数据文件写入成功：api_key.py")

print("")
print("")




#【加密密钥加载解密测试】
'''
1: 导入文件
2: 提取 数据
3: 提取 二进制数据
4: 进行 Base64 解码
5: 加载 Fernet 密钥
6: 进行 Fernet 解密
7: 进行 UTF-16 解码
'''
# 导入数据
import api_key
# 提取数据
Raw_API_Kay_Data = api_key.API_Key_Data
# 提取二进制数据
API_Key_Data = Raw_API_Kay_Data().key
# 进行Base64解码 →  加密API密钥
Decode_Encrypt_API_Key = base64.b64decode(API_Key_Data)
print(f"数据文件解码 → 加密API密钥: {Decode_Encrypt_API_Key}")
# 加载Fernet密钥
Fernet_Key = Fernet(Main_Pwd) # 主密钥
# 进行Fernet解密
Decrypt_Decode_API_Key = bytearray(Fernet_Key.decrypt(Decode_Encrypt_API_Key))
# 进行UTF-16解码
Decrypt_API_Key = Decrypt_Decode_API_Key.decode("utf-16")
print(f"加密API密钥解密 → API密钥: {Decrypt_API_Key}")






