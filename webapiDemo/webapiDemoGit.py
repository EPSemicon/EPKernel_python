'''
以下是悦谱的一家合作板厂在使用悦谱的webapi二次开发的PCB资料云分析的python代码范例
在征求对方同意隐去关键信息后,将代码作为二次开发案例上传至github
epkernel为方便用户使用将该流程进行一定程度的封装以便二次开发快速使用
epkernel将于2023年初更新云工程云分析相关开发,请保持关注
'''

import oss2,os,requests

'''
以下是阿里云对象存储oss2相关设置,内容暂不放出
'''
AccessKeyId='内容暂不放出'
AccessKeySecret='内容暂不放出'
ossUrl='内容暂不放出'
Bucket='内容暂不放出'
OSSBASEDIR='内容暂不放出'
access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', AccessKeyId)
access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', AccessKeySecret)
bucket_name = os.getenv('OSS_TEST_BUCKET', Bucket)
endpoint = os.getenv('OSS_TEST_ENDPOINT', ossUrl)
bucket_folder = OSSBASEDIR
bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

'''
以下定义了一个上传资料至对象存储的函数,内容暂不放出
此函数的目的是为了将本地文件转化为可用的http链接
'''
def uploadFile_OSS_getUrl(path,middlePath=None)->str:
    try:
        file_path = path
        filename=os.path.basename(path)
        if middlePath==None:
            oss_file_path = bucket_folder+filename
        else:
            oss_file_path = bucket_folder+ middlePath + filename
        bucket.put_object_from_file(oss_file_path, file_path)
        file_url2 = '内容暂不放出'+oss_file_path
        return file_url2
    except Exception as e:
        print(e)
        return e

'''
请求post的请求主体json内容,其中access_token内容暂不放出
'''
access_token1 = '内容暂不放出'
access_token2 = '内容暂不放出'
job_URL = uploadFile_OSS_getUrl('ep_panel_test.eps')
job_type = 1
step_name = 'pcs'
apply_time_stamp = '2022-01-03 14:42:21'
callback_post_URL = ''
callback_type = 0
dfm_version = 11

root = {
    'access_token1':access_token1,
    'access_token2':access_token2,
    'job_URL':job_URL,
    'job_type':job_type,
    'step_name':step_name,
    'apply_time_stamp':apply_time_stamp,
    'callback_post_URL':callback_post_URL,
    'callback_type':callback_type,
    'dfm_version':dfm_version
}

'''
使用悦谱webapi创建资料云分析订单
'''
response = requests.post('http://180.117.161.52:8083/analysis/dfm',json=root)
print(response.content)