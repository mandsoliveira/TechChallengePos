# 📦 Dashboard — Insight 1 Olist

**Tech Challenge POSTECH DTAT Fase 1**

Dashboard Streamlit interativo que analisa a relação entre tempo de entrega e receita do Olist.

## 🚀 Como rodar localmente

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Garantir que os CSVs estão na pasta raiz

```
insight1/
├── app.py
├── requirements.txt
├── insight1_mensal.csv
├── insight1_por_uf.csv
├── insight1_regiao_mensal.csv
├── insight1_logistica.ipynb
├── relatorio_executivo_insight1.docx
└── .streamlit/
    └── config.toml
```

### 3. Rodar o app

```bash
streamlit run app.py
```

O app abrirá automaticamente em http://localhost:8501

## 📊 Estrutura do Dashboard

| Aba | Conteúdo |
|-----|----------|
| Resumo Executivo | KPIs, frases de impacto, scatter geral |
| Análise Temporal | Evolução mensal, evolução por região |
| Geografia & Logística | Receita por UF, ticket médio, tempo por região |
| Recomendações | Síntese, recomendação ao investidor, limitações |

## 🎛️ Filtros Interativos (Sidebar)

- **Região** — multiselect por região geográfica
- **Estado (UF)** — filtra por estado do cliente
- **Período** — slider de meses
- **Tempo de entrega** — faixa em dias

Todos os gráficos atualizam em tempo real.

## 📁 Dados

Os CSVs são gerados pelo notebook `insight1_logistica.ipynb` a partir do dataset original.

Dataset original: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (~100 mil pedidos, 2016–2018)

---
POSTECH DTAT Fase 1 — Tech Challenge
