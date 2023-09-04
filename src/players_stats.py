import asyncio
from playwright.async_api import async_playwright

## O SITE QUE TA NO NAVEGADOR EH DIFERENTE DO OFICIAL 

async def extract_csgo_player_info():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless = False)
        page = await browser.new_page()

        await page.goto("https://www.hltv.org/stats/players/9216/tabseN")

        # Espera até que as estatísticas do jogador estejam disponíveis na página
        await page.wait_for_selector('.playerpage-ratings-container')

        # Extraia as estatísticas do jogador
        player_stats = await page.innerText('.playerpage-ratings-value')
        print(f"Estatísticas do jogador tabseN:\n{player_stats}")

        # Extraia as informações das próximas e recentes partidas
        upcoming_matches = await page.innerText('.upcoming-matches-box .upcoming-matches-team')
        recent_matches = await page.innerText('.matches-box .matches-team')

        print("\nPróximas partidas:")
        print(upcoming_matches)

        print("\nRecentes partidas:")
        print(recent_matches)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(extract_csgo_player_info())
