import pandas as pd
import numpy as np
import math
from sklearn.cluster import KMeans

file = pd.read_csv('역_버스정류장_위치_정보.csv', encoding='cp949')

latitudes = file['위도'].to_numpy()
longitudes = file['경도'].to_numpy()
coords = np.vstack((latitudes, longitudes)).T

mean_lat = latitudes.mean()
lat_km = coords[:, 0] * 111.0
lon_km = coords[:, 1] * 111.0 * np.cos(np.radians(mean_lat))
coords_km = np.vstack((lat_km, lon_km)).T

k = 100 # 실루엣 점수 0.3 정도
kmeans = KMeans(n_clusters=k, random_state=42)
labels = kmeans.fit_predict(coords_km)
centers = kmeans.cluster_centers_

file['클러스터'] = labels

output_path = '군집화_결과.csv'
file.to_csv(output_path, index=False, encoding='utf-8-sig')

centers_lat_deg = centers[:, 0] / 111.0
centers_lon_deg = centers[:, 1] / (111.0 * np.cos(np.radians(mean_lat)))
centroids_df = pd.DataFrame({
    '클러스터': np.arange(k),
    '위도': centers_lat_deg,
    '경도': centers_lon_deg
})
centroids_df.to_csv('군집화_결과(위도_경도).csv', index=False, encoding='utf-8-sig')