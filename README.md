# K-League 최종 패스 좌표 예측 프로젝트

K리그 경기 이벤트 로그를 활용해 마지막 패스 도착 좌표(end_x, end_y)를 예측하고, 공간 패턴과 오차 특성을 분석한 프로젝트입니다. 데이콘 대회를 바탕으로 진행했으며, 단순 제출 코드 재현이 아니라 이벤트 단위 원본 데이터를 game_episode 단위 학습 데이터로 재구성하고 모델 비교, 오차 분석 및 성능 개선까지 포함한 포트폴리오형 프로젝트로 확장했습니다.

[![DACON](https://img.shields.io/badge/DACON-Competition-blue)](https://dacon.io/competitions/official/236647/overview/description)
<hr style="background-color: #30363d; height: 1px; border: none; width: 90%;">

## 1. 프로젝트 요약

- 목표: 선수 및 경기 이벤트 데이터를 활용한 패스 도달 지점 예측
- 성과: Dacon 대회 상위 30%(290/937) 달성
- 핵심 강점: 모델링에 그치지 않고, 예측 실패 사례(Hard Cases)를 시각화하여 데이터의 특성을 분석하고 개선 방향을 도출함.
<hr style="background-color: #30363d; height: 1px; border: none; width: 90%;">

## 2. 모델 실험 및 비교 분석

최적의 예측 성능을 도출하기 위해 정형 데이터에 강한 트리 모델과 시계열 특성을 반영한 딥러닝 모델 두 가지 경로로 실험을 진행했습니다.

### 📊 모델 성능 비교

| 비교 항목 | 트리 기반 앙상블 (v8_pipeline) | 딥러닝 시퀀스 모델 (v3) |
| :---: | :---: | :---: |
| **모델 구조** | LightGBM + XGBoost + CatBoost | GRU/LSTM 기반 Multi-task Model |
| **핵심 전략** | **과적합 제어 및 다중 시드 앙상블** | 경기 흐름(이벤트 시퀀스) 학습 시도 |
| **검증 점수** | **OOF Score: 14.4575 (최종 채택)** | 성능 실험 및 분석 수행 |

### 🎯 V8 Pipeline: 과적합 완화 전략
단순 점수 향상이 아닌, 모델의 일반화 성능(Generalization)을 극대화하기 위해 V8 버전에서 다음의 **과적합 완화 전략**을 적용했습니다.

1. **피처 정제 (Feature Selection)**
   - Dist shift가 크거나 노이즈가 심한 6개 피처 제거 (22개 → **16개**)
   - `last_dist_to_goal`, `prev1_dist` 등 과적합 위험 요소 배제
2. **정규화 및 하이퍼파라미터 최적화**
   - **LightGBM**: `num_leaves` 하향 (63 → 31), `max_depth=5` 제한
   - **Regularization**: `l2_leaf_reg=5` 적용 및 학습률(`learning_rate`) 최적화
3. **다중 시드 앙상블 (Multi-seed Ensemble)**
   - 7개의 서로 다른 Seed(42, 123, 456, 789, 1004, 2024, 3333) 활용
   - 총 35개 모델(7 seeds × 5-folds)의 예측값을 결합하여 변동성 최소화
4. **데이터 무결성 유지**
   - `dy` 예측을 방해할 수 있는 Y-flip 데이터 증강을 제거하여 예측 정교도 향상

### 📈 최종 검증 결과 (Validation Summary)
- **Feature Count**: 16 Features
- **Ensemble Strategy**: Soft Voting (LGBM + XGB + CatBoost)
- **V8 OOF Score (Mean Euclidean Distance)**: <kbd>**14.4575**</kbd>

<hr style="background-color: #30363d; height: 1px; border: none; width: 90%;">

## 3. 주요 수행 내용

### 🛠️ 데이터 파이프라인 및 모델링 (train_v8_pipeline.py)

- **앙상블 기법 적용**: 세 가지 부스팅 모델의 편향을 상쇄하기 위해 Soft Voting 방식의 앙상블 적용
- **피처 정제**: 변별력이 낮거나 노이즈가 심한 피처(prev1_dist, angle_to_goal_diff 등)를 제거하여 모델의 안정성 확보.
- **실험 자동화**: AI 에이전트(Claude Code)를 활용해 피처 생성부터 하이퍼파라미터 튜닝까지의 사이클을 자동화하여 개발 속도를 높임.

### 🔍 에러 분석 및 시각화 (03_Hard_Cases_Visualization.ipynb)

단순 오차 수치 확인을 넘어, 실제 축구장 좌표 위에서 모델이 왜 틀렸는지를 시각화를 통해 분석했습니다.

<img width="1990" height="786" alt="패스 시작점 비교" src="https://github.com/user-attachments/assets/1de5bde1-c1f7-4628-ba3b-f77e3f7a2077" />
<img width="1390" height="490" alt="패스 각도 분석" src="https://github.com/user-attachments/assets/366e7ab1-e944-49cd-b2fe-d688822aacc8" />
<img width="2349" height="1419" alt="에러 크기별 패스 시작점 분포" src="https://github.com/user-attachments/assets/d85b73d4-9f97-4cf9-8f9e-393cf94f0794" />
<img width="1990" height="786" alt="실제 vs 예측 패스 비교" src="https://github.com/user-attachments/assets/2e83d4aa-caaa-4bf9-aa11-eaa11960977f" />
<img width="1389" height="490" alt="실제 vs 예측 패스 거리" src="https://github.com/user-attachments/assets/c3617ae5-427e-41fc-a243-66d96e107ce2" />
<img width="1921" height="820" alt="시작점 밀도 비교" src="https://github.com/user-attachments/assets/4958e455-6a7e-4bba-8385-0df6b11068f1" />
<img width="1389" height="490" alt="에러 분포" src="https://github.com/user-attachments/assets/1771da7a-261e-47e6-871a-2efbb2b213a1" />
<img width="1239" height="889" alt="가장 예측이 어려운 패스 20개" src="https://github.com/user-attachments/assets/55f1da0f-6ee6-4a0e-822a-358e0da46f3c" />

### Hard Cases 분석 결과

- **지역별 편차** <br> 수비 지역 및 중앙 지역에서 시작되는 패스의 예측 난이도가 상대적으로 높음.
- **Under-prediction 현상** <br> 20m 이상의 롱패스에서 실제 거리보다 짧게 예측하는 '평균 회귀' 경향 확인. 이는 모델이 안정적인 값을 선택하려는 성향 때문에 발생함.
<hr style="background-color: #30363d; height: 1px; border: none; width: 90%;">

## 4. 핵심 인사이트 및 한계점

### 💡 인사이트

- **이벤트 기반 거리 예측**: 'Carry'나 'Pass' 등 이벤트 타입별 평균 이동 거리가 예측의 강력한 기준점이 됨을 확인.
- **도메인 지식의 중요성**: 축구의 전술적 특성상 전진 패스와 횡패스의 물리적 데이터 특성이 다름을 시각화로 증명.

### ⚠️ 프로젝트의 한계점

- **극단값 예측 미흡**: 모델이 전체적인 평균을 맞추려다 보니, 결정적인 롱패스나 창의적인 킬패스 같은 Outlier를 충분히 포착하지 못함.
- **상황 정보 부족**: 주변 수비수의 위치나 패스를 받는 선수의 속도 등 세부적인 맥락 데이터가 결여되어 예측의 정교함에 한계가 있음.
- **개선 방향**: 향후 롱패스 오차에 더 높은 가중치를 주는 커스텀 손실 함수(Weighted Loss) 도입과 트리 모델-시퀀스 모델을 결합한 하이브리드 구조를 검토 중.

## 6. 기술 스택

<h3>🛠 Stacks</h3>

<table align="center">
  <tr>
    <td align="center" width="150px"><b>언어</b></td>
    <td>
      <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/>
    </td>
  </tr>
  <tr>
    <td align="center"><b>분석 / 모델링</b></td>
    <td>
      <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white"/>
      <img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white"/>
      <img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white"/>
      <img src="https://img.shields.io/badge/LightGBM-7AC331?style=flat-square&logo=github&logoColor=white"/>
      <img src="https://img.shields.io/badge/XGBoost-2A9D8F?style=flat-square&logo=github&logoColor=white"/>
      <img src="https://img.shields.io/badge/CatBoost-FFD200?style=flat-square&logo=github&logoColor=black"/>
      <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white"/>
    </td>
  </tr>
  <tr>
    <td align="center"><b>시각화</b></td>
    <td>
      <img src="https://img.shields.io/badge/Matplotlib-ffffff?style=flat-square&logo=matplotlib&logoColor=black"/>
      <img src="https://img.shields.io/badge/Seaborn-4479A1?style=flat-square&logo=python&logoColor=white"/>
    </td>
  </tr>
  <tr>
    <td align="center"><b>개발 도구</b></td>
    <td>
      <img src="https://img.shields.io/badge/Claude%20Code-D97757?style=flat-square&logo=anthropic&logoColor=white"/>
      <img src="https://img.shields.io/badge/Cursor%20CLI-51A19A?style=flat-square&logo=visualstudiocode&logoColor=white"/>
    </td>
  </tr>
</table>
