# 선형회귀-파라미터 없음
```py
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
from sklearn.model_selection import train_test_split

# 데이터 로드
data = pd.read_csv('/content/drive/MyDrive/찐막데이터.csv', encoding='cp949')

# 학습/테스트 분할
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

# MultiOutputRegressor 사용 (기본 모델: LinearRegression)
base_model = LinearRegression()
multi_model = MultiOutputRegressor(base_model)

# 모델 학습
multi_model.fit(X_train, y_train)

# 예측
y_pred = multi_model.predict(X_test)
target_cols = ['당월_매출_금액', '당월_매출_건수']
# 평가 함수
def evaluate_multioutput(y_true, y_pred, target_names):
    for i, name in enumerate(target_names):
        mse = mean_squared_error(y_true.iloc[:, i], y_pred[:, i])
        rmse = np.sqrt(mse)
        r2 = r2_score(y_true.iloc[:, i], y_pred[:, i])
        print(f"\n[📈 결과 - {name}]")
        print(f"MSE : {mse:.2f}")
        print(f"RMSE: {rmse:.2f}")
        print(f"R²  : {r2:.4f}")

# 결과 출력
evaluate_multioutput(y_test, y_pred, target_cols)

```
