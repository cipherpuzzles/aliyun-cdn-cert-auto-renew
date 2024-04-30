# Cipherpuzzles.com 服务器证书自动更新脚本

## 简介

这是一个用于自动更新 Cipherpuzzles.com 服务器证书的脚本。

先通过 certbot 向 Let's Encrypt 申请证书，通过 DNS-01 验证方式，使用阿里云的 DNS API 自动添加 TXT 记录。

然后将取得的证书文件拷贝到 Nginx 的证书目录下，并重启 Nginx 服务。

由于阿里云的CDN证书需要上传，之后，脚本会自动将证书上传到阿里云CAS服务。

最后，脚本会自动在阿里云CDN相关的域名下部署新证书。

## 用法

1. 整个 clone 到 /root/certbot 目录下

2. 修改 credentials.ini 文件中的阿里云的 AccessKey 和 SecretKey

3. 修改 updatedomain.ini 文件中的域名，一行一个

4. 运行 install.sh 脚本

5. 运行下面命令生成证书

```bash
/root/certbot/venv/bin/certbot certonly --authenticator dns-aliyun --dns-aliyun-credentials /root/certbot/credentials.ini -d cipherpuzzles.com -d *.cipherpuzzles.com
```

6. 证书生成后，运行下面命令更新证书

```bash
/root/certbot/venv/bin/certbot renew --deploy-hook /root/certbot/reload.sh
```

7. 将更新命令加入 crontab 定时任务

```bash
0 0 */7 * * /root/certbot/venv/bin/certbot renew --deploy-hook /root/certbot/reload.sh
```

（每 7 天执行一次）