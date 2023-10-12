## telegram群消息监听与自动发送消息系统

#### 系统说明
本系统用于接收telegram群组消息，并向发送了包含指定关键字的消息的用户打招呼
#### 环境准备
* 准备一个telegram账号，并将其加入需要进行消息监控的群组
* 参考[https://core.telegram.org/api/obtaining_api_id](https://core.telegram.org/api/obtaining_api_id) 注册telegram application api_id和api_hash
* git clone https://github.com/telegramdev1/TelegramMessage.git
* 修改app/config.py中的配置，必须要修改的配置包括api_id, api_hash, keywords, message
* 安装docker和docker-compose

#### 使用说明

1、运行`docker-compose up -d`启动容器

2、使用`docker exec -it 容器id /bin/bash` 进入容器内部，到/app目录下

3、执行`python3 get_group_id.py`,并按提示分别输入telegram手机号、验证码以及密码，登录账号以获取账号所添加的群组

4、运行start.sh，启动程序

5、访问80端口，可查看消息监控的记录，也可选择重新发送消息。

#### 注意事项
* 本系统还处于初级阶段，telegram对于发送消息有限制，过于频繁的向不同用户发送会导致账号被锁定，因此建议设定低频关键字
* 运行start.sh之前一定要先运行get_group_id.py脚本登录telegram账号并获取账号加入的群组id

## 详细教程可参考文章[https://zhuanlan.zhihu.com/p/660339299](https://zhuanlan.zhihu.com/p/660339299)
