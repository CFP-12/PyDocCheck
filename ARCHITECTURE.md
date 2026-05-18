# PyDocCheck - 모듈 아키텍처

## 모듈 분담 체계

### 1️⃣ Repository 모듈 (정민경)
**위치**: `src/pydoccheck/repository/`

- GitHub Repository 접근
- 문서 파일 탐색 (README, /docs, /examples 등)
- 문서 로드 및 메타데이터 생성

**입력**: GitHub Repository URL  
**출력**: DocumentInfo 리스트 + 원본 문서 내용

---

### 2️⃣ Parsers 모듈 (백지유)
**위치**: `src/pydoccheck/parsers/`

- Markdown/RST 파싱
- Python 코드 블록 추출
- 메타데이터 매핑 (위치, 언어, ID)
- 코드 전처리 (주석 제거, 실행 가능성 판단)

**입력**: 문서 내용 + DocumentInfo  
**출력**: CodeBlock 리스트

---

### 3️⃣ Execution 모듈 (강인후)
**위치**: `src/pydoccheck/execution/`

- 가상 환경 생성 (venv)
- 패키지 설치 (pip)
- 코드 실행 (subprocess)
- 로그 수집 (stdout/stderr)
- 환경 정리

**입력**: CodeBlock 리스트  
**출력**: ExecutionResult 리스트

---

### 4️⃣ Reporting 모듈 (조혜준)
**위치**: `src/pydoccheck/reporting/`

- 실행 결과 분석
- 오류 유형 분류
- 통계 계산
- CLI/Markdown/JSON 리포트 생성
- 시각화 (그래프)

**입력**: ExecutionResult 리스트  
**출력**: 최종 리포트 (CLI, Markdown, JSON)

---

### 🔧 공유 모듈
**위치**: `src/pydoccheck/models/` & `src/pydoccheck/utils/`

- 모든 팀원이 사용하는 데이터 구조
- 공통 헬퍼 함수

---

## 데이터 흐름

```
Repository Module
    ↓
    └─→ (DocumentInfo + Content)
        ↓
    Parsers Module
        ↓
        └─→ (CodeBlock List)
            ↓
        Execution Module
            ↓
            └─→ (ExecutionResult List)
                ↓
            Reporting Module
                ↓
                └─→ Final Report (CLI/MD/JSON)
```

---

## 팀원별 독립 작업

각 팀원은 자신의 모듈 폴더 내에서만 작업하면 **다른 팀원 코드에 영향 없음**:

✅ **정민경**: `src/pydoccheck/repository/` 만 수정  
✅ **백지유**: `src/pydoccheck/parsers/` 만 수정  
✅ **강인후**: `src/pydoccheck/execution/` 만 수정  
✅ **조혜준**: `src/pydoccheck/reporting/` 만 수정

---

## 모듈 간 인터페이스

각 모듈은 **들어오는 데이터(Input)**와 **나가는 데이터(Output)**만 신경쓰면 됨:

| 모듈 | Input | Output | 의존성 |
|------|-------|--------|--------|
| Repository | URL | DocumentInfo | 없음 |
| Parsers | DocumentInfo | CodeBlock | models.CodeBlock |
| Execution | CodeBlock | ExecutionResult | models.CodeBlock |
| Reporting | ExecutionResult | Report | - |

**TIP**: Input/Output 데이터 구조는 `models/` 에 정의되어 있으므로, 먼저 필요한 데이터 모델을 추가하면 됩니다.

---

## 코드 리뷰 & 머지

1. 각자 자신의 모듈만 수정
2. `models/` 수정이 필요하면 **팀원과 협의**
3. PR 올릴 때 자신의 모듈만 포함
4. 다른 팀원의 코드는 건드리지 않기
