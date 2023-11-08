from selenium import webdriver  # 웹사이트(및 웹 애플리케이션)의 유효성 검사에 사용되는 자동화 테스트 프레임워크
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re
import time
import datetime

url = 'https://kr.iherb.com/'
options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
options.add_argument('user-agent=' + user_agent)
options.add_argument('lang=ko_KR')

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executble_path=ChromeDriverManager().install())
# 크롬 드라이버
driver = webdriver.Chrome(service=service, options=options)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}

# category = ['seasonal-allergies', 'sleep', 'weight-loss', 'childrens-health', 'mens-health', 'womens-health']
category = ['anti-aging-longevity', 'ayurveda', 'bladder', 'bone-joint-cartilage', 'brain-cognitive', 'circulatory-support', 'colon', 'common-cold-flu', 'detox-cleanse', 'digestive-support', 'energy', 'eye-vision', 'hair-skin-nails', 'heart', 'immune-support', 'pain-relief', 'seasonal-allergies', 'sleep', 'weight-loss', 'childrens-health', 'mens-health', 'womens-health']
# category_kr = ['계절성 알레르기', '불면증', '체중 관리', '어린이 건강', '남성 건강', '여성 건강']
category_kr = ['노화_장수', '아유르베다', '방광', '뼈_관절_연골', '두뇌_인지', '순환기계', '장건강', '감기_독감', '디톡스_클렌징', '소화기계', '에너지', '눈_시력', '모발_피부_손발톱', '심혈관계', '면역기계', '통증완화', '계절성 알레르기', '불면증', '체중 조절', '어린이 건강', '남성 건강', '여성 건강']
# pages = [14, 13, 14, 16, 8, 16]  # 각 카테고리 별 총 페이지 수
df_nutrients = pd.DataFrame()

for i in range(len(category)):                          # 카테고리 변경
    # 데이터 프레임 및 리스트 초기화
    df_nutrient = pd.DataFrame()
    effect = []
    product_names = []

    for j in range(0, 7):                   # 이후 예측 데이터를 위해 최대 페이지 수 제한
        section_url = url + 'c/{}?p={}'.format(category[i], j)
        driver.get(section_url)             # 페이지 변경
        time.sleep(3)
        if i == 0 and j == 0:               # 크롬 첫 실행 시 쿠키 허용
            driver.find_element(By.XPATH, '//*[@id="truste-consent-button"]').click()
            print('cookie access')

        # for 문 반복을 위해 제품 수 측정 (마지막 페이지 제품 수가 48개 미만)
        # product = driver.find_elements(By.CLASS_NAME, 'product-cell-container')
        # product = len(product)

        # 제품 페이지 수집
        response = requests.get(section_url, headers=headers)
        response.raise_for_status()
        soup = bs(response.text, 'html.parser')

        product_url = []
        for z in soup.find_all('div', {'class': 'absolute-link-wrapper'}):
            for y in z.find_all({'a'}):
                if y.get('href') is not None:
                    product_url.append(y.get('href'))
        del product_url[0]              # 관계 없는 url 삭제
        for k in range(0, 48):          # 마지막 페이지 제품 수가 48개 미만일 경우 range=(0, product)
            try:
                driver.get(product_url[k])
                print('debug01')
                time.sleep(1)
                product_name = driver.find_element(By.XPATH, '//*[@id="name"]').text
                print('debug02')
                product_names.append(product_name)
                print(product_name)
                ## 영양제 효과 크롤링. 셋 중 하나만 실행 ##
                # 1. 상품 설명 전체 크롤링
                # nutrient_data = driver.find_element('xpath',
                #                                     '/html/body/div[8]/article/div[2]/div/section/div[2]/div/div/div[1]/div[1]/div/div').text
                # 제품 설명 전처리 (한글, 영어(대,소문자), 숫자만 수집. 그 외는 공백 처리)
                # nutrient_data = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', nutrient_data)
                # effect.append(nutrient_data)

                # 2. 상품 설명 크롤링
                # dt = ''
                # nutrient_data = driver.find_elements(By.XPATH, '//div[@itemprop="description"]/p')
                # if not nutrient_data == '':
                #     for data in nutrient_data:
                #         if not data.text == '':
                #             data = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', data.text)
                #             dt += data
                #     print(dt)
                #     effect.append(dt)

                # 3. 상품 설명 및 요약 크롤링
                dt = ''
                nutrient_data = driver.find_elements(By.XPATH, '//div[@itemprop="description"]/ul')
                for data in nutrient_data:
                    if not data.text == '':
                        data = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', data.text)
                        dt += data
                effect.append(dt)

            except:
                # 오류가 발생할 경우 error + 카테고리, 페이지, 제품 번호 출력
                print('error c.{} p.{} p.{}'.format(category[i], j, k))

    df_nutrient = pd.DataFrame({'effect': effect, 'name': product_names})
    df_nutrient['category'] = category_kr[i]
    df_nutrients = pd.concat([df_nutrients, df_nutrient], ignore_index=True)

    # crawling 폴더에 Nutrients_(카테고리)_(년월일).cvs 카테고리 마다 중간 저장
    # df_nutrient.to_csv(
    #     './crawling_data/nutrients_{}_{}.csv'.format(category[i], datetime.datetime.now().strftime('%Y%m%d')),
    #     index=False)

# print(df_titles.head(20))  # 상위 제목 20개 출력
df_nutrients.info()
# df_nutrients.to_csv(
#         './crawling_data/predict.csv'.format(datetime.datetime.now().strftime('%Y%m%d')),
#         index=False)        # 예측용 데이터
df_nutrients.to_csv(
        './crawling_data/nutrients_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')),
        index=False)      # 학습용 데이터

# print(df_titles['category'].value_counts())
