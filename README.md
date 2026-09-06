# Pag_g

레그(RAG) 챗봇 구현 연습.

## 프로젝트 구조

```
Pag_g/
├── rag/                # RAG 챗봇 소스 패키지 (구현 예정)
│   └── __init__.py
├── data/               # 원본 문서 저장 위치 (git 추적 제외)
├── tests/              # 테스트
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
