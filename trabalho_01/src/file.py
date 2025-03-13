import re #para regex


#o que deveria ser considerado isso?
#   abc"teste"
#texto ou identificador


#se inserir um caractere que nao existe, por exemplo, um @, o sistema tem que falar que ele é um caractere inválido

palavras_chave = {
     'if': 'palavra-chave',
     'else': 'palavra-chave',
     'while': 'palavra-chave',
     'int': 'palavra-chave',
     'float':'palavra-chave',

     '*':'operador',
     '+':'operador',
     '-':'operador',
     '/':'operador',
     '=':'operador',
     '!=':'operador',
     '<=':'operador',
     '>=':'operador',


     '(':'pontuacao',
     ')':'pontuacao',
     '{':'pontuacao',
     '}':'pontuacao',


}

itens ={
}

def get_tipo(item):
    resposta = palavras_chave.get(item)

    if resposta == None:
        if bool(re.match(r'^-?\d+(\.\d+)?$', item)):
            resposta = "numero"

        elif bool(re.match(r'^\".*\"$', item)):
            resposta = "texto"

        elif bool(re.match(r'^[a-zA-Z0-9]+$', item)):
            resposta = "identificador"
        else:
            resposta = "texto"

    return resposta

""" tecnincamente não leio o ; ';':'',"""



"""
modo de leitura antigo

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()


            print("File Contents:")

            content = content.split('\n');

            for line in content:
                teste = line.split("//")[0].replace(';', ' ')

                teste2 = (teste.split(' '))

                print(teste2)


                for teste3 in teste2:
                    print(teste3)
                    itens[teste3] = get_tipo(teste3)"""


def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print("File Contents:")

            content = content.split('\n');

            for line in content:
                token = ''
                if "//" in line:
                    line = line.split("//")[0]

                final_condition = ' ;(){}'
                for char in line:

                    if char in final_condition:
                        final_condition = ' ;(){}'
                        print(token)
                        itens[token] = get_tipo(token)
                        token = ''
                        continue

                    elif char == "\"": #nova condicao de parada
                        final_condition = '\"'
                        continue

                    else:
                        token += char

        print("----------------------------------------------------------------------------------------")

        print(itens)
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


file_path = "teste3.txt"
read_file(file_path)
