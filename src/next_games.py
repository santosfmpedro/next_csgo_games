import pandas as pd

from playwright.sync_api import sync_playwright

# Define uma função para fazer o web scraping
def scrape_upcoming_matches(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = False)
        page = browser.new_page()

        # Navega até a URL desejada
        page.goto(url)

        # Localiza todas as divs com a classe "upcomingMatch"
        match_elements = page.query_selector_all('.upcomingMatch')

        # Cria uma lista para armazenar os resultados
        results = []

        # Itera sobre cada elemento da lista e extrai os dados
        for match_element in match_elements:
            match_data = {}

            # Extrai o link da âncora que leva para a página do jogo
            match_link_element = match_element.query_selector('a.match.a-reset')
            if match_link_element:
                match_data['match_link'] = match_link_element.get_attribute('href')
            else:
                match_data['match_link'] = ''

            match_data['unix_timestamp'] = match_element.get_attribute('data-zonedgrouping-entry-unix')
            match_data['stars'] = match_element.get_attribute('stars')
            match_data['lan'] = match_element.get_attribute('lan')
            match_data['filteraslive'] = match_element.get_attribute('filteraslive')
            match_data['team1'] = match_element.get_attribute('team1')
            match_data['team2'] = match_element.get_attribute('team2')

            # Extrai informações adicionais dentro do elemento, verificando a existência dos elementos
            match_time_element = match_element.query_selector('.matchTime')
            if match_time_element:
                match_data['match_time'] = match_time_element.inner_text()
            else:
                match_data['match_time'] = ''

            match_rating_element = match_element.query_selector('.matchRating')
            if match_rating_element:
                match_data['match_rating'] = match_rating_element.inner_text()
            else:
                match_data['match_rating'] = ''

            match_meta_element = match_element.query_selector('.matchMeta')
            if match_meta_element:
                match_data['match_meta'] = match_meta_element.inner_text()
            else:
                match_data['match_meta'] = ''

            team1_name_element = match_element.query_selector('.matchTeamName.team1')
            if team1_name_element:
                match_data['team1_name'] = team1_name_element.inner_text()
            else:
                match_data['team1_name'] = ''

            team2_name_element = match_element.query_selector('.matchTeamName.team2')
            if team2_name_element:
                match_data['team2_name'] = team2_name_element.inner_text()
            else:
                match_data['team2_name'] = ''

            results.append(match_data)


        browser.close()

    return results

# Define uma função para fazer o web scraping dos links dos times
def scrape_team_links(match_data_list):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Itera sobre os dados de cada jogo
        for index, match_data in enumerate(match_data_list):
            match_link = match_data.get('match_link', '')

            if match_link:
                # Navega até a página do jogo
                page.goto(match_link)

                # Localiza a div com a classe "team1-gradient"
                team1_div = page.query_selector('.team1-gradient')

                if team1_div:
                    # Extrai o link do time na div
                    team_link = team1_div.query_selector('a')['href']
                    match_data_list[index]['team1_link'] = team_link

        browser.close()

    return match_data_list
# URL do site que contém as divs que você deseja raspar
url = 'https://www.hltv.org/events/6863/matches'  # Substitua pelo URL real

# Chama a função e obtém os resultados em uma lista de dicionários
# Chama a função e obtém os resultados iniciais em uma lista de dicionários
initial_match_data_list = scrape_upcoming_matches(url)

# Chama a função para obter os links dos times
updated_match_data_list = scrape_team_links(initial_match_data_list)

# Cria um DataFrame a partir dos dados
df = pd.DataFrame(updated_match_data_list)

df.to_csv('results.csv', index=False)  # I
# Imprime a lista de dicionários com os dados extraídos
print(df)
