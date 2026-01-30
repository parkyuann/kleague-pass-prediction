# K-League Pass Destination Prediction

> **K리그 경기 데이터 기반 패스 도착 좌표 예측 AI 프로젝트**
> 실제 경기 맥락을 이해하는 모델 설계와 분석 중심의 접근을 목표로 했습니다.

---

## 📌 Project Summary (1-minute read)

* **Competition**: Dacon Track1 – K리그·서울시립대 공개 AI 경진대회
* **Task**: 공격 전개 시퀀스의 *마지막 패스 도착 좌표(X, Y)* 예측
* **Type**: Regression
* **Metric**: Euclidean Distance
* **Key Point**: 단순 좌표 예측이 아닌, *전술적 맥락(Context)* 학습

---

## 1. How We Approached the Problem (Our Perspective)

이 프로젝트에서 가장 먼저 고민한 것은 **“모델이 무엇을 학습해야 하는가”**였습니다.

패스 도착 좌표 예측은 표면적으로는 단순한 회귀 문제처럼 보이지만, 실제로는 다음과 같은 복합적인 맥락을 포함합니다.

* 이전 플레이들의 흐름
* 공간 점유와 압박 상황
* 공격 전개의 방향성과 의도

우리는 이 문제를 **"좌표를 맞히는 문제"가 아니라, 공격 전개 맥락을 학습하는 문제**로 재정의했습니다.

따라서 개별 이벤트의 의미보다, **시퀀스 전체가 하나의 정보 단위가 되도록 입력을 구성하는 것**을 핵심 전략으로 삼았습니다.

---

## 2. Problem Definition (Reframed)

* **Input**: 하나의 공격 전개를 구성하는 플레이 시퀀스
* **Output**: 마지막 패스의 도착 좌표 (X, Y)

모든 좌표는 FIFA 권장 규격(105 × 68) 기준으로 정규화되어 있으며,
본 프로젝트에서는 이를 단순 좌표 예측이 아닌 **공간적 의사결정 결과를 추정하는 회귀 문제**로 정의했습니다.

* **Input**: 하나의 공격 전개를 구성하는 플레이 시퀀스
* **Output**: 마지막 패스의 도착 좌표 (X, Y)

모든 좌표는 FIFA 권장 규격(105 × 68) 기준으로 정규화되어 있으며,
본 문제는 **경기 흐름과 공간 점유 패턴을 간접적으로 학습하는 고차원 회귀 문제**로 정의했습니다.

---

## 3. Dataset Overview

* 실제 K리그 경기 데이터
* 경기장 크기 차이를 보정한 상대 좌표계 사용

**Used Files**

* `train.csv`, `test.csv`
* `test/{game_id}/{episode}.csv`
* `match_info.csv`

---

## 4. Modeling & Pipeline Design (What We Actually Did)

```
Raw Sequence Data
→ Sequence-aware Preprocessing
→ Input Reconstruction
→ Model Training
→ Inference
→ Error Analysis & Visualization
```

### 🔹 Why This Pipeline?

* 경기 데이터는 **고정 길이 입력이 아니며**, 에피소드마다 구조가 다릅니다.
* 따라서 단순 피처 엔지니어링보다, **시퀀스 구조를 최대한 보존하는 전처리**가 중요하다고 판단했습니다.

우리는 학습과 추론을 명확히 분리한 파이프라인을 구성하여:

* 반복 실험이 가능하고
* 코드 검증 환경에서도 그대로 재현될 수 있도록 설계했습니다.

또한 평가 지표가 Euclidean Distance였기 때문에,
좌표 축별 오차를 줄이기보다는 **공간적 거리 자체를 최소화하는 방향**으로 학습 전략을 설계했습니다.

---

## 5. Error Analysis: Hard Case Focus ⭐ (Our Key Differentiator)

대부분의 실험에서는 평균 성능 지표만으로 모델을 평가하지만,
우리는 **"어디서 틀리는가"가 모델 이해의 핵심**이라고 판단했습니다.

### What We Did

* 예측 오차가 큰 샘플(Hard Case) 선별
* 실제 패스 좌표 vs 예측 좌표 시각화
* 상황별 실패 패턴 분류

### What We Learned

* 특정 전개 유형(긴 패스, 측면 전환)에서 오차가 집중됨
* 이는 입력 시퀀스만으로는 표현되지 않는 맥락 정보의 한계를 시사

이 분석을 통해 모델의 성능뿐 아니라 **한계와 개선 방향까지 명확히 인식**할 수 있었습니다.

⭐
본 프로젝트의 핵심 차별점은 **Hard Case 분석**입니다.

단순히 평균 성능 지표에 의존하지 않고,

* 예측 오차가 큰 샘플을 선별
* 실제 패스 좌표 vs 예측 좌표 시각화
* 실패 패턴을 상황별로 분석

이를 통해 모델이 **어떤 맥락을 학습하지 못했는지**를 구조적으로 파악했습니다.

---

## 6. Evaluation

* **Metric**: Euclidean Distance
* Public / Private 데이터 분리 평가
* 상위 팀 대상 코드 검증 포함

본 프로젝트는 단순 성능 경쟁을 넘어,
**모델 설계 논리와 재현 가능성까지 평가받는 경험**이었습니다.

---

## 7. What This Project Says About Us

이 프로젝트를 통해 우리는 다음과 같은 역량을 보여주고자 했습니다.

* 문제를 주어진 형태 그대로 받아들이지 않고 **재정의하는 사고력**
* 점수 중심이 아닌 **모델 이해 중심의 분석 접근**
* 실패 사례를 통해 모델의 한계를 구조적으로 해석하는 능력
* 코드 검증 환경을 고려한 **재현 가능한 파이프라인 설계**

본 프로젝트는 공모전 참가 경험을 넘어,
**실제 데이터 문제를 어떻게 정의하고 풀어가는지에 대한 하나의 사례**입니다.

---

## 🔗 Links

* **GitHub Repository**
  [https://github.com/parkyuann/kleague-pass-prediction](https://github.com/parkyuann/kleague-pass-prediction)

