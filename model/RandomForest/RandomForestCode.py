import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# 코랩용 한글 폰트 설정
import matplotlib.font_manager as fm

# 나눔고딕 폰트 설치 (코랩에서)
!apt-get install -y fonts-nanum
!fc-cache -fv
!rm ~/.cache/matplotlib -rf

# 폰트 설정
plt.rcParams['font.family'] = 'NanumBarunGothic'
plt.rcParams['axes.unicode_minus'] = False

# 만약 위 폰트가 안되면 DejaVu Sans 사용
try:
    plt.rcParams['font.family'] = 'NanumBarunGothic'
except:
    plt.rcParams['font.family'] = 'DejaVu Sans'
    print("한글 폰트 설정 실패 - 기본 폰트 사용")

print(f"현재 폰트: {plt.rcParams['font.family']}")


def visualize_manual_tuning_results(results_df):
    param_names = [col for col in results_df.columns if col != 'mean_r2_score']
    for param_name in param_names:
        other_params = [p for p in param_names if p != param_name]
        plt.figure(figsize=(12, 8))
        if other_params:
            grouped = results_df.groupby(other_params)
            for name, group in grouped:
                label = ", ".join([f"{p}={v}" for p, v in zip(other_params, name if isinstance(name, tuple) else (name,))])
                group.sort_values(by=param_name).plot(x=param_name, y='mean_r2_score', ax=plt.gca(), label=label, marker='o', linestyle='-')
        else:
            results_df.sort_values(by=param_name).plot(x=param_name, y='mean_r2_score', ax=plt.gca(), marker='o', linestyle='-')
        plt.title(f'"{param_name}" 변화에 따른 모델 성능(R2 Score)', fontsize=16)
        plt.xlabel(param_name)
        plt.ylabel('평균 교차검증 점수 (R2)')
        plt.grid(True)
        plt.legend(title="다른 파라미터 조합")
        plt.tight_layout()
        plt.savefig(f'manual_tuning_lineplot_{param_name}.png')

    print(f"\n하이퍼파라미터 튜닝 결과 라인 그래프 {len(param_names)}개가 .png 파일로 저장되었습니다.")


def train_final_model():
    csv_path = '/content/drive/MyDrive/찐막데이터_2 (1).csv'
    try:
        data = pd.read_csv(csv_path, encoding='cp949')
    except Exception as e:
        print(f"오류: CSV 파일 로드 실패 - {e}")
        return

    categorical_features = ['클러스터', '연도_분기']
    numerical_features = [f'{i}시' for i in range(24)] + ['평균기온(℃)', '강수량(mm)', '공휴일 수']

    target_cols = [
        '당월_매출_금액', '당월_매출_건수', '주중_매출_금액', '주말_매출_금액', '월요일_매출_금액', '화요일_매출_금액',
        '수요일_매출_금액', '목요일_매출_금액', '금요일_매출_금액', '토요일_매출_금액', '일요일_매출_금액', '시간대_00~06_매출_금액',
        '시간대_06~11_매출_금액', '시간대_11~14_매출_금액', '시간대_14~17_매출_금액', '시간대_17~21_매출_금액', '시간대_21~24_매출_금액',
        '남성_매출_금액', '여성_매출_금액', '연령대_10_매출_금액', '연령대_20_매출_금액', '연령대_30_매출_금액', '연령대_40_매출_금액',
        '연령대_50_매출_금액', '연령대_60_이상_매출_금액', '주중_매출_건수', '주말_매출_건수', '월요일_매출_건수', '화요일_매출_건수',
        '수요일_매출_건수', '목요일_매출_건수', '금요일_매출_건수', '토요일_매출_건수', '일요일_매출_건수', '시간대_건수~06_매출_건수',
        '시간대_건수~11_매출_건수', '시간대_건수~14_매출_건수', '시간대_건수~17_매출_건수', '시간대_건수~21_매출_건수', '시간대_건수~24_매출_건수',
        '남성_매출_건수', '여성_매출_건수', '연령대_10_매출_건수', '연령대_20_매출_건수', '연령대_30_매출_건수', '연령대_40_매출_건수',
        '연령대_50_매출_건수', '연령대_60_이상_매출_건수'
    ]

    final_categorical_features = [col for col in categorical_features if col in data.columns]
    final_numerical_features = [col for col in numerical_features if col in data.columns]
    final_target_cols = [col for col in target_cols if col in data.columns]
    required_feature_cols = final_categorical_features + final_numerical_features
    
    # 결측값 확인 및 처리
    print(f"전체 데이터 크기: {data.shape}")
    print(f"결측값 있는 행 수: {data[required_feature_cols + final_target_cols].isnull().any(axis=1).sum()}")
    
    data.dropna(subset=required_feature_cols + final_target_cols, inplace=True)
    print(f"결측값 제거 후 데이터 크기: {data.shape}")

    if 'Unnamed: 0' in data.columns:
        data.drop(columns=['Unnamed: 0'], inplace=True)

    X = data[required_feature_cols]
    y = data[final_target_cols]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor = ColumnTransformer(transformers=[
        ('num', StandardScaler(), final_numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), final_categorical_features)
    ])

    # RandomForest 파라미터 그리드 - None 대신 정수 값 사용
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [5, 10, 15, 20],  # None 대신 큰 값들 사용
        'max_features': ['sqrt', 'log2']
    }

    primary_target = '당월_매출_금액'
    tuning_results = []
    kf = KFold(n_splits=3, shuffle=True, random_state=42)

    print("하이퍼파라미터 튜닝 시작...")
    total_combinations = np.prod([len(v) for v in param_grid.values()])
    count = 0
    
    for n in param_grid['n_estimators']:
        for d in param_grid['max_depth']:
            for f in param_grid['max_features']:
                count += 1
                scores = []
                
                # 파라미터 값 검증
                print(f"현재 파라미터: n_estimators={n}, max_depth={d}, max_features={f}")
                
                # max_depth가 None이거나 nan인지 확인
                if pd.isna(d) or d is None:
                    print(f"경고: max_depth 값이 잘못됨: {d}")
                    continue
                
                for train_idx, val_idx in kf.split(X_train):
                    X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
                    y_tr, y_val = y_train[primary_target].iloc[train_idx], y_train[primary_target].iloc[val_idx]

                    try:
                        model = RandomForestRegressor(
                            n_estimators=int(n), 
                            max_depth=int(d) if d is not None else None, 
                            max_features=f, 
                            random_state=42, 
                            n_jobs=-1
                        )
                        pipeline = Pipeline([
                            ('preprocessor', preprocessor),
                            ('regressor', model)
                        ])
                        pipeline.fit(X_tr, y_tr)
                        score = pipeline.score(X_val, y_val)
                        scores.append(score)
                    except Exception as e:
                        print(f"모델 학습 중 오류: {e}")
                        continue

                if scores:  # scores가 비어있지 않은 경우만
                    mean_score = np.mean(scores)
                    tuning_results.append({
                        'n_estimators': n,
                        'max_depth': d,
                        'max_features': f,
                        'mean_r2_score': mean_score
                    })
                    print(f"[{count}/{total_combinations}] n={n}, depth={d}, feat={f} => R2={mean_score:.4f}")

    if not tuning_results:
        print("하이퍼파라미터 튜닝 결과가 없습니다. 기본 파라미터를 사용합니다.")
        best_params = {'n_estimators': 100, 'max_depth': 10, 'max_features': 'sqrt'}
    else:
        results_df = pd.DataFrame(tuning_results)
        best_row = results_df.loc[results_df['mean_r2_score'].idxmax()]
        best_params = best_row.drop('mean_r2_score').to_dict()

        print("\n✅ 최적 하이퍼파라미터 조합:")
        print(best_params)
        print(f"최적 조합 R2 Score: {best_row['mean_r2_score']:.4f}")

        visualize_manual_tuning_results(results_df)

    # 최종 모델 학습
    final_model = RandomForestRegressor(
        n_estimators=int(best_params['n_estimators']),
        max_depth=int(best_params['max_depth']),
        max_features=best_params['max_features'],
        random_state=42, 
        n_jobs=-1
    )
    
    final_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', MultiOutputRegressor(final_model))
    ])
    
    final_pipeline.fit(X_train, y_train)
    y_pred = final_pipeline.predict(X_test)

    # 성능 평가
    metrics_df = pd.DataFrame(columns=['MSE', 'RMSE', 'MAE', 'R2 Score'])
    for i, target_name in enumerate(final_target_cols):
        mse = mean_squared_error(y_test.iloc[:, i], y_pred[:, i])
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test.iloc[:, i], y_pred[:, i])
        r2 = r2_score(y_test.iloc[:, i], y_pred[:, i])
        metrics_df.loc[target_name] = [mse, rmse, mae, r2]

    print("\n📊 최종 모델 성능 평가:")
    with pd.option_context('display.float_format', '{:,.2f}'.format):
        print(metrics_df)

    return final_pipeline, metrics_df

if __name__ == '__main__':
    model, metrics = train_final_model()
    if model:
        print("\n모델 학습 완료 ✅")
    else:
        print("\n모델 학습 실패 ❌")
