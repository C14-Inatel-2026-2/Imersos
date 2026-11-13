from pathlib import Path
from flask import Flask, render_template

from repository.livro_repository import LivroRepository
from services.livro_service import LivroService

app = Flask(__name__)

caminho = Path(__file__).resolve().parent / "dados" / "livros.json"

repository = LivroRepository(caminho)
service = LivroService(repository)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/livros")
def listar_livros():
    livros = service.listar_livros()
    return render_template("livros.html", livros=livros)
