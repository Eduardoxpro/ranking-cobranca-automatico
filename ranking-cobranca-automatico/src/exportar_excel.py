import pandas as pd
import os
from datetime import datetime

def exportar_excel(ranking):
    arquivo = f"output/Ranking_Cobranca_{datetime.now().strftime('%Y%m%d')}.xlsx"
    os.makedirs("output", exist_ok=True)
    ranking.to_excel(arquivo, index=False)
    print(f"EXCEL GERADO: {arquivo}")
