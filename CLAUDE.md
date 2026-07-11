# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

K리그 경기 이벤트 로그에서 각 공격 전개(`game_episode`)의 **마지막 패스 도착 좌표**(`end_x`, `end_y`)를 예측하는 Dacon 대회 프로젝트입니다. 평가 지표는 예측 좌표와 실제 좌표 간 **유클리드 거리 평균**이며, 최종 성적은 상위 30%(290/937)입니다.

필드 규격: `105 x 68` (FIFA 공식 규격). 예측값은 항상 이 범위 안으로 클리핑해야 합니다.

## Running the Pipelines

```bash
# 환경 설치
pip install -r requirements.txt

# 트리 기반 앙상블 V8 (최종 제출 모델)
python -m src.pipeline.train_v8_pipeline

# 시퀀스 딥러닝 V3
python train_sequence_v3.py
```

출력 결과물은 `models/`(모델 파일 및 결과 JSON)와 `data/submissions/`(제출 CSV)에 저장됩니다.

## Architecture

두 가지 독립적인 모델링 경로가 병렬로 존재합니다.

### 경로 A — 트리 기반 앙상블 (`src/pipeline/train_v8_pipeline.py`)
- LightGBM + XGBoost + CatBoost를 KFold(5-fold) + 다중 시드로 학습
- `game_episode` 단위로 집계된 피처를 사용 (마지막 이벤트 위치, 이벤트 타입별 평균 dx, 패스 각도 등)
- 과적합 위험 피처(`prev1_dist`, `angle_to_goal_diff` 등)는 의도적으로 제거됨
- 데이터 경로가 절대 경로(`E:/Dacon/kleague-pass-prediction/data/raw`)로 하드코딩되어 있음 — 환경 변경 시 수정 필요

### 경로 B — 시퀀스 멀티태스크 모델 (`train_sequence_v3.py` + `src/models/sequence_model_v3.py`)
- Transformer Encoder + BiLSTM + Attention 융합 구조
- Raw CSV에서 직접 시퀀스를 구성해 데이터 누수 방지 (parquet 경유 없음)
- 메인 태스크(`dx`, `dy`) + 보조 태스크(이벤트 타입/성공 여부/거리) 멀티태스크 학습
- 학습된 fold 가중치: `models/seq_v3_fold{1-5}.pt`
- CUDA 자동 감지: `torch.device('cuda' if torch.cuda.is_available() else 'cpu')`

### 공통 유틸리티 (`src/utils/`)
- `metrics.py`: `euclidean_distance`, `rmse_per_coordinate`, `clip_predictions` 등 평가 함수
- `paths.py`: `get_project_root()` 캐싱 기반 경로 헬퍼. `configs/`, `src/`, `data/` 세 폴더가 모두 존재하는 디렉토리를 루트로 인식

### 설정 (`configs/configs.yaml`)
모델 하이퍼파라미터, 피처 그룹 활성화 여부, 앙상블 가중치 등 핵심 설정이 집중되어 있습니다.

## Data Layout

```
data/raw/
├── train.csv          # 학습 이벤트 로그
├── test.csv           # 테스트 에피소드 목록 (좌표 없음)
├── test/<game_id>/*.csv  # 게임별 원시 이벤트 시퀀스
├── match_info.csv     # 경기 메타 정보
└── sample_submission.csv
```

테스트 에피소드 로드 시 `data/raw/test/` 하위 모든 CSV를 재귀 탐색해 concat합니다.

## Key Constraints

- `result_name` 컬럼의 NaN은 반드시 `'None'` 문자열로 채워야 합니다 (CatBoost 범주형 처리 이슈).
- 예측값 클리핑 범위: `end_x ∈ [0, 105]`, `end_y ∈ [0, 68]`.
- 시퀀스 모델의 최대 길이: `max_seq_length = 100` (`configs.yaml`).
