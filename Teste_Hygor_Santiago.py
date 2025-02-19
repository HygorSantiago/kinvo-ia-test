# Baixei os dois arquivos que foram disponibilizados em .txt, não considero essa 
# maneira correta pois só lê o código HTML no horário em que foi baixado. O melhor
# seria algo dinâmico que leia os dados atualizados no memento em que o código
# rodar. Porém, ainda não sei programar em HTML, o que seria de grande ajuda
# nesse caso. Não usei as bibliotecas indicadas, pois nunca trabalhei com elas
# e preferi fazer com o que já conhecia, obviamente vou estuda-las, juntamente 
# com todas as demais necessárias para a função.

# Não conhecia as bibliotecas Flask, Spacy e Scrapy, comecei a estuda-las, mas
# nada em profundidade. Achei muito interessante e vou me aprofundar mais. O teste
# foi bem desafiante por lidar com uma área totalmente nova para mim, nunca 
# desenvolvi trabalhos em linguagem natural ou extração de informações diretamente
# de páginas web.

# Inicialmente criei uma função para ler os arquivos .txt baixados.
def extrai_txt(nome_arquivo):
    arquivo = open(nome_arquivo,'r')
    return arquivo.read()

# Todo o processamento de extração das informações passando de linhas de código 
# para verbetes é feita nessa outra função.
def noticias(arquivo,chaves=['O post Finance News.',
                             '(leia aqui os detalhes).',
                             'Leia a análiseFinance News.',
                             '(clique nos links abaixo para ler os detalhes) ',
                             '(clique aqui)',
                             'Leia mais clicando neste link:']):
# "chaves" corresponde a palavras-chave que não agregam informação, coloquei 
# algumas que encontrei neste banco de dados, mas a função permite facilmente
# acrescentar outros ou alterar estes.

# Biblioteca re foi amplamente usada neste trabalho.
    import re
# Separa as notícias pela palavra chave "</item>", lendo atentamente o banco de
# dados entendi que esse seria um delimitador.
    original = arquivo.split('</item>')
# Inicializa os vetores que receberão as informações.
    corrigido = []
    titulo = []
# O loop processa as informações presentes em cada texto do arquivo já dividido.
    for i in range(len(original)):
        t = original[i]
        
# Localiza os delimitadores "<title>" e "</title>" e retorna a informação entre
# ambos, essa inforfação é o título de cada notícia.
        for localizador in re.finditer('<title>',t):
            B = localizador.end()
        for localizador in re.finditer('</title>',t):
            C = localizador.start()

# Localiza o delimitador "<description>", o texto onde contém a informação procurada
# está localizado a partir desse delimitador.
        for localizador in re.finditer('<description>',t):
            D = localizador.end()
            
        tex = t[D:]
      
# Alguns caracteres especiais constituintes do código original não contém informação
# relevante, assim foram simplesmente eliminados.
        especiais = ['<.*; ','</p>','<p>','<.*">','<.*>','\[.*\]']
        for j in especiais:
            tex = re.sub(j,'',tex)
            
# Eliminação das palavras chaves, já comentadas no início da função.
        for k in chaves:
            tex = re.sub(k,'',tex)

# Por fim, a correção de linhas múltiplas, parágrafos e identações, transformando
# o texto linear.
        tex = re.sub('\n.*>','',tex)
        tex = re.sub('\&.*;','',tex)
        tex = re.sub('\n',' ',tex)
        tex = re.sub('\t+',' ',tex)
        tex = re.sub(' +',' ',tex)
        
# Caso o texto final fique muito pequeno, não apresenta informação relevante,
# então só será salvo a partir de um tamanho mínimo.
        if len(tex) > 100:
            corrigido.append(tex)
            titulo.append(t[B:C])

# A função retorna o texto corrigido com o seu título.
    return corrigido,titulo
    
# Diretório onde os arquivos .txt foram salvos.
endereco = ['C:/Users/Hygor/Desktop/Python/Programas/Dadática Tech/Módulo 4/PLN/Teste/noticias_1.txt',
            'C:/Users/Hygor/Desktop/Python/Programas/Dadática Tech/Módulo 4/PLN/Teste/noticias_2.txt']

# Aplicação das duas funções criadas.
corrigido = []
titulo = []
for i in endereco:
    arquivo = extrai_txt(i)
    c,t = noticias(arquivo)
    corrigido += c
    titulo += t
    
# Para se separar as notícias relacionadas ao mercado financeiro fiz uma busca
# por palavras chave coerentes para o contexto.
chave = [' ibovespa ',
         ' btg ',
         ' investim.* ',
         ' investid.* ',
         ' ações ',
         ' aquisi.* ',
         ' opera.* ',
         ' receita bruta ']
import re
financeiro = []
for i in range(len(corrigido)):
    for c in chave:
        for localizador in re.finditer(c,corrigido[i].lower()):
            financeiro.append(i)

financeiro = sorted(set(financeiro))

# Por fim, a última variável criada corresponde às notícias relacionadas ao
# mercado financeiro, já devidamente corrigidas.
noticias_mercado_financeiro = [corrigido[i] for i in financeiro]

