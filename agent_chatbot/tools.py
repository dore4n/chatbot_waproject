from langchain_experimental.utilities import PythonREPL
from langchain.tools import tool
from typing import Annotated

repl = PythonREPL()

@tool
def python_repl(
    code: Annotated[str, "O código Python para gerar seu gráfico."]
):
    """Este tool executa o código Python fornecido e retorna se o código foi executado com sucesso ou não."""
    try:
        result = repl.run(code)
    except BaseException as e:
        return f"Falha na execução. Erro: {repr(e)}"
    return f"Saída do código: {result}"
