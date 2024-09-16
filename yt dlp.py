import os
import subprocess
from tkinter import Tk, filedialog
from colorama import init, Fore, Style
import yt_dlp

# Inicializar colorama para Windows
init(autoreset=True)

# Função para selecionar o diretório de download
def select_download_directory():
    Tk().withdraw()  # Esconde a janela principal do Tkinter
    download_dir = filedialog.askdirectory()
    return download_dir

# Função de progresso personalizada
def my_hook(d):
    if d['status'] == 'downloading':
        progress = d['_percent_str']
        speed = d['_speed_str']
        eta = d['eta']
        print(f"Progresso: {progress}, Velocidade: {speed}, ETA: {eta}s", end='\r')
    elif d['status'] == 'finished':
        print(Fore.GREEN + "\nDownload concluído!")

# Função para baixar vídeo com opções de rede e restrição geográfica
def download_video():
    url = input(Fore.CYAN + "\nInsira a URL do vídeo ou playlist: ")
    download_dir = select_download_directory()
    
    if download_dir:
        options = {
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'progress_hooks': [my_hook],
            'proxy': input("Digite o proxy (URL) ou deixe em branco para nenhum: ") or None,
            'socket_timeout': int(input("Tempo de espera do socket (em segundos) ou deixe em branco para padrão: ") or 5),
            'geo_bypass': input("Ignorar restrições geográficas? (S/N): ").lower() == 's',
            'geo_bypass_country': input("Forçar bypass para um país específico (ISO 3166-2, opcional): ") or None,
            'force_ipv4': input("Forçar IPv4? (S/N): ").lower() == 's',
            'force_ipv6': input("Forçar IPv6? (S/N): ").lower() == 's',
        }

        # Baixar o vídeo/playlist usando yt-dlp
        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                ydl.download([url])
            except Exception as e:
                print(Fore.RED + f"Erro no download: {e}")
    else:
        print(Fore.RED + "Nenhum diretório selecionado.")

    input(Fore.YELLOW + "\nPressione Enter para continuar...")
    main_menu()

# Função principal do menu
def main_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + Style.BRIGHT + "YT-DLP Interface - Menu Principal\n")
    print(Fore.YELLOW + "[1] Baixar Vídeo")
    print(Fore.RED + "[2] Sair")
    
    choice = input(Fore.CYAN + "\nEscolha uma opção: ")

    if choice == '1':
        download_video()
    elif choice == '2':
        exit()
    else:
        print(Fore.RED + "\nOpção Inválida!")
        input(Fore.YELLOW + "Pressione Enter para continuar...")
        main_menu()

# Iniciar o programa
if __name__ == '__main__':
    main_menu()
