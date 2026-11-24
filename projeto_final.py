from collections import deque

NOME_ALUNO = "Natanael Antônio Dos Reis Santana"
RA_ALUNO = "251-002126"

ARQUIVO = "dados_sistema.txt"
SEP = "|"


leitores = []
reservas = deque()
devolvidos = []
acervo = {}


def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip().replace(SEP, "/")
        if texto != "":
            return texto
        print("Erro: o campo não pode ser vazio.")


def ler_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem).strip())
        except ValueError:
            print("Erro: digite um número inteiro.")


def ler_caminho(mensagem):
    texto = ler_texto(mensagem)
    partes = [p.strip() for p in texto.split(">")]
    return [p for p in partes if p != ""]


def buscar_leitor(id_leitor):
    for leitor in leitores:
        if leitor["id"] == id_leitor:
            return leitor
    return None


def cadastrar_leitor():
    id_leitor = ler_texto("ID do leitor: ")
    if buscar_leitor(id_leitor) is not None:
        print("Erro: já existe um leitor com esse ID.")
        return
    nome = ler_texto("Nome do leitor: ")
    leitores.append({"id": id_leitor, "nome": nome})
    print("Leitor cadastrado com sucesso!")


def listar_leitores():
    if not leitores:
        print("Nenhum leitor cadastrado.")
        return
    for i, l in enumerate(leitores, start=1):
        print(f"{i}. ID: {l['id']} | Nome: {l['nome']}")
    print(f"Total: {len(leitores)} leitor(es).")


def atualizar_leitor():
    leitor = buscar_leitor(ler_texto("ID do leitor a atualizar: "))
    if leitor is None:
        print("Leitor não encontrado.")
        return
    print(f"Nome atual: {leitor['nome']}")
    leitor["nome"] = ler_texto("Novo nome: ")
    print("Leitor atualizado com sucesso!")


def remover_leitor():
    leitor = buscar_leitor(ler_texto("ID do leitor a remover: "))
    if leitor is None:
        print("Leitor não encontrado.")
        return
    leitores.remove(leitor)
    print("Leitor removido com sucesso!")


def reservar_livro():
    leitor = buscar_leitor(ler_texto("ID do leitor que está reservando: "))
    if leitor is None:
        print("Erro: leitor não cadastrado. Cadastre-o primeiro.")
        return
    livro = ler_texto("Título do livro: ")
    reservas.append((livro, leitor["nome"]))
    print(f"Reserva registrada. Posição na fila: {len(reservas)}")


def listar_reservas():
    if not reservas:
        print("A fila de reservas está vazia.")
        return
    for pos, (livro, nome) in enumerate(reservas, start=1):
        print(f"{pos}º | Livro: {livro} | Leitor: {nome}")


def atualizar_reserva():
    if not reservas:
        print("A fila de reservas está vazia.")
        return
    listar_reservas()
    pos = ler_inteiro("Posição da reserva a alterar: ")
    if pos < 1 or pos > len(reservas):
        print("Posição inválida.")
        return
    livro, nome = reservas[pos - 1]
    novo_livro = input(f"Novo livro (ENTER mantém '{livro}'): ").strip().replace(SEP, "/")
    novo_id = input("ID do novo leitor (ENTER mantém o atual): ").strip()
    if novo_livro != "":
        livro = novo_livro
    if novo_id != "":
        leitor = buscar_leitor(novo_id)
        if leitor is None:
            print("Leitor não encontrado. Mantendo o leitor anterior.")
        else:
            nome = leitor["nome"]
    reservas[pos - 1] = (livro, nome)
    print("Reserva atualizada com sucesso!")


def atender_reserva():
    if not reservas:
        print("Não há reservas para atender.")
        return
    livro, nome = reservas.popleft()
    print(f"Reserva atendida: '{livro}' liberado para {nome}.")


def devolver_livro():
    livro = ler_texto("Título do livro devolvido: ")
    devolvidos.append(livro)
    print("Livro colocado no topo da pilha de triagem.")


def listar_devolvidos():
    if not devolvidos:
        print("A pilha de devolvidos está vazia.")
        return

    for i, livro in enumerate(reversed(devolvidos)):
        marca = "  <-- TOPO" if i == 0 else ""
        print(f"- {livro}{marca}")
    print(f"Total: {len(devolvidos)} livro(s).")


def atualizar_topo():
    if not devolvidos:
        print("A pilha de devolvidos está vazia.")
        return
    print(f"Livro do topo: {devolvidos[-1]}")
    devolvidos[-1] = ler_texto("Novo título: ")
    print("Topo atualizado com sucesso!")


def triar_livro():
    if not devolvidos:
        print("Não há livros para triar.")
        return
    livro = devolvidos.pop()
    print(f"Livro '{livro}' triado e enviado para a estante.")


def navegar(caminho):
    no = acervo
    for parte in caminho:
        if parte not in no:
            return None
        no = no[parte]
    return no


def adicionar_no_acervo(caminho):
    no = acervo
    for parte in caminho:
        no = no.setdefault(parte, {})


def listar_acervo(no=None, nivel=0):
    if no is None:
        no = acervo
        if not acervo:
            print("O acervo está vazio.")
            return
    for nome, filhos in no.items():
        print("    " * nivel + "- " + nome)
        listar_acervo(filhos, nivel + 1)


def renomear_no(caminho, novo_nome):
    if navegar(caminho) is None:
        return False
    pai = navegar(caminho[:-1]) if len(caminho) > 1 else acervo
    antigo = caminho[-1]
    if novo_nome in pai and novo_nome != antigo:
        return False
    reconstruido = {}
    for chave, valor in pai.items():
        reconstruido[novo_nome if chave == antigo else chave] = valor
    pai.clear()
    pai.update(reconstruido)
    return True


def remover_no(caminho):
    if navegar(caminho) is None:
        return False
    pai = navegar(caminho[:-1]) if len(caminho) > 1 else acervo
    del pai[caminho[-1]]
    return True


def caminhos_folhas(no, prefixo=()):
    for nome, filhos in no.items():
        novo = prefixo + (nome,)
        if filhos:
            yield from caminhos_folhas(filhos, novo)
        else:
            yield novo


def menu_adicionar_no():
    print("Digite o caminho separado por '>'. Ex.: Ciências > Computação > Python")
    caminho = ler_caminho("Caminho: ")
    adicionar_no_acervo(caminho)
    print("Caminho inserido no acervo!")


def menu_renomear_no():
    caminho = ler_caminho("Caminho do nó a renomear (ex.: Ciências > Computação): ")
    novo = ler_texto("Novo nome: ")
    if renomear_no(caminho, novo):
        print("Nó renomeado com sucesso!")
    else:
        print("Nó não encontrado ou nome já existente no mesmo nível.")


def menu_remover_no():
    caminho = ler_caminho("Caminho do nó a remover: ")
    if navegar(caminho) is None:
        print("Nó não encontrado.")
        return
    if input("Isso remove também os filhos. Confirma? (S/N): ").strip().upper() == "S":
        remover_no(caminho)
        print("Nó removido com sucesso!")
    else:
        print("Remoção cancelada.")


def gerar_linhas():
    linhas = []
    for l in leitores:
        linhas.append(f"LISTA{SEP}{l['id']}{SEP}{l['nome']}")
    for livro, nome in reservas:
        linhas.append(f"FILA{SEP}{livro}{SEP}{nome}")
    for livro in devolvidos:
        linhas.append(f"PILHA{SEP}{livro}")
    for caminho in caminhos_folhas(acervo):
        linhas.append(f"ARVORE{SEP}{SEP.join(caminho)}")
    return linhas


def ha_alteracoes_nao_salvas():
    atual = gerar_linhas()
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            salvo = [linha.strip() for linha in f if linha.strip() != ""]
    except FileNotFoundError:
        return len(atual) > 0
    return salvo != atual


def salvar_dados():
    linhas = gerar_linhas()
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        for linha in linhas:
            f.write(linha + "\n")
    print(f"Dados salvos em '{ARQUIVO}'.")


def carregar_dados():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            linhas = f.readlines()
    except FileNotFoundError:
        print("Arquivo de dados ainda não existe. Salve os dados primeiro.")
        return


    if ha_alteracoes_nao_salvas():
        print("Atenção: há alterações que ainda NÃO foram salvas.")
        if input("Carregar mesmo assim e descartá-las? (S/N): ").strip().upper() != "S":
            print("Carregamento cancelado. Use a opção 5 para salvar antes.")
            return

    leitores.clear()
    reservas.clear()
    devolvidos.clear()
    acervo.clear()

    for linha in linhas:
        partes = linha.strip().split(SEP)
        tipo = partes[0]

        if tipo == "LISTA" and len(partes) == 3:
            leitores.append({"id": partes[1], "nome": partes[2]})
        elif tipo == "FILA" and len(partes) == 3:
            reservas.append((partes[1], partes[2]))
        elif tipo == "PILHA" and len(partes) == 2:
            devolvidos.append(partes[1])
        elif tipo == "ARVORE" and len(partes) >= 2:
            adicionar_no_acervo(partes[1:])
    print("Dados carregados com sucesso!")


def submenu(titulo, opcoes):
    while True:
        print(f"\n--- {titulo} ---")
        for numero, (texto, _) in opcoes.items():
            print(f"{numero}. {texto}")
        print("0. Voltar")
        escolha = input("Escolha: ").strip()
        if escolha == "0":
            return
        if escolha in opcoes:
            opcoes[escolha][1]()
        else:
            print("Opção inválida!")


def menu_leitores():
    submenu("LEITORES (LISTA)", {
        "1": ("Cadastrar leitor", cadastrar_leitor),
        "2": ("Listar leitores", listar_leitores),
        "3": ("Atualizar leitor", atualizar_leitor),
        "4": ("Remover leitor", remover_leitor),
    })


def menu_reservas():
    submenu("RESERVAS (FILA)", {
        "1": ("Reservar livro (entra no fim)", reservar_livro),
        "2": ("Listar fila de reservas", listar_reservas),
        "3": ("Atualizar reserva", atualizar_reserva),
        "4": ("Atender reserva (sai do início)", atender_reserva),
    })


def menu_devolvidos():
    submenu("DEVOLVIDOS (PILHA)", {
        "1": ("Devolver livro (push no topo)", devolver_livro),
        "2": ("Listar pilha", listar_devolvidos),
        "3": ("Atualizar livro do topo", atualizar_topo),
        "4": ("Triar livro (pop do topo)", triar_livro),
    })


def menu_acervo():
    submenu("ACERVO (ÁRVORE)", {
        "1": ("Adicionar área/assunto", menu_adicionar_no),
        "2": ("Listar acervo", listar_acervo),
        "3": ("Renomear nó", menu_renomear_no),
        "4": ("Remover nó", menu_remover_no),
    })


def menu_principal():
    print("=" * 60)
    print(f" Aluno: {NOME_ALUNO} | RA: {RA_ALUNO}")
    print(" Tema 5: Gerenciamento de Biblioteca")
    print("=" * 60)

    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1. Leitores (Lista)")
        print("2. Reservas (Fila)")
        print("3. Devolvidos (Pilha)")
        print("4. Acervo (Árvore)")
        print("5. Salvar dados")
        print("6. Carregar dados")
        print("0. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_leitores()
        elif opcao == "2":
            menu_reservas()
        elif opcao == "3":
            menu_devolvidos()
        elif opcao == "4":
            menu_acervo()
        elif opcao == "5":
            salvar_dados()
        elif opcao == "6":
            carregar_dados()
        elif opcao == "0":
            if ha_alteracoes_nao_salvas():
                resp = input("Há alterações não salvas. Salvar antes de sair? (S/N): ").strip().upper()
                if resp == "S":
                    salvar_dados()
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida! Escolha uma das opções do menu.")


if __name__ == "__main__":
    menu_principal()
