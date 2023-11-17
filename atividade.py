import json
import os
import hashlib
import sys
from colorama import Fore, Style


# Carregar usuários do arquivo JSON
def carregar_usuarios():
    if os.path.exists("usuarios.json"):
        with open("usuarios.json", "r") as arquivo:
            usuarios = json.load(arquivo)
        return usuarios
    else:
        return []


# Salvar usuários no arquivo JSON
def salvar_usuarios(usuarios):
    with open("usuarios.json", "w") as arquivo:
        json.dump(usuarios, arquivo, indent=4)


# Questão 1) Listar usuarios
def listar_usuarios(usuarios):
    for usuario in usuarios:
        print("-" * 30)
        print(f"{Fore.YELLOW}Nome completo:{Style.RESET_ALL}", usuario["nome_completo"])
        print(f"{Fore.YELLOW}Nome de login:{Style.RESET_ALL}", usuario["nome_login"])
        print(f"{Fore.YELLOW}E-mail:{Style.RESET_ALL}", usuario["email"])

# Questão 1) Adicionar usuarios
def adicionar_usuario(usuarios):
    # Input
    nome_completo = input("Digite o nome completo: ")
    nome_login = input("Digite o nome de login: ")
    senha = input("Digite a senha: ")
    email = input("Digite o e-mail: ")

    # Conversão Hash512
    senha_hash = hashlib.sha512(senha.encode()).hexdigest()

    # Dicionário (Apenas a senha hash sera salva no JSON)
    novo_usuario = {
        "nome_completo": nome_completo,
        "nome_login": nome_login,
        "senha_hash": senha_hash,
        "email": email
    }

    usuarios.append(novo_usuario)
    salvar_usuarios(usuarios)
    print(f"{Fore.GREEN}Usuário adicionado com sucesso!{Style.RESET_ALL}")

# Questão 1) Remover usuarios
def remover_usuario(usuarios):
    nome_login = input("Digite o nome de login do usuário que deseja remover: ")

    for usuario in usuarios:
        if usuario["nome_login"] == nome_login:
            usuarios.remove(usuario)
            salvar_usuarios(usuarios)
            print("-" * 30)
            print(f"{Fore.GREEN}Usuário removido com sucesso!{Style.RESET_ALL}")
            return
    print(f"{Fore.RED}Usuário não encontrado{Style.RESET_ALL}")


# Questão 2 - Login com hash (Arquivo JSON + login + senha)
def verificar_login(usuarios, nome_login, senha):
    # A senha eh convertida em hash.
    senha_hash = hashlib.sha512(senha.encode()).hexdigest()

    # Se pecorre o arquivo JSON fazendo a comparação com o login e a senha convertida
    for usuario in usuarios:
        if usuario["nome_login"] == nome_login and usuario["senha_hash"] == senha_hash:
            return True

    return False


# Questão 3 - Lista arquivos do diretorio atual (O 3 arquivos txt servem de exemplo para a listagem)
def listar_arquivos(n, diretorio="."):
    for nome_arquivo in os.listdir(diretorio):
        caminho_arquivo = os.path.join(diretorio, nome_arquivo)
        tamanho = os.path.getsize(caminho_arquivo)
        tamanho_formatado = _formatar_tamanho(tamanho)

        print(f"{temas(n) + nome_arquivo}\t{tamanho_formatado}")
        print(Style.RESET_ALL)  # Reseta as cores


# Questão 3 - Formatação do tamanho
def _formatar_tamanho(tamanho):
    for unidade in ['B', 'KB', 'MB', 'GB', 'TB']:
        if tamanho < 1024.0:
            break
        tamanho /= 1024.0
    return "{:.1f} {}".format(tamanho, unidade)


# Questão 3 - Escolhe a cor (o 'n' eh o argumento que altera a cor)
def temas(n):
    if n == 1:
        return Fore.MAGENTA
    elif n == 2:
        return Fore.GREEN


# Menu interativo
def menu(usuarios):

    while True:
        print("-" * 30)
        print("Opções:")
        print("1. Listar usuários")
        print("2. Adicionar usuário")
        print("3. Remover usuário")
        print("4. Login")
        print("5. Temas (Questão 3 - Listar os arquivos do dir atual)")
        print("6. Sair")
        print("-" * 30)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_usuarios(usuarios)
        elif opcao == "2":
            adicionar_usuario(usuarios)
        elif opcao == "3":
            remover_usuario(usuarios)
        elif opcao == "4":
            print("-" * 30)
            nome_login = input("Digite o nome de login: ")
            senha = input("Digite a senha: ")
            print("-" * 30)
            if verificar_login(usuarios, nome_login, senha):
                print("Usuário logado com sucesso!")

            else:
                print("Nome de login ou senha incorretos.")

        elif opcao == "5":
            print("-" * 30)
            print("Escolha um tema:")
            print("1 - Roxo")
            print("2 - Verde")
            print("-" * 30)
            n = int(input("Escolha uma opção: "))
            if n != 1 and n != 2:
                print(f"{Fore.RED}Opcão invalida!{Style.RESET_ALL}")
                return menu(usuarios)

            diretorio = "."  # Diretório padrão é o diretório atual
            if len(sys.argv) > 1:
                diretorio = sys.argv[1]
            listar_arquivos(n, diretorio)

        elif opcao == "6":
            break
        else:
            print(f"{Fore.RED}Opcão invalida!{Style.RESET_ALL}")


# Main
def main():
    usuarios = carregar_usuarios()
    menu(usuarios)


if __name__ == "__main__":
    main()
