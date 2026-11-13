from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash
import os

from repository.livro_repository import LivroRepository
from services.livro_service import LivroService

app = Flask(__name__)

caminho = Path(__file__).resolve().parent / "dados" / "livros.json"

repository = LivroRepository(caminho)
service = LivroService(repository)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "chave-apenas-para-desenvolvimento"
)

 
@app.get("/")
def index():
    return render_template("index.html")

@app.get("/livros")
def listar_livros():
    livros = service.listar_livros()
    return render_template("livros.html", livros=livros)

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_livro():
    if request.method == "POST":
        try:
            dados = {
                "titulo": request.form.get("titulo", "").strip(),
                "autor": request.form.get("autor", "").strip(),
                "isbn": request.form.get("isbn", "").strip(),
                "genero": request.form.get("genero", "").strip(),
                "ano": int(request.form.get("ano", "")),
                "status_leitura": request.form.get("status_leitura", "")
            }

            service.cadastrar_livro(**dados)

            flash("Livro cadastrado com sucesso!", "sucesso")
            return redirect(url_for("cadastrar_livro"))

        except ValueError as erro:
            mensagem = (
                "Informe um ano inteiro válido."
                if "invalid literal" in str(erro)
                else str(erro)
            )
            return render_template(
                "cadastrar.html", erro=mensagem
            ), 400

    return render_template("cadastrar.html")
