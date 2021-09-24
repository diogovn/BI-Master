# -*- coding: utf-8 -*-
#import os
#workdir_path = '/content/drive/My Drive/PUC/PROJ/'  # Inserir o local da pasta onde estão os arquivos de entrada (treino e teste)
#os.chdir(workdir_path)
import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split

class Dados():    
    def __init__(self, arq_vib,
                instalacoes = ['Itarare', 'TEFRAN', 'TEDUT', 'ESPAT', 'Iatajai', 'TEPAR'],
                tipo = 'Spectra',
                pontos = ['1H','1V','2H','2V','3H','3V','4H','4V'],
                linhas = [401],
                canais = [2],
                n_dados = 401):
        '''
        tipo: Spectra ou Cepstrum.
        instalacoes: lista de instalacoes consideradas.
        pontos: lista de pontos considerados.
        linhas: valor da coluna Linhas considerado.
        canais: lista de valores da coluna Canais considerados.    
        n_dados: numero de dados a serem considerados (exemplo: pode usar menos para o cepstrum, por exemplo).
        '''            
        self.arq_vib = arq_vib
        self.instalacoes = instalacoes
        self.tipo = tipo
        self.pontos = pontos
        self.linhas = linhas
        self.canais = canais
        self.n_dados = n_dados
        
        self.n_pontos = int(len(pontos))
        self.n_linhas = len(self.pontos) * len(self.canais)     
        
        
    def Carrega(self):
        df_vib = pd.DataFrame()
        for instalacao in self.instalacoes:
            df = pd.read_csv(self.arq_vib.format(instalacao,self.tipo))
            print(instalacao)
            print(df.shape)
            df_vib = df_vib.append(df)                
        
        df_vib = df_vib[df_vib['Linhas'].isin(self.linhas)]
        df_vib = df_vib[df_vib['Ponto'].isin(self.pontos)]
        df_vib = df_vib[df_vib['Canal'].isin(self.canais)]
        
        cols_exc = list(range(self.n_dados,6401))
        cols_exc = [str(i) for i in cols_exc]
        df_vib = df_vib.drop(cols_exc, axis=1)
        df_vib = df_vib.fillna(0)
        
        self.n_relatorios_df = int(len(df_vib)/self.n_linhas)
        print("df_vib.shape: " , df_vib.shape)
        print('Numero de relatorios: ', self.n_relatorios_df)
        
        self.df_vib = df_vib
    
    def DfArray(self):
        '''
        Monta DF com os dados de todos os pontos em um array de <n_pontos> linhas associados a um valor y (considera o primeiro valor)
        '''
        df_vib=self.df_vib
        x_array = df_vib.drop(['Situacao', 'Data', 'Instalacao', 'Equipamento', 'Ponto', 'Nome', 'Unidade',
                       'Deteccao', 'Canal', 'Linhas', 'Frequencia Final', 'Velocidade'], axis=1)
        
        y_array = df_vib['Situacao'][::self.n_linhas].astype(int) #pega um valor a cada n_linhas
        y_array = y_array.values
        x_array  = x_array .values.reshape(-1,self.n_linhas,self.n_dados,1)
        df_array = pd.DataFrame(columns=['y','x'])
        for i in range(len(y_array)):
            df1 = pd.DataFrame([[y_array[i], x_array [i,:,:,:]]],columns=['y','x'])
            df_array = df_array.append(df1,ignore_index=True)
        
        self.df_array = df_array
    
    def Oversample(self):
        df_array = self.df_array
        n_normais = len(df_array[df_array['y']==0])
        n_criticos = len(df_array[df_array['y']==1])
        print('Antes: {} normais e {} criticos'.format(n_normais,n_criticos))
        df_array1 = df_array[df_array['y']==1]
        df_array1 = df_array1.sample(n_normais - n_criticos, replace=True, random_state=0)
        df_array = df_array.append(df_array1)
        
        n_normais = len(df_array[df_array['y']==0])
        n_criticos = len(df_array[df_array['y']==1])
        print('Depois: {} normais e {} criticos'.format(n_normais,n_criticos))
        
        self.df_array = df_array

    def Array(self):
        df_array = self.df_array
        self.n_relatorios_array = len(df_array['x'])
        x_array = np.empty([self.n_relatorios_array,self.n_linhas,self.n_dados,1])
        y_array = np.empty([self.n_relatorios_array])
        for i in range(len(df_array)):
            x_array[i] = df_array['x'].iloc[i].reshape(1,self.n_linhas,self.n_dados,1)
            y_array[i] = df_array['y'].iloc[i]
        
        self.x_array = x_array
        self.y_array = y_array
        
    def Split(self,test_size=0.2,random_state=0):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x_array, self.y_array, test_size=test_size, random_state=random_state)

        
#%%
# dados = Dados()
# arq_vib = r'DadosVib/{}_{}.csv'
# tipo = 'Spectra'
# instalacoes = ['Itarare', 'TEFRAN', 'TEDUT', 'ESPAT']
# df = dados.Carrega(arq_vib=arq_vib, instalacoes=instalacoes, tipo=tipo)
# #arq_vib = r'D:\Diogo\PUC\BI Master\12.PROJ\Scripts\DadosVib\{}_{}.csv'
# #%%
# pontos = ['1H','1V','2H','2V','3H','3V','4H','4V']
# n_pontos = int(len(pontos))
# canal = 2
# linhas = 401  #coluna Linhas      pegando apenas grafico de velocidade
# n_dados = 401  #quantidade de dados
# df_filtrado = dados.Filtra(df, pontos=pontos, linhas=linhas, canal=canal, n_dados=n_dados)
# df_filtrado.head()