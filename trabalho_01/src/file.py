# Open a file and read its contents

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
""" tecnincamente não leio o ; ';':'',"""



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
                    resposta = palavras_chave.get(teste3)
                    if resposta != None:
                        print(resposta)
                    else:
                        print("nao tem: " + teste3)


    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
file_path = "teste.txt"  # Replace with your file path
read_file(file_path)
