# -*- coding: utf-8 -*-
import time,threading,usr
from datetime import date
from selenium.webdriver.support.ui import WebDriverWait


class MeUser(usr.User):
    def __init__(self,i,line):
        super().__init__(i,line)
        self.show='%d ' % (i+1)

    def sign0(self):
        driver=self.driver
        # 顺便把简单的网站签到一下
        driver.get('http://uhg.9you.com/')
        WebDriverWait(driver,5).until(lambda x:x.find_element_by_xpath('//*[@id="ind_loggedBox"]/p[2]/span').is_displayed())
        self.show+=driver.find_element_by_xpath('//*[@id="ind_loggedBox"]/p[2]/span').text
        driver.get('http://uhg.9you.com/vip/index/do_sign_in.html')
        time.sleep(delay-0.1)
        if driver.find_element_by_xpath('/html/body/div/h5[1]').text[0:5] == '签到成功！':
            self.ok += 1
            self.info=self.info + 'OK--(0) ' + driver.find_element_by_xpath('/html/body/div/h5[1]').text + '\n'
            self.show+=driver.find_element_by_xpath('/html/body/div/h5[1]').text[5:]+' '
        elif driver.find_element_by_xpath('/html/body/div/h5[2]').text == '今日已签到！':
            self.ok += 1
            self.info=self.info + 'OK--(0) 签到成功 请勿重复操作了！\n'
        else:
            self.fail += 1
            self.info=self.info + 'FAIL(0) 签到失败！\n'
        return

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
        self.info+=words


def user_process(i,line):
    time.sleep(i*8+85*(i//5))
    # time.sleep(i)
    user=MeUser(i,line)
    if not user.try_ready(lock,delay,log):
        return

    user.sign0()
    user.ring()

    lock.acquire()
    try:
        num[0] += user.ok
        num[1] += user.fail
        num[2] += user.p
        print(user.info,file=log)
        print(user.show,file=show)
        log.flush()
        show.flush()
    finally:
        lock.release()
    print(user.info)
    user.driver.close()
    user.driver.quit()
    del user
    return


delay=0.6
lock=threading.Lock()

# 读入用户信息
with open('accounts/me.txt','r') as f:
    accounts=f.readlines()
log=open('accounts/log_me.txt','a')
show=open('accounts/show_me.txt','a')
print(date.today().isoformat(),file=log)
print(date.today().isoformat(),file=show)
num=[0,0,0]
t=[threading.Thread(target=user_process,args=(i,line,)) for i,line in enumerate(accounts)]
for thread in t:
    thread.start()
for thread in t:
    thread.join()
print('done!  %d OK  %d FAIL  %d PASS' % (num[0],num[1],num[2]))
print('done!  %d OK  %d FAIL  %d PASS\n--------------------------------------------------'
      % (num[0],num[1],num[2]), file=log)
log.close()
show.close()