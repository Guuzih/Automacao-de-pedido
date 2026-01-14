
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def marcar_Romaneio(driver, pedido,status):
    try:
        # Espera até 10 segundos o pedido aparecer na tabela
        linha = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//tr[td[2]//p[text()='{pedido}']]")
            )
        )
        # Localiza o checkbox dentro da linha
        checkbox = linha.find_element(By.XPATH, ".//td[1]//input[@type='checkbox']")
        checkbox.click()
        print(f"Pedido {pedido} marcado com sucesso!")
    except TimeoutException:
        print(f"Pedido {pedido} nao encontrado na tabela.")
        status["separacao"] = "Algum pedido não localizado"
    except NoSuchElementException:
        print(f"Checkbox do pedido {pedido} nao encontrado.")
    return status

def marcar_Canhoto(driver, pedido,status):
    try:
        # Espera até 10s para encontrar o pedido
        linha = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//tbody[@class='scrollingContent']/tr[td[3]//font[text()='{pedido}']]")
            )
        )
        # Localiza o checkbox na primeira coluna da linha
        checkbox = linha.find_element(By.XPATH, ".//td[1]//input[@type='checkbox']")
        checkbox.click()
        print(f"Pedido {pedido} marcado com sucesso!")
    except TimeoutException:
        print(f"Pedido {pedido} nao encontrado na tabela.")
        status["canhoto"] = "Algum pedido não localizado"
    except NoSuchElementException:
        print(f"Checkbox do pedido \033[1m{pedido}\033 nao encontrado.")
        status["canhoto"] = "Algum pedido não localizado"
    return status


def marcar_Transporte(driver, pedido,status):
    
    try:
        # Espera até 10s para encontrar o pedido na 4ª coluna do tbody
        linha = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//tbody[@class='scrollingContent']/tr[td[4][text()='{pedido}']]")
            )
        )
        # Localiza o checkbox na segunda coluna da linha
        checkbox = linha.find_element(By.XPATH, ".//td[2]//input[@type='checkbox']")
        checkbox.click()
        print(f"Pedido {pedido} marcado com sucesso!")
    except TimeoutException:
        print(f"Pedido {pedido} nao encontrado na tabela.")
        status["transporte"] = "Algum pedido não localizado"
    except NoSuchElementException:
        print(f"Checkbox do pedido {pedido} nao encontrado.")
        status["transporte"] = "Algum pedido não localizado"
    return status

def atualizar_pedidos(driver, pedidos):
    
    # Itera pelos pedidos
    for i, pedido in enumerate(pedidos, start=1):
        try:
            # Acha a célula pelo número do pedido
            cell = driver.find_element(By.XPATH, f"//td[contains(., '{pedido}')]")
            
            # Pega a linha inteira
            row = cell.find_element(By.XPATH, "./ancestor::tr")
            
            # Última célula (td)
            last_td = row.find_elements(By.TAG_NAME, "td")[-1]
            
            # Substitui o conteúdo pelo índice (1, 2, 3, ...)
            driver.execute_script(
                "arguments[0].innerText = arguments[1];", 
                last_td, 
                str(i)
            )
            
            print(f"O {pedido} sera o {i} a ser entregue!")
        except Exception as e:
            print(f"Nao encontrei o pedido {pedido}")
    


def clicar_ultima_checkbox(driver):
    try:

        tbody = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//tbody[@class='scrollingContent']"))
        )


        linhas = tbody.find_elements(By.TAG_NAME, "tr")

        if not linhas:
            print("Nenhuma linha encontrada")
            return None

     
        ultima_linha = linhas[-1]


        checkbox = ultima_linha.find_element(By.XPATH, ".//input[@type='checkbox']")
        numero = ultima_linha.find_element(By.XPATH, ".//td[2]").text.strip()

        if not checkbox.is_selected():
            checkbox.click()
            print(f"Mapa: {numero}")
        else:
            print("Mapa não encontrado")

        return numero

    except Exception as e:
        print(f"Erro ao tentar marcar a última checkbox: {e}")
        return None

def esperar_pagina_carregar(driver, timeout=120):
    """Espera ate que o document.readyState seja 'complete' ou timeout seja atingido."""
    import time
    start = time.time()
    while True:
        estado = driver.execute_script("return document.readyState;")
        if estado == "complete":
            break
        if time.time() - start > timeout:
            print("Timeout esperando página carregar!")
            break
        time.sleep(0.5)
