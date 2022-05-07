## 文件

│  client.js
│  gameServer.py
│  index.html
│  README.md
│  server.py
│  test.py
│  
├─images
│      background.png
│      blackStone.png
│      favicon.ico
│      whiteStone.png
│      
├─log
│      gameServer.log
│      server.log
│      
└─play
    │  gamePlay.py
    │  
    └─\__pycache__
            gamePlay.cpython-37.pyc

- images：图片文件夹
- log：服务器端日志文件夹。server.log为server.py产生的日志（HTTP网页资源相关日志）；gameServer.log为gameServer.log产生的日志（游戏日志）；
- index.html：网页html文件
- server.py：网页服务后端文件。负责监听HTTP，发送网页资源。不负责进行游戏。监听端口号6790
- ***gameServer.py***：五子棋游戏后端服务程序。监听端口号6791
- ***client.js***：客户端交互脚本文件，与gameServer.py交互。
- gamePlay.py：实现棋盘与胜利检测，被gameServer.py调用

## 本地测试

1. python server.py
2. python gameServer.py
3. 在火狐浏览器中，打开两个网页，分别进入http://localhost:6790/index.html。输入名称，开始游戏

## 功能

1. 支持多对玩家同时游戏

## 改进

- 一方玩家掉线、服务器掉线等异常处理还没做

  ```
  gameServer.py --> GamePlay, main 的except部分
  client.js 
  ```

- 部署到实验室服务器上？