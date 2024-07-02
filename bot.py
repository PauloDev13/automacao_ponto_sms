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

# Importa a dependencia do ChromeDriverManager do webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager

# Importa a dependencia do element_as_select do botcity
from botcity.web.util import element_as_select

# Importa a dependencia do table_to_dict
from botcity.web.parsers import table_to_dict

# Importa a dependencia do botcity.plugins.excel
from botcity.plugins.excel import BotExcelPlugin

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

excel = BotExcelPlugin()
# excel.add_row(['DATA ENTRADA', 'ENTRADA', 'DATA SAÍDA', 'SAÍDA', 'TRABALHADA', 'JUSTIFICADA', 'STATUS'])

cpf = input('Digite o CPF (ex: 123.456.789-00): ')
month_start = input('Digite o Mês de início(ex: 1, 2, 3, 10, 11...): ')
month_end = input('Digite o Mês de final(ex: 1, 2, 3, 10, 11...): ')
ano = input('Digite o Ano (ex: 2024): ')

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

    # Pausa de 1 segundo
    bot.wait(1000)

    # busca o campo de login, clica nele e digita o login
    input_user = bot.find_element('//*[@id="cpf"]', By.XPATH)
    input_user.click()
    input_user.send_keys('')

    # Pressiona a tecla TAB
    input_user.send_keys(Keys.TAB)

    # No campo senha, digita a senha
    input_password = bot.find_element('//*[@id="senha"]', By.XPATH)
    input_password.send_keys('')

    # Acessa o IFrame onde está o captcha, clica nele e depois sai do IFrame
    bot.enter_iframe(0)
    captcha = bot.find_element('//*[@id="recaptcha-anchor"]', By.XPATH)
    captcha.click()
    bot.leave_iframe()

    # Pausa de 30 segundos
    bot.wait(30000)

    # Vai para o botão de logar e clica
    button_send = bot.find_element('//*[@id="form"]/input', By.XPATH)
    button_send.click()

    # Pausa de 1 segundo
    bot.wait(1000)

    # Define uma variável que vai receber o nome registrado no ponto
    str_name_employe = ''

    # Inicia um laço usando o intervalo dos meses informados
    for month in range(int(month_start), int(month_end) + 1):
        # Pausa de 2 segundos
        bot.wait(2000)

        # Monta a URL com o CPF, Mês e Ano para acessar os dados do ponto para cada mês
        bot.navigate_to(
            f'https://natal.rn.gov.br/sms/ponto/interno/aprova_justificativa/detalhes.php?cpf={cpf}&mes={month}&ano={ano}')

        # Se a variável str_name_employe estiver vazia, acessa o elemento do DOM que tem o nome do servidor
        if not str_name_employe:
            str_name_employe = bot.find_element(
                '/html/body/div[2]/div/div[2]/div[2]/div[4]/div/span/font[1]', By.XPATH)

        # Acessa a tabela com os dados do ponto e transforma num array de dicionários
        data_table = bot.find_element('//*[@id="mesatual"]/table', By.XPATH)
        data = table_to_dict(data_table)

        # Imprime os dados obtidos na tabela
        print(data)

        # Adiciona uma linha ao arquivo do Excel que seria criado com o mês e o ano pesquisados
        excel.add_row([f'MÊS: 0{month} - ANO: {ano}'])

        # Adiciona uma nova linha com o cabeçalho das colunas
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

        # Faz um loop nos dados obtidos na tabela de ponto
        for item in data:

            # Pausa de 1 segundo e 7 décimos
            bot.wait(1700)

            # Acessa cada chave do dicionário montado anteriormente
            str_data_entrada = item['data_entrada']
            str_entrada = item['entrada']
            str_data_saida = item['data_saída']
            str_saida = item['saída']
            str_trabalhada = item['trabalhada']
            str_hora_justificada = item['hora_justificada']
            str_status = item['status']

            # Adciona nova linha no arquivo do Excel a cada interação com os dados obtidos no dicionário
            excel.add_row(
                [
                    str_data_entrada,
                    str_entrada,
                    str_data_saida,
                    str_saida,
                    str_trabalhada,
                    str_hora_justificada,
                    str_status
                ]
            )

    # Cria o arquivo do Excel e salva no diretório com o nome do servidor + o ano da pesquisa
    excel.write(fr'C:\Users\paulo.morais\Desktop\BOT\{str_name_employe.tex}-{ano}.xlsx')

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


if __name__ == '__main__':
    main()
