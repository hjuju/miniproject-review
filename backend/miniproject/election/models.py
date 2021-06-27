from django.db import models

import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from django.db import models
import numpy as np
import folium
import json
import warnings
from miniproject.common.models import FileDTO, Printer, Reader

class Election_19th(Reader):

    def __init__(self):
        self.f = FileDTO()
        self.r = Reader()
        self.p = Printer()
        self.BORDER_LINES = [
            [(5, 1), (5,2), (7,2), (7,3), (11,3), (11,0)], # 인천
            [(5,4), (5,5), (2,5), (2,7), (4,7), (4,9), (7,9),
             (7,7), (9,7), (9,5), (10,5), (10,4), (5,4)], # 서울
            [(1,7), (1,8), (3,8), (3,10), (10,10), (10,7),
             (12,7), (12,6), (11,6), (11,5), (12, 5), (12,4),
             (11,4), (11,3)], # 경기도
            [(8,10), (8,11), (6,11), (6,12)], # 강원도
            [(12,5), (13,5), (13,4), (14,4), (14,5), (15,5),
             (15,4), (16,4), (16,2)], # 충청북도
            [(16,4), (17,4), (17,5), (16,5), (16,6), (19,6),
             (19,5), (20,5), (20,4), (21,4), (21,3), (19,3), (19,1)], # 전라북도
            [(13,5), (13,6), (16,6)], # 대전시
            [(13,5), (14,5)], #세종시
            [(21,2), (21,3), (22,3), (22,4), (24,4), (24,2), (21,2)], #광주
            [(20,5), (21,5), (21,6), (23,6)], #전라남도
            [(10,8), (12,8), (12,9), (14,9), (14,8), (16,8), (16,6)], #충청북도
            [(14,9), (14,11), (14,12), (13,12), (13,13)], #경상북도
            [(15,8), (17,8), (17,10), (16,10), (16,11), (14,11)], #대구
            [(17,9), (18,9), (18,8), (19,8), (19,9), (20,9), (20,10), (21,10)], #부산
            [(16,11), (16,13)], #울산
            [(27,5), (27,6), (25,6)],]

    def draw_data(self, tar_dara, campname):
        f = self.f
        r = self.r
        BORDER_LINES = self.BORDER_LINES
        f.context = './data_saved/'
        f.fname = 'final_elect_data'
        elec = r.csv(f)
        gamma = 0.75
        whitelabelmin = 20.
        datalabel = tar_dara
        tmp_max = max([np.abs(min(elec[tar_dara])),
                       np.abs(max(elec[tar_dara]))])
        vmin, vmax = -tmp_max, tmp_max
        mapdata = elec.pivot_table(index='y', columns='x', values=tar_dara)
        masked_mapdata = np.ma.masked_where(np.isnan(mapdata), mapdata)
        font_path = 'C:/Windows/Fonts/Arial.ttf'
        font_name = font_manager.FontProperties(fname=font_path).get_name()
        plt.rc('font', family=font_name)
        plt.rcParams['axes.unicode_minus'] = False
        plt.figure(figsize=(9, 11))
        plt.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=campname,
                   edgecolor='#aaaaaa', linewidth=0.5)
        # 지역 이름 표시
        for idx, row in elec.iterrows():
            # 광역시는 구 이름이 겹치는 경우가 많아서 시단위 이름도 같이 표시
            # (중구, 서구)
            if len(row['ID'].split()) == 2:
                dispname = '{}\n{}'.format(row['ID'].split()[0], row['ID'].split()[1])
            elif row['ID'][:2] == '고성':
                dispname = '고성'
            else:
                dispname = row['ID']
            # 서대문구, 서귀포시 같이 이름이 3자 이상인 경우에 작은 글자로 표시
            if len(dispname.splitlines()[-1]) >= 3:
                fontsize, linespacing = 10.0, 1.1
            else:
                fontsize, linespacing = 11, 1.
            annocolor = 'white' if np.abs(row[tar_dara]) > whitelabelmin else 'black'
            plt.annotate(dispname, (row['x'] + 0.5, row['y'] + 0.5), weight='bold',
                         fontsize=fontsize, ha='center', va='center', color=annocolor,
                         linespacing=linespacing)
        # 시도 경계
        for path in BORDER_LINES:
            ys, xs = zip(*path)
            plt.plot(xs, ys, c='black', lw=2)

        plt.gca().invert_yaxis()
        plt.axis('off')
        cb = plt.colorbar(shrink=.1, aspect=10)
        cb.set_label(datalabel)
        plt.tight_layout()
        plt.show()

    def folium_map(self, tar_data):
        f = self.f
        r = self.r
        f.context = './data_saved/'
        f.fname = 'final_elect_data'
        elec = r.csv(f)
        warnings.simplefilter(action='ignore', category=FutureWarning)
        pop_folium = elec.set_index('ID')
        del pop_folium['광역시도']
        del pop_folium['시군']
        pop_folium.head()
        geo_path = './data_saved/05. skorea_municipalities_geo_simple.json'
        geo_str = json.load(open(geo_path, encoding='utf-8'))
        map = folium.Map(location=[36.2002, 127.054], zoom_start=6)
        map.choropleth(geo_data=geo_str,
                       data=pop_folium[tar_data],
                       columns=[pop_folium.index, pop_folium[tar_data]],
                       fill_color='YlGnBu',  # PuRd, YlGnBu
                       key_on='feature.id')
        map.save(f'./data_saved/election_{tar_data}.html')


    @staticmethod
    def main():
        e = Election_19th()
        while 1:
            m = input('0. break\n'
                      '1. moon_vs_hong\n'
                      '2. moon_vs_ahn\n'
                      '3. ahn_vs_hong\n'
                      '4. folium n.1\n'
                      '5. folium n.2\n'
                      '6. folium n.3\n')
            if m == '0':
                break
            elif m == '1':
                e.draw_data('moon_vs_hong', 'RdBu')
            elif m == '2':
                e.draw_data('moon_vs_ahn', 'RdBu')
            elif m == '3':
                e.draw_data('ahn_vs_hong', 'RdBu')
            elif m == '4':
                e.folium_map('moon_vs_hong')
            elif m == '5':
                e.folium_map('moon_vs_ahn')
            elif m == '6':
                e.folium_map('ahn_vs_hong')
            else:
                continue

Election_19th.main()

'''
if __name__ == '__main__':
    e = Election_19th()
    e.draw_data('moon_vs_hong', 'RdBu')
'''
