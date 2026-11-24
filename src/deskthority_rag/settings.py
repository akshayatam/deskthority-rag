import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModelConfig:
    provider: str
    model: str


@dataclass(frozen=True)
class ModelsConfig:
    llm: ModelConfig
    embedding: ModelConfig
    reranker: ModelConfig


def load_models_config(path: Path) -> ModelsConfig:
    with path.open("rb") as file:
        config = tomllib.load(file)

    return ModelsConfig(
        llm=ModelConfig(
            provider=config["llm"]["provider"],
            model=config["llm"]["model"],
        ),
        embedding=ModelConfig(
            provider=config["embedding"]["provider"],
            model=config["embedding"]["model"],
        ),
        reranker=ModelConfig(
            provider=config["reranker"]["provider"],
            model=config["reranker"]["model"],
        ),
    )
