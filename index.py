from time import sleep
import face_recognition
import random
import simpy
import json


FOTOS_VISITANTES = [
    "faces/neo1.jpeg",
    "faces/neo2.jpeg",
    "faces/neo3.jpeg",
    
    "faces/morpheus1.jpeg",
    "faces/morpheus2.jpeg",
    "faces/morpheus3.jpeg",
    
    "faces/trinity1.jpeg",
    "faces/trinity2.jpeg",
    "faces/trinity3.jpeg",
    
    "faces/smith1.jpeg",
    "faces/smith2.jpeg",
    "faces/smith3.jpeg",
    
    "faces/mascara1.jpeg",
    "faces/mascara2.jpeg",
    "faces/mascara3.jpeg",
    
    "faces/sentinelas1.jpeg",
    "faces/sentinelas2.jpeg",
    "faces/sentinelas3.jpeg",
    
    "faces/bugs1.jpeg",
    "faces/bugs2.jpeg",
    "faces/bugs3.jpeg",
]
ARQUIVO_CONFIGURACAO = "./configuracao.json"

def carregar_arquivos():
    with open(ARQUIVO_CONFIGURACAO, "r") as arquivo_configuracao:
        configuracao = json.load(arquivo_configuracao)
    arquivo_configuracao.close()
    return configuracao

def simular_escolha_personagem():
    foto = {
        "foto": random.choice(FOTOS_VISITANTES)
    }
    return foto

def reconhecer_personagem():
    reconhecido = False
    mensagem    = "Personagem não reconhecido na base de dados, Entrada negada!!!"
    global dados
    personagens_permitidos = simular_escolha_personagem()
    
    try:
        foto_personagens_permitidos = face_recognition.load_image_file(personagens_permitidos["foto"])
        encoding_foto_personagem_permitido = face_recognition.face_encodings(foto_personagens_permitidos)[0]
    except:
        dados = []
        return reconhecido, mensagem, dados

    personagens_configuracao = carregar_arquivos()
    reconhecido = False
    total_reconhecimentos = 0
    for personagem in personagens_configuracao["personagens"]:
        
        for fotos_personagem in personagem['fotos']:
    
            foto_banco = face_recognition.load_image_file(fotos_personagem)
            encoding_foto_banco = face_recognition.face_encodings(foto_banco)
            if len(encoding_foto_banco) > 0:
                biden_encoding = encoding_foto_banco[0]
                foto_reconhecida = face_recognition.compare_faces([encoding_foto_personagem_permitido], biden_encoding)[0]
            
            if foto_reconhecida:
                    total_reconhecimentos += 1
        if total_reconhecimentos/len(personagem['fotos']) > 0.7:
            reconhecido = True
            mensagem    = "Foi reconhecido na base de dados, aguarde a checagem de permissão..."
            dados = personagem
            break
    
    return reconhecido, mensagem, dados


def verificar_permissao_zion(env):
    while True:
        print("verificando permissão para entrar em zion: ", env.now)
        reconhecido, mensagem, dados = reconhecer_personagem()
        if reconhecido:
            print(mensagem)
            sleep(2)
            if dados['permissao'] == True:
                liberar_entrada_zion(dados)
            else:
                negar_entrada_zion(dados)
            yield env.timeout(5)
        else:
            print(mensagem)
            yield env.timeout(5)
            
        print('==============================================================')
        sleep(5)

def negar_entrada_zion(dados):
    print('[ENTRADA NEGADA]', dados['nome'], 'Você não tem permissão para entrar em zion, essas são as suas acusações:', dados['habilidades'])

def liberar_entrada_zion(dados):
    print('[ENTRADA PERMITIDA]', dados['nome'], 'seja bem vindo a Zion, estávamos te esperando!')
    print('[HABILIDADES ENCONTRADAS]', dados['habilidades'])
    print('[CÓDIGO DE ACESSO]', random.randint(1, 100))




if __name__ == "__main__":
    env = simpy.Environment()
    env.process(verificar_permissao_zion(env))
    env.run(until=10000)