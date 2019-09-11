# -*- coding: utf-8 -*-
import time,threading,usr
from datetime import date


def user_process(i,line):
    user=usr.User(i,line)
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
t=[threading.Thread(target=user_process,args=(str(i+1),line,)) for i,line in enumerate(accounts)]
for i in range(len(t)):
    t[i].start()
    time.sleep(8)
    if i % 5 == 4:
        time.sleep(85)
for thread in t:
    thread.join()
print('done!  %d OK  %d FAIL  %d PASS' % (num[0],num[1],num[2]))
print('done!  %d OK  %d FAIL  %d PASS\n--------------------------------------------------'
      % (num[0],num[1],num[2]), file=log)
log.close()
show.close()