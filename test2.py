# -*- coding: utf-8 -*-
import time,threading,calendar,json,configparser,usr
from datetime import date

server_list=[1,3,5,7,12,16,17,48,2,18,21,39]


class SignUser(usr.User):
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
        elif '过' in message or '已经' in message or '重复' in message:
            self.ok += 1
            self.info=self.info + 'OK--' + tip + message + '\n'
        else:
            self.fail += 1
            self.info=self.info + 'FAIL' + tip + message + '\n'

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

    def sign2(self,days,api):
        if self.server[1] == '0':
            self.p += 1
            return
        # api2='/active/active/name/Party%s/act/2' % today.strftime('%Y%m')
        self.sign('(福利派对) ',api,self.server[1],'&value=online')
        if days == 2:
            time.sleep(5.1-delay*2)
            self.sign('(福利派对3天) ',api,'1','&value=onlineday3')

    def sign3(self,days,api):
        if self.server[2] == '0':
            self.p += 1
            return
        try:
            self.sign('(在线礼物) ',api,self.server[2],'&itemCode=login')
            if days == 2:
                time.sleep(10.1-delay*2)
                self.sign('(在线礼物3天) ',api,'1','&itemCode=login3')
            elif days == 6:
                time.sleep(10.1-delay*2)
                self.sign('(在线礼物7天) ',api,'1','&itemCode=login7')
            elif days == 9:
                time.sleep(10.1-delay*2)
                self.sign('(在线礼物10天) ',api,'1','&itemCode=login10')
        except Exception as e:
            print(self.info.split('\n')[0])
            print(str(e))
            self.fail += 1
            self.info=self.info + 'FAIL(在线礼物) ERROR请查看异常输出！\n' + str(e)
        # #  模式
        # time.sleep(10-delay*2)
        # try:
        #     self.sign('(在线礼物模式) ',api,self.server[2],'&itemCode=online1923')
        #     if days == 2:
        #         time.sleep(10.1-delay*2)
        #         self.sign('(在线礼物模式3天) ',api,'1','&itemCode=onlineday3')
        #     elif days == 6:
        #         time.sleep(10.1-delay*2)
        #         self.sign('(在线礼物模式7天) ',api,'1','&itemCode=onlineday7')
        #     elif days == 9:
        #         time.sleep(10.1-delay*2)
        #         self.sign('(在线礼物模式10天) ',api,'1','&itemCode=onlineday10')
        # except Exception as e:
        #     print(self.info.split('\n')[0])
        #     print(str(e))
        #     self.fail += 1
        #     self.info=self.info + 'FAIL(在线礼物模式) ERROR请查看异常输出！\n' + str(e)

    # def sign4(self):
    #     if self.server[3] == '0':
    #         self.p+=1
    #         return
    #     api='/active/active/name/NationalDayCelebration19/act/act2_1'
    #     self.sign('(国庆庆典) ',api,'1')

    def sign6(self,days,api):
        if self.server[5] == '0':
            self.p += 1
            # self.info=self.info + 'PASS(舞者回归) pass\n'
            return

        qu=days//3+1
        if days%3 == 1:
            for i in range(6):
                if i != 5:
                    self.sign('(舞者回归%d天%d) ' % (days,i+1),api+'5',self.server[5],'&value=%d_%d' % (qu,i+1))
                    time.sleep(10.1-delay*2)
                else:
                    self.sign('(舞者回归%d天%d) ' % (days,i+1),api+'5','1','&value=%d_6' % qu)

        if days == 10:
            for i in range(6):
                if i == 3:
                    continue
                self.sign('(舞者回归11天总%d) ' % (i+1),api+'6','1','&value=main%d' % (i+1))
                if i != 5:
                    time.sleep(10.1-delay*2)

    def sign7(self):
        if self.server[3] == '0':
            self.p += 1
            return
        api4='/active/active/name/OnlineGift190425/act/act1_2'
        self.sign('(热枕之心) ',api4,self.server[3],'&value=task_login')


def user_process(i,line):
    user=SignUser(i,line)
    if not user.try_ready(lock,delay,log):
        return

    user.sign1_2()  # 高峰
    user.sign0()
    user.ring()
    time.sleep(8 - delay*2)
    user.sign1_3()  # 非高峰

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
    elif today.day == calendar.monthrange(today.year,today.month)[1] - 1:
        user.sign1_29()

    if tasks[1] == '1':
        user.sign2(days1,api1)  # 福利派对
    if tasks[2] == '1':
        user.sign3(days2,api2)  # 在线礼物/模式
    if tasks[3] == '1':
        user.sign3(days3,api3)  # 南瓜之夜 # 热枕之心
    # if tasks[4] == '1':
    #     user.sign5()  # 免费福利
    if tasks[5] == '1':
        user.sign6(days5,api5)  # 舞者回归

    user.info = user.info + '%d OK  %d FAIL  %d PASS  %d TOTAL\n' % (user.ok,user.fail,user.p,user.ok+user.fail+user.p)
    lock.acquire()
    try:
        num[0] += user.ok
        num[1] += user.fail
        num[2] += user.p
        print(user.info)
        print(user.info,file=log)
        print(user.show,file=show)
        log.flush()
        show.flush()
    finally:
        lock.release()
    user.driver.close()
    user.driver.quit()
    del user
    return


lock=threading.Lock()
conf=configparser.ConfigParser(allow_no_value=True)
conf.read('accounts/config.ini',encoding='utf-8')
Setting=conf['Setting']
tasks=Setting['task']  # 需要签哪些到
delay=Setting.getfloat('delay')  # 延迟设定
# accounts=[account for account in conf['users'].items()]  # 读入用户信息
today = date.today()
if tasks[1] == '1':
    daybegin=eval('date(%s)' % conf['party']['daybegin'])
    days1=(today-daybegin).days
    api1 = '/active/active/name/Party%s/act/2' % today.strftime('%Y%m')

if tasks[2] == '1':
    daybegin=eval('date(%s)' % conf['onlinegift']['daybegin'])
    days2=(today-daybegin).days
    api2 = '/active/active/name/%s/act/1' % conf['onlinegift']['web']

if tasks[3] == '1':
    daybegin=eval('date(%s)' % conf['onlinegift2']['daybegin'])
    days3=(today-daybegin).days
    api3 = '/active/active/name/%s/act/1' % conf['onlinegift2']['web']

if tasks[5] == '1':
    daybegin = eval('date(%s)' % conf['friendback']['daybegin'])
    days5 = (today - daybegin).days
    api5 = '/active/active/name/%s/act/' % conf['friendback']['web']

log=open('accounts/log_test2.txt','a')
show=open('accounts/show_me.txt','a')
print(today.isoformat(),file=log)
print(today.isoformat(),file=show)

num=[0,0,0]
api='/active/active/name/%s/act/' % today.strftime('%B%Y')
t=[threading.Thread(target=user_process,args=(i,line,)) for i,line in conf['users'].items()]
for i in range(len(t)):
    t[i].start()
    time.sleep(8)
    if i % 5 == 4:
        time.sleep(85)
for thread in t:
    thread.join()
print('done!  %d OK  %d FAIL  %d PASS  %d TOTAL' % (num[0],num[1],num[2],sum(num)))
print('done!  %d OK  %d FAIL  %d PASS  %d TOTAL\n--------------------------------------------------'
      % (num[0],num[1],num[2],sum(num)), file=log)
log.close()
show.close()
