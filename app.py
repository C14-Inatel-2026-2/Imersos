import os
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFError, CSRFProtect
from dotenv import load_dotenv

from repository.emprestimo_repository import EmprestimoRepository
from repository.livro_repository import LivroRepository
from services.livro_service import LivroService

load_dotenv(Path(__file__).resolve().parent / ".env")

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

csrf = CSRFProtect(app)

# Configuração dos repositórios
pasta_dados = Path(__file__).resolve().parent / "dados"

livro_repository = LivroRepository(
    pasta_dados / "livros.json"
)

emprestimo_repository = EmprestimoRepository(
    pasta_dados / "emprestimos.json"
)

service = LivroService(
    livro_repository,
    emprestimo_repository
)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/livros")
def listar_livros():
    termo = request.args.get("termo", "").strip()
    campo = request.args.get("campo", "titulo").strip().lower()
    status = request.args.get("status", "").strip()
    erro_busca = None

    try:
        if termo:
            livros = service.buscar_livros(termo, campo)

        elif "termo" in request.args:
            livros = []
            erro_busca = "Informe um termo para realizar a busca."

        else:
            livros = service.listar_livros()

        if status:
            isbns_com_status = {
                livro.isbn
                for livro in service.filtrar_por_status(status)
            }

            livros = [
                livro
                for livro in livros
                if livro.isbn in isbns_com_status
            ]

    except ValueError as erro:
        livros = []
        erro_busca = str(erro)

    return render_template(
        "livros.html",
        livros=livros,
        termo=termo,
        campo=campo,
        status=status,
        erro_busca=erro_busca
    )


@app.post("/livros/<isbn>/status")
def alterar_status_livro(isbn):
    novo_status = request.form.get("status_leitura", "").strip()

    try:
        service.alterar_status(isbn, novo_status)

        flash(
            "Status de leitura atualizado com sucesso!",
            "sucesso"
        )

    except ValueError as erro:
        flash(str(erro), "erro")

    return redirect(url_for("listar_livros"))


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_livro():
    if request.method == "POST":

        try:
            ano = int(request.form.get("ano", "").strip())

        except ValueError:
            return render_template(
                "cadastrar.html",
                erro="Informe um ano de publicação válido."
            ), 400

        dados = {
            "titulo": request.form.get("titulo", "").strip(),
            "autor": request.form.get("autor", "").strip(),
            "isbn": request.form.get("isbn", "").strip(),
            "genero": request.form.get("genero", "").strip(),
            "ano": ano,
            "status_leitura": request.form.get(
                "status_leitura", ""
            ).strip()
        }

        try:
            service.cadastrar_livro(**dados)

            flash(
                "Livro cadastrado com sucesso!",
                "sucesso"
            )

            return redirect(url_for("cadastrar_livro"))

        except ValueError as erro:
            return render_template(
                "cadastrar.html",
                erro=str(erro)
            ), 400

    return render_template("cadastrar.html")


@app.route("/livros/<isbn>/editar", methods=["GET", "POST"])
def editar_livro(isbn):

    livro = next(
        (
            livro
            for livro in service.listar_livros()
            if livro.isbn == isbn
        ),
        None
    )

    if livro is None:
        flash("Livro não encontrado.", "erro")
        return redirect(url_for("listar_livros"))

    if request.method == "POST":

        try:
            ano = int(request.form.get("ano", "").strip())

        except ValueError:
            return render_template(
                "editar.html",
                livro=livro,
                erro="Informe um ano de publicação válido."
            ), 400

        dados = {
            "titulo": request.form.get("titulo", "").strip(),
            "autor": request.form.get("autor", "").strip(),
            "isbn": request.form.get("isbn", "").strip(),
            "genero": request.form.get("genero", "").strip(),
            "ano": ano,
            "status_leitura": request.form.get(
                "status_leitura", ""
            ).strip()
        }

        try:
            service.editar_livro(isbn, dados)

            flash(
                "Livro atualizado com sucesso!",
                "sucesso"
            )

            return redirect(url_for("listar_livros"))

        except ValueError as erro:
            return render_template(
                "editar.html",
                livro=livro,
                erro=str(erro)
            ), 400

    return render_template(
        "editar.html",
        livro=livro
    )


@app.post("/livros/<isbn>/remover")
def remover_livro(isbn):
    try:
        service.remover_livro(isbn)

        flash(
            "Livro removido com sucesso!",
            "sucesso"
        )

    except ValueError as erro:
        flash(str(erro), "erro")

    return redirect(url_for("listar_livros"))


@app.errorhandler(CSRFError)
def erro_csrf(erro):
    flash(
        "Não foi possível validar o formulário. "
        "Atualize a página e tente novamente.",
        "erro"
    )

    return redirect(url_for("index"))

