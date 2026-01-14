import subprocess
import threading
import tkinter as tk
from tkinter import scrolledtext, PhotoImage
import os
import queue

# ------------------- CONFIG MOTORISTAS -------------------
opcoes = {
    "Joao": {"veiculo": "Master", "placa": "FLX4G76"},
    "Edinei": {"veiculo": "Master", "placa": "QOY1H23"},
    "Vitor Capelli": {"veiculo": "FRETEIRO", "placa": "EQM2D57"},
    "Diego Porfilio": {"veiculo": "FRETEIRO", "placa": "PZJ9H46"},
    "Leandro ": {"veiculo": "FRETEIRO", "placa": "NGU3012"},
    "Luciano ": {"veiculo": "FRETEIRO", "placa": "FMW5938"},
    "Douglas ": {"veiculo": "FRETEIRO", "placa": "FGT8G33"},
    "Caue ": {"veiculo": "FRETEIRO", "placa": "DZD8I76"},
    "Paulo ": {"veiculo": "FRETEIRO", "placa": "MIA1B56"},
    "Caio ": {"veiculo": "FRETEIRO", "placa": "DOM3G18"},
    "Cleber Soares": {"veiculo": "FRETEIRO", "placa": "EYP5H21"},
    "Cleber Batista": {"veiculo": "FRETEIRO", "placa": "GKG5A09"},
    "Raimundo ": {"veiculo": "Caminhao", "placa": "FXB0282"},
    "Joao Frete": {"veiculo": "Caminhao", "placa": "FXB0282"},
    "Retirada - Cliente": {"veiculo": "Retirada - Cliente", "placa": "Retirada - Cliente"},
    "Retirada - Colabor": {"veiculo": "Retirada - Colabor", "placa": "Retirada - Colabor"},
    "": {"veiculo": "", "placa": ""},
}

processo = None
fila_logs = queue.Queue()

# ------------------- FUNÇÕES -------------------
def executar_script():
    global processo
    ID = entrada_id.get()
    pedidos = entrada_pedidos.get()
    motorista = motorista_var.get()
    data = entrada_data.get()
    jaimpresso = jaimpresso_var.get()

    if not pedidos.strip() or motorista == "Selecione":
        fila_logs.put("⚠ Preencha os pedidos e selecione um motorista\n")
        return

    veiculo = opcoes[motorista]["veiculo"]
    placa = opcoes[motorista]["placa"]

    fila_logs.put("🚚 Rodando automação com:\n")
    fila_logs.put(f"ID: {ID}\nPedidos: {pedidos}\nVeículo: {veiculo}\nPlaca: {placa}\nMotorista: {motorista}\nData: {data}\nJá impresso: {jaimpresso}\n\n")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    main_path = os.path.join(BASE_DIR, "main.py")

    processo = subprocess.Popen(
        ["python", main_path, ID, pedidos, veiculo, placa, motorista, data, jaimpresso],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    def ler_saida():
        for linha in processo.stdout:
            fila_logs.put(linha)

    threading.Thread(target=ler_saida, daemon=True).start()


def cancelar_script():
    global processo
    if processo and processo.poll() is None:
        processo.terminate()
        fila_logs.put("⛔ Operação cancelada pelo usuário!\n")
        processo = None
    else:
        fila_logs.put("⚠ Nenhum processo em execução para cancelar.\n")


def limpar_log():
    log.delete(1.0, tk.END)


def atualizar_log():
    while not fila_logs.empty():
        linha = fila_logs.get()
        log.insert(tk.END, linha)
        log.yview(tk.END)
    janela.after(200, atualizar_log)


# ------------------- INTERFACE -------------------
janela = tk.Tk()
janela.title("Automação de Pedidos - SOS Restaurante")
janela.geometry("950x750")
janela.configure(bg="#ecf0f1")

# ------------------- FUNDO -------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
bg_path = os.path.join(BASE_DIR, "sosfundo.png")
if os.path.exists(bg_path):
    bg_img = PhotoImage(file=bg_path)
    bg_label = tk.Label(janela, image=bg_img)
    bg_label.place(relwidth=1, relheight=1)

# ------------------- CABEÇALHO -------------------
header_path = os.path.join(BASE_DIR, "soscabecalho.png")
if os.path.exists(header_path):
    header_img = PhotoImage(file=header_path)
    tk.Label(janela, image=header_img, bd=0).pack(fill="x")

# ------------------- FRAME DE INPUTS -------------------
frame_inputs = tk.Frame(janela, bg="#ffffff", bd=3, relief="groove", padx=15, pady=15)
frame_inputs.pack(pady=20, padx=20)

def add_label(entry_row, texto):
    label = tk.Label(frame_inputs, text=texto, bg="#ffffff", font=("Arial", 10, "bold"))
    label.grid(row=entry_row, column=0, sticky="e", padx=5, pady=5)
    return label

# Inputs
add_label(0, "ID:")
entrada_id = tk.Entry(frame_inputs, width=40)
entrada_id.grid(row=0, column=1, pady=5)

add_label(1, "Pedidos (separados por vírgula):")
entrada_pedidos = tk.Entry(frame_inputs, width=40)
entrada_pedidos.grid(row=1, column=1, pady=5)

add_label(2, "Motorista:")

motorista_var = tk.StringVar(janela)
motorista_var.set("Selecione")

# Frame para OptionMenu + botão Motorista
frame_motorista = tk.Frame(frame_inputs, bg="#ffffff")
frame_motorista.grid(row=2, column=1, pady=5, sticky="w")

menu_motorista = tk.OptionMenu(frame_motorista, motorista_var, *opcoes.keys())
menu_motorista.config(width=25, font=("Arial", 10))
menu_motorista.pack(side="right")


add_label(3, "Data:")
entrada_data = tk.Entry(frame_inputs, width=40)
entrada_data.insert(0, "01/08/2025")
entrada_data.grid(row=3, column=1, pady=5)

add_label(4, "Já impresso?")
jaimpresso_var = tk.StringVar(janela)
jaimpresso_var.set("NAO")
menu_jaimpresso = tk.OptionMenu(frame_inputs, jaimpresso_var, "SIM", "NAO")
menu_jaimpresso.grid(row=4, column=1, pady=5, sticky="w")

# ------------------- FRAME DE BOTOES -------------------
frame_botoes = tk.Frame(janela, bg="#ecf0f1")
frame_botoes.pack(pady=15)

def estilizar_botao(botao, cor_normal, cor_hover):
    botao.config(bg=cor_normal, fg="white", font=("Arial", 11, "bold"), relief="flat", padx=10, pady=5, width=20)
    botao.bind("<Enter>", lambda e: botao.config(bg=cor_hover))
    botao.bind("<Leave>", lambda e: botao.config(bg=cor_normal))

btn_executar = tk.Button(frame_botoes, text="▶ Executar Automação", command=executar_script)
btn_cancelar = tk.Button(frame_botoes, text="⛔ Cancelar", command=cancelar_script)
btn_limpar = tk.Button(frame_botoes, text="🧹 Limpar Log", command=limpar_log)

btn_executar.grid(row=0, column=0, padx=10)
btn_cancelar.grid(row=0, column=1, padx=10)
btn_limpar.grid(row=0, column=2, padx=10)

# Aplica estilos
estilizar_botao(btn_executar, "#27ae60", "#2ecc71")
estilizar_botao(btn_cancelar, "#c0392b", "#e74c3c")
estilizar_botao(btn_limpar, "#2980b9", "#3498db")

# ------------------- LOG -------------------
log = scrolledtext.ScrolledText(janela, width=95, height=18, font=("Courier New", 9), bd=2, relief="sunken", bg="#fdfdfd")
log.pack(pady=15)

# ------------------- LOOP -------------------
atualizar_log()
janela.mainloop()
