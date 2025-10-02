#💸 Análise Financeira Pessoal
Este projeto é uma aplicação interativa desenvolvida com Python e Streamlit, voltada para o controle e visualização de finanças pessoais. A proposta é oferecer uma interface intuitiva para registrar transações, aplicar filtros dinâmicos e gerar gráficos que ajudam a entender o comportamento financeiro ao longo do tempo.

#🎯 Objetivo
A aplicação permite ao usuário:
- Inserir transações financeiras (entradas e saídas)
- Filtrar dados por banco, tipo de transação e mês
- Visualizar saldos por instituição
- Acompanhar a evolução do saldo acumulado
- Identificar categorias de gastos mais frequentes
- Analisar padrões de consumo por dia da semana
  
#🧠 Lógica de Programação
A estrutura do código está organizada em blocos funcionais:

1. Importação de Bibliotecas
Utiliza bibliotecas como pandas, plotly, numpy, sklearn e streamlit para manipulação de dados, visualização gráfica e interface web.

2. Leitura e Preparação dos Dados
Os dados são carregados de um arquivo CSV (dados_financeiros.csv) e convertidos para o tipo datetime, permitindo filtros temporais e agrupamentos mensais.

3. Filtros Dinâmicos
O usuário pode selecionar:
- Banco específico
- Tipo de transação (Entrada/Saída)
- Mês de referência
Esses filtros são aplicados diretamente ao DataFrame, gerando uma visão personalizada dos dados.

4. Inserção de Transações
A interface lateral permite adicionar novas transações com campos como data, tipo, banco, categoria, descrição e valor. Os dados são salvos via função adicionar_transacao().

5. Backup e Limpeza
Um botão permite gerar backup dos dados e limpar o arquivo CSV, útil para reiniciar o controle financeiro.

6. Cálculo de Saldos
Os saldos por banco são calculados com a função obter_saldo() e exibidos em cartões coloridos (verde para saldo positivo, vermelho para negativo).

7. Visualizações Gráficas
São gerados diversos gráficos interativos com plotly:
- Linha: Entradas vs Saídas por mês
- Rosca: Distribuição de gastos por categoria
- Barras: Entradas e saídas por banco
- Área: Evolução do saldo acumulado
- Heatmap: Gastos por dia da semana

8. Exibição dos Dados
Ao final, o DataFrame filtrado é exibido na íntegra para consulta detalhada.

#🚀 Como Executar
- Clone o repositório
- Instale as dependências com pip install -r requirements.txt
- Execute com streamlit run app.py
- Interaja com os filtros e gráficos na interface web
