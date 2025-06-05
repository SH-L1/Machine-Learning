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

# 통합데이터+매출 -> 최종테이블 만든뒤 클러서터별로 조사하는 코드

```py
import pandas as pd

# 월별 통합 데이터 불러오기
monthly_df = pd.read_csv('/content/drive/MyDrive/유동인구_통합_최종 (2).csv', encoding='utf-8-sig') #유동인구_통합_최종 파일경로 넣기

# ▶️ 월 정보에서 연도와 월 숫자 추출
monthly_df[['연도', '월_숫자']] = monthly_df['월'].str.split('_', expand=True).astype(int)

# ▶️ 분기 정보 생성
monthly_df['분기'] = ((monthly_df['월_숫자'] - 1) // 3) + 1
monthly_df['연도_분기'] = monthly_df['연도'].astype(str)  + monthly_df['분기'].astype(str)

# ▶️ 집계 기준 설정
time_columns = ['0시'] + [f'{i}시' for i in range(1, 24)]

agg_dict = {col: 'sum' for col in time_columns}
agg_dict.update({
    '평균기온(℃)': 'mean',
    '강수량(mm)': 'sum',
    '공휴일 수': 'sum'
})

# ▶️ 클러스터 + 연도_분기 기준 그룹화
quarterly_df = monthly_df.groupby(['클러스터', '연도_분기']).agg(agg_dict).reset_index()

# ▶️ 컬럼 순서 정리
final_columns = ['클러스터', '연도_분기'] + time_columns + ['평균기온(℃)', '강수량(mm)', '공휴일 수']
quarterly_df = quarterly_df[final_columns]

# ▶️ 저장
#quarterly_df.to_csv('유동인구_통합_분기별.csv', index=False, encoding='utf-8-sig')

sell=pd.read_csv('/content/drive/MyDrive/합친데이터2.csv') # 3년치 매출테이블 전부 합친 파일

#----------------------------------------------------------------------------------------

# 두 병합 기준 컬럼을 문자열(str) 타입으로 변환
quarterly_df['연도_분기'] = quarterly_df['연도_분기'].astype(str)
sell['기준_년분기_코드'] = sell['기준_년분기_코드'].astype(str)

# 병합 수행
merged_df = pd.merge(
    quarterly_df,
    sell,
    left_on=['클러스터', '연도_분기'],
    right_on=['클러스터', '기준_년분기_코드'],
    how='inner'  # 필요 시 'left' 또는 'outer'
)

# 중복 컬럼 제거
merged_df = merged_df.drop(columns=['기준_년분기_코드'])

# 저장 (선택)
#merged_df.to_csv('유동인구_매출_분기별_통합.csv', index=False, encoding='utf-8-sig')
data=merged_df.copy()

#----------------------------------------------------------------------------------------
data=merged_df.drop(columns=[
       '월요일_매출_금액', '화요일_매출_금액', '수요일_매출_금액', '목요일_매출_금액', '금요일_매출_금액',
       '토요일_매출_금액', '일요일_매출_금액', '시간대_00~06_매출_금액', '시간대_06~11_매출_금액',
       '시간대_11~14_매출_금액', '시간대_14~17_매출_금액', '시간대_17~21_매출_금액',
       '시간대_21~24_매출_금액', '남성_매출_금액', '여성_매출_금액', '연령대_10_매출_금액',
       '연령대_20_매출_금액', '연령대_30_매출_금액', '연령대_40_매출_금액', '연령대_50_매출_금액',
       '연령대_60_이상_매출_금액', '주중_매출_건수', '주말_매출_건수', '월요일_매출_건수', '화요일_매출_건수',
       '수요일_매출_건수', '목요일_매출_건수', '금요일_매출_건수', '토요일_매출_건수', '일요일_매출_건수',
       '시간대_건수~06_매출_건수', '시간대_건수~11_매출_건수', '시간대_건수~14_매출_건수',
       '시간대_건수~17_매출_건수', '시간대_건수~21_매출_건수', '시간대_건수~24_매출_건수', '남성_매출_건수',
       '여성_매출_건수', '연령대_10_매출_건수', '연령대_20_매출_건수', '연령대_30_매출_건수',
       '연령대_40_매출_건수', '연령대_50_매출_건수', '연령대_60_이상_매출_건수'])
#----------------------------------------------------------------------------------------

plt.figure(figsize=(25,25))
k=data[data['클러스터']==0].corr()    # 원하는 클러스터 조사(0 대신 넣기)
sns.heatmap(k,annot=True,cmap='coolwarm')
```
