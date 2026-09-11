# Pag_g

레그(RAG) 챗봇 구현 연습.

> 최종 업데이트: 2026-09-11

## 기술 스택

| 구분 | 기술 | 용도 |
| --- | --- | --- |
| 언어 | Python 3.11 | 전체 구현 |
| LLM | [Ollama](https://ollama.com/) (로컬, `llama3.1`) | 답변 생성 |
| 벡터 스토어 | [ChromaDB](https://www.trychroma.com/) | 임베딩 저장 및 유사도 검색 |
| 문서 파싱 | [pypdf](https://pypi.org/project/pypdf/) | PDF 텍스트 추출 |
| 설정 관리 | [python-dotenv](https://pypi.org/project/python-dotenv/) | `.env` 환경변수 로드 |
| 테스트 | [pytest](https://pytest.org/) | 단위 테스트 |

## 진행 상태

- [x] 프로젝트 스캐폴딩 (`rag/`, `data/`, `tests/`, 환경변수 템플릿)
- [x] 문서 로더 — PDF/TXT 로딩, `data/` 디렉토리 스캔 (`rag/loader.py`)
- [ ] 청킹 — `RAG_CHUNK_SIZE` / `RAG_CHUNK_OVERLAP` 기반 문서 분할
- [ ] 임베딩 + 벡터 스토어 색인 (ChromaDB)
- [ ] 검색(retrieval) — `RAG_TOP_K` 기반 유사 청크 검색
- [ ] LLM 연동 — 로컬 Ollama로 답변 생성
- [ ] CLI / 실행 진입점

## 프로젝트 구조

```
Pag_g/
├── rag/                # RAG 챗봇 소스 패키지
│   ├── __init__.py
│   └── loader.py       # 문서 로더 (PDF/TXT)
├── data/               # 원본 문서 저장 위치 (git 추적 제외)
├── tests/              # 테스트
│   └── test_loader.py
├── .env.example        # 환경변수 템플릿 (.env 로 복사해 사용)
├── requirements.txt    # 의존성
└── README.md
```

## 개발 환경 준비

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env         # 이후 .env 값 채우기
```

LLM은 로컬 [Ollama](https://ollama.com/)를 사용한다. 서버를 띄우고 모델을 받아둔다.

```bash
ollama serve
ollama pull llama3.1
```

## 환경변수

`.env.example` 참고. 주요 값:

| 변수 | 설명 |
| --- | --- |
| `OLLAMA_HOST` | 로컬 Ollama 서버 주소 |
| `RAG_MODEL` | 답변 생성에 쓸 로컬 Ollama 모델 |
| `CHROMA_DIR` | 벡터 스토어 저장 경로 |
| `RAG_TOP_K` | 검색 시 가져올 청크 수 |
| `RAG_CHUNK_SIZE` / `RAG_CHUNK_OVERLAP` | 청킹 파라미터 |
