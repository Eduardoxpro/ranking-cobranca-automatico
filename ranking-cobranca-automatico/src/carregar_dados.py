# src/carregar_dados.py
import pandas as pd
import os

def carregar_dados():
    caminho = os.path.join("data", "raw", "clientes_12000.csv")
    if not os.path.exists(caminho):
        print("Arquivo CSV não encontrado! Criando 12.000 clientes agora...")
        import numpy as np
        np.random.seed(42)
        n = 12000
        df_temp = pd.DataFrame({
            'Cliente_ID': range(1, n+1),
            'Nome_Cliente': [f'Cliente {i}' for i in range(1, n+1)],
            'CNPJ_CPF': np.random.choice(['11.222.333/0001-99', '22.333.444/0001-88'], n),
            'Data_Vencimento': pd.to_datetime(np.random.choice(pd.date_range('2023-01-01', '2026-12-31'), n)),
            'Valor_Devido': np.round(np.random.lognormal(8.5, 1.4, n), 2),
            'Valor_Pago': np.round(np.random.uniform(0, 200000, n), 2),
            'Cidade': np.random.choice(['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba'], n),
            'Regiao': np.random.choice(['Sudeste', 'Sul', 'Nordeste', 'Centro-Oeste'], n)
        })
        os.makedirs("data/raw", exist_ok=True)
        df_temp.to_csv(caminho, index=False)
        print("CSV criado com sucesso!")
    
    print("Carregando 12.000 clientes...")
    df = pd.read_csv(caminho, parse_dates=['Data_Vencimento'])
    print("Clientes carregados com sucesso!")
    return df