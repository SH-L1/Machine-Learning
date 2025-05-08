# 버스역,지하철역 시간대별 승하차정보 전처리
### abs(승차-하차) = 순하차 값을 구하는 코드
##### 24개의 순하차 컬럼을 각각 파일마다 만들어야 하므로 이 코드 전부 적용
```py
import pandas as pd
data=pd.read_csv('file_path')

data['00시순하차']=abs(data['00시하차총승객수']-data['00시승차총승객수'])
data.drop(columns=['00시하차총승객수','00시승차총승객수'],inplace=True)

for i in range(1,24):
  data[f'{i}시순하차']=abs(data[f'{i}시하차총승객수']-data[f'{i}시승차총승객수'])
  data.drop(columns=[f'{i}시하차총승객수',f'{i}시승차총승객수'],inplace=True,axis=1)
```
