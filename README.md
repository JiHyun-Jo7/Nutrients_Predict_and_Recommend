# 💊Nutrients Predict and Recommend
---
## 1. 개발 환경 (IDE)
- Win10
- Pycharm 2023.2
- Python 3.7

---
##  2. Project Objectives (프로젝트 목표)
- I tried to compensate for the disappointment in the [last nutritional classification program](https://github.com/JiHyun-Jo7/IntelCapsule)  
In addition, a new nutritional recommendation system through symptoms was added to the program
- crawl nutritional information on iHub (https://iherb.com/), a famous nutritional supplement site around the world,  
Through this, 1. predict the effect with the name of nutritional supplements and  
2. Create a program that recommends nutritional supplements when providing symptoms
- [이전에 진행한 영양제 분류 프로젝트](https://github.com/JiHyun-Jo7/IntelCapsule)에서 아쉬웠던 점을 보완하고자 했으며,  
  전에 없던 증상을 통한 추천 시스템을 새로 추가했다
- 전세계 유명 영양제 사이트인 [아이허브](https://kr.iherb.com/) 에서 영양제 정보를 크롤링 한 후,  
  1. 영양제 이름으로 효과를 추측하고 2. 증상을 제공하면 영양제를 추천하는 프로그렘을 만든다 
---
## 3. Code Review
### 01. [Crawling Data](https://github.com/JiHyun-Jo7/Nutrients_Predict_and_Recommend/blob/14c4883aed4a2f3beeb2dda1c5409048e4b9d581/01_crawling_data.py)
```
# Before
for i in range(6):
    section_url = 'https://kr.iherb.com/c/{}'.format(category[i])
    df_titles = pd.DataFrame()
    titles = []
    for j in range(1, pages[i] + 1):  # pages[i]+1
        if j == 1:
            url = section_url
        else:
            url = section_url + '?p={}'.format(j)
        driver.get(url)
        time.sleep(3)
        product = driver.find_elements(By.CLASS_NAME, 'product-cell-container')
```
- 데이터 크롤링을 하기 위해서는 상품의 데이터가 필요하다 하지만 해당 웹사이트에서 제품들의 URL에는 규칙성이 없다
- 이전 프로젝트에선 path를 사용하여 제품 사이트에 접근했는데 페이지에 접속할때마다 쿠키 허용을 반드시 해야해 피로감이 컸다
- 중간에 뜨는 광고창 때문에 PATH 마저 불규칙적으로 변했고 이로인해 PATH를 찾지 못하는 오류가 자주 발생해 많은 시간이 소요됐다
```
# After
        response = requests.get(section_url, headers=headers)
        response.raise_for_status()
        soup = bs(response.text, 'html.parser')

        product_url = []
        for z in soup.find_all('div', {'class': 'absolute-link-wrapper'}):
            for y in z.find_all({'a'}):
                if y.get('href') is not None:
                    product_url.append(y.get('href'))
        del product_url[0]              # Delete unrelated url
```
- 이번 프로젝트에선 자동으로 쿠키 허용, 광고창을 종료하였고 제품 페이지를 수집하여 접속했다
- 그 결과 오류 발생 빈도도 대폭 감소하였으며 크롤링 소요 시간 또한 대폭 감소하였다

### 02. [Data Concat](https://github.com/JiHyun-Jo7/Nutrients_Predict_and_Recommend/blob/e2ea50df5acf610e29da6c590f75c5b2601d9b4f/02_data_concat.py)

### 03. [Preprocessing](https://github.com/JiHyun-Jo7/Nutrients_Predict_and_Recommend/blob/e2ea50df5acf610e29da6c590f75c5b2601d9b4f/03_preprocessing.py)
```
Z = np.array(df.name)
for i in range(len(Z)):
    if Z[i] is not None:
        for j in range(i):
            if i != j and Z[j] is not None:
                ratio = SequenceMatcher(None, Z[i], Z[j]).ratio()
                if ratio >= 0.95:
                    print('similar data,{} :{}'.format(i, Z[i]))
                    print('remove data,{} :{}'.format(j, Z[j]))
                    df.effect[j] = None
                    df.category[j] = None
                    df.name[j] = None
```
- Previous projects eliminated deduplication based on the product's validity, but this time, we tried deduplication based on the product name
- It was very effective in removing products with different capacities and flavors,  
but there was a problem that products by gender and age were removed together
- In addition, when duplicate tests were conducted in all categories, the number of data in the latter category became very poor
- 이전 프로젝트에서는 제품의 효과를 기준으로 중복을 제거했지만 이번에는 제품 명을 기준으로 한 중복처리를 시도했다
- 용량, 맛이 다른 제품을 제거하는데 매우 효과적이었지만 성별, 연령별 제품이 함께 제거되는 것이 문제였다
- 또한 중복 검사를 모든 카테고리로 검사하니 후반 카테고리의 데이터 수가 매우 빈약해지는 문제가 발생했다

```
for i in range(len(df.effect)):
    tk_x = okt.pos(df.effect[i], stem=True)
    df_token = pd.DataFrame(tk_x, columns=['word', 'class'])
    # 영어, 명사, 동사, 형용사 형태의 단어만 남김
    df_token = df_token[
        ((df_token['class'] == 'Alpha') | (df_token['class'] == 'Noun') | (df_token['class'] == 'Verb') | (df_token['class'] == 'Adjective'))]
    # 명사, 동사, 형용사 형태의 단어만 남김
    # df_token = df_token[
    #     ((df_token['class'] == 'Noun') | (df_token['class'] == 'Verb') | (df_token['class'] == 'Adjective'))]
    print(df_token)
    words = []                                                 # 품사 태그 제거
    for word in df_token.word:
        if 1 < len(word):                                      # 한글자 단어 제거
            if word not in stopwords:                          # 불용어 제거
                print(word)
                words.append(word)
                cleaned_sentence = ' '.join(words)
    print(cleaned_sentence)
    try:
        if len(cleaned_sentence.split()) < 15:                     # 단어가 15개 미만인 문장 제거
            cleaned_sentence = None
    except: cleaned_sentence = None
    cleaned_sentences.append(cleaned_sentence)
df['cleaned_sentences'] = cleaned_sentences
```
- Save only English, nouns, verbs, and adjectives among morphemes and remove fire words
- Remove short sentences that do not help you learn
- 형태소 중 영어, 명사, 동사, 형용사만 살리고 불용어를 제거
- 학습에 도움이 되지 않는 짧은 문장은 제거

### 04. [Model Learning](https://github.com/JiHyun-Jo7/Nutrients_Predict_and_Recommend/blob/e2ea50df5acf610e29da6c590f75c5b2601d9b4f/04_model_learning.py)
- 24 Categories
- Model structure
  - 차원 축소 레이어(Embedding), 컨볼루션 레이어(Conv1D), LSTM 레이어로 구성
  - Add Dropout Layer to prevent overfitting during learning
  - 학습 중 과적합을 방지하기 위해 Dropout 레이어 추가

### 05. [Model_predict](https://github.com/JiHyun-Jo7/Nutrients_Predict_and_Recommend/blob/e2ea50df5acf610e29da6c590f75c5b2601d9b4f/05_model_predict.py)
- 6 categories (for testing) were predicted successfully, but 24 categories are in preprocessing ...
- 카테고리 6개(테스트 용)는 예측 성공하였으나 카테고리 24개는 전처리 진행 중 ...
---
