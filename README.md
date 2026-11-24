# Vintage Wiki RAG

**A citation-first AI research assistant for vintage mechanical keyboards.**

Vintage Wiki RAG transforms community-maintained keyboard documentation into searchable, verifiable technical knowledge using hybrid retrieval, local language models, and Agentic RAG.

**Status:** In development  
**Initial scope:** Alps SKCL/SKCM switch documentation from the MK Wiki  
**Target corpus:** Approximately 4,000 Markdown documents

## Objectives

- Deliver accurate, source-grounded answers with citations.
- Support technical queries about switches, variants, and part numbers.
- Enable cross-document comparisons and multi-step reasoning.
- Build a modular, locally deployable retrieval system.
- Measure retrieval quality, factual accuracy, and performance.

## Technology Stack

| Component | Technology |
|---|---|
| LLM | Qwen3.5-9B |
| Embeddings | Qwen3-Embedding-0.6B |
| Reranking | Qwen3-Reranker-0.6B |
| Vector Database | Qdrant |
| Framework | LangChain |
| Agent Orchestration | LangGraph |
| Inference | Ollama |
| Backend | FastAPI |
| Evaluation | RAGAS, custom benchmarks |

## Implementation Timeline

| Phase | Milestone | Deliverable |
|---|---|---|
| 01 | Data Foundation | Markdown ingestion, normalization, metadata, and chunking |
| 02 | Baseline RAG | Local embeddings, Qdrant indexing, and cited responses |
| 03 | Advanced Retrieval | Hybrid search, reranking, and identifier matching |
| 04 | Agentic RAG | Query routing, multi-step retrieval, and evidence validation |
| 05 | Evaluation | Retrieval benchmarks, answer quality tests, and performance analysis |
| 06 | Application | FastAPI, chat interface, and source exploration |
| 07 | Expansion | Incremental indexing and full corpus integration |

## System Architecture

```text
Markdown Corpus
    |
Document Processing
    |
Embedding + Indexing
    |
Qdrant Vector Database
    |
Hybrid Retrieval
    |
Reranking
    |
LangChain / LangGraph
    |
Local LLM
    |
Cited Response
```

## Development Strategy

The first implementation focuses exclusively on Alps switch documentation.

Each phase establishes a measurable baseline before introducing additional complexity. The system will expand to the full corpus only after retrieval quality and citation accuracy are validated.

## Sources and Attribution

The project draws on community-maintained resources, including the [Deskthority Wiki](https://deskthority.net/wiki/Main_Page).

Original sources are credited and linked wherever applicable. Source content remains subject to its respective licensing terms.

This project is independent and is not affiliated with Deskthority.

## Project Status

Active development. Architecture, components, and milestones may evolve as evaluation results become available.
