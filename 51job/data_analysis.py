import pandas as pdimport numpy as npfrom pyecharts import options as optsfrom pyecharts.charts import Piefrom pyecharts.charts import Barfrom pyecharts.faker import Fakerimport jiebafrom wordcloud import WordClouddf = pd.read_csv('data.csv')# 学历薪资图def edu_salary():    df1 = df.copy()    # 处理nan的教育和薪资，删除不要的列    df1 = df1.dropna(0, subset=['edu', 'salary'])    df1 = df1[['edu', 'salary']]    # 转换单位    for i in range(df1.shape[0]):        tmp_salary = df1.iloc[i, 1]        if tmp_salary.endswith('万/月'):            tmp_salary = tmp_salary.replace('万/月', '')            min_max = tmp_salary.split('-')            salary = 10000 * (float(min_max[1]) + float(min_max[0]))/2            df1.iloc[i, 1] = salary        elif tmp_salary.endswith('万/年'):            tmp_salary = tmp_salary.replace('万/年', '')            min_max = tmp_salary.split('-')            salary = 10000 * (float(min_max[1]) + float(min_max[0]))/(2*12)            df1.iloc[i, 1] = salary        elif tmp_salary.endswith('千/月'):            tmp_salary = tmp_salary.replace('千/月', '')            min_max = tmp_salary.split('-')            salary = 1000 * (float(min_max[1]) + float(min_max[0]))/2            df1.iloc[i, 1] = salary        elif tmp_salary.endswith('元/天'):            tmp_salary = tmp_salary.replace('元/天', '')            salary = float(tmp_salary) * 30            df1.iloc[i, 1] = salary                name_list = ['大专', '本科']    c = (        Bar()        .add_xaxis(            [                "最低薪资",                "平均薪资",                "最高薪资",            ]        )        .add_yaxis("本科生", [df1[df1['edu']=='本科'].salary.min(),                              df1[df1['edu']=='本科'].salary.mean(),                             df1[df1['edu']=='本科'].salary.max()])        .add_yaxis("专科生", [df1[df1['edu']=='大专'].salary.min(),                             df1[df1['edu']=='大专'].salary.mean(),                             df1[df1['edu']=='大专'].salary.max()])        .set_global_opts(            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0)),            title_opts=opts.TitleOpts(title="学历-薪资对比"),        )        .render("学历-薪资对比.html")    )# 学历分布def edu_fenbu():    xueli_list = df.edu.value_counts().values.tolist()    c = (        Pie()        .add("haha", [list(z) for z in zip(['本科','大专','硕士'], xueli_list)])        .set_global_opts(title_opts=opts.TitleOpts(title="学历比例"))        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))        .render("学历比例.html")    )# 词云图def word_cloud():    detail_list = df['detail'].values.tolist()    # 清洗掉一些无用的常出现的字    for i in range(len(detail_list)):        detail_list[i] = detail_list[i].replace('微信分享', '').\            replace('关键字', '').replace('职能类别', '').replace('岗位要求', '').\                replace('岗位职责', '').replace('职位描述', '').replace(':', '').\                    replace('：','')    jieba.load_userdict('it_dict.txt')    segs = jieba.cut('\n'.join(detail_list))    cloud_text=",".join(segs)    wc = WordCloud(    background_color="white", #背景颜色    max_words=200, #显示最大词数    min_font_size=15,    max_font_size=50,    font_path='simhei.ttf',    width=400  #图幅宽度    )    wc.generate(cloud_text)    wc.to_file("pic.png")# edu_salary()# edu_fenbu()# word_cloud()