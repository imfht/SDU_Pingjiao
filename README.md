# SDU_Pingjiao
一键提交山东大学的评教系统（其实是清华大学的）,一共提供两个版本供大家使用,
## 版本一,个人使用
```
git clone https://github.com/fiht/SDU_Pingjiao
sudo pip install requests
python pingjia.py
```
使用大致效果如图  
![](http://oerpz7veb.bkt.clouddn.com/public/16-12-6/96408717.jpg)
## 版本二,搭建给舍友用  
估计也没几个人愿意折腾的...
* 安装依赖
```bash
git clone https://github.com/fiht/SDU_Pingjiao
sudo pip install requests flask redis
sudo apt-get install redis-server
```
* 在本机启动redis
```bash
redis-server
```
* 配置邮件信息
使用QQ邮箱的话 编辑**SendEmail.py**
** 将MAILADD字段修改成你自己的邮箱
** 去QQ邮箱设置页面获取SMTP认证码,填入SendEmail字段
** 运行 python SendEmail.py 执行发信测试,没报错/已经收到邮件,即为配置成功

* 启动flask
```bash
python main.py
```
* 启动RockRedis(从redis里面取出数据)
```bash
python RockRedis.py
```
* 访问http://localhost:5000 进行测试

![](http://oerpz7veb.bkt.clouddn.com/public/16-12-6/53247761.jpg)
