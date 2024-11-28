import re

class TipoToken:
    NUM_INT = "NUM_INT"
    NUM_DEC = "NUM_DEC"
    IDENTIFICADOR = "IDENTIFICADOR"
    TEXTO = "TEXTO"
    PALAVRA_RESERVADA = "PALAVRA_RESERVADA"
    COMENTARIO = "COMENTARIO"
    OPERADOR = "OPERADOR"
    SIMBOLO_ESPECIAL = "SIMBOLO_ESPECIAL"
    DESCONHECIDO = "DESCONHECIDO"

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor})"

# Palavras reservadas
palavras_reservadas = [
    "int", "float", "char", "boolean", "void", "if", "else", "for", "while",
    "scanf", "println", "main", "return", "double", "struct", "switch", "case", "default", "break", "continue"
]

# Tabela de símbolos
tabela_simbolos = {}
indice_tabela_simbolos = 0

def imprimir_token(token):
    print(f"{token.tipo}: {token.valor}")

def eh_palavra_reservada(valor):
    return valor in palavras_reservadas

def eh_numero_inteiro(valor):
    return valor.isdigit()

def eh_numero_decimal(valor):
    return bool(re.fullmatch(r"\d+\.\d+", valor))

def eh_identificador(valor):
    return bool(re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", valor))

def eh_comentario(valor):
    return valor.startswith("//")

def eh_operador(valor):
    operadores = {"=", "+", "-", "*", "/", "%", "&&", "||", "!", ">", "<", ">=", "<=", "!=", "=="}
    return valor in operadores

def eh_simbolo_especial(valor):
    return valor in "()[]{};," 

def analisar_lexico(entrada):
    global indice_tabela_simbolos
    tokens = []
    token_strings = re.findall(r'//.*|".*?"|\w+|[^\s\w]', entrada)
    for token_str in token_strings:
        if eh_comentario(token_str):
            token = Token(TipoToken.COMENTARIO, token_str)
        elif eh_numero_decimal(token_str):
            token = Token(TipoToken.NUM_DEC, token_str)
        elif eh_numero_inteiro(token_str):
            token = Token(TipoToken.NUM_INT, token_str)
        elif eh_palavra_reservada(token_str):
            token = Token(TipoToken.PALAVRA_RESERVADA, token_str)
        elif eh_identificador(token_str):
            token = Token(TipoToken.IDENTIFICADOR, token_str)
            if token_str not in tabela_simbolos:
                indice_tabela_simbolos += 1
                tabela_simbolos[token_str] = indice_tabela_simbolos
        elif token_str.startswith('"') and token_str.endswith('"'):
            token = Token(TipoToken.TEXTO, token_str.strip('"'))
        elif eh_operador(token_str):
            token = Token(TipoToken.OPERADOR, token_str)
        elif eh_simbolo_especial(token_str):
            token = Token(TipoToken.SIMBOLO_ESPECIAL, token_str)
        else:
            token = Token(TipoToken.DESCONHECIDO, token_str)
        tokens.append(token)
    return tokens

# Analisador Sintático
class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0

    def obter_token_atual(self):
        return self.tokens[self.posicao] if self.posicao < len(self.tokens) else None

    def consumir_token(self):
        token = self.obter_token_atual()
        self.posicao += 1
        return token

    def verificar_token(self, tipo):
        token = self.obter_token_atual()
        return token and token.tipo == tipo

    def analisar_programa(self):
        while self.obter_token_atual() is not None:
            if not self.analisar_declaracao():
                print(f"Erro de sintaxe: token inesperado {self.obter_token_atual()}")
                break

    def analisar_declaracao(self):
        return (
            self.analisar_declaracao_variavel() or
            self.analisar_declaracao_funcao() or
            self.analisar_estrutura_controle() or
            self.analisar_comentario()
        )

    def analisar_declaracao_variavel(self):
        if self.verificar_token(TipoToken.PALAVRA_RESERVADA):
            tipo = self.consumir_token()
            if self.verificar_token(TipoToken.IDENTIFICADOR):
                self.consumir_token()
                if self.verificar_token(TipoToken.OPERADOR):
                    self.consumir_token()
                    self.analisar_expressao()
                if self.verificar_token(TipoToken.SIMBOLO_ESPECIAL):
                    self.consumir_token()
                    return True
        return False

    def analisar_declaracao_funcao(self):
        # Exemplo simplificado
        pass

    def analisar_estrutura_controle(self):
        # Exemplo simplificado
        pass

    def analisar_comentario(self):
        if self.verificar_token(TipoToken.COMENTARIO):
            self.consumir_token()
            return True
        return False

    def analisar_expressao(self):
        # Exemplo simplificado
        pass

def main():
    caminho_arquivo = input("Digite o caminho do arquivo com o código-fonte: ").strip()
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            tokens = []
            for linha in arquivo:
                tokens.extend(analisar_lexico(linha.strip()))
            print("\nTokens:")
            for token in tokens:
                imprimir_token(token)

            print("\nIniciando análise sintática...")
            analisador = AnalisadorSintatico(tokens)
            analisador.analisar_programa()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return
    except IOError as e:
        print(f"Erro ao abrir o arquivo: {e}")
        return

    imprimir_tabela_simbolos()

if __name__ == "__main__":
    main()
