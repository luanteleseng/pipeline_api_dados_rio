import os
import time

def limpar_arquivos_antigos(diretorio_base: str, dias: int = 7):
    """
    Remove arquivos com mais de X dias em um diretório recursivamente.
    """
    agora = time.time()
    limite_segundos = dias * 86400

    for raiz, _, arquivos in os.walk(diretorio_base):
        for nome in arquivos:
            caminho = os.path.join(raiz, nome)
            try:
                if os.path.isfile(caminho):
                    idade = agora - os.path.getmtime(caminho)
                    if idade > limite_segundos:
                        os.remove(caminho)
                        print(f"Arquivo removido: {caminho}")
            except Exception as e:
                print(f"Não foi possível remover {caminho}: {e}")
