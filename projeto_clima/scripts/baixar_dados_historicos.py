#!/usr/bin/env python
"""
Script para baixar dados históricos do Sul Fluminense
Uso: python scripts/baixar_dados_historicos.py --anos 2020,2021,2022,2023
"""
import sys
import os
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.servicos.dados_historicos import HistoricalDataLoader

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--anos', type=str, default='2020,2021,2022,2023',
                       help='Anos para baixar (separados por vírgula)')
    args = parser.parse_args()
    
    anos = [int(a) for a in args.anos.split(',')]
    
    print("="*60)
    print(" DOWNLOAD DE DADOS HISTÓRICOS - SUL FLUMINENSE")
    print("="*60)
    
    loader = HistoricalDataLoader()
    dados = loader.carregar_dados_sul_fluminense(anos, resolucao=0.1)
    
    if not dados.empty:
        print("\n" + "="*60)
        print(" DOWNLOAD CONCLUÍDO")
        print("="*60)
        print(f" Registros: {len(dados)}")
        print(f" Período: {dados['data'].min()} a {dados['data'].max()}")
        print(f" Pontos: {dados.groupby(['lat', 'lon']).ngroups}")
        print(f" Arquivo: sul_fluminense_completo.parquet")
        
        # Salva arquivo completo
        dados.to_parquet("sul_fluminense_completo.parquet")
    else:
        print("Nenhum dado baixado")

if __name__ == "__main__":
    main()