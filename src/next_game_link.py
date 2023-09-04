from playwright.sync_api import sync_playwright

# URL da página que você deseja analisar
url = 'https://www.hltv.org/matches/2366082/big-vs-monte-esl-pro-league-season-18'

with sync_playwright() as p:
    browser = p.chromium.launch(headless= False)
    page = browser.new_page()
    page.goto(url)
    
    # Agora você pode usar o Playwright para interagir com a página, como clicar em botões, preencher formulários, etc.
    
    # Aqui, encontramos todas as divs com a classe "team1-gradient"
    team_divs_1 = page.query_selector_all('.team1-gradient')
    team_divs_2 = page.query_selector_all('.team2-gradient')
    
   #s divs e extrair os links das equipes
    for div in team_divs_1:
        team_link = div.query_selector('a').get_attribute('href')
        print("Link da equipe 1:", team_link)

    for div in team_divs_2:
        team_link = div.query_selector('a').get_attribute('href')
        print("Link da equipe 2:", team_link)
    
    browser.close()