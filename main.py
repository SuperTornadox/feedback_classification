
print('This is a user feedback system designed & developed by hexuchen\n')
print('本项目开发是为了解决用户反馈分类重复劳动的问题,使用关键词检索完成简单分类\n')
print('在完成简单分类以后,对于新的用户反馈,使用月之暗面大模型进行分类,并将新的反馈自动录入检索库中\n')
print('如果你对于本系统有改进建议,欢迎通过邮箱交流: xuchenhe@nyu.edu\n')
print('未来本项目将开源并持续更新,请期待\n')

import re
import time
import sys
import os
import pandas as pd
from openai import OpenAI

########   when packaging    #########
# root_route_0=os.path.dirname(os.path.realpath(sys.executable))
# root_route = os.path.dirname(root_route_0)+'/CL_v2'

#######   when developing   #########
root_route='venv/file'
print(f"当前路径为{root_route}")

class Kwd_cld:
    keyword=None
    problem_genre=None
    child_genre=None
    grand_genre=None
kwd_clds=[]

################  创建时间戳 #########################
time_now=time.strftime("%m_%d_%H_%M_%S",time.localtime())
print("\n"*2)
print(f"创建时间戳为:{time_now}")
################  创建时间戳 #########################

#################  Moonshot AI API 配置 #########################
client = OpenAI(
            api_key="sk-k7hAn18odQ5jX98CVnhiUtKIfn9vU4vV2m9OvAbgII25OxK9",
            base_url="https://api.moonshot.cn/v1",
        )
################  Moonshot AI API 配置 #########################

################### 文件 IO #########################
file_name='用户反馈_M6W1.xlsx'
input_route=f'{root_route}/{file_name}'
#输入的文档需要将所有原声放在第 0 列
input_dataframe = pd.read_excel(input_route)
input_column = input_dataframe.iloc[:,0]
final_output_route=f'{root_route}/整理完成_用户反馈_{time_now}.xlsx'
################### 文件 IO #########################

def feedback_classification(start_number,input_route,output_route):
    classified_cnt=0
    print("*" * 40)
    print("\n")
    print(f"完成所需的时间为:{len(input_dataframe) * 0.3 / 60}分钟")
    print("*" * 40)
    print("\n")
    print(f"受限于 Moonshot AI的RPM(200)限制,现在每分钟可以稳定处理200条用户数据")
    print("Let's get started from now !")
    print("*"*40)
    for i in range(len(input_column)):
        feedback=input_column[i]
        try:
             # 对于未分类的反馈进行意图猜测
            completion = client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=[
                    {"role": "user",
                         "content": f"请你帮我判断这一句反馈是以下8类中的哪一类："
                                    f"1.类型名称：推荐内容不满意，几个例子是：1.推送的笔记很多都是2023年，再给流量方面能不能注意下笔记时效性，很多笔记都无用了，时间长了，就不想看了。2.你们一天给我推外地吃的干嘛！！3.能不能不要推荐非本地的美食"
                                    f"2.类型名称：收藏夹按地区分类，几个例子是：1.收藏夹不能细分地区了！！好不方便！！！！2. 什么时候把收藏里的街道区域分类改回来，客户体验真垃圾啊，垃圾 3. 现在为什么收藏只能选择城市不能细化到区县，找想吃的店很不方便！！！！！！"
                                    f"3.类型名称：反复验证，几个例子是：1.一直让验证身份 2.总是频繁出现需要验证的情况，只要打开就会被验证，希望平台优化 3.为什么最近每次进大众点评软件总是让我进行各种各样的验证？我是有什么不正确的操作引起的吗？非常影响我的体验，请给我一个合理的解释"
                                    f"4.类型名称：暗黑模式，几个例子是：1.我要夜间模式2.安卓版赶紧出暗黑模式，大晚上眼睛都要瞎了3.可以出深色模式吗4.没有深色模式"
                                    f"5.类型名称：重复验证，几个例子是：1. 建议出个拉黑店家，看到这家就烦 2.不要刷到这家，谢谢 3.不要再推这个店了 ，恶心"
                                    f"6.类型名称：评价暴露隐私，几个例子是：1.为什么我给商家打低分以后，商家会联系我改评价啊？我的手机号他是怎么知道的啊？ 2.我只给口腔打了个预约电话，我电话就被卖了接各种口腔广告。这个哪里投诉 3.公开我出行.消费的信息前，应该有证询框。"
                                    f"7.类型名称：评价不显示，几个例子是：1.客户给我们店评价了为什么不显示，商量也上不去 2.客服，你好！我们柜台上午顾客买完东西后，评论了怎么不显示啊 3.评论的内容为何没发布"
                                    f"8.类型名称：其他，不属于上面 7 类的则是其他"
                                    f"所以，[{feedback}]是一条用户反馈，类型名称为："

                    },  # 这里使用少shot提示法进行尝试

                    ],
                    temperature=0,  # temperature设置为0,提高回答的稳定性
            )
            message = completion.choices[0].message.content
        except Exception as e:
                final_keyword="敏感词"
                final_child_genre="无法分类"
                final_grand_genre="其他"

        #print(f"[{feedback}]中含有关键词:[{final_keyword}],因此被分为:[{final_child_genre}]")
        #将数据写入表内

        print(f"现在分类到第{i}/{len(input_dataframe)}条")
        print(f"反馈为：{feedback}\n")
        print(f"分类结果为：{message}")

    input_dataframe.columns=["用户原声","大类","子类","关键词"]

classified_count=feedback_classification(start_number=0,input_route=input_route,output_route=final_output_route)
#start_number表示从第几行处理,这样遇到进程被打断时可以继续处理y
print(f"本次总共有{len(input_column)}条用户反馈,其中关键词分类{classified_count}条，MoonshotAI 辅助分类{len(input_column)-classified_count}条")