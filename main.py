
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from marcar_pedido import esperar_pagina_carregar, clicar_ultima_checkbox, marcar_Canhoto, marcar_Romaneio, marcar_Transporte, atualizar_pedidos
import sys
import io
import re


options = webdriver.ChromeOptions()
#options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-logging")
options.add_argument("--log-level=3")
options.add_argument("--silent")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=AudioServiceOutOfProcess") 
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
#driver = webdriver.Edge(options=options)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

if len(sys.argv) < 7:
    print("** Argumentos insuficientes!")
    sys.exit(1)

status = {
    "separacao": "OK!",
    "canhoto": "OK!",
    "transporte": "OK!"
}

ID = sys.argv[1]
pedid = sys.argv[2]
veiculo = sys.argv[3]
placa = sys.argv[4]
motorista = sys.argv[5]
data = sys.argv[6]
jaimpresso = sys.argv[7]

urlRomaneio = 'https://sv13.brascomm.net.br/cgi-bin/exec.cgi?PRG=ftp130a1&ID='+ID
urlCanhoto = 'https://sv13.brascomm.net.br/cgi-bin/exec.cgi?PRG=ftp183a1&ID='+ID
urlTransporte = 'https://sv13.brascomm.net.br/cgi-bin/exec.cgi?PRG=ftp174a1&ID='+ID
urlMotorista = 'https://sv13.brascomm.net.br/cgi-bin/exec.cgi?PRG=ftp131a1&ID='+ID

pattern = r'^\d+(,\d+)*$'

if re.fullmatch(pattern, pedid):
    print('')
    print('-------- PEDIDOS --------\n')
    pedidos = [pedido + "-0" for pedido in pedid.split(",")]
    print(pedidos)
    print(f"\nTotal de pedidos: {len(pedidos)}")
    print('')
else:
    print('')
    messagebox.showerror(
    "Erro",
    "Digite apenas numeros separados por virgula."  
)
    print("Digite apenas numeros separados por virgula")
    sys.exit(1)
    print('')

print('')
print('-------- SEPARACAO --------')
print('')


driver.get(urlRomaneio)

driver.find_element(By.NAME, "DADATA").clear()
driver.find_element(By.NAME, "DADATA").send_keys(data)
driver.execute_script("newget()")
esperar_pagina_carregar(driver)

for pedido in pedidos:
        marcar_Romaneio(driver, pedido,status)
        time.sleep(0.5)

driver.execute_script("save();")



print('')
print('-------- MAPA --------')
print('')

driver.execute_script(f"window.open('{urlMotorista}');")
driver.switch_to.window(driver.window_handles[-1])

esperar_pagina_carregar(driver)

NumMapa = clicar_ultima_checkbox(driver)

driver.find_element(By.NAME, "VEICULO").send_keys(veiculo)
driver.find_element(By.NAME, "PLACA").send_keys(placa)
driver.find_element(By.NAME, "MOTORISTA").send_keys(motorista)

driver.execute_script("save();")

time.sleep(0.5)   

print('')
print('-------- CANHOTO --------')
print('')

driver.execute_script(f"window.open('{urlCanhoto}');")
driver.switch_to.window(driver.window_handles[-1])
esperar_pagina_carregar(driver)

driver.find_element(By.NAME, "DADATA").clear()
driver.find_element(By.NAME, "DADATA").send_keys(data)
driver.execute_script("newget()")
esperar_pagina_carregar(driver)


for pedido in pedidos:
        marcar_Canhoto(driver, pedido,status)
        time.sleep(0.5)
driver.execute_script("save();")

print('')
print('-------- TRANSPORTE --------')
print('')

driver.execute_script(f"window.open('{urlTransporte}','_blank');")
driver.switch_to.window(driver.window_handles[-1])
esperar_pagina_carregar(driver)

driver.find_element(By.NAME, "DADATA").clear()
driver.find_element(By.NAME, "DADATA").send_keys(data)

if jaimpresso == "SIM":
  driver.find_element(By.NAME, "JAIMPRESSOS").click()
driver.execute_script("newget()")
esperar_pagina_carregar(driver)

for pedido in pedidos:
        marcar_Transporte(driver, pedido,status)
        time.sleep(0.5)

driver.execute_script("save();")



print('')
print('-------- ROTERIZACAO DAS ENTREGAS --------')
print('')
esperar_pagina_carregar(driver)
atualizar_pedidos(driver, pedidos)

print('')
print('------------------------')
print('')
print(f"** Mapa: {NumMapa} - Motorista: {motorista}" )
messagebox.showinfo(
    "Sucesso",
    f"** Romaneio: {status['separacao']}\n"
    f"** Canhoto: {status['canhoto']}\n"
    f"** Transporte: {status['transporte']}\n"
)