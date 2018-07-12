配置新网站
========= 
## 需要安装的包：
 
* nginx 
* Python 3 
* Git 
* pip 
* virtualenv 

以 Ubuntu 为例， 可以执行下面的命令安装： 

    sudo apt- get install nginx git python3 python3- pip
    sudo pip3 install virtualenv 
    
## 配置 Nginx 虚拟 主机 
* 参考 nginx.template.conf 
* 把 SITENAME 替换 成 所需 的 域名， 例如 staging. my- domain. com 

## Upstart 任务 * 参考 gunicorn-upstart.template.conf 
* 把 SITENAME 替换成所需的域名，例如 staging.my-domain.com 

## 文件夹 结构： 假设有用户账户，家目录为/home/username

/home/username 
        └ ─ ─ sites 
                └ ─ ─ SITENAME
                         ├ ─ ─ database 
                         ├ ─ ─ source 
                         ├ ─ ─ static 
                         └ ─ ─ _vevn