# src/calcular_score.py
from datetime import datetime
import pandas as pd

def calcular_atraso_e_score(df):
    hoje = pd.to_datetime('today').normalize()
    df['Dias_em_Atraso'] = (hoje - df['Data_Vencimento']).dt.days.clip(lower=0)
    df['Saldo_Devedor'] = (df['Valor_Devido'] - df['Valor_Pago']).clip(lower=0)
    df['Score_Prioridade'] = df['Dias_em_Atraso'] * df['Saldo_Devedor']
    print(f"Score calculado! Maior score: R$ {df['Score_Prioridade'].max():,.0f}")
    return df
