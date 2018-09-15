import os
from django.core.mail import EmailMultiAlternatives


os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == '__main__':
    subject, from_email, to = '来自www.baidu.com的测试邮件', 'xxxxxx@sina.com', 'xxxxx@qq.com'
    text_content = '欢迎访问www.baidu.com，这里是百度搜索站点，专注于网络知识的分享搜索和分享！'
    html_content = '<p>欢迎访问<a href="http://www.baidu.com" target=blank>www.baidu.com</a>，</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



