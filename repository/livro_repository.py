import json
from pathlib import Path


class LivroRepository:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = Path(caminho_arquivo)

    def salvar(self, livros):
        with open(self.caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(
                livros,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def carregar(self):
        if not self.caminho_arquivo.exists():
            return []

        try:
            with open(self.caminho_arquivo, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)

        except json.JSONDecodeError:
            return []