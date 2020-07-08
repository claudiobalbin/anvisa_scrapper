import pandas as pd
import time
from time import gmtime, strftime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from progress.bar import Bar

options = Options()
options.headless = True
dados = pd.read_csv('simpro.csv')
# dados = pd.read_csv('simpro_reganvisa_nao_localizados_202007061433.csv')
# rows_list = []
rows_n_local = []
print('{} | Processamento iniciado para {} registros.'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime()), len(dados)))
bar = Bar('Consultando registros...', max=len(dados))

for index,row in dados.iterrows():
    rows_list = []
    cd_reg_anvisa = row[0]
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 2) # TODO: o wait do selenium não está funcionando, pode ser um bug de versão
    
    # print('Consultando codigo: {}'.format(cd_reg_anvisa))
    driver.get('https://consultas.anvisa.gov.br/#/saude/q/?numeroRegistro={}'.format(cd_reg_anvisa))
    # time.sleep(2)

    try:
        reg_anvisa = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), \'8003400014\')]')))    
        reg_anvisa.click()
        time.sleep(1)        
        nome_tecnico = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Nome Técnico')]/following-sibling::td")))
        # print('Nome Técnico: {}'.format(nome_tecnico.text))
        rows_list.append([cd_reg_anvisa, nome_tecnico.text])
        resultado = pd.DataFrame(rows_list, columns=['cd_reg_anvisa', 'nome_tecnico'])
        resultado.to_csv('resultado.csv', mode='a', header=False, index=False, sep=';', quoting=2)
    except:
        # Nao localizou
        # print('Registro não localizado.')
        rows_n_local.append([cd_reg_anvisa])
    finally:
        driver.quit()
    bar.next()
    pass

bar.finish()
n_localiz = pd.DataFrame(rows_n_local)
# resultado = pd.DataFrame(rows_list, columns=['cd_reg_anvisa', 'nome_tecnico'])
# resultado.to_csv('resultado.csv', mode='a', header=False, index=False, sep=';', quoting=2)

print('{} | Processamento concluído com {} registros localizados e {} não localizados.'.format(
    strftime("%Y-%m-%d %H:%M:%S", gmtime()), len(resultado), len(n_localiz)))
