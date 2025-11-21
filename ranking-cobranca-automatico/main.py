# main.py – VERSÃO INTERATIVA (escolhe quantos clientes cobrar)
import pandas as pd
import numpy as np
import os
from datetime import datetime

print("═" * 60)
print("   RANKING AUTOMÁTICO DE COBRANÇA – ATÉ 12.000 CLIENTES")
print("═" * 60)

# === GERA OU CARREGA OS 12.000 CLIENTES ===
caminho = "data/raw/clientes_12000.csv"

if not os.path.exists(caminho):
    print("CSV não encontrado! Gerando 12.000 clientes agora...")
    np.random.seed(42)
    n = 12000
    df = pd.DataFrame({
        'Cliente_ID': range(1, n+1),
        'Nome_Cliente': [f'Cliente {i}' for i in range(1, n+1)],
        'CNPJ_CPF': np.random.choice(['11.222.333/0001-99', '22.333.444/0001-88', '33.444.555/0001-77'], n),
        'Data_Vencimento': pd.to_datetime(np.random.choice(pd.date_range('2023-01-01', '2026-12-31'), n)),
        'Valor_Devido': np.round(np.random.lognormal(8.5, 1.4, n), 2),
        'Valor_Pago': np.round(np.random.uniform(0, 150000, n), 2),
        'Cidade': np.random.choice(['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba', 'Porto Alegre'], n),
        'Regiao': np.random.choice(['Sudeste', 'Sul', 'Nordeste', 'Centro-Oeste', 'Norte'], n)
    })
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv(caminho, index=False)
    print("CSV criado com sucesso!")
else:
    print("Carregando 12.000 clientes...")
    df = pd.read_csv(caminho, parse_dates=['Data_Vencimento'])

# === CALCULA SCORE ===
hoje = pd.to_datetime('today').normalize()
df['Dias_em_Atraso'] = (hoje - df['Data_Vencimento']).dt.days.clip(lower=0)
df['Saldo_Devedor'] = (df['Valor_Devido'] - df['Valor_Pago']).clip(lower=0)
df['Score_Prioridade'] = df['Dias_em_Atraso'] * df['Saldo_Devedor']

# === RANKING COMPLETO ===
ranking_completo = df.sort_values('Score_Prioridade', ascending=False).reset_index(drop=True)
ranking_completo['Posicao'] = ranking_completo.index + 1

# === PERGUNTA QUANTOS VOCÊ QUER COBRAR HOJE ===
while True:
    try:
        qtd = int(input("\nQuantos clientes você quer cobrar hoje? (1 a 12000): "))
        if 1 <= qtd <= 12000:
            break
        else:
            print("Por favor, digite um número entre 1 e 12000.")
    except ValueError:
        print("Digite apenas números!")

ranking_hoje = ranking_completo.head(qtd).copy()

# === EXPORTA EXCEL COMPLETO (sempre os 12.000) ===
os.makedirs("output", exist_ok=True)
arquivo = f"output/Ranking_Cobranca_{datetime.now():%Y%m%d}.xlsx"
ranking_completo.to_excel(arquivo, index=False)

# === MOSTRA SÓ OS QUE VOCÊ VAI COBRAR HOJE ===
print(f"\nHoje você vai cobrar os {qtd} clientes mais urgentes:")
print(ranking_hoje[['Posicao', 'Nome_Cliente', 'Dias_em_Atraso', 'Saldo_Devedor', 'Score_Prioridade']]
      .to_string(index=False))

print(f"\nExcel completo (12.000 linhas) salvo em: {arquivo}")
print("Bora faturar pesado hoje!")