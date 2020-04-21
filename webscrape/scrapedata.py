#coding:utf-8
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests
import time


race_data_columns=[
    'race_id',
    'race_round',
    'race_title',
    'race_course',
    'weather',
    'ground_status',
    'time',
    'date',
    'where_racecourse',
    'total_horse_number',
    'frame_number_first',
    'horse_number_first',
    'frame_number_second',
    'horse_number_second',
    'frame_number_third',
    'horse_number_third',
    'tansyo',
    'hukusyo_first',
    'hukusyo_second',
    'hukusyo_third',
    'wakuren',
    'umaren',
    'wide_1_2',
    'wide_1_3',
    'wide_2_3',
    'umatan',
    'renhuku3',
    'rentan3'
    ]

horse_data_columns=[
    'race_id',
    'rank',
    'frame_number',
    'horse_number',
    'horse_id',
    'sex_and_age',
    'burden_weight',
    'rider_id',
    'goal_time',
    'goal_time_dif',
    'time_value',
    'half_way_rank',
    'last_time',
    'odds',
    'popular',
    'horse_weight',
    'tame_time',
    'tamer_id',
    'owner_id'
]


def scrape_race_and_horse_data_by_html(race_id, html):
    race_list = [race_id]
    horse_list_list = []
    soup = BeautifulSoup(html, 'html.parser')
    #####################
    # race_data
    #####################
    data_intro = soup.find("div", class_="data_intro")
    
    race_list.append(data_intro.find("dt").get_text().strip("\n")) # race_round
    race_list.append(data_intro.find("h1").get_text().strip("\n")) # race_title

    race_details1 = data_intro.find("p").get_text().strip("\n").split("\xa0/\xa0")
    race_list.append(race_details1[0]) # race_course
    race_list.append(race_details1[1]) # weather
    race_list.append(race_details1[2]) # ground_status
    race_list.append(race_details1[3][5:10]) # time

    race_details2 = data_intro.find("p", class_="smalltxt").get_text().strip("\n").split(" ")
    race_list.append(race_details2[0]) # date
    race_list.append(race_details2[1]) # where_racecourse


    result_rows = soup.find("table", class_="race_table_01 nk_tb_common").findAll('tr') 
    race_list.append(len(result_rows)-1) # total_horse_number
    for i in range(1,4):
        row = result_rows[i].findAll('td')
        race_list.append(row[1].get_text()) # frame_number_first or second or third
        race_list.append(row[2].get_text()) # horse_number_first or second or third


    pay_back_tables = soup.findAll("table", class_="pay_table_01")

    pay_back1 = pay_back_tables[0].findAll('tr')
    race_list.append(pay_back1[0].find("td", class_="txt_r").get_text()) #tansyo
    hukuren = pay_back1[1].find("td", class_="txt_r")
    tmp = []
    for string in hukuren.strings:
        tmp.append(string)
    for i in range(3):
        try:
            race_list.append(tmp[i]) # hukuren_first or second or third
        except IndexError:
            race_list.append("0")
    try:
        race_list.append(pay_back1[2].find("td", class_="txt_r").get_text())
    except IndexError:
        race_list.append("0")

    try:
        race_list.append(pay_back1[3].find("td", class_="txt_r").get_text())
    except IndexError:
        race_list.append("0")



    pay_back2 = pay_back_tables[1].findAll('tr')
    # wide 1&2
    wide = pay_back2[0].find("td", class_="txt_r")
    tmp = []
    for string in wide.strings:
        tmp.append(string)
    for i in range(3):
        try:
            race_list.append(tmp[i]) # hukuren_first or second or third
        except IndexError:
            race_list.append("0")

    # umatan
    race_list.append(pay_back2[1].find("td", class_="txt_r").get_text()) #umatan

    race_list.append(pay_back2[2].find("td", class_="txt_r").get_text()) #renhuku3
    try:
        race_list.append(pay_back2[3].find("td", class_="txt_r").get_text()) #rentan3
    except IndexError:
        race_list.append("0")
    ####################
    # horse data
    ####################
    for rank in range(1, len(result_rows)):
        horse_list = [race_id]
        result_row = result_rows[rank].findAll("td")
        # rank
        horse_list.append(result_row[0].get_text().strip())
        # frame_number
        horse_list.append(result_row[1].get_text().strip())
        # horse_number
        horse_list.append(result_row[2].get_text().strip())
        # horse_id
        horse_list.append(result_row[3].find('a').get('href').split("/")[-2].strip())
        # sex_and_age
        horse_list.append(result_row[4].get_text().strip())
        # burden_weight
        horse_list.append(result_row[5].get_text().strip())
        # rider_id
        horse_list.append(result_row[6].find('a').get('href').split("/")[-2].strip())
        # goal_time
        horse_list.append(result_row[7].get_text().strip())
        # goal_time_dif
        horse_list.append(result_row[8].get_text().strip())
        # time_value(premium)
        horse_list.append(result_row[9].get_text().strip())
        # half_way_rank
        horse_list.append(result_row[10].get_text().strip())
        # last_time
        horse_list.append(result_row[11].get_text().strip())
        # odds
        horse_list.append(result_row[12].get_text().strip())
        # popular
        horse_list.append(result_row[13].get_text().strip())
        # horse_weight
        horse_list.append(result_row[14].get_text().strip())
        # tame_time(premium)
        horse_list.append(result_row[15].get_text().strip())
        # tamer_id
        horse_list.append(result_row[18].find('a').get('href').split("/")[-2].strip())
        # owner_id
        horse_list.append(result_row[19].find('a').get('href').split("/")[-2].strip())

        horse_list_list.append(horse_list)

    return race_list, horse_list_list

def request_html(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    html = response.text
    time.sleep(1)
    return html

def create_csv(year, mon, urls):
    CSV_DIR = "csv/"+str(year)
    if not os.path.isdir(CSV_DIR):
        os.makedirs(CSV_DIR)
    save_race_csv = CSV_DIR+"/race_"+str(mon)+".csv"
    horse_race_csv = CSV_DIR+"/horse_"+str(mon)+".csv"
    time.sleep(2)
    race_df = pd.DataFrame(columns=race_data_columns )
    horse_df = pd.DataFrame(columns=horse_data_columns )

    count = 0

    for url in urls:
        print(url)
        list = url.split("/")
        race_id = list[-2]
        
        html = request_html(url)
        race_list, horse_list_list = scrape_race_and_horse_data_by_html(race_id, html)
        #horse_data
        for horse_list in horse_list_list:
            horse_se = pd.Series(horse_list, index=horse_df.columns)
            horse_df = horse_df.append(horse_se, ignore_index=True)
        #race_data
        race_se = pd.Series(race_list, index=race_df.columns )
        race_df = race_df.append(race_se, ignore_index=True )

        #250Ç≤Ç∆Ç…ÉfÅ[É^ÇCSVÇ…ïœä∑ÇµÇƒÇ®Ç≠
        if count == 250:
            count = 0
            race_df.to_csv(save_race_csv, header=True, index=False)
            horse_df.to_csv(horse_race_csv, header=True, index=False)

        

    race_df.to_csv(save_race_csv, header=True, index=False)
    horse_df.to_csv(horse_race_csv, header=True, index=False)
