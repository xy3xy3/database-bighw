用python fastapi，sqlmodel实现的数据库大作业


# 选题

在线购物系统
应用需求：在线购物平台，用户可以浏览商品、下单购买，管理员可以管理商品库存和订单。系统记录用户的订单信息和支付状态。

主要实体：

用户（User）：记录用户的基本信息和权限（管理员/普通用户）。
商品（Product）：记录商品的信息，如名称、价格、库存、类别等。
订单（Order）：记录用户的订单信息，如购买的商品、数量、总价、订单状态等。
支付（Payment）：记录订单的支付信息，包括支付方式、支付状态。
商品分类（Category）：商品的类别，如电子产品、书籍、服装等。
界面功能：

用户注册登录界面
商品浏览和购买界面
购物车和订单管理功能
管理员商品和订单管理界面

# 环境配置

使用conda python 3.12 环境
```shell
conda create -n dbhw python=3.12 -y
conda activate dbhw
```

安装依赖包
```shell
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt
```