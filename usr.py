# -*- coding: utf-8 -*-
import time,random,cv,ua
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


class User(object):
    def __init__(self,i,line):
        param=line.split()
        self.userName=param[0]
        self.password=param[1]
        if len(param) == 3:
            self.server=param[2]
        self.info='账号%s %s\n' % (i,param[0])
        self.ok=0
        self.fail=0
        self.p=0  # p pass
        self.trytime=0
        self.driver=None
        self.show=i+' '

    def check_login(self):
        driver=self.driver
        driver.get("http://shop.9you.com/")
        try:
            driver.find_element_by_class_name('loginUsecenter')
            return True
        except Exception:
            print(self.info.split()[0] + '\n需要先登录')
            return False

    def login(self):
        driver=self.driver
        driver.get("http://shop.9you.com/sso/login")
        driver.find_element_by_id('userName').send_keys(self.userName)
        driver.find_element_by_id('password').send_keys(self.password)
        driver.find_element_by_id('submitlog').click()
        return

    def captcha(self):
        self.trytime += 1
        if self.trytime > 5:
            print(self.info.split()[0] + '验证滑块失败超过最高次数5次，终止！！！')
            return
        driver = self.driver
        WebDriverWait(driver, 5).until(lambda x: x.find_element_by_class_name('yidun_slider')).is_displayed()
        time.sleep(1.111)
        #  获取滑块
        element = driver.find_element_by_class_name('yidun_slider')  # 滑动滑块
        ActionChains(driver).click_and_hold(on_element=element).perform()
        WebDriverWait(driver, 5).until(lambda x: x.find_element_by_class_name('yidun_bg-img'))
        WebDriverWait(driver, 5).until(lambda x: x.find_element_by_class_name('yidun_jigsaw'))
        ref1 = driver.find_element_by_class_name('yidun_bg-img').get_attribute('src')
        ref2 = driver.find_element_by_class_name('yidun_jigsaw').get_attribute('src')
        x, y = cv.offset(ref1, ref2)
        # time.sleep(0.483)
        # ActionChains(driver).move_by_offset(xoffset=y*2//3+7, yoffset=0).perform()
        # ActionChains(driver).drag_and_drop_by_offset(element,y*2//3+7,0).perform()
        #  生成拖拽移动轨迹，加3是为了模拟滑过缺口位置后返回缺口的情况
        #  原图缩小了2/3的规模（480*240->320*160），再加上滑块和原图的10Px偏移，减去小图与原图的3-4Px左边距
        #  得到公式xoffset=y*2//3+10-3=y*2//3+7,然后加3模拟过缺口位置
        track_list = cv.get_track(y * 2 // 3 + 10)
        # print(track_list)
        # print(len(track_list))
        # 根据轨迹拖拽圆球
        for track in track_list:
            # time.sleep(random.uniform(0,0.01))
            ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
        # 模拟人工滑动超过缺口位置返回至缺口的情况，数据来源于人工滑动轨迹，同时还加入了随机数，都是为了更贴近人工滑动轨迹
        imitate = ActionChains(driver).move_by_offset(xoffset=-1, yoffset=0)
        time.sleep(0.015)
        imitate.perform()
        time.sleep(random.randint(6, 10) / 10)
        imitate.perform()
        time.sleep(0.04)
        imitate.perform()
        time.sleep(0.012)
        imitate.perform()
        time.sleep(0.019)
        ActionChains(driver).move_by_offset(xoffset=1, yoffset=0).perform()
        # 放开圆球
        ActionChains(driver).pause(random.randint(6, 14) / 10).release(element).perform()
        time.sleep(0.333)
        try:
            driver.find_element_by_class_name('yidun--success')
            driver.find_element_by_id('userName').send_keys(self.userName)
            driver.find_element_by_id('password').send_keys(self.password)
            driver.find_element_by_id('submitlog').click()
        except Exception:
            print(self.info.split()[0] + '验证滑块失败')
            self.captcha()

    def try_ready(self,lock,delay,log):
        option = Options()
        option.add_argument('--user-data-dir=user-data/%s' % self.userName)
        # option.add_argument('--disable-infobars')
        option.add_experimental_option('useAutomationExtension', False)
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_argument('--start-maximized')
        option.add_argument(ua.getheader())
        self.driver = webdriver.Chrome(options=option)
        if not self.check_login():
            self.login()
            # 判断登陆是否成功
            time.sleep(delay)
            if len(self.driver.current_url) < 22:  # len('http://shop.9you.com/')=21
                return True
            elif self.driver.find_element_by_class_name('cuowu').text.strip() == '账号异常，请拖动滑块至指定区域':  # 验证滑块
                self.captcha()
                time.sleep(delay)
                if len(self.driver.current_url) < 22:  # len('http://shop.9you.com/')=21
                    return True
                else:
                    print(self.info + self.driver.find_element_by_class_name('cuowu').text + '\n')
                    lock.acquire()
                    try:
                        print(self.info.split('\n')[0] + ' FATAL ERROR！！！')
                        print(self.info.split('\n')[0] + ' FATAL ERROR！！！', file=log)
                        log.flush()
                    finally:
                        lock.release()
                    return False
            else:
                print(self.info + self.driver.find_element_by_class_name('cuowu').text + '\n')
                lock.acquire()
                try:
                    print(self.info.split('\n')[0] + ' FATAL ERROR！！！')
                    print(self.info.split('\n')[0] + ' FATAL ERROR！！！', file=log)
                    log.flush()
                finally:
                    lock.release()
                return False
        return True

    def sign0(self):
        driver=self.driver
        # 顺便把简单的网站签到一下
        driver.get('http://uhg.9you.com/')
        try:
            WebDriverWait(driver,5).until(lambda x:x.find_element_by_xpath('//*[@id="ind_loggedBox"]/p[2]/span').is_displayed())
            self.show+=driver.find_element_by_xpath('//*[@id="ind_loggedBox"]/p[2]/span').text
            driver.get('http://uhg.9you.com/vip/index/do_sign_in.html')
            time.sleep(0.9)
            if driver.find_element_by_xpath('/html/body/div/h5[1]').text[0:5] == '签到成功！':
                # self.ok += 1
                self.info=self.info + 'OK--(0) ' + driver.find_element_by_xpath('/html/body/div/h5[1]').text + '\n'
                self.show+=driver.find_element_by_xpath('/html/body/div/h5[1]').text[5:]+' '
            elif driver.find_element_by_xpath('/html/body/div/h5[2]').text == '今日已签到！':
                # self.ok += 1
                self.info=self.info + 'OK--(0) 签到成功 请勿重复操作了！\n'
            else:
                self.fail += 1
                self.info=self.info + 'FAIL(0) 签到失败！\n'
        except TimeoutException:
            self.fail+=1
            self.info = self.info + 'FAIL(0) 请先补充资料！\n'
        except:
            self.fail += 1
            self.info = self.info + 'FAIL(0) 自行确认是否签上！\n'

    def ring(self):
        driver=self.driver
        driver.get('http://shop.9you.com/NewDaily/')
        WebDriverWait(driver,5).until(lambda x:x.find_element_by_xpath(
            '/html/body/div[4]/div[6]/div[2]/div/div[3]/div[2]/p[2]').is_displayed())
        describe=driver.find_elements_by_class_name('describe')
        words=''
        for i in range(3):
            words+=describe[i].text.split()[0]+' '
        self.show+=' '+words
        self.info+='OK--(戒指) '+words+'\n'
