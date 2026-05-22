import users_wrapper as users

opcao = True

while opcao:
    print("1 - Listar usuários")
    print("2 - Ler usuário")
    print("3 - Listar tarefas de um usuário")
    print("4 - Criar usuário")
    print("5 - Editar usuário")
    print("6 - Excluir usuário")
    print("7 - Sair")

    opcao = input("Digite a opção desejada: ")

    if opcao == "1":
        lista = users.list()

        if lista:
            print("Usuários encontrados:")
            for usuario in lista:
                print(f"{usuario['id']} - {usuario['name']} ({usuario['email']})")
        else:
            print("Não consegui listar os usuários.")

    if opcao == "2":
        user_id = input("Digite o ID do usuário: ")
        usuario = users.read(user_id)

        if usuario:
            print("Dados do usuário:")
            print(f"Nome: {usuario['name']}")
            print(f"Email: {usuario['email']}")
            print(f"Telefone: {usuario['phone']}")
            print(f"Site: {usuario['website']}")
        else:
            print("Usuário não encontrado.")

    if opcao == "3":
        user_id = input("Digite o ID do usuário: ")
        tarefas = users.todos(user_id)

        if tarefas:
            print("Tarefas do usuário:")
            for tarefa in tarefas:
                if tarefa["completed"]:
                    situacao = "concluída"
                else:
                    situacao = "pendente"

                print(f"- {tarefa['title']} | {situacao}")
        else:
            print("Não encontrei tarefas para esse usuário.")

    if opcao == "4":
        print("Digite os dados do usuário:")

        usuario = {}
        usuario["name"] = input("Nome: ")
        usuario["email"] = input("Email: ")
        usuario["phone"] = input("Telefone: ")
        usuario["website"] = input("Site: ")

        confirmar = input("Deseja criar esse usuário? (s/n): ")

        if confirmar == "s":
            novo_usuario = users.create(usuario)

            if novo_usuario:
                print(f"Usuário {novo_usuario['name']} criado com sucesso.")
            else:
                print("Erro ao criar usuário.")
        else:
            print("Cadastro cancelado.")

    if opcao == "5":
        user_id = input("Digite o ID do usuário: ")
        usuario = users.read(user_id)

        if usuario:
            print("Usuário encontrado:")
            print(f"Nome: {usuario['name']}")
            print(f"Email: {usuario['email']}")
            print(f"Telefone: {usuario['phone']}")
            print(f"Site: {usuario['website']}")

            print("Agora digite os novos dados:")

            usuario["name"] = input("Novo nome: ")
            usuario["email"] = input("Novo email: ")
            usuario["phone"] = input("Novo telefone: ")
            usuario["website"] = input("Novo site: ")

            usuario_atualizado = users.update(user_id, usuario)

            if usuario_atualizado:
                print(f"Usuário {usuario_atualizado['name']} atualizado com sucesso.")
            else:
                print("Erro ao atualizar usuário.")
        else:
            print("Usuário não encontrado.")

    if opcao == "6":
        user_id = input("Digite o ID do usuário: ")
        usuario = users.read(user_id)

        if usuario:
            print("Usuário encontrado:")
            print(f"Nome: {usuario['name']}")
            print(f"Email: {usuario['email']}")

            confirmar = input("Tem certeza que deseja excluir? (s/n): ")

            if confirmar.lower() == "s":
                apagado = users.delete(user_id)

                if apagado:
                    print("Usuário excluído com sucesso.")
                else:
                    print("Erro ao excluir usuário.")
            else:
                print("Exclusão cancelada.")
        else:
            print("Usuário não encontrado.")

    if opcao == "7":
        print("Saindo do programa...")
        opcao = False