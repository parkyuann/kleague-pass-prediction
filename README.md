# K-League 최종 패스 좌표 예측

K리그 경기 이벤트 로그를 바탕으로, 각 공격 전개(`game_episode`)의 **마지막 패스 도착 좌표**(`end_x`, `end_y`)를 예측하는 프로젝트입니다.  
대회 제출용 모델링을 넘어서, 원본 데이터 기반 파이프라인 구성과 Hard Case 분석까지 포함해 예측 실패 원인을 함께 검증했습니다.

[![DACON](https://img.shields.io/badge/DACON-Competition-blue)](https://dacon.io/competitions/official/236647/overview/description)

---

## 1. 프로젝트 목표

### 해결하려는 문제
- 단일 이벤트가 아닌 **공격 전개의 문맥**을 반영해 최종 패스 목적지를 예측
- 평가 지표인 유클리드 거리 기준으로 공간 오차를 최소화
- 평균 점수뿐 아니라 실패 사례를 분석해 모델 한계를 파악

### 결과
- Dacon 대회 기준 상위 30%(290/937)
- 트리 기반 앙상블(`v8`)을 최종 제출 모델로 채택

---

## 2. 접근 방식 개요

프로젝트는 두 가지 경로를 병행했습니다.

### A. 트리 기반 앙상블 (`src/pipeline/train_v8_pipeline.py`)
- 모델: LightGBM + XGBoost + CatBoost
- 전략:
  - 과적합 위험 피처 제거(`prev1_dist`, `angle_to_goal_diff` 등)
  - 정규화 강화(깊이/리프 제약, L1/L2 강화)
  - 다중 시드 + KFold로 예측 안정성 확보
- 출력: 테스트 `game_episode`별 `end_x`, `end_y` 제출 파일 생성

### B. 시퀀스 멀티태스크 모델 (`train_sequence_v3.py`, `src/models/sequence_model_v3.py`)
- 모델: Transformer Encoder + BiLSTM + Attention 융합
- 전략:
  - 원본 CSV에서 직접 시퀀스를 구성해 데이터 누수 방지
  - 메인 태스크(`dx`, `dy`) + 보조 태스크(이벤트 타입/성공 여부/거리) 멀티태스크 학습
  - 5-Fold 학습 후 fold 앙상블 예측

---

## 3. 데이터와 문제 정의

### 입력/출력
- 입력: 각 `game_episode` 내 이벤트 시퀀스
- 출력: 마지막 이벤트의 패스 도착 좌표 `end_x`, `end_y`

### 사용 데이터
- `data/raw/train.csv`
- `data/raw/test.csv`
- `data/raw/test/<game_id>/*.csv`
- `data/raw/match_info.csv`
- `data/raw/sample_submission.csv`

### 좌표 기준
- 필드 크기: `105 x 68` (FIFA 규격)
- 주요 평가: 유클리드 거리 평균

---

## 4. 학습/추론 파이프라인

1. 원본 CSV 로드 및 `game_episode` 단위 재구성  
2. 피처 생성(트리 경로) 또는 시퀀스 구성(딥러닝 경로)  
3. KFold 기반 학습 및 OOF 검증  
4. 테스트 에피소드 추론 후 좌표 범위 클리핑  
5. `sample_submission` 키 기준으로 최종 제출 파일 생성  

`src/utils/metrics.py`에서 유클리드 거리, RMSE, MAE 지표 계산 유틸을 제공합니다.

---

## 5. Hard Case 분석

점수만 비교하지 않고, 고오차 샘플을 별도로 시각화해 패턴을 점검했습니다.

- 수비/중앙 지역 시작 패스에서 예측 난이도 증가
- 긴 패스 구간에서 실제보다 짧게 예측하는 경향(under-prediction) 확인
- 모델 개선 방향(극단값 대응 손실, 맥락 피처 확장) 도출

---

## 6. 주요 시각화

핵심 결과를 빠르게 확인할 수 있는 시각화만 선별했습니다.

### 실제 vs 예측 패스 비교
모델이 일반적인 전개에서는 얼마나 근접하게 좌표를 맞추는지 보여줍니다.

<img width="1990" height="786" alt="실제 vs 예측 패스 비교" src="https://github.com/user-attachments/assets/2e83d4aa-caaa-4bf9-aa11-eaa11960977f" />

### 에러 크기별 시작점 분포
어떤 지역에서 오차가 커지는지(난이도 높은 구역) 확인할 수 있습니다.

<img width="2349" height="1419" alt="에러 크기별 패스 시작점 분포" src="https://github.com/user-attachments/assets/d85b73d4-9f97-4cf9-8f9e-393cf94f0794" />

### 실제 vs 예측 패스 거리
롱패스 구간에서 발생하는 under-prediction 패턴을 확인할 수 있습니다.

<img width="1389" height="490" alt="실제 vs 예측 패스 거리" src="https://github.com/user-attachments/assets/c3617ae5-427e-41fc-a243-66d96e107ce2" />

### 가장 예측이 어려운 패스 사례
Hard Case 샘플을 직접 확인해 실패 유형을 분석할 수 있습니다.

<img width="1239" height="889" alt="가장 예측이 어려운 패스 20개" src="https://github.com/user-attachments/assets/55f1da0f-6ee6-4a0e-822a-358e0da46f3c" />

---

## 7. 실행 방법

### 환경 준비
```bash
pip install -r requirements.txt
```

### 트리 기반 V8 파이프라인 실행
```bash
python -m src.pipeline.train_v8_pipeline
```

### 시퀀스 V3 모델 실행
```bash
python train_sequence_v3.py
```

실행 후 결과물은 주로 `models/`, `data/submissions/`에 저장됩니다.

---

## 8. 디렉터리 구조

```text
kleague-pass-prediction/
├─ configs/
│  └─ configs.yaml
├─ data/
│  ├─ raw/
│  └─ submissions/
├─ docs/
├─ models/
├─ notebooks/
├─ src/
│  ├─ models/
│  ├─ pipeline/
│  └─ utils/
├─ train_sequence_v3.py
├─ requirements.txt
└─ README.md
```

---

## 9. 개선 방향

- 시계열 분할 기반 검증으로 실제 배포 시나리오와의 정합성 강화
- 롱패스/희소 상황에 가중치를 주는 손실 함수 실험
- 트리 모델과 시퀀스 모델의 후처리 결합(스태킹/재순위화) 검토
