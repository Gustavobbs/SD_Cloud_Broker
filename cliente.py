
import requests
import json
import sys

PROV_URL = 'http://ec2-18-188-83-224.us-east-2.compute.amazonaws.com:5000/'

class Cliente:
    def __init__(self):
        self.quantidade = 0
        self.recurso = {}

    def menu(self):
        while True:
            print '1. Consultar VM'
            print '2. Liberar VM'
            print '3. Sair'
            opc = input('')

            if opc == 1:
                pid = input('Digite seu pid: ')
                response = self.buscar()
                posicao = 0
                if len(response) > 0:
                    preco = int(response[posicao]['preco'])
                if(len(response) > 1):
                    i = 0
                    for vms in response:
                        if(int(vms['preco']) < preco):
                            preco = int(vms['preco'])
                            posicao = i
                        i = i + 1

                print('\nRecurso encontrado:')
                print("\tvCPU: " + response[posicao]['vcpu'])
                print("\tHD: " + response[posicao]['hd'])
                print("\tRAM: " + response[posicao]['ram'])
                print("\tPreco: " + response[posicao]['preco'] + "\n")

                reservar = input('Deseja reservar o recurso? (1/0) ')
                if(reservar == 1):
                    resposta = {
                        'vcpu': response[posicao]['vcpu'],
                        'hd': response[posicao]['hd'],
                        'ram': response[posicao]['ram'],
                        'preco': response[posicao]['preco']
                    }
                    response = self.postRequest(resposta, PROV_URL + 'cliente/reservar/' + str(pid))

                    if response['Ok'] == True:
                        print '\n--> VM reservada com sucesso.\n'
                    else:
                        print '\n--> Erro ao reservar VM.\n'

                elif(reservar == 0):
                    print('Ate a proxima.\n')

            elif opc == 2:
                response = self.consultar()
                i = 1
                for vms in response:
                    print("VM n. " + str(i) + ":")
                    print("\tID: "),
                    print(vms['_id'])
                    print("\tvCPU: " + vms['vcpu'])
                    print("\tHD: " + vms['hd'])
                    print("\tRAM: " + vms['ram'])
                    print("\tPreco: " + vms['preco'] + "\n")
                    i = i + 1

                opcao = input('Deseja desalocar algum recurso? (1/0) ')
                if(opcao == 1):
                    posicao = input('Qual recurso deseja desalocar?')
                    if(posicao > len(response)):
                        print('Recurso nao encontrado.\n')
                    else:
                        posicao = posicao - 1
                        resposta = {
                            'vcpu': response[posicao]['vcpu'],
                            'hd': response[posicao]['hd'],
                            'ram': response[posicao]['ram'],
                            'preco': response[posicao]['preco']
                        }
                        response = self.postRequest(resposta, PROV_URL + 'cliente/liberar')

                        if response['Ok'] == True:
                            print '\n--> VM liberada com sucesso.\n'
                        else:
                            print '\n--> Erro ao liberar VM.\n'

                if(opcao == 0):
                    print('Ate a proxima.\n')


            elif opc == 3:
                return 0

    def buscar(self):
        recursos = {
            'vcpu':'',
            'ram':'',
            'hd':'',
        }
        recursos['vcpu'] = str(input('Quantidade de vCPUs: '))
        recursos['ram'] = str(input('Quantidade de memoria RAM (em GB): '))
        recursos['hd'] = str(input('Quantidade de disco (HD, em GB): '))
    
        return self.postRequest(recursos, PROV_URL + 'search')

    def postRequest(self, data, url):
        headers = {'Content-Type': 'application/json',}
        post = requests.post(url=url, data=json.dumps(data), headers=headers)

        return post.json()

    def consultar(self):
        pid = input('Digite seu pid: ')
        recursos = {}

        return self.postRequest(recursos, PROV_URL + "cliente/consultar/" + str(pid))

if __name__ == '__main__':
    p = Cliente()
    p.menu()
