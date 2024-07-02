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
# excel.add_row(['DATA ENTRADA', 'ENTRADA', 'TRABALHADA', 'JUSTIFICADA', 'STATUS'])
excel.add_row(['DATA ENTRADA', 'ENTRADA', 'DATA SAÍDA', 'SAÍDA', 'TRABALHADA', 'JUSTIFICADA', 'STATUS', 'EDITAR'])
cpf = input('Digite o CPF (ex: 123.456.789-00): ')
mes = input('Digite o Mes (ex: 02, 03, 04, 05...): ')
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

    # Opens the BotCity website.
    bot.browse("https://natal.rn.gov.br/sms/ponto/index.php")

    # Implement here your logic...
    bot.wait(1000)

    input_user = bot.find_element('//*[@id="cpf"]', By.XPATH)
    input_user.click()
    input_user.send_keys('06543548479')

    input_user.send_keys(Keys.TAB)
    #
    input_password = bot.find_element('//*[@id="senha"]', By.XPATH)
    # input_password.click()
    input_password.send_keys('pgm2024')

    bot.enter_iframe(0)

    bot.wait(1000)

    captcha = bot.find_element('//*[@id="recaptcha-anchor"]', By.XPATH)
    captcha.click()

    bot.wait(10000)

    bot.leave_iframe()

    button_send = bot.find_element('//*[@id="form"]/input', By.XPATH)
    button_send.click()

    bot.wait(1000)

    bot.navigate_to(
        f'https://natal.rn.gov.br/sms/ponto/interno/aprova_justificativa/detalhes.php?cpf={cpf}&mes={mes}&ano={ano}')

    bot.wait(1000)

    data_table = bot.find_element('//*[@id="mesatual"]/table', By.XPATH)
    data = table_to_dict(data_table)

    bot.wait(3000)

    print(data)

    for item in data:
        excel.add_row(item.values())
        str_data_entrada = item['data_entrada']
        print(str_data_entrada)
        str_entrada = item['entrada']
        print(str_entrada)
            # str_data_saida = item['data_saída']
            # print(str_data_saida)
            # str_saida = item['saída']
            # print(str_saida)
        # str_trabalhada = item['trabalhada']
        # print(str_trabalhada)
        str_hora_justificada = item['hora_justificada']
        print(str_hora_justificada)
        str_status = item['status']
        print(str_status)

    # excel.add_row([str_data_entrada,
    #                 str_entrada,
    #                 # str_data_saida,
    #                 # str_saida,
    #                 str_trabalhada,
    #                 str_hora_justificada,
    #                 str_status]
    #                       )

    # excel.write(r'C:\Desenvolvimento\_projeto_python\automacao_ponto_sms\Teste.xlsx')
    # Wait 3 seconds before closing
    bot.wait(5000)
    # input()

    # Finish and clean up the Web Browser
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
