# 📦 Insight 1 · Olist | Logística & Receita

**Tech Challenge — Fase 1 | POSTECH DTAT**

🔗 **Dashboard:** [techchallengepos-insight1.streamlit.app](https://techchallengepos-insight1.streamlit.app/)

---

## Sobre o Projeto

Este projeto analisa se o crescimento de pedidos e receita do Olist está sendo limitado pela logística. A partir do cruzamento de dados geográficos e temporais de ~100 mil pedidos (2016–2018), identificamos que a eficiência logística é o fator determinante na geração de receita por estado.

---

## Principais Descobertas

- **SP, RJ e MG concentram 62,6%** da receita total de R$ 15,36M
- **Pearson r = −0,643** (p < 0,001) — correlação negativa entre tempo de entrega e receita
- Volume cresceu de 262 para **7.261 pedidos/mês** (+333/mês), com desaceleração nos meses finais
- **Sudeste: 69%** dos pedidos (entrega 10d) vs **Norte: <2%** (entrega 22d)

---

## Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Estrutura

| Arquivo | Descrição |
|---------|-----------|
| `app.py` | Dashboard Streamlit |
| `requirements.txt` | Dependências |
| `insight1_mensal.csv` | Dados agregados por mês |
| `insight1_por_uf.csv` | Dados agregados por UF |
| `insight1_regiao_mensal.csv` | Dados por região/mês |
| `insight1_logistica.ipynb` | Notebook com análise completa |
| `relatorio_executivo_insight1.docx` | Relatório executivo |

---

## Fonte de Dados

OLIST. Brazilian E-Commerce Public Dataset. Kaggle. Disponível em: [kaggle.com/datasets/olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

---

POSTECH DTAT Fase 1 — Tech Challenge
