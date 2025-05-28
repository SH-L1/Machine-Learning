# 버스역,지하철역 시간대별 승하차정보 전처리
### 하차-승차 = 순하차 값을 구하는 코드
##### 24개의 순하차 컬럼을 각각 파일마다 만들어야 하므로 이 코드 전부 적용
```py
# 버스역
import pandas as pd
data=pd.read_csv('file_path')

data['00시순하차']=data['00시하차총승객수']-data['00시승차총승객수']
data.drop(columns=['00시하차총승객수','00시승차총승객수'],inplace=True)

for i in range(1,24):
  data[f'{i}시순하차']=data[f'{i}시하차총승객수']-data[f'{i}시승차총승객수']
  data.drop(columns=[f'{i}시하차총승객수',f'{i}시승차총승객수'],inplace=True,axis=1)
```

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
    data[new_col] = data[original_col_하차] - data[original_col_승차]

    # 원본 컬럼 삭제
    data.drop(columns=[original_col_하차, original_col_승차], inplace=True)


for month in range(1, 13):
    month_str = f'2024{month:02d}'

    month_int = int(month_str)
    a=data[data['사용월'] == month_int]
    a.to_csv(f'{month_int}')
```
