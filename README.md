
## 安装配置

### conf目录

##### WhiteList.txt      
白名单邮件列表，指某些允许在github上出现的邮箱
```
xxxx@baidu.com
xxxx@baidu.com
```

    
##### WrongList.txt      
退信邮件列表，指某些退信邮箱
```
xxxx@baidu.com
xxxx@baidu.com

```

##### access_token.txt    
github API的token

```
asdfasdfasdfasdfasdfasdf
kioquwioejroqowjorjqiojo

```
    
##### config.txt
邮箱、UA、等基础配置
    
```
#匹配邮箱的正则
globalPattern =(\w+@\.baidu\.com)
#告警发件人设置
Mail_host =smtp.163.com
Mail_user =username
Mail_pass =password
Mail_postfix =163.com
#扫描最新更新代码的页数，推荐4以下
maxpageFor_Compare =2
#扫描邮箱算法页数，推荐5以下
maxpageFor_Email =2
#浏览器UA
globalUA =User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.4456.99 Safari/537.36
```
##### receiveEmail.txt    
告警接收人邮箱
```
test1@163.com
test2@163.com
```

### result目录
##### gitresult.txt

最新更新代码的时间，无需人工改动

### keywords目录

##### CompareKeyWord.txt
扫描最新更新代码用到的keyword

```
#建议按语言区分
baidu.com+password+smtp+language:python
```


##### keyWordList.txt
扫描邮箱算法使用到的keyword

```
#建议粗略一点
baidu.com+password
```



    
    
    
    
