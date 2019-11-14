import cv2 as cv
from urllib import request
import numpy as np


# def show(pic):
#     cv.imshow('Show', pic)
#     cv.waitKey(0) & 0xFF
#     cv.destroyAllWindows()


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
    target = cv.imread(targ, 0)
    template = cv.imread(temp, 0)
    #  裁剪
    # template=template[:,~np.all(template==0,0)]
    # template=template[~np.all(template==0,1)]
    template=template[:,np.any(template,0)]
    template=template[np.any(template,1)]
    # cv.imwrite(temp,template)
    #
    # cv.imwrite(targ, target)
    # target = cv.imread(targ)
    # template = cv.imread(temp)
    #  找出最佳匹配
    result = cv.matchTemplate(target, template, cv.TM_CCOEFF)
    #  偏移量
    _,_,_,a=cv.minMaxLoc(result)
    # x = np.unravel_index(result.argmax(), result.shape)
    return a[0]


# 滑块移动轨迹
def get_track(distance):
    track=[]
    left=distance
    threshold=distance*2//5
    # t=random.randint(2,3)/10
    v0=distance//10
    aa=(distance//45, -distance//36)
    v=v0
    while left > 0:
        a=aa[0] if left > threshold else aa[1]
        v = max(v0, v+a)
        v = min(left, v)
        left -= v
        track.append(v)
        # print('%d %d' %(left,v))
    # print(track)
    return track


'''
href1='https://necaptcha.nosdn.127.net/aea7b62db77f4a4c9b1693cc4f0c132b@2x.jpg'
href2='https://necaptcha.nosdn.127.net/b88254d95fdc424893d71caf243b4b73@2x.png'
temp = 'template.png'
targ = 'target.jpg'
request.urlretrieve('http'+href1[5:], targ)
request.urlretrieve('http'+href2[5:], temp)
target = cv.imread(targ, 0)
template = cv.imread(temp, 0)
# cv.imwrite(temp, template)

# template=cv.imread(temp)
# template=cv.cvtColor(template,cv.COLOR_BGR2GRAY)
#  裁剪
template=template[:,~np.all(template==0,0)]
template=template[~np.all(template==0,1)]
cv.imwrite(temp,template)
#  缺块大小 大多为88*88 或82*82
w, h = template.shape[::-1]

# cv.imwrite(targ, target)
# target = cv.imread(targ)
# show(target)
# target = cv.cvtColor(target, cv.COLOR_BGR2GRAY)
# show(target)
# target = abs(255 - target)
# show(target)
cv.imwrite(targ, target)
target = cv.imread(targ)
template = cv.imread(temp)
show(template)
#  找出最佳匹配
result = cv.matchTemplate(target, template, cv.TM_CCOEFF_NORMED)
#  偏移量
x, y = np.unravel_index(result.argmax(), result.shape)
# 展示圈出来的区域
cv.rectangle(target, (y, x), (y + w, x + h), (7, 249, 151), 2)
show(target)
'''