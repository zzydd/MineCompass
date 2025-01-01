# **Mine Compass**

### 一个用于设置现实里 Minecraft罗盘 的小工具

### 相关硬件项目：[chaosgoo/mcompass](https://github.com/chaosgoo/mcompass)

![项目主图](https://github.com/zzydd/MineCompass/blob/main/images/show-main.png?raw=true "项目主图")

---

# 声明

### Minecraft游戏素材版权均归微软所有

### 程序使用的素材为网上第三方绘制的免费资源

### 程序图标素材来源：[icon8.com](https://igoutu.cn/icons)

<br />

---

# 使用说明

## 1：设备信息页

![设备信息页](https://github.com/zzydd/MineCompass/blob/main/images/PageA-1.png?raw=true "设备信息页")

### 扫描速度：决定扫描超时和网络请求超时设置

* 由于ESP32性能有限，扫描时建议设置音速及以下
* 速度切换立即生效，哪怕正在扫描
* 如果网络质量较好也可尝试光速

|   |光速   |音速   |飞速   |快速   |
| :------------: | :------------: | :------------: | :------------: | :------------: |
|扫描超时   |0.25s   |0.50s   |1.00s   |2.00s   |
|普通超时   |1.00s   |3.00s   |5.00s   |10.0s   |

<br />

### 点击扫描设备，程序开始搜索局域网内的指南针

* 如果搜索不到，可以尝试降低速度再次扫描
* 如果多次搜索不到，请检查设备是否就绪

### 连接成功后，会显示连接设备的基本信息

* 只有连接成功才可以进入后续设置页面

![设备信息页-连接成功](https://github.com/zzydd/MineCompass/blob/main/images/PageA-3.png?raw=true "设备信息页-连接成功")
