import json
from pathlib import Path


class LivroRepository:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = Path(caminho_arquivo)

    def salvar(self, livros):
        # Cria o diretório pai caso ele ainda não exista
        self.caminho_arquivo.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(self.caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(
                livros,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def carregar(self):
        # Caso o arquivo ainda não exista, retorna uma lista vazia
        if not self.caminho_arquivo.exists():
            return []

        try:
            with open(self.caminho_arquivo, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)

        # Caso o arquivo exista, mas possua um JSON inválido
        except json.JSONDecodeError:
            return []