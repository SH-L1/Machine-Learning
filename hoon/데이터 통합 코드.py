import pandas as pd

population_df = pd.read_csv('유동인구_통합_데이터.csv', encoding='utf-8-sig')
weather_df = pd.read_csv('기온_강수량_updated.csv', encoding='utf-8-sig')

holiday_2019_df = pd.read_csv('2019_공휴일.csv', encoding='utf-8-sig')
holiday_2023_df = pd.read_csv('2023_공휴일.csv', encoding='utf-8-sig')
holiday_2024_df = pd.read_csv('2024_공휴일.csv', encoding='utf-8-sig')


holiday_2019_df['연도'] = 2019
holiday_2019_df['날짜'] = holiday_2019_df.apply(lambda x: f"2019_{x['월']:02d}", axis=1)

holiday_2023_df['연도'] = 2023
holiday_2023_df['날짜'] = holiday_2023_df.apply(lambda x: f"2023_{x['월']:02d}", axis=1)

holiday_2024_df = holiday_2024_df[['월', '공휴일 수']].copy()
holiday_2024_df['연도'] = 2024
holiday_2024_df['날짜'] = holiday_2024_df.apply(lambda x: f"2024_{x['월']:02d}", axis=1)

all_holidays_df = pd.concat([holiday_2019_df, holiday_2023_df, holiday_2024_df], ignore_index=True)
all_holidays_df = all_holidays_df[['날짜', '공휴일 수']]

result_df = pd.merge(
    population_df,
    weather_df,
    left_on='월',
    right_on='날짜',
    how='left'
)

result_df = result_df.drop(columns=['날짜'])

result_df = pd.merge(
    result_df,
    all_holidays_df,
    left_on='월',
    right_on='날짜',
    how='left'
)

result_df = result_df.drop(columns=['날짜'])

result_df['공휴일 수'] = result_df['공휴일 수'].fillna(0).astype(int)

time_columns = ['0시'] + [f'{i}시' for i in range(1, 24)]
final_columns = ['클러스터'] + time_columns + ['월', '평균기온(℃)', '강수량(mm)', '공휴일 수']
result_df = result_df[final_columns]

output_filename = '유동인구_통합_최종.csv'
result_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
