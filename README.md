# 📦 Insight 5 · Olist | Categorias & Logística

**Tech Challenge — Fase 1 | POSTECH DTAT**

---

## Sobre o Projeto

Este projeto analisa se as categorias de produto que mais faturam no Olist conseguem entregar bem. A partir do cruzamento de dados de produtos, pedidos e itens (~100 mil pedidos, 2016–2018), identificamos que as categorias líderes em receita frequentemente enfrentam os piores indicadores logísticos — especialmente aquelas com produtos pesados e volumosos.

**Pergunta de negócio:** As categorias que mais faturam conseguem entregar bem?

---

## Principais Descobertas

- As **Top 15 categorias** concentram a maioria da receita total
- Correlação entre **peso do produto** e **tempo de entrega** — categorias pesadas demoram mais
- Identificamos um **quadrante problemático**: categorias com alta receita + entrega lenta
- Índice de eficiência logística (receita / tempo médio) revela quais categorias destravam mais valor por dia de espera

---

## Como rodar localmente

### 1. Preparar os dados

Certifique-se de que os CSVs brutos do dataset Olist estão em `~/Downloads/dataset pos fiap/` (ou ajuste o `DATA_DIR` em `preparar_dados.py`).

```bash
pip install -r requirements.txt
python preparar_dados.py
```

Isso gera os 3 CSVs agregados usados pelo dashboard:
- `insight5_categorias.csv`
- `insight5_mensal.csv`
- `insight5_cat_mensal.csv`

### 2. Rodar o dashboard

```bash
streamlit run app.py
```

O dashboard abre automaticamente em `http://localhost:8501`.

---

## Estrutura

| Arquivo | Descrição |
|---------|-----------|
| `app.py` | Dashboard Streamlit |
| `preparar_dados.py` | Script que processa os CSVs brutos e gera agregações |
| `requirements.txt` | Dependências |
| `insight5_categorias.csv` | Dados agregados por categoria |
| `insight5_mensal.csv` | Evolução mensal |
| `insight5_cat_mensal.csv` | Top 15 categorias ao longo do tempo |
| `.streamlit/config.toml` | Tema visual (light mode) |

---

## Dashboard — 4 Abas

1. **Resumo Executivo** — Métricas-chave e dispersão com quadrantes (Ideal, Problemática, etc.)
2. **Receita & Entrega** — Top categorias por receita, tempo de entrega e eficiência logística
3. **Peso & Dimensões** — Correlação entre peso/volume dos produtos e tempo de entrega
4. **Recomendações** — Síntese, categorias prioritárias e limitações

---

## Fonte de Dados

OLIST. Brazilian E-Commerce Public Dataset. Kaggle. Disponível em: [kaggle.com/datasets/olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

---

POSTECH DTAT Fase 1 — Tech Challenge
