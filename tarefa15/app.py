import os
import json
from datetime import datetime
from functools import wraps

import requests
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, session, request, flash

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "chave-temporaria")

SUAP_API_BASE = "https://suap.ifrn.edu.br/api/"

oauth = OAuth(app)

oauth.register(
    name="suap",
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    access_token_url="https://suap.ifrn.edu.br/o/token/",
    authorize_url="https://suap.ifrn.edu.br/o/authorize/",
    api_base_url=SUAP_API_BASE,
)


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "access_token" not in session:
            flash("Faça login com o SUAP para acessar esta página.", "warning")
            return redirect(url_for("index"))
        return func(*args, **kwargs)

    return wrapper


def primeiro_valor(*valores, padrao=""):
    for valor in valores:
        if valor not in [None, ""]:
            return valor
    return padrao


def procurar_valor_recursivo(dados, campos_procurados):
    """
    Procura um campo dentro de dicionários/listas, inclusive dados aninhados.
    Isso ajuda porque a API do SUAP pode retornar nome, matrícula e foto
    em lugares diferentes dependendo do usuário.
    """
    if isinstance(dados, dict):
        for chave, valor in dados.items():
            if chave in campos_procurados and valor not in [None, ""]:
                return valor

        for valor in dados.values():
            encontrado = procurar_valor_recursivo(valor, campos_procurados)
            if encontrado:
                return encontrado

    elif isinstance(dados, list):
        for item in dados:
            encontrado = procurar_valor_recursivo(item, campos_procurados)
            if encontrado:
                return encontrado

    return ""


def url_foto_completa(url):
    if not url:
        return ""

    if isinstance(url, dict):
        return ""

    if url.startswith("http"):
        return url

    return "https://suap.ifrn.edu.br" + url


def suap_get(caminho, params=None):
    token = session.get("access_token")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = SUAP_API_BASE + caminho.lstrip("/")

    resposta = requests.get(url, headers=headers, params=params, timeout=20)
    resposta.raise_for_status()

    return resposta.json()


def montar_usuario_nav(perfil, aluno):
    nome = primeiro_valor(
        perfil.get("nome"),
        perfil.get("nome_usual"),
        perfil.get("nome_completo"),
        perfil.get("nome_registro"),
        aluno.get("nome"),
        aluno.get("nome_usual"),
        aluno.get("nome_completo"),
        procurar_valor_recursivo(perfil, [
            "nome",
            "nome_usual",
            "nome_completo",
            "nome_registro"
        ]),
        procurar_valor_recursivo(aluno, [
            "nome",
            "nome_usual",
            "nome_completo",
            "nome_registro"
        ]),
        padrao="Usuário"
    )

    matricula = primeiro_valor(
        aluno.get("matricula"),
        perfil.get("matricula"),
        perfil.get("identificacao"),
        procurar_valor_recursivo(aluno, ["matricula", "identificacao"]),
        procurar_valor_recursivo(perfil, ["matricula", "identificacao"]),
        padrao="Sem matrícula"
    )

    foto = primeiro_valor(
        perfil.get("url_foto_75x100"),
        perfil.get("url_foto_150x200"),
        perfil.get("url_foto"),
        perfil.get("foto"),
        aluno.get("url_foto_75x100"),
        aluno.get("url_foto_150x200"),
        aluno.get("url_foto"),
        aluno.get("foto"),
        procurar_valor_recursivo(perfil, [
            "url_foto_75x100",
            "url_foto_150x200",
            "url_foto",
            "foto"
        ]),
        procurar_valor_recursivo(aluno, [
            "url_foto_75x100",
            "url_foto_150x200",
            "url_foto",
            "foto"
        ]),
        padrao=""
    )

    return {
        "nome": nome,
        "matricula": matricula,
        "foto": url_foto_completa(foto)
    }


def carregar_dados_usuario():
    perfil = {}
    aluno = {}

    try:
        perfil = suap_get("rh/meus-dados/")
    except Exception:
        perfil = {}

    try:
        aluno = suap_get("ensino/meus-dados-aluno/")
    except Exception:
        aluno = {}

    session["perfil"] = perfil
    session["aluno"] = aluno
    session["usuario_nav"] = montar_usuario_nav(perfil, aluno)


def normalizar_resultados(dados):
    if isinstance(dados, dict):
        if "results" in dados:
            return dados["results"]

        return [dados]

    if isinstance(dados, list):
        return dados

    return []


def buscar_boletim(ano):
    disciplinas = []

    for periodo in [1, 2]:
        try:
            dados = suap_get(f"ensino/meu-boletim/{ano}/{periodo}/")
            resultados = normalizar_resultados(dados)

            for disciplina in resultados:
                disciplina["_periodo"] = periodo
                disciplinas.append(disciplina)

        except Exception:
            continue

    return disciplinas


@app.context_processor
def inserir_dados_globais():
    return {
        "usuario_nav": session.get("usuario_nav"),
        "ano_atual": datetime.now().year
    }


@app.template_filter("mostrar")
def mostrar(valor):
    if valor is True:
        return "Sim"

    if valor is False:
        return "Não"

    if valor in [None, ""]:
        return "-"

    if isinstance(valor, (dict, list)):
        return json.dumps(valor, ensure_ascii=False, indent=2)

    return valor


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    redirect_uri = os.getenv("REDIRECT_URI", "http://localhost:5000/login/authorized")
    return oauth.suap.authorize_redirect(redirect_uri)


@app.route("/login/authorized")
def login_authorized():
    try:
        token = oauth.suap.authorize_access_token()

        session["access_token"] = token.get("access_token")
        session["refresh_token"] = token.get("refresh_token")

        carregar_dados_usuario()

        flash("Login realizado com sucesso.", "success")
        return redirect(url_for("perfil"))

    except Exception as erro:
        flash(f"Erro ao fazer login com o SUAP: {erro}", "danger")
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.", "success")
    return redirect(url_for("index"))


@app.route("/perfil")
@login_required
def perfil():
    try:
        if not session.get("perfil") or not session.get("aluno"):
            carregar_dados_usuario()

    except Exception:
        flash("Não foi possível atualizar os dados do perfil agora.", "warning")

    return render_template(
        "perfil.html",
        perfil=session.get("perfil", {}),
        aluno=session.get("aluno", {})
    )


@app.route("/boletim")
@login_required
def boletim():
    ano = request.args.get("ano", str(datetime.now().year))
    anos = list(range(datetime.now().year, datetime.now().year - 6, -1))

    disciplinas = buscar_boletim(ano)

    return render_template(
        "boletim.html",
        ano=ano,
        anos=anos,
        disciplinas=disciplinas
    )


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)