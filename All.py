#!/usr/bin/python
# -*- coding:utf-8 -*-

from numpy import *
import numpy as np
from os import listdir
import os
import pandas as pd
import requests
from os import listdir

# save txt files from Internet into source folder
data = pd.read_csv('middle_sample.csv')
os.mkdir('source')

urls = 'https://www.sec.gov/Archives/' + data['index']

for num, url in enumerate(urls):
    if url[-4:] == '.txt':
        text = requests.get(url).text

        fileName = ''
        for j in range(6):
            fileName += str(data.iloc[num][j]) + '-'
        fileName = 'source/' + fileName[:-1] + '.txt'
        file = open(fileName, 'w')
        file.write(text)
        file.close()


def my_find(fileName, keyword):
    text = open('source/' + fileName).read()
    keyword_len = len(keyword)
    index_keyword = []

    for i in range(int(len(text) / keyword_len)):
        if text.find(keyword) != -1:
            index_str = text.find(keyword)
            index_keyword.append(index_str)
            text = text[index_str + keyword_len:]

    index_keyword_len = len(index_keyword)

    if index_keyword_len == 0:
        print('no keyword found'.format(fileName))
    else:
        new_index_keyword = zeros(index_keyword_len)



        for i in range(index_keyword_len):
            if i == 0:
                new_index_keyword[i] = index_keyword[i]
            else:
                new_index_keyword[i] = index_keyword[i] + index_keyword[i - 1] + keyword_len
        index_keyword = []

    # change float type to int

        for i in range(len(new_index_keyword)):
            index_keyword.append(int(new_index_keyword[i]))

    return index_keyword

# Into lower case
def table_find(fileName, keyword):
    text = open('source/' + fileName).read()
    text = text.lower()
    keyword_len = len(keyword)
    index_keyword = []
    for i in range(int(len(text) / keyword_len)):
        if text.find(keyword) != -1:
            index_str = text.find(keyword)
            index_keyword.append(index_str)
            text = text[index_str + keyword_len:]

    index_keyword_len = len(index_keyword)
    if index_keyword_len == 0:
        print('No table of content'.format(fileName))
    else:
        new_index_keyword = zeros(index_keyword_len)
        out = zeros(index_keyword_len)

        for i in range(index_keyword_len):
            new_index_keyword[i] = index_keyword[i]

        for i in range(len(new_index_keyword)):
            out[i] = sum(new_index_keyword[:i + 1]) + keyword_len * (i)

        index_keyword = []

        for i in range(len(out)):
            index_keyword.append(int(out[i]))

    return index_keyword


# main extract txt

def main():
    os.mkdir('result')      # output files folder
    keyword = 'LETTER OF CREDIT AND REIMBURSEMENT AGREEMENT'
    table = 'Table of Contents'.lower()

    for fileName in listdir('source'):
        text = open('source/' + fileName).read()

        final_Keyword = 0;
        final_Table = 0;
        temp_distance = np.inf;

        index_Keyword = my_find(fileName, keyword=keyword)
        index_Table = table_find(fileName, keyword=table)

        if len(index_Keyword) != 0 and len(index_Table) != 0:
            for k_1 in range(len(index_Keyword)):
                for k_2 in range(len(index_Table)):
                    distance = index_Table[k_2] - index_Keyword[k_1]
                    if distance > 0:  # if table comes after keywords
                        if distance < temp_distance:
                            final_Keyword = index_Keyword[k_1]
                            final_table = index_Table[k_2]
                            temp_distance = distance

            text2 = text[final_Keyword:]
            fid = open('result/' + fileName, 'w')
            fid.write(text2)
            fid.close()

if __name__ == "__main__" :
    main()
    os.mkdir('finally')      # creat Finally folder to save outcome which meets the criteria

    keyword_pre = 'CREDIT AGREEMENT'.lower()
    keyword_suf = 'LOAN AGREEMENT'.lower()
    keyword_pre_len = len(keyword_pre)
    keyword_suf_len = len(keyword_suf)

    item = 'table of content'

    for file in listdir('./testfile/'):
        text_list = []
        with open('./testfile/' + file) as fr:
            for line in fr.readlines():
                text_list.append(line.lower())
            for i, line in enumerate(text_list):
                if keyword_pre in text_list[i]:
                    for j, letter in enumerate(text_list):
                        if item in text_list[j] and 0 <= j - i <= 12:
                            ind = text_list[i].find(keyword_pre)
                            text_list = []
                            with open('./testfile/' + file) as f:
                                for li in f.readlines():
                                    text_list.append(li)
                                text_list[i] = text_list[i][ind + keyword_pre_len:]
                                new_txt = ''.join(text_list[i:])
                                fid = open('./finally/' + file, 'w')
                                fid.write(new_txt)
                                break

    for file in listdir('./testfile/'):
        text_list = []
        with open('./testfile/' + file) as fr:
            for line in fr.readlines():
                text_list.append(line.lower())
            for i, line in enumerate(text_list):
                if keyword_suf in text_list[i]:
                    for j, letter in enumerate(text_list):
                        if item in text_list[j] and 0 <= j - i <= 12:
                            ind = text_list[i].find(keyword_suf)
                            text_list = []
                            with open('./testfile/' + file) as f:
                                for li in f.readlines():
                                    text_list.append(li)
                                text_list[i] = text_list[i][ind + keyword_suf_len:]
                                new_txt = ''.join(text_list[i:])
                                fid = open('./result/' + file, 'w')
                                fid.write(new_txt)
                                break

