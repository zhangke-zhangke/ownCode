from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import PIL.Image as image
import cv2


def get_wordcloud(class_words):
    for target,words in class_words.items():
        # 把列表里多个字符串合并成一个
        str_words = ''
        for w in words:
            str_words += w
        # print(f"类别{target}，词：{str_words}")

        # 词云模板
        # mask = np.array(image.open(r"C:\Users\dell\Desktop\QQ图片20210628205023.jpg"))
        wordcloud = WordCloud(font_path='C:\Windows\Fonts\AdobeHeitiStd-Regular.otf').generate(str_words)

        # # 展示图片
        # image_produce = wordcloud.to_image()
        # image_produce.show()

        # 保存词云图片
        wordcloud.to_file(fr'D:\Gitlab\extract_key\word_cloud_img\words_cloud_class{target}.jpg')


def load_data():
    data = pd.read_csv('result_20220629.csv',sep=',')
    data = data[['class', 'cut_words']]

    class_words = {}
    for key, value in data.groupby('class'):
        class_words[key] = value['cut_words'].tolist()


    return class_words


if __name__ == '__main__':
    class_words = load_data()
    get_wordcloud(class_words)