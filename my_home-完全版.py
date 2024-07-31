'''我的主页'''
import streamlit as st
from PIL import Image
import wordcloud
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

page = st.sidebar.radio(
    '我的主页', ['我的兴趣推荐', '我的图片处理器', '我的智慧词典', '我的评论区', '我的地图'])


def page_1():
    '''我的兴趣推荐'''
    with open('霞光.mp3', 'rb') as f:
        mymp3 = f.read()
    st.audio(mymp3, format='audio/mp3', start_time=0)
    st.write('我的视频推荐')
    st.write('-----------------------------')
    st.write('我的游戏推荐')
    st.write('巅峰极速')
    st.write('我的名著推荐')
    st.write('<<简爱>>')
    st.write('我的试卷推荐')
    st.write('-----------------------------')


def page_2():
    '''我的图片处理器'''
    st.write(":sunglasses:图片处理器:sunglasses:")
    uploaded_file = st.file_uploader("上传图片", type=['png', 'jpeg', 'jpg'])
    if uploaded_file:
        # 获取图片文件的名称、类型和大小
        file_name = uploaded_file.name
        file_type = uploaded_file.type
        file_size = uploaded_file.size
        img = Image.open(uploaded_file)
        st.image(img)
        st.image(img_change(img, 0, 2, 1))
    st.write('-----------------------------')
    st.write(':orange[词云生成小工具]')
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # 将上传的文件转换成文本
        string_data = uploaded_file.read().decode("utf-8")
        st.image(ciyvn(string_data))
    else:
        pass


def page_3():
    '''我的智能词典'''
    st.write('智能词典')
    # 从本地文件中将词典信息读取出来，并存储在列表中
    with open('words_space.txt', 'r', encoding='utf-8') as f:
        words_list = f.read().split('\n')
    # 将列表中的每一项内容再进行分割，分为“编号、单词、解释”
    for i in range(len(words_list)):
        words_list[i] = words_list[i].split('#')
    # 将列表中的内容导入字典，方便查询，格式为“单词：编号、解释”
    words_dict = {}
    for i in words_list:
        words_dict[i[1]] = [int(i[0]), i[2]]
    # 从本地文件中将单词的查询次数读取出来，并存储在列表中
    with open('check_out_times.txt', 'r', encoding='utf-8') as f:
        times_list = f.read().split('\n')
    # 将列表转为字典
    for i in range(len(times_list)):
        times_list[i] = times_list[i].split('#')
    times_dict = {}
    for i in times_list:
        times_dict[int(i[0])] = int(i[1])
    # 创建输入框
    word = st.text_input('请输入要查询的单词')
    # 显示查询内容
    if word in words_dict:
        st.write(words_dict[word])
        n = words_dict[word][0]
        if n in times_dict:
            times_dict[n] += 1
        else:
            times_dict[n] = 1
        with open('check_out_times.txt', 'w', encoding='utf-8') as f:
            message = ''
            for k, v in times_dict.items():
                message += str(k) + '#' + str(v) + '\n'
            message = message[:-1]
            f.write(message)
        st.write('查询次数：', times_dict[n])
        if word == 'python':
            st.code('''
                    # 恭喜你触发彩蛋，这是一行python代码
                    print('hello world')''')


def page_4():
    '''我的留言区'''
    st.write('我的留言区')
    # 从文件中加载内容，并处理成列表
    with open('leave_messages.txt', 'r', encoding='utf-8') as f:
        messages_list = f.read().split('\n')
    for i in range(len(messages_list)):
        messages_list[i] = messages_list[i].split('#')
    name = st.selectbox('我是……', ['阿短', '编程猫', '梁壹'])
    new_message = st.text_input('想要说的话……')
    if st.button('留言'):
        messages_list.append(
            [str(int(messages_list[-1][0])+1), name, new_message])
        with open('leave_messages.txt', 'w', encoding='utf-8') as f:
            message = ''
            for i in messages_list:
                message += i[0] + '#' + i[1] + '#' + i[2] + '\n'
            message = message[:-1]
            f.write(message)
    for i in messages_list:
        if i[1] == '阿短':
            with st.chat_message('🌞'):
                st.text(i[1])
                st.text(i[2])
        elif i[1] == '梁壹':
            with st.chat_message('🌝'):
                st.write(i[1], ':', i[2])
        elif i[1] == '编程猫':
            with st.chat_message('🍥'):
                st.text(i[1])
                st.text(i[2])


def page_5():
    data = {
        'latitude': [37.7749, 34.0522, 40.7128],
        'longitude': [-122.4194, -118.2437, -74.0060],
        'name': ['San Francisco', 'Los Angeles', 'New York']
    }

    st.map(data, zoom=4, use_container_width=True)


def img_change(img, rc, gc, bc):
    '''图片处理'''
    width, height = img.size
    img_array = img.load()
    for x in range(width):
        for y in range(height):
            # 获取RGB值
            r = img_array[x, y][rc]
            g = img_array[x, y][gc]
            b = img_array[x, y][bc]
            img_array[x, y] = (r, g, b)
    return img


def ciyvn(str):
    img_codemao = np.array(Image.open('codemao.png'))
    w = wordcloud.WordCloud(mask=img_codemao, font_path='fangzheng.TTF',
                            background_color='white', max_words=2000, width=2000, height=2000)
    w.generate(str)
    image_colors = wordcloud.ImageColorGenerator(image=img_codemao)
    w.recolor(color_func=image_colors)
    w.to_file('shortstory.png')
    img = Image.open('shortstory.png')
    return img


if page == '我的兴趣推荐':
    page_1()
elif page == '我的图片处理器':
    page_2()
elif page == '我的智慧词典':
    page_3()
elif page == '我的评论区':
    page_4()
elif page == '我的地图':
    page_5()
