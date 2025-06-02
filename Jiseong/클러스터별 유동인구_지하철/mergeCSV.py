import pandas as pd

file_2019 = "2019/지하철_클러스터_시간대별_유동인구_2019_통합.csv"
file_2023 = "2023/지하철_클러스터_시간대별_유동인구_2023_통합.csv"
file_2024 = "2024/지하철_클러스터_시간대별_유동인구_2024_통합.csv"

df_2019 = pd.read_csv(file_2019)
df_2023 = pd.read_csv(file_2023)
df_2024 = pd.read_csv(file_2024)

df_2019['월'] = df_2019['월'].str.replace(r'^2019-\d{2}$', lambda m: m.group(0), regex=True)  # 그대로 유지
df_2023['월'] = df_2023['월'].str.replace(r'^2019-(\d{2})$', r'2023-\1', regex=True)
df_2024['월'] = df_2024['월'].str.replace(r'^2019-(\d{2})$', r'2024-\1', regex=True)

merged_df = pd.concat([df_2019, df_2023, df_2024], ignore_index=True)

merged_df.to_csv("지하철_클러스터_시간대별_유동인구_통합.csv", index=False, encoding='utf-8')
