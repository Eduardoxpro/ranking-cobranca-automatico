def gerar_ranking(df):
    ranking = df.sort_values(by='Score_Prioridade', ascending=False).reset_index(drop=True)
    ranking['Posicao'] = ranking.index + 1
    print("Ranking gerado com sucesso!")
    return ranking[[
        'Posicao', 'Cliente_ID', 'Nome_Cliente', 'CNPJ_CPF',
        'Data_Vencimento', 'Dias_em_Atraso', 
        'Valor_Devido', 'Valor_Pago', 'Saldo_Devedor',
        'Score_Prioridade', 'Cidade', 'Regiao'
    ]].copy()
