import random
import math
from sys import argv

def create_data_model():
    data = {}
    data['matriz_distancia'] = [
        [
            0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354,
            468, 776, 662
        ],
        [
            548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674,
            1016, 868, 1210
        ],
        [
            776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164,
            1130, 788, 1552, 754
        ],
        [
            696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822,
            1164, 560, 1358
        ],
        [
            582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708,
            1050, 674, 1244
        ],
        [
            274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628,
            514, 1050, 708
        ],
        [
            502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856,
            514, 1278, 480
        ],
        [
            194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320,
            662, 742, 856
        ],
        [
            308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662,
            320, 1084, 514
        ],
        [
            194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388,
            274, 810, 468
        ],
        [
            536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764,
            730, 388, 1152, 354
        ],
        [
            502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114,
            308, 650, 274, 844
        ],
        [
            388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194,
            536, 388, 730
        ],
        [
            354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0,
            342, 422, 536
        ],
        [
            468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536,
            342, 0, 764, 194
        ],
        [
            776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274,
            388, 422, 764, 0, 798
        ],
        [
            662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730,
            536, 194, 798, 0
        ],
    ]
    data['num_vehicles'] = 4
    data['depot'] = 0
    return data

# hiperparâmetros
tamanho_populacao = 100
#maximo valor = 1 (nao passar ou risco de crash/bug)
tx_mutacao = 0.50
tx_crossover = 0.10 #0.15
tx_tragedia = 0.05
geracoes_max = 10000
geracoes_tragedia = 100

def top20(populacao_fit):
  top = {}
  i = 0
  for key in populacao_fit.keys():
    top[key] = populacao_fit[key]
    i += 1
    if i == 10:
      break  
  return top

def swap(individuo):
  van1 = random.randint(0, len(individuo)-1)
  van2 = random.randint(0, len(individuo)-1)
  while van1 == van2:
    van2 = random.randint(0, len(individuo)-1)
  geneX = random.randint(1, len(individuo[van1])-1)
  geneY = random.randint(1, len(individuo[van2])-1)
  
  tmp_x = individuo[van1][geneX]
  individuo[van1][geneX] = individuo[van2][geneY]
  individuo[van2][geneY] = tmp_x 

  return individuo

def mutacao(individuo):
  tx = int(tx_crossover*len(data['matriz_distancia'][0]))
  for i in range(tx):
    individuo = swap(individuo)

  return individuo

#calcula a soma das distancias para cada individuo
def fitness(individuo):
  score = 0
  cidade = 0
  proxima = 0

  for i in range(len(individuo)):
    for j in range(len(individuo[i])):
      if j+1 < len (individuo[i]):
        cidade = individuo[i][j]
        proxima = individuo[i][j+1]
      else:
        cidade = individuo[i][j]
        #ultima cidade se liga com a primeira (0)
        proxima = individuo[i][0]

      score += data['matriz_distancia'][cidade][proxima]
  return score


def melhores_rotas(pop):
  score_fitness = {}

  for i in range(len(pop)):
    score = fitness(pop[i]) 
    if not score in score_fitness:
      score_fitness[score] = pop[i]
    else:
      found = False
      while not found:
        if score in score_fitness:
          score += 1
        else:
          score_fitness[score] = pop[i]
          found = True

  sorted_score = {key:score_fitness[key] for key in sorted(score_fitness)}
  return sorted_score

def procriacao(pai, mae):
  #copia os genes do pai para o filho
  filho = []
  for i in range(len(pai)):
    filho.append(pai[i])
    
  genes = len(data['matriz_distancia'][0])
  
  for i in range(int(genes * tx_crossover)):
    van = random.randint(0, data['num_vehicles']-1)
    gene_Y = random.randint(0, len(mae[van])-1)
    gene_mae = mae[van][gene_Y]
    gene_X = filho[van][gene_Y]
    #adiciona o gene da mae no lugar do gene do filho 
    filho[van][gene_Y] = gene_mae

    #subistitui o gene antigo (filho) pelo substituido (mae), para nao ter repeticao
    found = False
    for j in range(len(filho)):
      for k in range(len(filho[i])):
        if filho[j][k] == gene_mae:
          filho[j][k] = gene_X
          found = True
          break
      if found:
        break

  return filho

def gerar_filhos(top_20):
  i = 0 
  nextgen = {}
  populacao = []
  chaves = list(top_20)

  for key in top_20:
    while i <= len(top_20[key]):
      try:
        chave = chaves[chaves.index(key) + i]
      except(ValueError, IndexError):
        break
      ind = procriacao(top_20[key], top_20[chave])
      populacao.append(ind)
      i += 1
    i = 0 

  nextgen = top20(melhores_rotas(populacao))
  return nextgen

def cat_dict(dic1, dic2):
  dic3 = {**dic1, **dic2}
  return dic3
    
def proxima_geracao(populacao_fit, tragedia):
  #seleciona os 20 melhores da populacao
  next_gen = top20(populacao_fit)
  #cruza os 20 melhores entre si
  breed = gerar_filhos(next_gen)
  next_gen = cat_dict(next_gen, breed)

  #if tragedia:
  #  pass
  
  top_20 = top20(next_gen)
  mutantes = []

  for i in range(int(tx_mutacao * tamanho_populacao)):
    key = random.choice(list(populacao_fit.keys()))
    if not key in top_20:
      mutantes.append(mutacao(populacao_fit[key]))
      if key in next_gen:
        next_gen.pop(key)
    else:
      i -= 1

  dif_size = tamanho_populacao - (len(mutantes) + len(next_gen))
  for i in range(dif_size):
    mutantes.append(criar_individuo())
    
  next_gen = [*next_gen.values()]
  for i in range(len(mutantes)):
    next_gen.append(mutantes[i])
    
  return next_gen

def criar_individuo():
  cidades = len(data['matriz_distancia'][0])
  disponiveis = list(range(1, cidades))
  escolha = []
  max_size = int(cidades/data['num_vehicles'])
  inserted = 0
  tmp_a = []

  while len(disponiveis) > 0:
    num = random.randint(0, len(disponiveis) -1)
    if inserted ==  max_size:
      tmp_a.insert(0,0)
      escolha.append(tmp_a)
      tmp_a = []
      inserted = 0
    else:
      inserted += 1
      tmp_a.append(disponiveis[num])
      disponiveis.pop(num)
      if len(disponiveis) == 0:
        #coloca a cidade de partida no comeco da lista
        tmp_a.insert(0,0)
        escolha.append(tmp_a)

  return escolha

def melhor_rota():
  n_gen = populacao
  #loading vars
  l_size = 20
  msg = "Loading ["
  load_status = 0
  progress = 0
  word = msg + "X"*progress + "*"*(l_size - progress - 1) + "]"
  print('\r' + word, end='')

  for i in range(geracoes_max):
    n_gen = proxima_geracao(melhores_rotas(n_gen), False)
    #tela de loading
    load_status += 1
    if load_status >= int(geracoes_max/l_size) and progress != (l_size -1):
      progress += 1
      load_status = 0
      word = msg + "X"*progress + "*"*(l_size - progress - 1) + "]"
      print('\r' + word, end='')

  pop_fit = melhores_rotas(n_gen)
  melhor_individuo = list(pop_fit.keys())[0]
  print(f"\n\nscore: {melhor_individuo}\ncaminho: {pop_fit[melhor_individuo]}\n")
  

#quantidade de geracoes pode ser passado como argumento 
if len(argv) > 1:
  try:
    geracoes_max = int(argv[1])
  except:
    pass

data = create_data_model()
populacao = []

for i in range(tamanho_populacao):
  populacao.append(criar_individuo())

print("\n#### EP IA - Roteamento de veiculos  ####\n")

melhor_rota()

print("\n\nAlunos:\nJoao Mario Motidome Barradas\nKaue Sales Barbosa\nLeandro Borges De Moura\n")
