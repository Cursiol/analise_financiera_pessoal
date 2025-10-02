# iniciando o Back-end
# insersão de dados
# ter os bancos cadastrados (Nubank, Banco do Brasil, Caixa)
# primeiro ter os campos de entrada de dinheiro - (Salario, vendas, Dividendos/Investimentos)
# segundo ter os campos de saida de dinheiro - (Apartamento, Casa, Internet, Lanches/Comidas, SupermercadoEssencial, Supermercado, Impressão 3D, Combustivel/Carro, Presentes, Lazer, Roupas/Calçados, Cuidados Pessoais, Assinaturas, SemParar, Cartão de Credito)
# tem que fazer os calculos, se teve gasto? de onde saiu esse gasto? tem que subtrait automatico do saldo
# teve entrada? tem que fazer o calculo da entrada na conta que eu selecionei certinho

# ========= BACK END ================

#importando as bibliotecas Utilizadas
import pandas as pd
from datetime import datetime
import os
import shutil

#Iniciando a função para adicionar os bancos
bancos = ['Nubank', 'Banco do Brasil', 'Caixa Economica']

#categorias de entrada e saida
cat_entrada = ['Salário', 'Vendas', 'Dividendos/Investimentos']
cat_saida = ['Apartamento',
             'Casa',
             'Celular',
             'Lanches/Comida',
             'Super. Essencial',
             'Super. Diferente',
             'Impressão 3D',
             'Combustivel/Manut.',
             'Presentes',
             'Lazer',
             'Roupas/Calçados',
             'Cuidados Pessoais',
             'Assinaturas',
             'SemParar',
             'Cartão de Credito']

# função para obter o saldo atual do banco
def obter_saldo(banco, df):
    if banco not in df['Banco'].values:
        return 0
    saldo = df[df['Banco'] == banco]['Valor'].sum()
    return saldo

#Função para adicionar a transação/movimentação de dinheiro
def adicionar_transacao(tipo, categoria, banco, descricao, valor, data):
    arquivo = 'dados_financeiros.csv'

    #carregar ou criar o DataFrame
    if os.path.exists(arquivo):
        df = pd.read_csv(arquivo)
    else:
        df = pd.DataFrame(columns=['Data', 'Tipo', 'Categoria', 'Banco', 'Descrição', 'Valor', 'Saldo Banco'])

    # calcula o novo saldo
    saldo_atual = obter_saldo(banco, df)
    novo_saldo = saldo_atual + valor if tipo == 'Entrada' else saldo_atual - abs(valor)

    #cria nova linha
    nova_linha = {
        "Data": data.strftime("%d-%m-%y"),
        "Tipo": tipo,
        "Categoria": categoria,
        "Banco": banco,
        "Descrição": descricao,
        "Valor": valor if tipo == "Entrada" else -abs(valor),
        "Saldo Banco": novo_saldo
    }

    #adidiona e salva
    df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
    df.to_csv(arquivo,index=False)

#Limpar os dados do arquivo csv
def gerar_bkp_e_limpar():
    original = 'dados_financeiros.csv'
    backup = 'dados_financeiros_backup.csv'

    #gera o Backup
    shutil.copy(original, backup)

    #limpa o original mantendo os cabeçalhos
    colunas = ['Data', 'Tipo', 'Categoria', 'Banco', 'Descrição', 'Valor', 'Saldo Banco']
    df_vazio = pd.DataFrame(columns=colunas)
    df_vazio.to_csv(original, index=False)









