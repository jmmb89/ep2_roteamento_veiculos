import random
import math

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
tx_mutacao = 0.50
tx_crossover = 0.15
tx_tragedia = 0.05
geracoes_max = 100_000
geracoes_tragedia = 100

n_cidades = 17
#17 cidades

def fitness(individuo):
  score = 0
  cidade = 0
  proxima = 0

  for i in range(len(individuo)):
    if i+1 < len(individuo):
      cidade = individuo[i]
      proxima = individuo[i+1]
    else:
      cidade = individuo[i]
      #ultima cidade se liga com a primeira (fechar o ciclo)
      proxima = individuo[0]
    score += data['matriz_distancia'][cidade][proxima]
  return score

def melhores_rotas(populacao):
  score_fitness = {}     
  for i in range(len(populacao)):
    score = fitness(populacao[i])
    if not score in score_fitness:
      score_fitness[score] = populacao[i]
    else:
      match = False
      #para nao subistituir caminhos diferentes com mesmo score
      while not match:
        if score in score_fitness:
          score += 1
        else:
          score_fitness[score] = populacao[i]
          match = True
          
  sorted_score = {key:score_fitness[key] for key in sorted(score_fitness)}
  return sorted_score

def top_20(populacao_fit):
  top = {}
  i = 0
  for k in populacao_fit.keys():
    top[k] = populacao_fit[k]
    i += 1
    if i == 20:
      break  
  return top

#adiciona um score sem sobreescrever se for igual 
def concatenar_score(dict1, dict2):
  for key in dict2:
    if not key in dict1:
      dict1[key] = dict2[key]
    else:
      match = False
      score = key
      while not match:
        if score in dict1:
          score += 1
        else:
          dict1[score] = dict2[key]
          match = True
  
  return dict1

def proxima_geracao(populacao_fit):
  #seleciona os 20 melhores para a proxima pop
  next_gen = top_20(populacao_fit)

  breed = gerar_filhos(populacao_fit)
  next_gen = concatenar_score(next_gen, breed)
  
  next_gen = [*next_gen.values()]
  return next_gen
  
def procriacao(pai, mae):
  filho = []
  
  for i in range(0, int(len(pai)/2)):
    filho.append(pai[i])

  while len(filho) != len(pai):
    gene_mae = mae[random.randint(1, len(mae) -1)]
    if not gene_mae in filho:
      filho.append(gene_mae)

  #print(f"pai:{pai}\nmae:{mae}\nfil:{filho}\n")
  return filho  

def gerar_filhos(genova):
  i = 0
  nextgen = {}
  populacao = []
  chaves = list(genova)
  for key in genova:
    while i <= len(genova[key]):
      try :
        chave = chaves[chaves.index(key) + i]
      except(ValueError, IndexError):
        break
      ind = procriacao(genova[key],genova[chave])
      populacao.append(ind)
      i += 1
    i = 0
    
  nextgen = melhores_rotas(populacao)

  return top_20(nextgen)

def mutacao(individuo):
  i = random.randint(1, len(individuo) -1)
  genea = individuo[i]
  #print(f"individuo:{individuo}\n")
  
  j = i
  while j == i :
    j = random.randint(1, len(individuo) -1)

  geneb = individuo[j]
  individuo[j] = genea
  individuo[i] = geneb
  #print(f"individuo:{individuo}\n")
  return individuo


def criar_individuo():
  cidades = len(data['matriz_distancia'][0])
  disponiveis = list(range(1, cidades))
  escolha = []

  while len(disponiveis) > 0:
    num = random.randint(0, len(disponiveis) -1)
    escolha.append(disponiveis[num])
    disponiveis.pop(num)
  #cidade de partida = 0
  escolha.insert(0, 0)

  return escolha

def melhor_rota(populacao):
  max_ger = 1000
  n_gen = populacao
	#load vars
  l_size = 20
  msg = "Loading ["
  load_status = 0
  progress = 0

  word = msg + "X"*progress + "*"*(l_size-progress - 1) + "]"
  print('\r' + word, end='')

  for i in range(max_ger):
    n_gen = proxima_geracao(melhores_rotas(n_gen))

    #tela de loading
    load_status += 1
    if load_status >= int(max_ger/20) and progress != (l_size -1):
      progress += 1
      load_status = 0
      word = msg + "X"*progress + "*"*(l_size-progress-1) + "]"
      print('\r' + word, end='')

  pop_final = melhores_rotas(n_gen)
  melhor_individuo = list(pop_final.keys())[0]
  print(f"\n\nscore:{melhor_individuo}\ncaminho: {pop_final[melhor_individuo]}\n")

data = create_data_model()
populacao = []

for i in range(tamanho_populacao):
  populacao.append(criar_individuo())


print("#### EP AI ####\n")

melhor_rota(populacao)

print("\n\nAlunos:\nJoao Mario Motidome Barradas\nKaue Sales Barbosa\nLeandro Borges De Moura\n")
