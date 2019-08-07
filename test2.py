# -*- coding: utf-8 -*-
import time,threading,calendar,random,ua,json
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from cv import offset
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

server_list=[1,3,5,7,12,16,17,48,2,18,21,39]


# 滑块移动轨迹
def get_track(distance):
    track=[]
    current=0
    mid=distance*3/5
    t=random.randint(2,3)/10
    v=6
    while current<distance:
        if current<mid:
            a=3
        else:
            a=-5
        move=v*t+1/2*a*t*t
        v=max(6,v+a*t)
        current+=move
        track.append(round(move))
        # print(v)
    # print(track)
    return track


class User(object):
    def __init__(self,i,line):
        param=line.split()
        self.userName=param[0]
        self.password=param[1]
        self.server=param[2]
        self.info='账号%s %s\n' % (str(i+1),param[0])
        self.ok=0
        self.fail=0
        self.p=0  # p pass
        self.trytime=0
        self.driver=None

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
        self.trytime+=1
        if self.trytime>5:
            print(self.info.split()[0] + '验证滑块失败超过最高次数5次，终止！！！')
            return
        driver=self.driver
        WebDriverWait(driver,5).until(lambda x:x.find_element_by_class_name('yidun_slider')).is_displayed()
        time.sleep(1.111)
        #  获取滑块
        element = driver.find_element_by_class_name('yidun_slider')    # 滑动滑块
        ActionChains(driver).click_and_hold(on_element=element).perform()
        WebDriverWait(driver,5).until(lambda x:x.find_element_by_class_name('yidun_bg-img'))
        WebDriverWait(driver,5).until(lambda x:x.find_element_by_class_name('yidun_jigsaw'))
        ref1=driver.find_element_by_class_name('yidun_bg-img').get_attribute('src')
        ref2=driver.find_element_by_class_name('yidun_jigsaw').get_attribute('src')
        x, y =offset(ref1,ref2)

        #  生成拖拽移动轨迹，加3是为了模拟滑过缺口位置后返回缺口的情况
        #  原图缩小了2/3的规模（480*240->320*160），再加上滑块和原图的10Px偏移，减去小图与原图的3-4Px左边距
        #  得到公式xoffset=y*2//3+10-3=y*2//3+7,然后加3模拟过缺口位置
        track_list=get_track(y*2//3+10)
        # print(track_list)
        # print(len(track_list))
        # 根据轨迹拖拽圆球
        for track in track_list:
            # time.sleep(random.uniform(0,0.01))
            ActionChains(driver).move_by_offset(xoffset=track,yoffset=0).perform()
        # 模拟人工滑动超过缺口位置返回至缺口的情况，数据来源于人工滑动轨迹，同时还加入了随机数，都是为了更贴近人工滑动轨迹
        imitate=ActionChains(driver).move_by_offset(xoffset=-1, yoffset=0)
        time.sleep(0.015)
        imitate.perform()
        time.sleep(random.randint(6,10)/10)
        imitate.perform()
        time.sleep(0.04)
        imitate.perform()
        time.sleep(0.012)
        imitate.perform()
        time.sleep(0.019)
        imitate.perform()
        time.sleep(0.033)
        ActionChains(driver).move_by_offset(xoffset=1, yoffset=0).perform()
        # 放开圆球
        ActionChains(driver).pause(random.randint(6,14)/10).release(element).perform()
        time.sleep(3.333)
        try:
            driver.find_element_by_class_name('yidun--success')
            driver.find_element_by_id('userName').send_keys(self.userName)
            driver.find_element_by_id('password').send_keys(self.password)
            driver.find_element_by_id('submitlog').click()
        except Exception:
            print(self.info.split()[0] + '验证滑块失败')
            self.captcha()

    def sign(self,tip,api,server,choice=''):
        if server=='0':
            self.p+=1
            return
        driver=self.driver
        self.trytime=0
        time.sleep(delay)
        # 选区1
        server=server_list[int(server,16)-1]
        js1='''post=$.ajax({
        type:'POST',
        url:'%s',
        data:'serverId=%d%s',
        dataType:'json'
        })''' % (api,server,choice)
        driver.execute_script(js1)
        time.sleep(delay)
        js2='return (post.readyState==4 && post.status==200)'
        while not driver.execute_script(js2):
            time.sleep(delay)
            self.trytime+=1
            if self.trytime >5:
                self.fail += 1
                self.info=self.info + 'FAIL' + tip + '5次尝试均失败！' + '\n'
                return
        js3='return post.responseText'
        response=driver.execute_script(js3)
        data=json.loads(response,encoding='utf-8')
        code,message=data['code'],data['message']
        if code == 1:
            self.ok += 1
            self.info=self.info + 'OK--' + tip + message + '\n'
        elif '过' in message or '已经' in message or '重复' in message :
            self.ok += 1
            self.info=self.info + 'OK--' + tip + message + '\n'
        else:
            self.fail += 1
            self.info=self.info + 'FAIL' + tip + message + '\n'
        return

    def sign1(self):
        self.sign('(每日) ',api+'1',self.server[0])

    def sign1_29(self):
        if self.server[0] != '0':
            self.sign('(每日29) ',api+'3','1','&itemCode=1')

    def sign1_2(self):
        self.sign('(高峰) ', api+'4',self.server[0],'&value=1')

    def sign1_3(self):
        self.sign('(非高峰) ', api+'4',self.server[0],'&value=2')

    def sign1_7(self):
        if self.server[0] != '0':
            self.sign('(高峰7) ', api+'5','1','&value=7')

    def sign1_15(self):
        if self.server[0] != '0':
            self.sign('(高峰15) ', api+'5','1','&value=15')

    def sign1_25(self):
        if self.server[0] != '0':
            self.sign('(高峰25) ', api+'5','1','&value=25')

    def sign1_last(self):
        if self.server[0] != '0':
            web=['',api+'11','1','&value=maxScore']
            arg=['',api+'11','1','']
            choice_list=[10,25,50,75,100,110]
            for i,value in enumerate(choice_list):
                arg[0]='(活跃度%d) ' % (i+1)
                arg[3]=web[3]+str(value)
                self.sign(*arg)
                time.sleep(5.1-delay*2)
            self.sign('(活跃度80) ',api+'12','1','&value=exchange80')

    def sign2(self):
        if self.server[1] == '0':
            self.p += 1
            return
        dbegin=11
        api2='/active/active/name/Party%s/act/2' % date.today().strftime('%Y%m')
        self.sign('(福利派对) ',api2,self.server[1],'&itemCode=online')
        if date.today().day == 2+dbegin:
            time.sleep(5.1-delay*2)
            self.sign('(福利派对3天) ',api2,'1','&itemCode=onlineday3')

    def sign3(self,dbegin,web):
        if self.server[2] == '0':
            self.p += 1
            return
        day=date.today()
        # month=date.today().month
        # day=day+31*(month-7)  # day-day_start+day_num*(month-last_month)
        # dbegin=date(2019,7,30)
        days=(day-dbegin).days
        api3='/active/active/name/%s/act/1' % web
        try:
            self.sign('(在线礼物) ',api3,self.server[2],'&itemCode=login')
            if days == 2:
                time.sleep(10.1-delay*2)
                self.sign('(在线礼物3天) ',api3,'1','&itemCode=login3')
            elif days == 6:
                time.sleep(10.1-delay*2)
                self.sign('(在线礼物7天) ',api3,'1','&itemCode=login7')
            elif days == 9:
                time.sleep(10.1-delay*2)
                self.sign('(在线礼物10天) ',api3,'1','&itemCode=login10')
        except Exception as e:
            print(self.info.split('\n')[0])
            print(str(e))
            self.fail += 1
            self.info=self.info + 'FAIL(在线礼物) ERROR请查看异常输出！\n' + str(e)
        #  模式
        time.sleep(10-delay*2)
        try:
            self.sign('(在线礼物模式) ',api3,self.server[2],'&itemCode=online1923')
            if days == 2:
                time.sleep(10.1-delay*2)
                self.sign('(在线礼物模式3天) ',api3,'1','&itemCode=onlineday3')
            elif days == 6:
                time.sleep(10.1-delay*2)
                self.sign('(在线礼物模式7天) ',api3,'1','&itemCode=onlineday7')
            elif days == 9:
                time.sleep(10.1-delay*2)
                self.sign('(在线礼物模式10天) ',api3,'1','&itemCode=onlineday10')
        except Exception as e:
            print(self.info.split('\n')[0])
            print(str(e))
            self.fail += 1
            self.info=self.info + 'FAIL(在线礼物模式) ERROR请查看异常输出！\n' + str(e)
        return

    def sign7(self):
        if self.server[3] == '0':
            self.p += 1
        api4='/active/active/name/OnlineGift190425/act/act1_2'
        self.sign('(热枕之心) ',api4,self.server[3],'&value=task_login')

    def sign6(self):
        if self.server[3] == '0':
            self.p += 1
        day=date.today().day
        month=date.today().month
        day=day-28+31*(month-3)  # day-day_start+day_num*(month-last_month)
        driver=self.driver
        if day%3 == 2:
            driver.get('http://shop.9you.com/show/active/name/FriendBack190326/act/2')
            qi='/html/body/div[3]/div[12]/ul/li[%d]' % ((day+1)/3)
            web=['/html/body/div[3]/div[13]/div[?]/ul/li[!]','xpath_/html/body/div[5]/div/a[2]',
            '0','/html/body/div[5]/div/div/label/input[1]']
            for i in range(6):
                WebDriverWait(driver,5).until(lambda x:x.find_element_by_xpath(qi))  # 等待领取按钮加载
                driver.find_element_by_xpath(qi).click()
                web[0]='/html/body/div[3]/div[13]/div[%d]/ul/li[%d]' % (day//3+1,i+1)
                if i != 5:
                    self.sign(self.server[5],'(舞者回归%d天%d) ' % (day,i+1),*web)
                    driver.refresh()
                    time.sleep(10-delay*2)
                else:
                    self.sign('1','(舞者回归%d天%d) ' % (day,i+1),*web)
        if day == 11:
            web=['/html/body/div[3]/a[?]','xpath_/html/body/div[6]/div/a[2]','0','/html/body/div[6]/div/div/label/input[1]']
            driver.refresh()
            for i in range(6):
                if i == 3:
                    continue
                web[0]='/html/body/div[3]/a[%d]' % (i+2)
                self.sign('1','(舞者回归11天总%d) ' % (i+1),*web)
                if i != 5:
                    driver.refresh()
                    time.sleep(10-delay*2)


def user_process(i,line):
    today=date.today()
    time.sleep(i*8+85*(i//5))
    # time.sleep(i)
    user=User(i,line)
    option=Options()
    option.add_argument('--user-data-dir=user-data/%s' % user.userName)
    # option.add_argument('--disable-infobars')
    option.add_experimental_option('useAutomationExtension',False)
    option.add_experimental_option('excludeSwitches',['enable-automation'])
    option.add_argument('--start-maximized')
    option.add_argument(ua.getheader())
    user.driver=webdriver.Chrome(options=option)
    if not user.check_login():
        user.login()
        # 判断登陆是否成功
        time.sleep(delay)
        if len(user.driver.current_url) < 22:  # len('http://shop.9you.com/')=21
            pass
        elif user.driver.find_element_by_class_name('cuowu').text.strip()=='账号异常，请拖动滑块至指定区域':  # 验证滑块
            user.captcha()
            time.sleep(delay)
            if len(user.driver.current_url) < 22:  # len('http://shop.9you.com/')=21
                pass
            else:
                print(user.info + user.driver.find_element_by_class_name('cuowu').text + '\n')
                lock.acquire()
                try:
                    print(user.info.split('\n')[0]+' FATAL ERROR！！！')
                    print(user.info.split('\n')[0]+' FATAL ERROR！！！',file=log)
                    log.flush()
                finally:
                    lock.release()
                return
        else:
            print(user.info + user.driver.find_element_by_class_name('cuowu').text + '\n')
            lock.acquire()
            try:
                print(user.info.split('\n')[0]+' FATAL ERROR！！！')
                print(user.info.split('\n')[0]+' FATAL ERROR！！！',file=log)
                log.flush()
            finally:
                lock.release()
            return

    user.sign1_2()  # 高峰
    timestamp=time.time()

    # 领取7 15 25天
    if today.day == 7:
        user.sign1_7()
    elif today.day == 15:
        user.sign1_15()
    elif today.day == 25:
        user.sign1_25()

    user.sign1()  # 每日

    # 活跃度(月底)
    if today.day == calendar.monthrange(today.year,today.month)[1]:
        user.sign1_last()
    # 签到29天
    elif today.day == calendar.monthrange(today.year,today.month)[1] - 2:
        user.sign1_29()

    if tasks[1] == '1':
        user.sign2()  # 福利派对
    if tasks[2] == '1':
        daybegin=date(2019,7,30)
        user.sign3(daybegin,'OnlineGift2019052002')  # 在线礼物/模式
    if tasks[3] == '1':
        daybegin=date(2019,8,6)
        user.sign3(daybegin,'OnlineGift2019061802')  # 南瓜之夜 # 热枕之心
    # if tasks[4] == '1':
    #     user.sign5()  # 免费福利
    if tasks[5] == '1':
        user.sign6()  # 舞者回归
    ins=time.time()-timestamp+delay*2

    if ins < 10.1:
        time.sleep(10.1-ins)
    user.sign1_3()  # 非高峰

    user.info = user.info + '%d OK  %d FAIL  %d PASS  %d TOTAL\n' % (user.ok,user.fail,user.p,user.ok+user.fail+user.p)
    lock.acquire()
    try:
        num[0] += user.ok
        num[1] += user.fail
        num[2] += user.p
        print(user.info)
        print(user.info,file=log)
        log.flush()
    finally:
        lock.release()
    user.driver.close()
    user.driver.quit()
    del user
    return


lock=threading.Lock()

# 读入任务是否开始的信息
with open('accounts/task.txt','r') as task:
    tlines=task.readlines()
    tasks=tlines[0]
    delay=float(tlines[1])
# 读入用户信息
with open('accounts/account.txt','r') as f:
    accounts=f.readlines()

log=open('accounts/log_test2.txt','a')
print(date.today().isoformat(),file=log)

num=[0,0,0]
api='/active/active/name/%s/act/' % date.today().strftime('%B%Y')
t=[threading.Thread(target=user_process,args=(i,line,)) for i,line in enumerate(accounts)]
for thread in t:
    thread.start()
for thread in t:
    thread.join()
print('done!  %d OK  %d FAIL  %d PASS  %d TOTAL' % (num[0],num[1],num[2],sum(num)))
print('done!  %d OK  %d FAIL  %d PASS  %d TOTAL\n--------------------------------------------------'
      % (num[0],num[1],num[2],sum(num)), file=log)
log.close()
