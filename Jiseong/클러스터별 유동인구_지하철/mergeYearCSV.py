import pandas as pd
import re

cluster_df = pd.read_csv("군집화_결과.csv")
subway_cluster = cluster_df[cluster_df['type'] == 'subway'].copy()

all_months = []

for i in range(1, 13):
    subway_df = pd.read_csv(f"2024{i:02}.csv")
    matched_rows = []

    for _, cluster_row in subway_cluster.iterrows():
        matched = subway_df[subway_df['지하철역'].astype(str).str.contains(cluster_row['이름'], na=False)]
        if not matched.empty:
            cluster_data = pd.DataFrame([cluster_row] * len(matched)).reset_index(drop=True)
            merged = pd.concat([cluster_data, matched.reset_index(drop=True)], axis=1)
            matched_rows.append(merged)

    if matched_rows:
        merged_df = pd.concat(matched_rows, ignore_index=True)

        time_cols = [col for col in merged_df.columns if '순하차인원' in col]

        cluster_time_sum = merged_df.groupby('클러스터')[time_cols].sum().reset_index()
        cluster_time_sum = cluster_time_sum.astype(int)

        new_columns = {}
        for col in cluster_time_sum.columns:
            if '순하차인원' in col:
                match = re.search(r'(\d{2})시', col)
                if match:
                    hour = int(match.group(1))
                    new_columns[col] = f"{hour}시"
            else:
                new_columns[col] = col  # 클러스터 등은 그대로

        cluster_time_sum = cluster_time_sum.rename(columns=new_columns)

        cluster_time_sum['월'] = f"2019-{i:02}"

        all_months.append(cluster_time_sum)

final_df = pd.concat(all_months, ignore_index=True)
final_df.to_csv("지하철_클러스터_시간대별_유동인구_2024_통합.csv", index=False, encoding='utf-8')