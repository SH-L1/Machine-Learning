# 📊 군집 기반 상권 매출 예측 플랫폼

## 👥 팀원
- 신승민  
- 신창영  
- 임성훈  
- 임지성  

---

## 🧩 프로젝트 개요

최근 자영업 시장의 침체가 사회적 문제로 이어지고 있습니다.  
본 프로젝트는 **유동인구, 날씨, 공휴일, 지역 연령대** 등 다양한 공공 데이터를 활용하여  
**클러스터 기반의 월 매출 예측 모델**을 만들고, 자영업자에게 다음을 지원합니다:

- ✔ 매출 예측  
- ✔ 재고 최적화  
- ✔ 인력 관리  
- ✔ 마케팅 전략 수립  

---

## 🎯 핵심 목표

1. **역 기반 지역 군집화** → 지역 단위 세분화  
2. **클러스터별 상권 매출 예측 모델 생성**  
3. **인사이트 제공** → 연령대, 요일별 수요 예측  
4. **자영업 지원형 웹 플랫폼 구축**  

---

## 📂 사용 데이터셋

| 데이터 | 설명 | 출처 |
|--------|------|------|
| 지하철/버스 승하차 | 역별 시간대 유동인구 | 서울열린데이터광장 |
| 상권 매출 | 월별 추정 매출 및 건수 | 서울시 상권분석 서비스 |
| 날씨 | 초단기 실황 (온도, 강수 등) | 기상청 API |
| 공휴일 | 연도별 공휴일 정보 | GitHub (holidays-kr) |
| 역 위치 | 위경도 좌표 | 국토교통부, 한국철도공사 |
| 연령 정보 | 지역별 평균 연령대 | 서울통계플랫폼 |

---

## ⚙️ 데이터 전처리 & 클러스터링

### ✅ 역 좌표 통합 (지하철 + 버스): 총 7,477개  
<img src="https://github.com/user-attachments/assets/d02fce3b-2e23-4b4e-bdd1-dc7d2b386dbb" width="600"/>

---

### ✅ KMeans 클러스터링

#### 📌 초기 K = 2550  
엘보우 + 실루엣계수를 통해 K=2550으로 초기 추정  
<img src="https://github.com/user-attachments/assets/7adebb16-a615-41c8-8bbe-2075bd0ac9ae" width="600"/>

#### 📌 상관관계가 낮게 형성됨  
<img src="https://github.com/user-attachments/assets/982e85b9-f30c-44ca-b2bb-35ea294afbf8" width="600"/>

#### 📌 최적 K ≈ 259 → 상관관계 증가  
K를 줄였을 때 상관관계가 증가  
<img src="https://github.com/user-attachments/assets/b9436e17-430a-49e4-bbbe-d66f85100f07" width="600"/>

#### 📌 K값 제거 후 상관관계 비교  
기존보다 높은 상관관계 확인됨  
<img src="https://github.com/user-attachments/assets/6410d254-32b1-4621-adc7-065ab1409dca" width="600"/>

---

### ✅ 메인 테이블 구성  
클러스터별 시간대 유동인구 + 상권 매출 + 날씨 + 공휴일  

<img src="https://github.com/user-attachments/assets/f969854c-c45c-44c2-89c5-5225f8e6b0a5" width="600"/>

---

## 📈 모델링

### 🔧 적용 알고리즘

- **RandomForest**
  
  최적의 파라미터 설정  
  <img src="https://github.com/user-attachments/assets/c1f77d51-f3ca-49ae-a9c2-0b48ffa565f9" width="600"/>

  실제값 - 예측값 시각화  
  <img src="https://github.com/user-attachments/assets/5db7ca2f-771c-4f24-bc8e-771aec58b752" width="600"/>

---

- **XGBoost**
  
  최적의 파라미터  
  <img src="https://github.com/user-attachments/assets/bd076ff7-1b60-4f7e-863e-f5439131d12c" width="600"/>

  실제값 - 예측값 시각화  
  <img src="https://github.com/user-attachments/assets/c9fa5e8f-30d5-427e-9530-497c25658e6b" width="600"/>

---

- **LightGBM**  

  최적의 파라미터  
  <img src="https://github.com/user-attachments/assets/056df880-aedb-48ae-beb5-57bea6fa0090" width="600"/>

  실제값 - 예측값 시각화  
  <img src="https://github.com/user-attachments/assets/2ea05277-a691-464e-b707-93d614aa9dbe" width="600"/>

---

### 🔍 평가 지표

- **RMSLE (Root Mean Squared Log Error)**  
- 이상치 제거 후 **27% 성능 향상** (7.1 → 5.17)

📷 *추천 시각화: RMSLE 비교 그래프, 모델별 예측 결과 시각화*

---

## 🧠 인사이트 예시

### 클러스터 100 (가양2동)

- 평균연령: 서울 2위 (50~60대 중심)  
- 매출에 영향 주는 변수:  
  - **60대 이상 비율**  
  - **요일: 수요일**

➡ 해당 요일에 **재고 확대**, **메뉴 타겟팅**, **직원 증원** 전략 추천

📷 *추천 이미지: 클러스터별 변수 영향력 그래프*

---

## 🛠️ 기술 스택

| 분류 | 도구 |
|------|------|
| 언어 | Python |
| 개발환경 | Google Colab |
| 주요 라이브러리 | Pandas, NumPy, Scikit-Learn, XGBoost, LightGBM, Folium |
| 시각화 도구 | Matplotlib, Plotly, Seaborn |

---

## 🖥️ 웹사이트 서비스 방향 (구현 계획)

| 기능 | 설명 |
|------|------|
| 위치 기반 군집 조회 | 사용자의 위치를 입력 → 소속 클러스터 자동 할당 |
| 매출 예측 결과 제공 | 해당 지역군의 월별 예측 매출 표시 |
| 연령 기반 인사이트 | 연령대-매출 상관 분석 기반 맞춤 전략 제공 |
| 관리자 UI (향후 확장) | 지역/요일별 인력 추천, 재고관리 예측 추가 예정 |

📷 *추천 이미지: 사용자 위치 기반 클러스터 맵 + 예측 UI 설계안*

---

## 📦 프로젝트 구조

