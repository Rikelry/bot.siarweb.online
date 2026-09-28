import os
import sys

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright


def abrir_pagina(page, url):
    page.goto(url)
    page.wait_for_load_state("domcontentloaded")


def refeicao_ja_solicitada(page, tipo):
    formulario = page.locator(
        f'form:has(input[name="tipo"][value="{tipo}"])'
    )

    if formulario.count() == 0:
        return True

    acao = formulario.locator('input[name="acao"]').input_value()

    return acao == "cancelar"


def solicitar_refeicao(page, tipo, dashboard_url):
    formulario = page.locator(
        f'form:has(input[name="tipo"][value="{tipo}"])'
    )

    if formulario.count() == 0:
        print(f"{tipo}: formulário não encontrado.")
        return False

    botao = formulario.locator('button[type="submit"]')

    if not botao.is_visible() or not botao.is_enabled():
        print(f"{tipo}: botão indisponível.")
        return False

    botao.click()
    page.wait_for_load_state("domcontentloaded")

    abrir_pagina(page, dashboard_url)

    if not dashboard_carregado(page):
        print(f"{tipo}: dashboard não carregado após a solicitação.")
        return False

    if refeicao_ja_solicitada(page, tipo):
        print(f"{tipo}: solicitação registrada com sucesso.")
        return True

    print(f"{tipo}: solicitação não foi confirmada.")
    return False


def dashboard_carregado(page):
    if "/app/dashboard.php" not in page.url:
        return False

    if page.get_by_text("Sistema de Refeitório").count() == 0:
        return False

    if page.get_by_text("Informações Importantes").count() == 0:
        return False

    return True


def main():
    load_dotenv()

    # Public
    siarweb_url = os.getenv("SIARWEB_URL")
    dashboard_url = os.getenv("DASHBOARD_URL")

    # Private
    matricula = os.getenv("MATRICULA")
    data_nasc = os.getenv("DATA_NASC")
    pin = os.getenv("PIN")

    if not siarweb_url or not dashboard_url or not matricula or not data_nasc or not pin:
        print("Erro: uma ou mais configurações não foram encontradas.")
        return

    try:
        with sync_playwright() as p:
            headless = os.getenv("CI") == "true"

            browser = p.chromium.launch(headless=headless)
            page = browser.new_page()

            # Acessa o SIARWEB
            abrir_pagina(page, siarweb_url)

            # Abre a página de login
            page.get_by_text("Acessar o Sistema").click()

            # Preenche matrícula e data de nascimento
            page.locator("#matricula").press_sequentially(
                matricula,
                delay=100,
            )

            page.locator("#data_nasc").press_sequentially(
                data_nasc,
                delay=100,
            )

            # Aguarda o JavaScript processar a data
            page.wait_for_timeout(1000)

            # Envia o login
            page.locator("#btnLogin").click()
            page.wait_for_load_state("domcontentloaded")

            if "/app/validar_pin.php" not in page.url:
                print("Falha no login.")
                print("URL:", page.url)
                browser.close()
                return

            print("✓ Login realizado.")

            # Preenche o PIN
            page.locator("body").press_sequentially(
                pin,
                delay=100,
            )

            # Envia o PIN
            page.locator("#btnPin").click()
            page.wait_for_load_state("domcontentloaded")

            if "/app/dashboard.php" not in page.url:
                print("Falha na autenticação com o PIN.")
                print("URL:", page.url)
                browser.close()
                return

            print("✓ PIN autenticado.")

            if not dashboard_carregado(page):
                print("Falha: dashboard não carregado corretamente.")
                browser.close()
                return

            print("✓ Dashboard carregado.")

            # Verifica as refeições
            almoco_solicitado = refeicao_ja_solicitada(page, "ALMOCO")
            jantar_solicitado = refeicao_ja_solicitada(page, "JANTAR")

            almoco_solicitado_agora = False
            jantar_solicitado_agora = False

            print("\n--- REFEIÇÕES ---")

            if almoco_solicitado:
                print("Almoço: já solicitado.")
            else:
                print("Almoço: será solicitado.")

            if jantar_solicitado:
                print("Jantar: já solicitado.")
            else:
                print("Jantar: será solicitado.")

            # Solicita almoço se necessário
            if not almoco_solicitado:
                almoco_solicitado_agora = solicitar_refeicao(page, "ALMOCO", dashboard_url)
                almoco_solicitado = almoco_solicitado_agora

            # Solicita jantar se necessário
            if not jantar_solicitado:
                jantar_solicitado_agora = solicitar_refeicao(page, "JANTAR", dashboard_url)
                jantar_solicitado = jantar_solicitado_agora

            # Recarrega o dashboard para confirmar o estado final das refeições
            abrir_pagina(page, dashboard_url)

            # Verifica novamente o estado das refeições
            almoco_solicitado = refeicao_ja_solicitada(page, "ALMOCO")
            jantar_solicitado = refeicao_ja_solicitada(page, "JANTAR")

            print("\n--- RESULTADO ---")

            if almoco_solicitado_agora:
                print("✓ Almoço solicitado agora.")
            elif almoco_solicitado:
                print("✓ Almoço já estava solicitado.")
            else:
                print("✗ Almoço não confirmado.")

            if jantar_solicitado_agora:
                print("✓ Jantar solicitado agora.")
            elif jantar_solicitado:
                print("✓ Jantar já estava solicitado.")
            else:
                print("✗ Jantar não confirmado.")

            print("\n✓ Processo concluído.")

            browser.close()

    except Exception as erro:
        print("\nErro inesperado durante a execução.")
        print("Detalhes:", erro)
        sys.exit(1)


if __name__ == "__main__":
    main()