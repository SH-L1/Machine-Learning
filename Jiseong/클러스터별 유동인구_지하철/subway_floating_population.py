import pandas as pd

cluster_df = pd.read_csv("군집화_결과.csv")
cluster_centers = cluster_df.groupby('클러스터')[['위도', '경도']].mean().reset_index()

for i in range(1, 13):
    sub = f"2024{i:02}.csv"
    subway_df = pd.read_csv(sub)

    subway_cluster = cluster_df[cluster_df['type'] == 'subway'].copy()

    matched_rows = []
    for _, cluster_row in subway_cluster.iterrows():
        matched = subway_df[subway_df['지하철역'].astype(str).str.contains(cluster_row['이름'], na=False)]
        if not matched.empty:
            for _, match in matched.iterrows():
                merged_row = pd.concat([cluster_row, match], axis=0)
                matched_rows.append(merged_row)

    merged_df = pd.DataFrame(matched_rows)

    time_cols = [col for col in merged_df.columns if '순하차인원' in col]
    cluster_time_sum = merged_df.groupby('클러스터')[time_cols].sum().reset_index()
    cluster_time_sum = cluster_time_sum.astype(int)

    cluster_time_sum.columns = [
        col.replace(" 순하차인원", "") if "순하차인원" in col else col
        for col in cluster_time_sum.columns
    ]

    cluster_time_sum = pd.merge(cluster_time_sum, cluster_centers, on='클러스터', how='left')

    cluster_time_sum.to_csv(f"지하철_클러스터_시간대별_유동인구_2024{i:02}.csv", index=False, encoding='utf-8-sig')
