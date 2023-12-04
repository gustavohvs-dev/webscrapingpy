import pandas as pd

# Parâmetros 
reportPath = 'webscraping_report.xlsx'
removeCharsString = '!?"@#$%¨&*()-_=+;:.,/[]´`{^}~|<>”“1234567890'
removeStopWords = ["", "\\n", "de", "Ao", "a", "o", "que", "e", "é", "do", "da", "de", "dos", "das", "em", "um", "para", "com", "não", "uma", "os", "no", "se",
    "na", "por", "mais", "as", "dos", "como", "mas", "ao", "ele", "das", "à", "seu", "sua", "ou", "quando",
    "muito", "nos", "já", "eu", "também", "só", "pelo", "pela", "até", "isso", "ela", "entre", "depois", "sem",
    "mesmo", "aos", "seus", "quem", "nas", "me", "esse", "eles", "você", "essa", "num", "nem", "suas", "meu",
    "às", "minha", "numa", "pelos", "elas", "qual", "nós", "lhe", "deles", "essas", "esses", "pelas", "este",
    "dele", "tu", "te", "vocês", "vos", "lhes", "meus", "minhas", "teu", "tua", "teus", "tuas", "nosso",
    "nossa", "nossos", "nossas", "dela", "delas", "esta", "estes", "estas", "aquele", "aquela", "aqueles",
    "aquelas", "isto", "aquilo", "estou", "está", "estamos", "estão", "estive", "esteve", "estivemos", "estiveram",
    "estava", "estávamos", "estavam", "estivera", "estivéramos", "esteja", "estejamos", "estejam", "estivesse",
    "estivéssemos", "estivessem", "estiver", "estivermos", "estiverem", "hei", "há", "havemos", "hão", "houve",
    "houvemos", "houveram", "houvera", "houvéramos", "haja", "hajamos", "hajam", "houvesse", "houvéssemos",
    "houvessem", "houver", "houvermos", "houverem", "houverei", "houverá", "houveremos", "houverão", "houveria",
    "houveríamos", "houveriam", "sou", "somos", "são", "era", "éramos", "eram", "fui", "foi", "fomos", "foram",
    "fora", "fôramos", "seja", "sejamos", "sejam", "fosse", "fôssemos", "fossem", "for", "formos", "forem", "serei",
    "será", "seremos", "serão", "seria", "seríamos", "seriam", "tenho", "tem", "temos", "têm", "tinha", "tínhamos",
    "tinham", "tive", "teve", "tivemos", "tiveram", "tivera", "tivéramos", "tenha", "tenhamos", "tenham", "tivesse",
    "tivéssemos", "tivessem", "tiver", "tivermos", "tiverem", "terei", "terá", "teremos", "terão", "teria", "teríamos",
    "teriam", "A", "O", "CNN", "faz", "fazer", "feito", "eu", "me", "tu", "te", "você", "ele", "ela", "nós", "nos", "vós", "vos", "eles", "elas", "meu", "minha", 
    "meus", "minhas", "teu", "tua", "teus", "tuas", "seu", "sua", "seus", "suas", "nosso", "nossa", "nossos", 
    "nossas", "vosso", "vossa", "vossos", "vossas", "meu", "meus", "minha", "minhas", "teu", "teus", "tua", 
    "tuas", "seu", "seus", "sua", "suas", "nosso", "nossos", "nossa", "nossas", "vosso", "vossos", "vossa", 
    "vossas", "me", "mim", "comigo", "te", "ti", "contigo", "você", "o", "a", "lhe", "nos", "nos", "convosco", 
    "vos", "vos", "os", "as", "lhes", "se", "si", "consigo", "após", "no"]

# Listas e variáveis
fix1 = []
fix2 = []

# Análise de dados
data = pd.read_excel(reportPath, engine='openpyxl')

# Tratativa 1 - Remoção de caracteres especiais
for words in data['content']:
    try:
        wordsRow = str(words)
        wordsRow = wordsRow.split("<h1>")
        phrase = wordsRow[1] 
        for char in removeCharsString:
            phrase = phrase.replace(char, "")
        fix1.append(phrase)
    except:
        print(">>> Não foi possível identificar a frase")

# Tratativa 2 - Remoção de stopwords
for words in fix1:
    words = str(words)
    arrayWords = words.split(" ")
    print(arrayWords)
    for verifyWord in arrayWords:
        try:
            removeIndex = removeStopWords.index(verifyWord)
            arrayWords.remove(verifyWord)
            print(">>> Removendo stopword: " + verifyWord)
        except:
            print(">>> Mantendo termo: " + verifyWord)
    fix2.append(arrayWords)

# Criando dicionário de palavras
dictionary = {}

for arrayWords in fix2:
    for word in arrayWords:
        if(dictionary.get(word)):
            dictionary.update({word: dictionary[word]+1})
        else:
            dictionary[word] = 1
        

# Relatório no terminal
print("\n######## DICIONÁRIO DE PALAVRAS ########")
print(dictionary)

# Criando relatório em excel
report = {"words": dictionary.keys(), "frequence": dictionary.values()}
dataframe = pd.DataFrame(report)
dataframe.to_excel('webscraping_words.xlsx')

