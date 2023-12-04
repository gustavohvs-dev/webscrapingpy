import requests
import pandas as pd
from bs4 import BeautifulSoup

# Parâmetros 
url = 'https://www.cnnbrasil.com.br/'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
shouldVisitPagesLimit = 100

# Listas e variáveis
shouldVisitPages = []
visitedPages = []
visitedPagesStatusCode = []
visitedPagesContent = []
isLimitReached = False
shouldVisitPagesIndex = 0
countSuccessVisitedPages = 0
countFailedVisitedPages = 0

# Busca inicial
site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')

# Busca novos links
if(site.status_code == 200):
    if(isLimitReached == False):
        for a in soup.find_all('a', href=True):
            link = a.get('href')
            belongsUrl = url in link
            if(belongsUrl == True):
                try:
                    pageIndex = shouldVisitPages.index(link)
                    #print("- Página já existente na lista de pesquisa: " + link)
                except:
                    if(len(shouldVisitPages) < shouldVisitPagesLimit):
                        shouldVisitPages.append(link)
                        print("+ Nova página adicionada na lista de pesquisa: " + link)
                    else:
                        isLimitReached = True
                        print("Limite máximo de páginas atingido, interrompendo coleta de novas páginas")
                        break
else:
    print("Não foi possível acessar a página")

# Inicia a visitação em cada página armazenada
for i in range(shouldVisitPagesLimit):
    
    # Busca
    site = requests.get(shouldVisitPages[i], headers=headers, timeout=10)
    soup = BeautifulSoup(site.content, 'html.parser')
    print("Visitando página ("+str(i+1)+"/"+str(shouldVisitPagesLimit)+"): " + shouldVisitPages[i])
    visitedPages.append(shouldVisitPages[i])

    # Coleta o status da página
    statusCode = site.status_code
    visitedPagesStatusCode.append(site.status_code)

    # Busca novos links
    if(statusCode == 200):
        countSuccessVisitedPages += 1
        if(isLimitReached == False):
            for a in soup.find_all('a', href=True):
                link = a.get('href')
                belongsUrl = url in link
                if(belongsUrl == True):
                    try:
                        pageIndex = shouldVisitPages.index(link)
                        #print("- Página já existente na lista de pesquisa: " + link)
                    except:
                        if(len(shouldVisitPages) < shouldVisitPagesLimit):
                            shouldVisitPages.append(link)
                            print("+ Nova página adicionada na lista de pesquisa: " + link)
                        else:
                            isLimitReached = True
                            print("> Limite máximo de páginas atingido, interrompendo coleta de novas páginas")
                            break
        # Coleta tags <h1>
        content = ''
        for h1 in soup.find_all('h1'):
            content += "<h1>" + h1.text.strip()
        visitedPagesContent.append(content)
    else:
        countFailedVisitedPages += 1
        print("Não foi possível acessar a página")

# Exibe relatório no terminal
print("\n######## RELATÓRIO ########")
print(">>> Quantidade de páginas visitadas com sucesso: " + str(countSuccessVisitedPages))
print(">>> Quantidade de falhas no acesso de páginas: " + str(countFailedVisitedPages))

# Cria relatório em txt
arquivo = open("webscraping_report.txt", 'w+')
arquivo.writelines('\n######## RELATÓRIO ########')
arquivo.writelines('\n>>> Quantidade de páginas visitadas com sucesso: ' + str(countSuccessVisitedPages))
arquivo.writelines('\n>>> Quantidade de falhas no acesso de páginas: ' + str(countFailedVisitedPages))
arquivo.close()

# Cria relatório em excel
report = {"websites": visitedPages, "status": visitedPagesStatusCode, "content": visitedPagesContent}
dataframe = pd.DataFrame(report)
dataframe.to_excel('webscraping_report.xlsx')