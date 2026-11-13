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
    termo = request.args.get("termo", "").strip()
    campo = request.args.get("campo", "titulo").strip().lower()
    erro_busca = None

    try:
        if termo:
            livros = service.buscar_livros(termo, campo)
        elif "termo" in request.args:
            livros = []
            erro_busca = "Informe um termo para realizar a busca."
        else:
            livros = service.listar_livros()

    except ValueError as erro:
        livros = []
        erro_busca = str(erro)

    return render_template(
        "livros.html",
        livros=livros,
        termo=termo,
        campo=campo,
        erro_busca=erro_busca
    )

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

@app.route("/livros/<isbn>/editar", methods=["GET", "POST"])
def editar_livro(isbn):
    livro = next(
        (livro for livro in service.listar_livros()
         if livro.isbn == isbn),
        None
    )

    if livro is None:
        flash("Livro não encontrado.", "erro")
        return redirect(url_for("listar_livros"))

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

            service.editar_livro(isbn, dados)

            flash("Livro atualizado com sucesso!", "sucesso")
            return redirect(url_for("listar_livros"))

        except ValueError as erro:
            return render_template(
                "editar.html",
                livro=livro,
                erro=str(erro)
            ), 400

    return render_template("editar.html", livro=livro)

@app.post("/livros/<isbn>/remover")
def remover_livro(isbn):
    try:
        service.remover_livro(isbn)

        flash("Livro removido com sucesso!", "sucesso")

    except ValueError as erro:
        flash(str(erro), "erro")

    return redirect(url_for("listar_livros"))
