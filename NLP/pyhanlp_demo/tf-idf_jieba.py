'''
    tf-idf
'''
# from jieba import analyse
#
#
# def jieba_tfidf(text):
#
#     # jiba自带的idf词频文件（xxxxx\Lib\site-packages\jieba\analyse\idf.txt）
#     tfidf = analyse.extract_tags
#
#     keywords = tfidf(text)
#     print(keywords)
#
#     '''
#         ['TF', '短语', '文章', 'IDF', '此词', '类别', '出现', '一篇', '某个', '区分', '频率', '适合', '分类', '用来', '很少', '思想', '并且', '或者', '能力', '具有']
#     '''
#
#
# if __name__ == '__main__':
#     text = '''
#             TF-IDF的主要思想是：如果某个词或短语在一篇文章中出现的频率TF高，并且在其他文章中很少出现，则认为此词或者短语具有很好的类别区分能力，适合用来分类
#     '''
#
#     jieba_tfidf(text)





# ===================================================================================================

'''
    textrank
'''
from jieba import analyse

def jieba_textrank(text):
    textrank = analyse.textrank  # 引入jieba中的TextRank
    keywords = textrank(text, 5)
    print(keywords)

if __name__ == '__main__':
    text = """
        
    """

    jieba_textrank(text)