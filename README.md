# 프로젝트 개발순서
### 1.데이터 수집
  - 시간별 버스역,지하철역 승하차 인원정보
  - 역들의 좌표정보
  - 공휴일,날씨
  - 상권별 매출정보
<br>

### 2.데이터 전처리
##### 시간별 버스역,지하철역 승하차 인원정보 -> 각각 시간대별로 하차-승차 = 순하차 컬럼 만들고 승차,하차 drop
```py
# 버스역
import pandas as pd
data=pd.read_csv('file_path')

data['00시순하차']=abs(data['00시하차총승객수']-data['00시승차총승객수'])
data.drop(columns=['00시하차총승객수','00시승차총승객수'],inplace=True)

for i in range(1,24):
  data[f'{i}시순하차']=abs(data[f'{i}시하차총승객수']-data[f'{i}시승차총승객수'])
  data.drop(columns=[f'{i}시하차총승객수',f'{i}시승차총승객수'],inplace=True,axis=1)
data['사용년월'] = pd.to_datetime(data['사용년월'].astype(str), format='%Y%m')
```
<br>

```py
#지하철역
import pandas as pd

data = pd.read_csv('/content/drive/MyDrive/서울시 지하철 호선별 역별 시간대별 승하차 인원 정보1 (1).csv')

for i in range(0, 24):
    # 시간대 포맷 조정 (한 자리 숫자 앞에 0 추가)
    hour = f"{i:02d}"  # 00, 01, 02 형식으로 변환
    next_hour = f"{(i+1):02d}"  # 다음 시간대도 같은 형식으로 변환

    # 원본 컬럼명과 새 컬럼명
    original_col_하차 = f"{hour}시-{next_hour}시 하차인원"
    original_col_승차 = f"{hour}시-{next_hour}시 승차인원"
    new_col = f"{hour}시-{next_hour}시 순하차인원"

    # 순하차인원 계산
    data[new_col] = abs(data[original_col_하차] - data[original_col_승차])

    # 원본 컬럼 삭제
    data.drop(columns=[original_col_하차, original_col_승차], inplace=True)


for month in range(1, 13):
    month_str = f'2024{month:02d}'

    month_int = int(month_str)
    a=data[data['사용월'] == month_int]
    a.to_csv(f'{month_int}')
```
##### 역 이름과 좌표들 매칭작업
<br>

### 3.모델학습
  - 최종 학습할 데이터셋의 독립변수 -> 시간대별 순하차 인원,날씨,공휴일,성별매출,연령별 매출,요일별 매출  종속변수-> 매출
  - 선형회귀,랜덤포레스트,XGBoost,GBM 각각 4가지 사용하여 학습진행(교차검증) -> 바로 평가하는게 아닌 독립변수로 다시 묶어줘야함 -> 묶어준 독립변수로 다시 선형회귀 학습 진행(스택킹)
##### 군집화(각각 역의 좌표들을 학습해서 군집화 실행. 군집들과 매출 상권의 이름을 사용해서 맵핑)
<br><br>
##### 실루엣계수
```py
# 군집화 하기 전 최적의 k값 찾는 과정-실루엣계수
import pandas as pd
import numpy as np
import math
from sklearn.cluster import KMeans

file = pd.read_csv('/content/drive/MyDrive/역_버스정류장_위치_정보.csv', encoding='cp949')

latitudes = file['위도'].to_numpy()
longitudes = file['경도'].to_numpy()
coords = np.vstack((latitudes, longitudes)).T

mean_lat = latitudes.mean()
lat_km = coords[:, 0] * 111.0
lon_km = coords[:, 1] * 111.0 * np.cos(np.radians(mean_lat))
coords_km = np.vstack((lat_km, lon_km)).T
coords_km

test=[]
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
for k in range(1,10000):
    if not k%5==0:
      continue
    k_model = KMeans(n_clusters=k, random_state=42)
    labels = k_model.fit_predict(coords_km)
    score = silhouette_score(coords_km, labels)
    test.append(score)
    print(k/10001*100)

```
<br>
<img src="https://github.com/SH-L1/Machine-Learning/blob/main/image/%E1%84%89%E1%85%B5%E1%86%AF%E1%84%85%E1%85%AE%E1%84%8B%E1%85%A6%E1%86%BA%E1%84%80%E1%85%A8%E1%84%89%E1%85%AE.png" width="600" height="300"/>
<br><br>

##### 엘보우기법
```py
# 엘보우기법
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
test2=[]
for i in range(5001, 10001):
    if not i % 50 ==0:
      continue
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=42)
    kmeans.fit(coords_km)
    test2.append(kmeans.inertia_)
```
<br>
<img src="https://github.com/SH-L1/Machine-Learning/blob/main/image/%E1%84%8B%E1%85%A6%E1%86%AF%E1%84%87%E1%85%A9%E1%84%8B%E1%85%AE%E1%84%80%E1%85%B5%E1%84%87%E1%85%A5%E1%86%B8.png"/>
<br><br>

### 4.모델 평가
  - RMSLE -> 회귀 평가
  - 엘보우기법,실루엣계수-> 군집화 평가(K값 정하는 기준이 됨)
<br>

### 5.웹사이트에서 모델을 사용한 서비스 개발(최종)
  - 사용자의 위치(좌표) 를 받으면 그 좌표가 포함된 군집을 지도상에 나타내줌
  - 사용자의 위치가 포함된 군집의 과거 매출과 유동인구를 시각적 그래프로 한번에 보여주고
  - 매출을 예측하는 데이터도 시각적 그래프로 한번에 나타내줌
  - 매출예측을 기반해서 재고관리와 고용원관리를 알려주고, 재고관리와 고용원관리를 할수있는 UI를 웹사이트 내에 제공
  - 학습할때 사용했던 독립변수(유동인구,날씨,공휴일,성별 매출,연령별 매출,요일별 매출) 중 가장 상관관계가 높은 애를 알려주는 문구 추가(인사이트)
<br>

# 임시 메모장
지도에 띄워주는건 folium 사용
