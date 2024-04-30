#!/root/certbot/venv/bin/python3
# -*- coding: utf-8 -*-
from datetime import datetime
from configparser import ConfigParser
from Tea.core import TeaCore
from alibabacloud_cas20200407.client import Client as cas20200407Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_cas20200407 import models as cas_20200407_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_tea_util import models as util_models
from alibabacloud_cdn20180510.client import Client as Cdn20180510Client
from alibabacloud_cdn20180510 import models as cdn_20180510_models

def getAliyunBaseConfig():
    cfg = ConfigParser()
    with open('credentials.ini', 'r', encoding='utf-8') as cfgFileStream:
        cfg.read_string("[main]\n" + cfgFileStream.read())

    accessKey = cfg['main']['dns_aliyun_access_key']
    accessKeySecret = cfg['main']['dns_aliyun_access_key_secret']

    aliyunConfig = open_api_models.Config(
            access_key_id=accessKey,
            access_key_secret=accessKeySecret
    )
    return aliyunConfig

def getAliyunCASClient():
    aliyunConfig = getAliyunBaseConfig()
    aliyunConfig.endpoint = f'cas.aliyuncs.com' # cn-hangzhou
    aliyunCASClient = cas20200407Client(aliyunConfig)
    return aliyunCASClient
 
def getAliyunCDNClient():
    aliyunConfig = getAliyunBaseConfig()
    aliyunConfig.endpoint = f'cdn.aliyuncs.com' # cn-hangzhou
    aliyunCDNClient = Cdn20180510Client(aliyunConfig)
    return aliyunCDNClient

def readCertFile(filepath):
    with open(filepath, 'r', encoding='utf-8') as certFile:
        return certFile.read()

def getUpdateDomains():
    with open('updatedomain.ini', 'r', encoding='utf-8') as domainfile:
        domainString = domainfile.read()
        domainList = domainString.split('\n')
        domainList = [domain for domain in domainList if domain and not domain.startswith('#')]
        return ','.join(domainList)


def uploadCert():
    cert = readCertFile('/etc/letsencrypt/live/cipherpuzzles.com/fullchain.pem')
    key = readCertFile('/etc/letsencrypt/live/cipherpuzzles.com/privkey.pem')

    client = getAliyunCASClient()
    request = cas_20200407_models.UploadUserCertificateRequest()
    timestr = datetime.now().strftime("%Y%m%d%H%M%S")
    certName = 'a_cipherpuzzles_com_%s' % timestr
    request.name = certName
    request.cert = cert
    request.key = key

    response = client.upload_user_certificate(request)
    print('upload certifications to CAS')
    print(UtilClient.to_jsonstring(TeaCore.to_map(response.body)))

    return certName

def updateDomainCerts(certName):
    updateDomains = getUpdateDomains()

    client = getAliyunCDNClient()
    request = cdn_20180510_models.BatchSetCdnDomainServerCertificateRequest()
    request.domain_name = updateDomains
    request.cert_name = certName
    request.cert_type = 'cas'
    request.sslprotocol = 'on'

    runtime = util_models.RuntimeOptions()
    response = client.batch_set_cdn_domain_server_certificate_with_options(request, runtime)
    print('update cdn https for %s' % updateDomains)
    print(UtilClient.to_jsonstring(TeaCore.to_map(response.body)))

def main():
    certName = uploadCert()
    updateDomainCerts(certName)


if __name__ == '__main__':
    main()
