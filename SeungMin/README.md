# 버스역,지하철역 시간대별 승하차정보 전처리
### abs(승차-하차) = 순하차 값을 구하는 코드
##### 24개의 순하차 컬럼을 각각 파일마다 만들어야 하므로 이 코드 전부 적용
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

```py
#지하철역
import pandas as pd
data = pd.read_csv('/content/sample_data/서울시 지하철 호선별 역별 시간대별 승하차 인원 정보1.csv')

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
data['사용월'] = pd.to_datetime(data['사용월'].astype(str), format='%Y%m')
```
