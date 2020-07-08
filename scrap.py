import pandas as pd
import time
from time import gmtime, strftime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from progress.bar import Bar

options = Options()
options.headless = True
# dados = pd.read_csv('simpro.csv')
dados = pd.read_csv('simpro_reganvisa_nao_localizados_202007061433.csv')

n_localizados = 0
print('{} | Processamento iniciado para {} registros.'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime()), len(dados)))
bar = Bar('Consultando registros...', max=len(dados))

driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 2) # TODO: o wait do selenium não está funcionando, pode ser um bug de versão

for index,row in dados.iterrows():
    rows_list = []
    cd_reg_anvisa = row[0]

    try:
        driver.get('https://consultas.anvisa.gov.br/#/saude/q/?numeroRegistro={}'.format(cd_reg_anvisa))
        # time.sleep(1)

        # https://consultas.anvisa.gov.br/#/saude/q/?numeroRegistro=8003400016
        titulo = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[contains(text(), \'Resultado da Consulta\')]')))

        reg_anvisa = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[contains(text(), \'{}\')]'.format(cd_reg_anvisa))))
        reg_anvisa.click()
        time.sleep(1)

        nome_tecnico = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Nome Técnico')]/following-sibling::td")))
        rows_list.append([cd_reg_anvisa, nome_tecnico.text])
    except TimeoutException as e:
        n_localizados += 1
        rows_list.append([cd_reg_anvisa, ''])
    except Exception as ex:
        print('Erro em {}: {}'.format(cd_reg_anvisa, str(ex)))
    finally:
        resultado = pd.DataFrame(rows_list, columns=['cd_reg_anvisa', 'nome_tecnico'])
        resultado.to_csv('resultado.csv', mode='a', header=False, index=False, sep=';', quoting=2)
    bar.next()
    pass

driver.quit()
bar.finish()

print('{} | Processamento concluído com {} registros localizados e {} não localizados.'.format(
    strftime("%Y-%m-%d %H:%M:%S", gmtime()), len(resultado), n_localizados))
