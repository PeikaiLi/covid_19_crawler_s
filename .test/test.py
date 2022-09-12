from bs4 import BeautifulSoup
import re
import json




with open('onepage.html',encoding='utf-8') as f:
    r = f.read()
    

import datetime 

_today = datetime.datetime.now().strftime('%m/%d/%Y')



#   
soup = BeautifulSoup(r, 'lxml')

###########################################################################################
### overall_information

str(soup.find('script', attrs={'id': 'getStatisticsService'}))
overall_information = re.search(r'(\{"id".*\})\}', str(soup.find('script', attrs={'id': 'getStatisticsService'})))
#  .*     贪婪匹配,  尽可能多的去匹配结果
# {"id" 开始贪婪匹配 到 两个}} 结尾
# overall_information.group() # 运行本行可见
# 1. 正则表达式中的三组括号把匹配结果分成三组
#    group()  同 group(0) 就是匹配正则表达式整体结果
#    group(1) 列出第一个括号匹配部分，group(2) 列出第二个括号匹配部分，group(3) 列出第三个括号匹配部分。
#    group(num=0)    匹配的整个表达式的字符串，group() 可以一次输入多个组号，在这种情况下它将返回一个包含那些组所对应值的元组。
#    groups()    返回一个包含所有小组字符串的元组，从 1 到 所含的小组号。
# 2. 没有匹配成功的，re.search（）返回None

def overall_parser(overall_information):
      # .group(0)==group() 表示所有的re结果，.group(1)表目标为第一个
    overall_information = json.loads(overall_information.group(1))
    overall_information.pop('id')
    overall_information.pop('createTime')
    overall_information.pop('modifyTime')
    overall_information.pop('imgUrl')
    overall_information.pop('deleted')
    overall_information['countRemark'] = overall_information['countRemark'].replace(' 疑似', '，疑似').replace(' 治愈', '，治愈').replace(' 死亡', '，死亡').replace(' ', '')
    
    # 去重限定日期

    # if not self.db.find_one(collection='DXYOverall', data=overall_information):
    #     # find_one去重,如果数据库里面找到了这一条完全一样的信息，就停止爬取
    #     overall_information['updateTime'] = self.crawl_timestamp
    #     self.db.insert(collection='DXYOverall', data=overall_information)
        
        
        
###########################################################################################
### area_information    
area_information_test = str(soup.find('script', attrs={'id': 'getAreaStat'}))

with open("script_id_getAreaStat.xml", mode="w", encoding='utf-8') as f:
    f.write(area_information_test)
 

area_information = re.search(r'\[(.*)\]', str(soup.find('script', attrs={'id': 'getAreaStat'})))
# 每一个[] 里面贪婪匹配，变成一个group(i)

def area_parser(area_information):
        area_information = json.loads(area_information.group(0))
        
        with open("area_information.json", mode="w", encoding='utf-8') as json_file:
            json.dump(area_information, json_file, ensure_ascii=False, indent=4)
      
        
        

 
    
    
        for area in area_information:
            area['comment'] = area['comment'].replace(' ', '')

            # Because the cities are given other attributes,
            # this part should not be used when checking the identical document.
            
            # But I think if city information changed 
            # we still should save this difference, 
            # so I comment code about pop('cities')
            # cities_backup = area.pop('cities')
    
            # 去重限定日期
            area['_today'] =_today
            if self.db.find_one(collection='DXYArea_f', data=area):
                continue

            # If this document is not in current database, insert this attribute back to the document.
            # area['cities'] = cities_backup

            area['countryName'] = '中国'
            area['countryEnglishName'] = 'China'
            area['continentName'] = '亚洲'
            area['continentEnglishName'] = 'Asia'
            area['provinceEnglishName'] = city_name_map[area['provinceShortName']]['engName']

            for city in area['cities']:
                if city['cityName'] != '待明确地区':
                    try:
                        city['cityEnglishName'] = city_name_map[area['provinceShortName']]['cities'][city['cityName']]
                    except KeyError:
                        print(area['provinceShortName'], city['cityName'])
                        pass
                else:
                    city['cityEnglishName'] = 'Area not defined'

            area['updateTime'] = self.crawl_timestamp

            self.db.insert(collection='DXYArea', data=area)





###########################################################################################
### area_fetchRecentStatV2  

with open("script_id_fetchRecentStatV2.xml", mode="w", encoding='utf-8') as f:
   f.write(str(soup.find('script', attrs={'id': 'fetchRecentStatV2'})))
    
area_fetchRecentStatV2 = re.search(r'\[(.*)\]', str(soup.find('script', attrs={'id': 'fetchRecentStatV2'})))

# if area_fetchRecentStatV2:
#    self.area_fetch_parser(area_fetchRecentStatV2=area_fetchRecentStatV2)
def area_fetch_parser(area_fetchRecentStatV2):
        """
        无症状感染者
    
        Parameters
        ----------
        area_information : TYPE
            DESCRIPTION.
    
        Returns
        -------
        None.
    
        """
        area_information = json.loads(area_fetchRecentStatV2.group(0))
        
        with open("area_information_fetch.json", mode="w", encoding='utf-8') as json_file:
            json.dump(area_information, json_file, ensure_ascii=False, indent=4)
            
            
        for area in area_information:
            # 遍历所有地区
            
            # Because the cities are given other attributes,
            # this part should not be used when checking the identical document.
            
            # But I think if city information changed 
            # we still should save this difference, 
            # so I comment code about pop('cities')
            # cities_backup = area.pop('cities')
    
            # 去重限定日期
            area['_today'] = _today
            if self.db.find_one(collection='DXYArea_f', data=area):
                continue
    
            # If this document is not in current database, insert this attribute back to the document.
            # area['cities'] = cities_backup
    
            area['countryName'] = '中国'
            area['countryEnglishName'] = 'China'
            area['continentName'] = '亚洲'
            area['continentEnglishName'] = 'Asia'
            area['provinceEnglishName'] = city_name_map[area['provinceShortName']]['engName']
    
            for city in area['cities']:
                if city['cityName'] != '待明确地区':
                    try:
                        city['cityEnglishName'] = city_name_map[area['provinceShortName']]['cities'][city['cityName']]
                    except KeyError:
                        print(area['provinceShortName'], city['cityName'])
                        pass
                else:
                    city['cityEnglishName'] = 'Area not defined'
            
            area['updateTime'] = self.crawl_timestamp
    
            self.db.insert(collection='DXYArea_f', data=area)






###########################################################################################
### abroad_information  


with open("script_id_getListByCountryTypeService2true.xml", mode="w", encoding='utf-8') as f:
   f.write(str(soup.find('script', attrs={'id': 'getListByCountryTypeService2true'})))
   
   
abroad_information = re.search(r'\[(.*)\]', str(soup.find('script', attrs={'id': 'getListByCountryTypeService2true'})))

# if abroad_information:
#     self.abroad_parser(abroad_information=abroad_information)

def abroad_parser(abroad_information):
        countries = json.loads(abroad_information.group(0))
        with open("abroad_information.json", mode="w", encoding='utf-8') as json_file:
            json.dump(countries, json_file, ensure_ascii=False, indent=4)
        
        
        for country in countries:
            try:
                country.pop('id')
                country.pop('tags')
                country.pop('sort')
                # Ding Xiang Yuan have a large number of duplicates,
                # values are all the same, but the modifyTime are different.
                # I suppose the modifyTime is modification time for all documents, other than for only this document.
                # So this field will be popped out.
                country.pop('modifyTime')
                # createTime is also different even if the values are same.
                # Originally, the createTime represent the first diagnosis of the virus in this area,
                # but it seems different for abroad information.
                country.pop('createTime')
                country['comment'] = country['comment'].replace(' ', '')
            except KeyError:
                pass
            country.pop('countryType')
            country.pop('provinceId')
            country.pop('cityName')
            # The original provinceShortName are blank string
            country.pop('provinceShortName')
            # Rename the key continents to continentName
            country['continentName'] = country.pop('continents')

            # 不必要的去重限定日期
            # country['_today'] = self._today
            
            if self.db.find_one(collection='DXYArea', data=country):
                continue

            country['countryName'] = country.get('provinceName')
            country['provinceShortName'] = country.get('provinceName')
            country['continentEnglishName'] = continent_name_map.get(country['continentName'])
            country['countryEnglishName'] = country_name_map.get(country['countryName'])
            country['provinceEnglishName'] = country_name_map.get(country['countryName'])

            country['updateTime'] = self.crawl_timestamp

            self.db.insert(collection='DXYArea', data=country)






#################################
news_chinese = re.search(r'\[(.*?)\]', str(soup.find('script', attrs={'id': 'getTimelineService1'})))
news_chinese.group(0)

def news_parser(news):
    news = json.loads(news.group(0))
    print(news)
    for _news in news:
        _news.pop('pubDateStr')
        
        # # 去重限定日期
        # _news['_today'] = self._today
        # if self.db.find_one(collection='DXYNews', data=_news):
            # continue
        # _news['crawlTime'] = self.crawl_timestamp

        # self.db.insert(collection='DXYNews', data=_news)


news_english = re.search(r'\[(.*?)\]', str(soup.find('script', attrs={'id': 'getTimelineService2'})))
if news_english:
    news_parser(news=news_english)

#################################
#################################

rumors = re.search(r'\[(.*?)\]', str(soup.find('script', attrs={'id': 'getIndexRumorList'})))





