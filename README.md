# 6조 기계학습 프로젝트 - 매출 예측을 위한 군집 기반 분석

### 👥 팀원
- 신승민  
- 신창영  
- 임성훈  
- 임지성  
---

## 📌 프로젝트 개요

본 프로젝트는 서울 시내의 버스 및 지하철 역 좌표 데이터를 활용하여 군집화를 수행한 후,<br><br>
각 군집에 대해 매출을 예측하는 모델을 개발하는 데 목적이 있습니다.<br><br>
궁극적으로 자영업자들에게 유용한 매출 인사이트를 제공하는 웹 기반 서비스를 구현하고자 합니다.

---

## 📊 데이터 구성 및 전처리

- **초기 데이터**
  - 역 개수: 11,561개
  - 중복 제거 후 고유 역 수: 7,477개

- **전처리**
  - 중복된 역(예: 광화문역) 통합
  - 좌표 기반 시각화
  - 버스역 + 지하철역 통합 산점도 생성

<img src="https://github.com/user-attachments/assets/9a71cf1d-65fb-4cef-8dc6-afb40f4b2c55" width="1000"/>

> 🡆  서울 시내 7477개 역의 분포를 지도 위에 시각화한 결과

---

## 🔍 데이터 분석 및 군집화

- **군집화 대상:** 7,477개의 역
- **기법:** K-Means

- **K 값 탐색**
  - 엘보우 기법 기준: inertia가 완만해지는 지점 ≈ K=25 이상
  - 실루엣 계수 기준: 최대값 K=2550 → 과적합 우려


<img src="https://github.com/user-attachments/assets/d02fce3b-2e23-4b4e-bdd1-dc7d2b386dbb" width="400"/>

> 🡆  K-Means로 군집화한 7477개의 역. 각 색상은 서로 다른 군집을 나타냄.


<img src="https://github.com/user-attachments/assets/8ee302bc-9193-4bc6-ab12-b76d7c083f7e" width="600"/>

> 🡆  엘보우 기법을 사용한 inertia 분석. K값이 약 25 이상부터 효과 감소.


<img src="https://github.com/user-attachments/assets/0fb1ebe7-b9e6-4745-ab5f-6634bff64a87" width="600"/>

> 🡆  K값에 따른 실루엣 계수. 2550일 때 가장 높지만, 해석 가능성 낮음.

- **최적 K 값 결정**
  - 최종 군집 수: K=259
  - 이유: 많은 군집을 통합하면서도 유의미한 상관관계 확보

<img src="https://github.com/user-attachments/assets/a9217159-ac7c-41cc-bc7b-88a1c5b3dbce" width="600"/>

> 🡆  최종 선정된 K=259일 때의 군집화 결과. 변수 간 상관관계 개선됨.

---

## 🏗️ 기준 테이블 구성

- 기준 테이블: 지하철/버스의 시간대별 승하차 데이터 (0시 ~ 23시)
- 2550개 군집 기반의 최종 통합 테이블
- 메인 데이터셋 구축

<img src="https://github.com/user-attachments/assets/3dc244dd-5e60-43ba-ad09-82d93da217e4" width="600"/>

> 🡆  메인데이터셋


---

## 📉 예측 모델링

### 사용된 모델
- 선형 회귀 (Baseline)
- XGBoost
- LightGBM
- 랜덤 포레스트

### 성능 비교 (RMSLE)

| 모델 유형             | RMSLE        |
|----------------------|--------------|
| Baseline (선형 회귀)*10^9 | 3.79266662887 |
| 프로젝트 모델 (스택킹)*10^9  | 0.00899928144 |


---
## 🧹 데이터 전처리 및 피처 엔지니어링

- **0의 값을 1e-5로 대체**하여 로그 스케일 계산의 안정성 확보  
- **시간당 유동인구 증가율**: (i+1시 유동인구) / (i시 유동인구)  
- **시간당 유동인구 증가값**: (i+1시 유동인구) - (i시 유동인구)  
- 두 피처는 모델이 시간중요도 도출 사례

---

## 🖥️ 웹사이트 UI (시안)

- 사용자의 위치 입력 → 해당 클러스터 자동 예측  
- 예측 결과 및 관련 인사이트 시각화 제공  
- 예: 특정 요일의 재고 보충, 인력 배치 추천 등  


<img src="https://github.com/user-attachments/assets/3a15c426-462a-4cf0-9356-352a3859c940" width="600"/>

> 🡆  메인화면 UI

<img src="https://github.com/user-attachments/assets/019b9922-436b-44bc-beaa-2292432455cc" width="600"/>

> 🡆  사용자 위치 군집

<img src="https://github.com/user-attachments/assets/b73b428b-cd88-4ed0-b80d-eab39ff5ed89" width="600"/>

> 🡆  클러스터 기반 지역분석을 통한 인사이트 제공

<img src="https://github.com/user-attachments/assets/50798a3f-4219-4bd8-95e2-2b0ce6ab1bff" width="600"/>

> 🡆  인사이트 기반 제고관리

<img src="https://github.com/user-attachments/assets/b801722b-e357-47c9-bdc0-6d92d366c35a" width="600"/>

> 🡆  인사이트 기반 인력관리


---

## 🛠️ 기술 스택

- **프레임워크**: Scikit-Learn
- **라이브러리**: Numpy, Pandas
- **개발환경**: Google Colab


