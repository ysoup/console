#!/user/bin/python
# -*- coding:utf-8 -*-

import nltk
import numpy
import jieba
import codecs
import re

N = 50  # 单词数量
CLUSTER_THRESHOLD = 8  # 单词间的距离
TOP_SENTENCES = 4  # 返回的top n句子


# 分句
def sent_tokenizer(texts):
    line_break = re.compile('[\r\n]')
    sentences = []
    punt_list = u'?!。？！～【】'

    for line in line_break.split(texts):
        line = line.strip()
        if not line:
            continue

        start = 0
        i = 0  # 每个字符的位置
        token = ''
        for text in line:
            if text in punt_list and token not in punt_list:  # 检查标点符号下一个字符是否还是标点
                sentences.append(line[start:i + 1])  # 当前标点符号位置
                start = i + 1  # start标记到下一句的开头
                i += 1
            else:
                i += 1  # 若不是标点符号，则字符位置继续前移
                token = list(line[start:i + 2]).pop()  # 取下一个字符
        if start < len(line):
            sentences.append(line[start:])  # 这是为了处理文本末尾没有标点符号的情况
    return sentences


# 停用词
def load_stopwordslist(path):
    # print('load stopwords...')
    stoplist = [line.strip() for line in codecs.open(path, 'r', encoding='utf8').readlines()]
    stopwrods = {}.fromkeys(stoplist)
    return stopwrods


# 摘要
def summarize(text):
    stopwords = load_stopwordslist('./stopwords.txt')
    sentences = sent_tokenizer(text)

    words = [w for sentence in sentences for w in jieba.cut_for_search(sentence) if w not in stopwords if
             len(w) > 1 and w != '\t']

    wordfre = nltk.FreqDist(words)
    topn_words = [w[0] for w in sorted(wordfre.items(), key=lambda d: d[1], reverse=True)][:N]
    scored_sentences = _score_sentences(sentences, topn_words)
    # approach 1,利用均值和标准差过滤非重要句子
    # 均值
    avg = numpy.mean([s[1] for s in scored_sentences])
    # 标准差
    std = numpy.std([s[1] for s in scored_sentences])
    mean_scored = [(sent_idx, score) for (sent_idx, score) in scored_sentences if score > (avg + 0.5 * std)]
    # approach 2，返回top n句子
    top_n_scored = sorted(scored_sentences, key=lambda s: s[1])[-TOP_SENTENCES:]
    top_n_scored = sorted(top_n_scored, key=lambda s: s[0])

    return dict(top_n_summary=[sentences[idx] for (idx, score) in top_n_scored],
                mean_scored_summary=[sentences[idx] for (idx, score) in mean_scored])


# 句子得分
def _score_sentences(sentences, topn_words):
    scores = []
    sentence_idx = -1
    for s in [list(jieba.cut_for_search(s)) for s in sentences]:
        sentence_idx += 1
        word_idx = []
        for w in topn_words:
            try:
                # 关键词出现在该句子中的索引位置
                word_idx.append(s.index(w))
            except ValueError:  # w不在句子中
                pass
        word_idx.sort()
        if len(word_idx) == 0:
            continue
        # 对于两个连续的单词，利用单词位置索引，通过距离阀值计算族
        clusters = []
        cluster = [word_idx[0]]
        i = 1
        while i < len(word_idx):
            if word_idx[i] - word_idx[i - 1] < CLUSTER_THRESHOLD:
                cluster.append(word_idx[i])
            else:
                clusters.append(cluster[:])
                cluster = [word_idx[i]]
            i += 1
        clusters.append(cluster)
        # 对每个族打分，每个族类的最大分数是对句子的打分
        max_cluster_score = 0
        for c in clusters:
            significant_words_in_cluster = len(c)
            total_words_in_cluster = c[-1] - c[0] + 1
            score = 1.0 * significant_words_in_cluster * significant_words_in_cluster / total_words_in_cluster
            if score > max_cluster_score:
                max_cluster_score = score
        # 去除标题
        if sentence_idx > 0:
            scores.append((sentence_idx, max_cluster_score))
    return scores


def get_summary_topn_words(summary_text, top_n=20):
    summary_sentences = sent_tokenizer(summary_text)
    stopwords = load_stopwordslist('./stopwords.txt')
    summary_words = [w for sentence in summary_sentences for w in jieba.cut(sentence) if w not in stopwords if
                     len(w) > 1 and w != '\t']
    summary_wordfre = nltk.FreqDist(summary_words)
    summary_topn_words = [w[0] for w in sorted(summary_wordfre.items(), key=lambda d: d[1], reverse=True)][:top_n]
    return summary_topn_words


def get_category(text, category_keywords_list):
    category_list = []
    for category_keywords in category_keywords_list:
        keywords = []
        category_keywords_detail = re.split(',|，', category_keywords['keyword'])
        for w in category_keywords_detail:
            word = {}
            count = text.count(w)
            word["word"] = w
            word["count"] = count  # / float(len(cotent))
            if count > 0:
                keywords.append(word)
        if keywords:
            keywords.sort(key=lambda x: x["count"], reverse=True)
            category = {}
            category['id'] = category_keywords['id']
            category['list'] = keywords
            category_list.append(category)

    return category_list[0]['id'] if category_list else 0


if __name__ == '__main__':
    text = (

        u'''
       【蚂蚁金服副总裁蒋国飞：区块链是比AI影响更为广泛的技术】在两年的时间里，区块链技术成为没人能忽略的技术浪潮，阿里作为中国技术巨头之一，也投身其中。蚂蚁金服副总裁、技术实验室负责人蒋国飞认为，区块链技术是更为底层的技术变革。它最大的逻辑自信是能够让多方达成互信，而正是因为这是一个需要多方参与的过程。技术的落地是缓慢——等待所有的参与者看到区块链的明亮面，并且达成共识，而正是因为多方参与，它的影响又是深远的。相比之前的AI技术，蒋国飞认为区块链的影响更为广泛，也更为公平和开放，大小公司都能在其中找到自己的位置和机会。

       ''')
    title = u'韩国财长金东渊：没有关停数字货币交易所的计划”'

    content = u''.join(text)
    top = get_summary_topn_words(content)
    print(u'\r\n'.join(top))
    content = title + u'\r\n' + content
    dict = summarize(content)
    # print ''.join(dict['top_n_summary'])
    print('-----------approach 1-------------')
    for sent in dict['mean_scored_summary']:
        print(sent)
    print('-----------approach 2-------------')
    for sent in dict['top_n_summary']:
        print(sent)