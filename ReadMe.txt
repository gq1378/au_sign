account.txt说明
userName password 每日的区  福利派对  在线礼物  南瓜之夜  免费福利  舞者回归
pppppppp xxxxxxxx   1       0        1	     1       0        1
连续奖励全部在华东一领取

每日 长期
福利派对 7天
在线礼物 10天
南瓜之夜 
免费福利 
舞者回归 12天 4*3

element.txt说明
签到按钮      选区后确认按钮    高/非 选项          选区的那个空白
class_btn1    sureSign          0    /html/body/div[3]/div[2]/input[1]
xpath		class				xpath
\	     .tanc1 .sure     .tanc1 ul :nth-child(1)	(#area)1
\		\		1		1
其中class_代表以class_name查找，没有则为按xpath查找

$('.tanc1 ul :nth-child(1)').attr('class','btn_l active')
$('#area1').val('1')
$('.tanc1 .sure').click()

task.txt说明
101111
1代表有此任务 0代表没有