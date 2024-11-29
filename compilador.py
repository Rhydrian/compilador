import re

class TipoToken:
    NUM_INT = "NUM_INT"
    NUM_DEC = "NUM_DEC"
    IDENTIFICADOR = "IDENTIFICADOR"
    TEXTO = "TEXTO"
    PALAVRA_RESERVADA = "PALAVRA_RESERVADA"
    SIMBOLO_ESPECIAL = "SIMBOLO_ESPECIAL"
    DESCONHECIDO = "DESCONHECIDO"

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

# Palavras reservadas em C
palavras_reservadas = [
    "int", "return", "void"
]

def eh_palavra_reservada(valor):
    return valor in palavras_reservadas

def eh_numero_inteiro(valor):
    return valor.isdigit()

def eh_identificador(valor):
    return bool(re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", valor)) and not eh_palavra_reservada(valor)

def eh_simbolo_especial(valor):
    return valor in "(){};," 

def analisar_lexico(entrada):
    """
    Realiza a análise léxica para identificar tokens no código.
    """
    tokens = []
    token_strings = re.findall(r'".*?"|\w+|[^\s\w]', entrada)
    for token_str in token_strings:
        if eh_palavra_reservada(token_str):
            tokens.append(Token(TipoToken.PALAVRA_RESERVADA, token_str))
        elif eh_numero_inteiro(token_str):
            tokens.append(Token(TipoToken.NUM_INT, token_str))
        elif eh_identificador(token_str):
            tokens.append(Token(TipoToken.IDENTIFICADOR, token_str))
        elif token_str.startswith('"') and token_str.endswith('"'):
            tokens.append(Token(TipoToken.TEXTO, token_str.strip('"')))
        elif eh_simbolo_especial(token_str):
            tokens.append(Token(TipoToken.SIMBOLO_ESPECIAL, token_str))
        else:
            tokens.append(Token(TipoToken.DESCONHECIDO, token_str))
    return tokens

# Analisador Sintático
class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0

    def token_atual(self):
        return self.tokens[self.posicao] if self.posicao < len(self.tokens) else None

    def consumir(self):
        token = self.token_atual()
        self.posicao += 1
        return token

    def verificar(self, tipo, valor=None):
        token = self.token_atual()
        if not token:
            return False
        if token.tipo != tipo:
            return False
        if valor and token.valor != valor:
            return False
        return True

    def erro(self, mensagem):
        raise SyntaxError(f"Erro sintático: {mensagem} na posição {self.posicao}")

    # Função para analisar um programa inteiro
    def analisar_programa(self):
        """
        Programa → Declaracao*
        """
        while self.token_atual() is not None:
            self.analisar_declaracao()

    # Função para analisar uma declaração de função
    def analisar_declaracao(self):
        """
        Declaração → DeclaracaoFuncao | EstruturaControle | Comentarios
        """
        if self.verificar(TipoToken.PALAVRA_RESERVADA, "int"):
            self.analisar_declaracao_funcao()
        elif self.verificar(TipoToken.PALAVRA_RESERVADA, "void"):
            self.analisar_declaracao_funcao()
        elif self.verificar(TipoToken.PALAVRA_RESERVADA, "if"):
            self.analisar_estrutura_if()
        elif self.verificar(TipoToken.PALAVRA_RESERVADA, "while"):
            self.analisar_estrutura_while()
        elif self.verificar(TipoToken.PALAVRA_RESERVADA, "for"):
            self.analisar_estrutura_for()
        elif self.verificar(TipoToken.PALAVRA_RESERVADA, "switch"):
            self.analisar_estrutura_switch()
        elif self.verificar(TipoToken.PALAVRA_RESERVADA, "case"):
            self.analisar_estrutura_case()
        else:
            self.erro("Tipo de declaração desconhecido.")

    # Analisador de declaração de função
    def analisar_declaracao_funcao(self):
        """
        DeclaracaoFuncao → Tipo ID ( Parametros ) Bloco
        """
        tipo = self.consumir()  # Consome o tipo (ex. "int")
        if not self.verificar(TipoToken.IDENTIFICADOR):
            self.erro("Esperado identificador após o tipo.")
        self.consumir()  # Consome o nome da função
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, "("):
            self.erro("Esperado '(' após nome da função.")
        self.consumir()  # Consome '('
        self.analisar_parametros()
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, ")"):
            self.erro("Esperado ')' após os parâmetros.")
        self.consumir()  # Consome ')'
        self.analisar_bloco()

    # Função para analisar parâmetros de uma função
    def analisar_parametros(self):
        """
        Parametros → Parametro* 
        """
        while not self.verificar(TipoToken.SIMBOLO_ESPECIAL, ")"):
            self.analisar_parametro()

    def analisar_parametro(self):
        """
        Parametro → Tipo ID
        """
        if not self.verificar(TipoToken.PALAVRA_RESERVADA):
            self.erro("Esperado tipo de dado para parâmetro.")
        self.consumir()  # Consome o tipo
        if not self.verificar(TipoToken.IDENTIFICADOR):
            self.erro("Esperado identificador para o parâmetro.")
        self.consumir()  # Consome o identificador

    # Analisador de blocos de código
    def analisar_bloco(self):
        """
        Bloco → { Declaracao* }
        """
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, "{"):
            self.erro("Esperado '{' no início do bloco.")
        self.consumir()  # Consome '{'
        while not self.verificar(TipoToken.SIMBOLO_ESPECIAL, "}"):
            self.analisar_declaracao()
        self.consumir()  # Consome '}'

    # Estrutura de controle "if"
    def analisar_estrutura_if(self):
        """
        EstruturaControle → if ( Expressao ) Bloco
        """
        self.consumir()  # Consome 'if'
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, "("):
            self.erro("Esperado '(' após 'if'.")
        self.consumir()  # Consome '('
        self.analisar_expressao()
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, ")"):
            self.erro("Esperado ')' após expressão em 'if'.")
        self.consumir()  # Consome ')'
        self.analisar_bloco()

    # Estrutura de controle "while"
    def analisar_estrutura_while(self):
        """
        EstruturaControle → while ( Expressao ) Bloco
        """
        self.consumir()  # Consome 'while'
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, "("):
            self.erro("Esperado '(' após 'while'.")
        self.consumir()  # Consome '('
        self.analisar_expressao()
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, ")"):
            self.erro("Esperado ')' após expressão em 'while'.")
        self.consumir()  # Consome ')'
        self.analisar_bloco()

    # Estrutura de controle "for"
    def analisar_estrutura_for(self):
        """
        EstruturaControle → for ( Expressao ; Expressao ; Expressao ) Bloco
        """
        self.consumir()  # Consome 'for'
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, "("):
            self.erro("Esperado '(' após 'for'.")
        self.consumir()  # Consome '('
        self.analisar_expressao()
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, ";"):
            self.erro("Esperado ';' após a expressão no 'for'.")
        self.consumir()  # Consome ';'
        self.analisar_expressao()
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, ";"):
            self.erro("Esperado ';' após a expressão no 'for'.")
        self.consumir()  # Consome ';'
        self.analisar_expressao()
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, ")"):
            self.erro("Esperado ')' após expressões no 'for'.")
        self.consumir()  # Consome ')'
        self.analisar_bloco()

    # Estrutura de controle "switch"
    def analisar_estrutura_switch(self):
        """
        EstruturaControle → switch ( Expressao ) { CaseLista }
        """
        self.consumir()  # Consome 'switch'
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, "("):
            self.erro("Esperado '(' após 'switch'.")
        self.consumir()  # Consome '('
        self.analisar_expressao()
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, ")"):
            self.erro("Esperado ')' após expressão no 'switch'.")
        self.consumir()  # Consome ')'
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, "{"):
            self.erro("Esperado '{' após 'switch'.")
        self.consumir()  # Consome '{'
        self.analisar_case_lista()
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, "}"):
            self.erro("Esperado '}' após bloco 'switch'.")
        self.consumir()  # Consome '}'

    def analisar_case_lista(self):
        """
        CaseLista → CaseDecl* 
        """
        while self.verificar(TipoToken.PALAVRA_RESERVADA, "case"):
            self.analisar_estrutura_case()

    # Estrutura de controle "case"
    def analisar_estrutura_case(self):
        """
        CaseDecl → case Expressao : Bloco
        """
        self.consumir()  # Consome 'case'
        self.analisar_expressao()
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, ":"):
            self.erro("Esperado ':' após 'case'.")
        self.consumir()  # Consome ':'
        self.analisar_bloco()

    # Analisador de expressões (simplificado para demonstração)
    def analisar_expressao(self):
        """
        Expressao → IDENTIFICADOR | NUM_INT | NUM_DEC | TEXTO
        """
        token = self.token_atual()
        if token.tipo not in {TipoToken.IDENTIFICADOR, TipoToken.NUM_INT, TipoToken.NUM_DEC, TipoToken.TEXTO}:
            self.erro(f"Expressão inválida. Encontrado: {token.valor}")
        self.consumir()


    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0

    def token_atual(self):
        return self.tokens[self.posicao] if self.posicao < len(self.tokens) else None

    def consumir(self):
        token = self.token_atual()
        self.posicao += 1
        return token

    def verificar(self, tipo, valor=None):
        token = self.token_atual()
        if not token:
            return False
        if token.tipo != tipo:
            return False
        if valor and token.valor != valor:
            return False
        return True

    def erro(self, mensagem):
        raise SyntaxError(f"Erro sintático: {mensagem} na posição {self.posicao}")

    def analisar_programa(self):
        """
        Programa → int main() { ChamadaFuncao }
        """
        if not self.verificar(TipoToken.PALAVRA_RESERVADA, "int"):
            self.erro("Esperado 'int' no início do programa.")
        self.consumir()  # Consome 'int'
        if not self.verificar(TipoToken.IDENTIFICADOR, "main"):
            self.erro("Esperado 'main' após 'int'.")
        self.consumir()  # Consome 'main'
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, "("):
            self.erro("Esperado '(' após 'main'.")
        self.consumir()  # Consome '('
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, ")"):
            self.erro("Esperado ')' após '('.")
        self.consumir()  # Consome ')'
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, "{"):
            self.erro("Esperado '{' no início do bloco.")
        self.consumir()  # Consome '{'
        self.analisar_chamada_funcao()
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, "}"):
            self.erro("Esperado '}' no final do bloco.")
        self.consumir()  # Consome '}'

    def analisar_chamada_funcao(self):
        """
        ChamadaFuncao → printf ( TEXTO ) ;
        """
        if not self.verificar(TipoToken.IDENTIFICADOR, "printf"):
            self.erro("Esperado 'printf' para chamada de função.")
        self.consumir()  # Consome 'printf'
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, "("):
            self.erro("Esperado '(' após 'printf'.")
        self.consumir()  # Consome '('
        if not self.verificar(TipoToken.TEXTO):
            self.erro("Esperado string dentro de 'printf'.")
        self.consumir()  # Consome o texto
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, ")"):
            self.erro("Esperado ')' após string.")
        self.consumir()  # Consome ')'
        if not self.verificar(TipoToken.SIMBOLO_ESPECIAL, ";"):
            self.erro("Esperado ';' após 'printf'.")
        self.consumir()  # Consome ';'

def main():
    caminho_arquivo = input("Digite o caminho do arquivo com o código-fonte: ").strip()
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            tokens = []
            for linha in arquivo:
                tokens.extend(analisar_lexico(linha.strip()))
            print("Tokens:")
            for token in tokens:
                print(f"{token.tipo}: {token.valor}")

            print("\nIniciando análise sintática...")
            analisador = AnalisadorSintatico(tokens)
            analisador.analisar_programa()
            print("Análise sintática concluída com sucesso!")
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
    except SyntaxError as e:
        print(f"Erro durante a análise sintática: {e}")


if __name__ == "__main__":
    main()
