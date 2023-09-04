import psutil

# 获取内存信息
memory_info = psutil.virtual_memory()

# 打印内存信息
print("总内存容量 (GB):", memory_info.total / (1024 ** 3))  # 转换为GB
print("已使用内存 (GB):", memory_info.used / (1024 ** 3))  # 转换为GB
print("可用内存 (GB):", memory_info.available / (1024 ** 3))  # 转换为GB

