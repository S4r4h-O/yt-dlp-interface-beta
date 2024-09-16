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

# Função para exibir e capturar múltiplas opções
def select_options():
    print(Fore.CYAN + "\nEscolha as opções desejadas (separadas por vírgula):")
    print("[1] Definir proxy")
    print("[2] Tempo de espera do socket")
    print("[3] Ignorar restrições geográficas")
    print("[4] Forçar bypass para um país específico")
    print("[5] Forçar IPv4")
    print("[6] Forçar IPv6")
    print("[7] Baixar lista de reprodução sem expandir vídeos")
    print("[8] Começar transmissões ao vivo do início")
    print("[9] Aplicar filtros específicos de vídeo")
    print("[10] Registrar vídeos baixados em um arquivo")
    print("[11] Escolher o formato de saída do vídeo (por padrão, melhor qualidade)")

    choices = input("Digite os números das opções desejadas (ex: 1,3,5): ")
    selected_options = choices.split(',')

    return selected_options

# Função para baixar vídeo com as opções selecionadas
def download_video():
    url = input(Fore.CYAN + "\nInsira a URL do vídeo ou playlist: ")
    download_dir = select_download_directory()
    
    if download_dir:
        options = {
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'progress_hooks': [my_hook],
            'sponsorblock_mark': ['default'],  # SponsorBlock padrão
            'format': 'best',  # Sempre baixar na melhor qualidade
        }

        selected_options = select_options()

        # Aplicando as opções com base na escolha do usuário
        if '1' in selected_options:
            options['proxy'] = input("Digite o proxy (URL) ou deixe em branco para nenhum: ") or None
        if '2' in selected_options:
            options['socket_timeout'] = int(input("Tempo de espera do socket (em segundos) ou deixe em branco para padrão: ") or 5)
        if '3' in selected_options:
            options['geo_bypass'] = True
        if '4' in selected_options:
            options['geo_bypass_country'] = input("Forçar bypass para um país específico (ISO 3166-2, opcional): ") or None
        if '5' in selected_options:
            options['force_ipv4'] = True
        if '6' in selected_options:
            options['force_ipv6'] = True
        if '7' in selected_options:
            options['flat_playlist'] = True
        if '8' in selected_options:
            options['live_from_start'] = True
        if '9' in selected_options:
            options['match_filters'] = input("Aplicar filtros específicos de vídeo (regex, opcional): ") or None
        if '10' in selected_options:
            options['download_archive'] = input("Deseja registrar vídeos baixados em um arquivo? Informe o nome do arquivo ou deixe em branco: ") or None
        if '11' in selected_options:
            # Seleção de formato de saída
            print(Fore.CYAN + "\nEscolha o formato de saída:")
            print("[1] mp4")
            print("[2] mp3")
            print("[3] wav")
            print("[4] opus")
            print("[5] Deixar padrão (melhor qualidade disponível)")
            format_choice = input("Digite o número do formato desejado: ")

            # Mapear a escolha do usuário para o formato adequado
            format_map = {
                '1': 'mp4',
                '2': 'mp3',
                '3': 'wav',
                '4': 'opus'
            }
            
            # Verificar a escolha do formato e aplicar as opções correspondentes
            if format_choice in format_map:
                chosen_format = format_map[format_choice]
                if chosen_format in ['mp3', 'wav', 'opus']:
                    options['extractaudio'] = True
                    options['audioformat'] = chosen_format
                else:
                    options['format'] = chosen_format

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

# Função para baixar apenas os títulos de uma playlist
def download_titles():
    url = input(Fore.CYAN + "\nInsira a URL da playlist: ")
    
    options = {
        'flat_playlist': True,
        'quiet': True,
        'force_generic_extractor': True,
        'extract_flat': True,
        'print': 'title',
    }

    # Mostrar títulos usando yt-dlp
    with yt_dlp.YoutubeDL(options) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            print(Fore.RED + f"Erro ao obter títulos: {e}")

    input(Fore.YELLOW + "\nPressione Enter para continuar...")
    main_menu()

# Função principal do menu
def main_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + Style.BRIGHT + "YT-DLP Interface - Menu Principal\n")
    print(Fore.YELLOW + "[1] Baixar Vídeo/Playlist")
    print("[2] Baixar apenas títulos da Playlist")
    print(Fore.RED + "[3] Sair")
    
    choice = input(Fore.CYAN + "\nEscolha uma opção: ")

    if choice == '1':
        download_video()
    elif choice == '2':
        download_titles()
    elif choice == '3':
        exit()
    else:
        print(Fore.RED + "\nOpção Inválida!")
        input(Fore.YELLOW + "Pressione Enter para continuar...")
        main_menu()

# Iniciar o programa
if __name__ == '__main__':
    main_menu()
