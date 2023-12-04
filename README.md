# Nutrients_Predict_and_Recommend 💊
---
## 개발 환경 (IDE)
- Win10
- Pycharm 2023.2
- Python 3.7

---
##  Project Objectives (프로젝트 목표)
- I tried to compensate for the disappointment in the last nutritional classification program  
In addition, a new nutritional recommendation system through symptoms was added to the program
- 이전에 진행한 영양제 분류 프로젝트에서 아쉬웠던 점을 보완하고자 했으며,  
  전에 없던 증상을 통한 추천 시스템을 새로 추가했다
- link : https://github.com/JiHyun-Jo7/IntelCapsule
---
## [01. Crawling Data](https://github.com/JiHyun-Jo7/Nutrients_Predict_and_Recommend/blob/14c4883aed4a2f3beeb2dda1c5409048e4b9d581/01_crawling_data.py)
```
# 이전 코드
```
- 데이터 크롤링을 하기 위해서는 상품의 데이터가 필요하다 하지만 해당 웹사이트에서 제품들의 URL에는 규칙성이 없다
- 이전 프로젝트에선 path를 사용하여 제품 사이트에 접근했는데 접속할때마다 쿠키 허용을 반드시 해야했고,
- 중간에 뜨는 광고창 때문에 PATH 마저 불규칙적으로 변해 오류가 자주 발생하고 PATH를 찾지 못하는 등 등 많은 시간이 소요됐다.
```
# 이번 코드
```
- 이번 프로젝트에선 자동으로 쿠키 허용, 광고창을 종료하였고 제품 페이지를 수집하여 접속했다.
- 그 결과 오류 발생 빈도도 대폭 감소하였으며 크롤링 소요 시간 또한 대폭 감소하였다.
---
## [02. ]
