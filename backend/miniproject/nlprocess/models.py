from django.db import models
import tqdm
from miniproject.common.models import Reader, FileDTO, Printer
from icecream import ic
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import nltk
from konlpy.tag import Okt
import platform
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import urllib.parse
import time


class NLService(Reader):

    def __init__(self):
        self.f = FileDTO()
        self.r = Reader()
        self.p = Printer()

    def show_alice(self):
        f = self.f
        r = self.r
        p = self.p
        f.context = './data/'
        f.fname = '09. alice.txt'
        text = r.txt(f)
        f.fname = '09. alice_mask.png'
        alice_mask = r.img(f)
        # ic(text)
        # ic(type(alice_mask))

        stopwords = set(STOPWORDS)
        stopwords.add("said")

        path = "c:/Windows/Fonts/Arial.ttf"
        if platform.system() == 'Darwin':
            rc('font', family='AppleGothic')
        elif platform.system() == 'Windows':
            font_name = font_manager.FontProperties(fname=path).get_name()
            rc('font', family=font_name)
        else:
            print('Unknown system... sorry~~~~')

        plt.figure(figsize=(8, 8))  # 최초 창의 크기를 설정
        plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')
        plt.axis('off')
        # plt.show()

        wc = WordCloud(background_color='white', max_words=2000, mask=alice_mask,
                       stopwords=stopwords)
        wc = wc.generate(text)
        # ic(wc.words_)
        plt.figure(figsize=(12, 12))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.show()

    def show_present(self):

        f = self.f
        r = self.r
        p = self.p
        f.context = './data/'
        path = "c:/Windows/Fonts/malgun.ttf"

        if platform.system() == 'Darwin':
            rc('font', family='AppleGothic')
        elif platform.system() == 'Windows':
            font_name = font_manager.FontProperties(fname=path).get_name()
            rc('font', family=font_name)
        else:
            print('Unknown system... sorry~~~~')

        plt.rcParams['axes.unicode_minus'] = False

        tmp1 = 'https://search.naver.com/search.naver?where=kin'
        html = tmp1 + '&sm=tab_jum&ie=utf8&query={key_word}&start={num}'

        response = urlopen(html.format(num=1, key_word=urllib.parse.quote('여친 선물')))
        # ic(response)
        soup = BeautifulSoup(response, "html.parser")
        # ic(soup)
        tmp = soup.find_all('strong')
        # ic(tmp)
        tmp_list = []
        for line in tmp:
            tmp_list.append(line.text)
        # ic(tmp_list)

        present_candi_text = []
        for n in tqdm.tqdm(range(1, 1000, 10)):
            response = urlopen(html.format(num=n, key_word=urllib.parse.quote('여자 친구 선물')))
            soup = BeautifulSoup(response, "html.parser")
            tmp = soup.find_all('strong')
            for line in tmp:
                present_candi_text.append(line.text)
            time.sleep(0.5)
        # ic(present_candi_text)

        t = Okt()
        present_text = ''
        for each_line in present_candi_text[:10000]:
            present_text = present_text + each_line + '\n'

        tokens_ko = t.morphs(present_text)
        # ic(tokens_ko)

        ko = nltk.Text(tokens_ko, name='여자 친구 선물')
        ic(len(ko.tokens))
        ic(len(set(ko.tokens)))
        ko.vocab().most_common(100)

        plt.figure(figsize=(15, 6))
        ko.plot(50)
        plt.show()

        data = ko.vocab().most_common(300)
        # for win : font_path='c:/Windows/Fonts/malgun.ttf'
        # /Library/Fonts/AppleGothic.ttf
        wordcloud = WordCloud(font_path=path,
                              relative_scaling=0.2,
                              # stopwords=STOPWORDS,
                              background_color='white',
                              ).generate_from_frequencies(dict(data))
        plt.figure(figsize=(16, 8))
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()

        f.fname = '09. heart.jpg'
        mask = r.img(f)
        image_colors = ImageColorGenerator(mask)
        data = ko.vocab().most_common(200)

        # for win : font_path='c:/Windows/Fonts/malgun.ttf'
        # /Library/Fonts/AppleGothic.ttf
        wordcloud = WordCloud(font_path=path,
                              relative_scaling=0.1, mask=mask,
                              background_color='white',
                              min_font_size=1,
                              max_font_size=100).generate_from_frequencies(dict(data))

        default_colors = wordcloud.to_array()
        plt.figure(figsize=(12, 12))
        plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
        plt.axis('off')
        plt.show()


if __name__ == '__main__':
    nls = NLService()
    nls.show_alice()
    nls.show_present()


