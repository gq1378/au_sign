from cv2 import cv2
from urllib import request
import numpy as np


# def show(pic):
#     cv2.imshow('Show', pic)
#     cv2.waitKey(0) & 0xFF
#     cv2.destroyAllWindows()


def offset(href1,href2):
    #  获取原始图片
    temp = 'template.png'
    targ = 'target.jpg'
    if href1[-7:-3]=='@2x.':
        href1='http'+href1[5:]
        href2='http'+href2[5:]
    else:
        href1='http'+href1[5:-4]+'@2x.jpg'
        href2='http'+href2[5:-4]+'@2x.png'
    request.urlretrieve(href1, targ)
    request.urlretrieve(href2, temp)
    target = cv2.imread(targ, 0)
    template = cv2.imread(temp, 0)
    #  裁剪
    template=template[:,~np.all(template==0,0)]
    template=template[~np.all(template==0,1)]
    cv2.imwrite(temp,template)

    cv2.imwrite(targ, target)
    target = cv2.imread(targ)
    template = cv2.imread(temp)
    #  找出最佳匹配
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    #  偏移量
    x, y = np.unravel_index(result.argmax(), result.shape)
    return x,y

'''
href1='https://necaptcha.nosdn.127.net/aea7b62db77f4a4c9b1693cc4f0c132b@2x.jpg'
href2='https://necaptcha.nosdn.127.net/b88254d95fdc424893d71caf243b4b73@2x.png'
temp = 'template.png'
targ = 'target.jpg'
request.urlretrieve('http'+href1[5:], targ)
request.urlretrieve('http'+href2[5:], temp)
target = cv2.imread(targ, 0)
template = cv2.imread(temp, 0)
# cv2.imwrite(temp, template)

# template=cv2.imread(temp)
# template=cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)
#  裁剪
template=template[:,~np.all(template==0,0)]
template=template[~np.all(template==0,1)]
cv2.imwrite(temp,template)
#  缺块大小 大多为88*88 或82*82
w, h = template.shape[::-1]

# cv2.imwrite(targ, target)
# target = cv2.imread(targ)
# show(target)
# target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
# show(target)
# target = abs(255 - target)
# show(target)
cv2.imwrite(targ, target)
target = cv2.imread(targ)
template = cv2.imread(temp)
show(template)
#  找出最佳匹配
result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
#  偏移量
x, y = np.unravel_index(result.argmax(), result.shape)
# 展示圈出来的区域
cv2.rectangle(target, (y, x), (y + w, x + h), (7, 249, 151), 2)
show(target)
'''