import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

try:
    plt.rcParams['font.family'] = 'Malgun Gothic'
except RuntimeError:
    try:
        plt.rcParams['font.family'] = 'AppleGothic'
    except RuntimeError:
        pass
plt.rcParams['axes.unicode_minus'] = False


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
        plt.xlabel(param_name, fontsize=12)
        plt.ylabel('평균 교차검증 점수 (R2)', fontsize=12)
        plt.grid(True)
        plt.legend(title="다른 파라미터 조합")
        plt.tight_layout()
        
        plot_filename = f'manual_tuning_lineplot_{param_name}.png'
        plt.savefig(plot_filename)
        
    print(f"\n하이퍼파라미터 튜닝 결과 라인 그래프 {len(param_names)}개가 .png 파일로 저장되었습니다.")


def train_final_model():
    csv_path = '유동인구_매출데이터.csv'
    try:
        data = pd.read_csv(csv_path, encoding='cp949')
    except Exception as e:
        print(f"오류: CSV 파일 로드 실패 - {e}")
        return

    if data.empty:
        print("오류: 로드된 데이터가 비어있습니다.")
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
    all_required_cols = required_feature_cols + final_target_cols
    
    missing_cols = [col for col in all_required_cols if col not in data.columns]
    if missing_cols:
        print(f"오류: 데이터에 다음 필수 컬럼이 없습니다: {missing_cols}")
        return
        
    data.dropna(subset=all_required_cols, inplace=True)
    if 'Unnamed: 0' in data.columns:
        data = data.drop(columns=['Unnamed: 0'], errors='ignore')

    if data.empty or not required_feature_cols or not final_target_cols:
        print("오류: 데이터 부족 또는 특징/타겟 컬럼 정의 오류로 학습이 불가합니다.")
        return

    X = data[required_feature_cols]
    y = data[final_target_cols]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor = ColumnTransformer(transformers=[
        ('num', StandardScaler(), final_numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), final_categorical_features)
    ])
    
    param_grid = {
        'n_estimators': [100, 200, 300, 500],
        'max_depth': [3, 5, 7, 10, 15],
        'learning_rate': [0.5, 0.1, 0.05, 0.01]
    }
    
    primary_target = '당월_매출_금액'
    if primary_target not in y_train.columns:
        print(f"오류: 튜닝 기준 타겟 '{primary_target}'을 찾을 수 없습니다.")
        return

    tuning_results = []
    kf = KFold(n_splits=3, shuffle=True, random_state=42)

    print("하이퍼파라미터 튜닝 시작... (For문 기반)")
    param_combinations = np.prod([len(v) for v in param_grid.values()])
    print(f"총 {param_combinations}개의 파라미터 조합을 테스트합니다...")
    
    count = 0
    for n in param_grid['n_estimators']:
        for d in param_grid['max_depth']:
            for lr in param_grid['learning_rate']:
                count += 1
                current_scores = []
                for train_index, val_index in kf.split(X_train):
                    X_cv_train, X_cv_val = X_train.iloc[train_index], X_train.iloc[val_index]
                    y_cv_train, y_cv_val = y_train[primary_target].iloc[train_index], y_train[primary_target].iloc[val_index]
                    
                    pipeline = Pipeline(steps=[
                        ('preprocessor', preprocessor),
                        ('regressor', xgb.XGBRegressor(objective='reg:squarederror', 
                                                       n_estimators=n, max_depth=d, learning_rate=lr,
                                                       random_state=42, n_jobs=-1, verbosity=0))
                    ])
                    pipeline.fit(X_cv_train, y_cv_train)
                    score = pipeline.score(X_cv_val, y_cv_val)
                    current_scores.append(score)
                
                mean_score = np.mean(current_scores)
                tuning_results.append({
                    'n_estimators': n,
                    'max_depth': d,
                    'learning_rate': lr,
                    'mean_r2_score': mean_score
                })
                print(f"[{count}/{param_combinations}] 완료: n_est={n}, depth={d}, lr={lr} -> R2 Score={mean_score:.4f}")

    print("하이퍼파라미터 튜닝 완료.")
    
    results_df = pd.DataFrame(tuning_results)
    best_params_row = results_df.loc[results_df['mean_r2_score'].idxmax()]
    best_params = best_params_row.drop('mean_r2_score').to_dict()
    
    print("\n최적 하이퍼파라미터 조합:")
    print(best_params)
    print(f"최적 조합의 교차검증 R2 Score: {best_params_row['mean_r2_score']:.4f}")

    visualize_manual_tuning_results(results_df)
    
    if 'n_estimators' in best_params:
        best_params['n_estimators'] = int(best_params['n_estimators'])
    if 'max_depth' in best_params:
        best_params['max_depth'] = int(best_params['max_depth'])

    tuned_xgb = xgb.XGBRegressor(objective='reg:squarederror', random_state=42, n_jobs=-1, verbosity=0, **best_params)
    tuned_multioutput_model = MultiOutputRegressor(tuned_xgb)
    
    final_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', tuned_multioutput_model)
    ])
    
    final_pipeline.fit(X_train, y_train)
    y_pred = final_pipeline.predict(X_test)

    metrics_df = pd.DataFrame(columns=['MSE', 'RMSE', 'MAE', 'R2 Score'])
    for i, target_name in enumerate(final_target_cols):
        mse = mean_squared_error(y_test.iloc[:, i], y_pred[:, i])
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test.iloc[:, i], y_pred[:, i])
        r2 = r2_score(y_test.iloc[:, i], y_pred[:, i])
        metrics_df.loc[target_name] = [mse, rmse, mae, r2]

    print("\n최종 모델 평가 결과:")
    with pd.option_context('display.float_format', '{:,.2f}'.format):
        print(metrics_df)

    return final_pipeline, metrics_df


if __name__ == '__main__':
    tuned_model, final_metrics = train_final_model()

    if tuned_model:
        print("\n모델 학습 및 평가를 성공적으로 완료했습니다.")
    else:
        print("\n모델 학습에 실패했습니다. 위의 오류 메시지를 확인해주세요.")
