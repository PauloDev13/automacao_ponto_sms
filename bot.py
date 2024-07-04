"""
WARNING:

Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
in order to get all the dependencies on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the dependencies.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install --upgrade -r requirements.txt`
- Use the same interpreter as the one used to install the bot (`pip install --upgrade -r requirements.txt`)

Please refer to the documentation for more information at
https://documentation.botcity.dev/tutorials/python-automations/web/
"""

# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

# Importa a dependencia do ChromeDriverManager do webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager

# Importa a dependencia do element_as_select do botcity
from botcity.web.util import element_as_select

# Importa a dependencia do table_to_dict
from botcity.web.parsers import table_to_dict

# Importa a dependencia do botcity.plugins.excel
from botcity.plugins.excel import BotExcelPlugin

from settings import Settings

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

excel = BotExcelPlugin()
# excel.add_row(['DATA ENTRADA', 'ENTRADA', 'DATA SAÍDA', 'SAÍDA', 'TRABALHADA', 'JUSTIFICADA', 'STATUS'])

cpf = input('Digite o CPF (ex: 123.456.789-00): ')
month_start = int(input('Digite o mês de inicial(ex: 01, 02, 10, 11...): '))
year_start = int(input('Digite o ano inicial (ex: 2005): '))
month_end = int(input('Digite o mês final(ex: 01, 02, 10, 11...): '))
year_end = int(input('Digite o ano final (ex: 2005): '))

# str_name_employe: WebElement = ''

def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()

    bot.headless = False

    bot.browser = Browser.CHROME

    # Baixa e instala a versão mais recente do ChromeDriver
    bot.driver_path = ChromeDriverManager().install()

    # Uncomment to set the WebDriver path
    # bot.driver_path = "<path to your WebDriver binary>"

    # Acessa a URL do sistema de ponto.
    bot.browse('https://natal.rn.gov.br/sms/ponto/index.php')

    # busca o campo de login, clica nele e digita o login
    input_user = bot.find_element('//*[@id="cpf"]', By.XPATH)
    input_user.click()
    input_user.send_keys(Settings().USER_LOGIN)

    # Pressiona a tecla TAB
    input_user.send_keys(Keys.TAB)

    # No campo senha, digita a senha
    input_password = bot.find_element('//*[@id="senha"]', By.XPATH)
    input_password.send_keys(Settings().USER_PASSWORD)

    # Acessa o IFrame onde está o captcha, clica nele e depois sai do IFrame
    bot.enter_iframe(0)
    captcha = bot.find_element('//*[@id="recaptcha-anchor"]', By.XPATH)
    # print(f'CAPTCHA: {captcha}')
    captcha.click()
    bot.leave_iframe()

    # Pausa de 30 segundos
    bot.wait(30000)

    # Vai para o botão de logar e clica
    button_send = bot.find_element('//*[@id="form"]/input', By.XPATH)
    button_send.click()

    # global_array = []
    # str_name_employe = ''

    # excel.add_row(
    #     [
    #         'DATA ENTRADA',
    #         'ENTRADA',
    #         'DATA SAÍDA',
    #         'SAÍDA',
    #         'TRABALHADA',
    #         'JUSTIFICADA',
    #         'STATUS'
    #     ]
    # )

    for year in range(year_start, year_end + 1):
        if year == year_start:
            # Chama a função loop_for_data que lê os dados da tabela
            loop_for_data(month_start, 13, year, bot)

            # Atribui a variável str_name_employe o valor contido no span (nome do servidor)
            str_name_employe = bot.find_element(
                '/html/body/div[2]/div/div[2]/div[2]/div[4]/div/span/font[1]', By.XPATH)

        elif year < year_end:
            # Chama a função loop_for_data que lê os dados da tabela
            loop_for_data(1, 13, year, bot)
        else:
            # Chama a função loop_for_data que lê os dados da tabela
            loop_for_data(1, month_end + 1, year, bot)

    # Cria o arquivo do Excel e salva no diretório
    excel.write(
        fr'C:\Users\prmorais\Desktop\BOT\{str_name_employe.text}_DE_{month_start}.{year_start}_A_{month_end}.{year_end}.xlsx')

    # Espera 3 secundos antes de fechar o browser
    bot.wait(3000)


    # Finaliza e limpa o Web Browser
    # You MUST invoke the stop_browser to avoid
    # leaving instances of the webdriver open
    bot.stop_browser()

    # Uncomment to mark this task as finished on BotMaestro
    # maestro.finish_task(
    #     task_id=execution.task_id,
    #     status=AutomationTaskFinishStatus.SUCCESS,
    #     message="Task Finished OK."
    # )

def not_found(label):
    print(f"Element not found: {label}")


def loop_for_data(month_1: int, month_2: int, year: int, bot:WebBot):
    for month in range(month_1, month_2):
        # Monta a URL com os query params CPF, Mês e Ano para acessar os dados
        bot.navigate_to(
            f'https://natal.rn.gov.br/sms/ponto/interno/aprova_justificativa/detalhes.php?cpf={cpf}&mes={month}&ano={year}')

        # Acessa a tabela e transforma os dados coletados num array de dicionários
        data_table = bot.find_element('//*[@id="mesatual"]/table', By.XPATH)
        data = table_to_dict(data_table)

        # Adciona linhas de cabeçalho em cada mês no arquivo do Excel
        excel.add_row('*****************************************************************')
        excel.add_row(f'MÊS: {month} - ANO: {year}')
        excel.add_row('*****************************************************************')
        excel.add_row(
            [
                'DATA ENTRADA',
                'ENTRADA',
                'DATA SAÍDA',
                'SAÍDA',
                'TRABALHADA',
                'JUSTIFICADA',
                'STATUS'
            ]
        )

        # Chama a função add_data_rows_excel que adiciona os dados no arquivo Excel
        add_data_rows_excel(data)


def add_data_rows_excel(data):
    # Atribui às variáveis os valores do array com dicionário data
    for item in data:
        str_data_entrada: str = item.get('data_entrada')
        str_entrada = item.get('entrada')
        str_data_entrada: str = item.get('data_entrada')
        str_saida = item.get('saída')
        str_trabalhada = item.get('trabalhada')
        str_hora_justificada = item.get('hora_justificada')
        str_status = item.get('status')

        # Adciona nova linha no arquivo do Excel a cada interação com os dados
        excel.add_row(
            [
                str_data_entrada,
                str_entrada,
                # str_data_saida,
                str_data_entrada,
                str_saida,
                str_trabalhada,
                str_hora_justificada,
                str_status
            ]
        )

if __name__ == '__main__':
    main()
