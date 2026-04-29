"""
Script de preparação de dados — Insight 5: Categorias líderes com problemas logísticos
Tech Challenge Fase 1 — POSTECH DTAT

Lê os CSVs brutos do dataset Olist, faz limpeza, joins e agregações,
e salva CSVs agregados que serão consumidos pelo dashboard Streamlit.

Uso:
    python preparar_dados.py

Requer que os CSVs brutos estejam no caminho configurado em DATA_DIR.
"""
import os
import pandas as pd
import numpy as np

# ── Configuração ────────────────────────────────────────────────────────
DATA_DIR = os.path.expanduser("~/Downloads/dataset pos fiap/")
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Carregamento ────────────────────────────────────────────────────────
print("[1/5] Carregando CSVs brutos...")
df_orders = pd.read_csv(os.path.join(DATA_DIR, "olist_orders_dataset.csv"))
df_items = pd.read_csv(os.path.join(DATA_DIR, "olist_order_items_dataset.csv"))
df_products = pd.read_csv(os.path.join(DATA_DIR, "olist_products_dataset.csv"))
df_trans = pd.read_csv(os.path.join(DATA_DIR, "product_category_name_translation.csv"))

print(f"  orders:       {df_orders.shape}")
print(f"  items:        {df_items.shape}")
print(f"  products:     {df_products.shape}")
print(f"  translation:  {df_trans.shape}")

# ── Limpeza ─────────────────────────────────────────────────────────────
print("\n[2/5] Limpeza dos dados...")

# Filtrar apenas pedidos entregues
n_antes = len(df_orders)
df_orders = df_orders[df_orders["order_status"] == "delivered"].copy()
print(f"  Filtro 'delivered': {n_antes} -> {len(df_orders)} pedidos")

# Converter datas
df_orders["order_purchase_timestamp"] = pd.to_datetime(
    df_orders["order_purchase_timestamp"], errors="coerce"
)
df_orders["order_delivered_customer_date"] = pd.to_datetime(
    df_orders["order_delivered_customer_date"], errors="coerce"
)

# Remover nulos de datas
n_antes = len(df_orders)
df_orders = df_orders.dropna(
    subset=["order_purchase_timestamp", "order_delivered_customer_date"]
).copy()
print(f"  Remocao datas nulas: {n_antes} -> {len(df_orders)} pedidos")

# Calcular tempo de entrega
df_orders["tempo_entrega"] = (
    df_orders["order_delivered_customer_date"] - df_orders["order_purchase_timestamp"]
).dt.days

# Remover outliers
n_antes = len(df_orders)
df_orders = df_orders[
    (df_orders["tempo_entrega"] >= 0) & (df_orders["tempo_entrega"] <= 60)
].copy()
print(f"  Remocao outliers [0,60] dias: {n_antes} -> {len(df_orders)} pedidos")

# ── Joins ───────────────────────────────────────────────────────────────
print("\n[3/5] Realizando joins...")

# products + translation (categoria em inglês -> usar português quando disponível)
df_products = df_products.merge(
    df_trans, on="product_category_name", how="left"
)
# Preferir o nome em português (original); se faltar, usar o inglês
df_products["categoria"] = df_products["product_category_name"].fillna(
    df_products["product_category_name_english"]
)
df_products["categoria"] = df_products["categoria"].fillna("sem_categoria")

# Join items + products (para ter categoria e dimensões)
df = df_items.merge(
    df_products[[
        "product_id", "categoria",
        "product_weight_g", "product_length_cm",
        "product_height_cm", "product_width_cm",
    ]],
    on="product_id", how="inner",
)
print(f"  items + products: {len(df)} linhas")

# Join com orders (para ter tempo de entrega e data)
df = df.merge(
    df_orders[[
        "order_id", "order_purchase_timestamp",
        "order_delivered_customer_date", "tempo_entrega",
    ]],
    on="order_id", how="inner",
)
print(f"  + orders: {len(df)} linhas")

# Calcular volume do produto (cm3)
df["volume_cm3"] = (
    df["product_length_cm"] * df["product_height_cm"] * df["product_width_cm"]
)

# ── Agregações ──────────────────────────────────────────────────────────
print("\n[4/5] Calculando agregações...")

# ▶ Agregação por categoria (principal)
# receita = soma de price
# tempo_medio = média de tempo_entrega ponderada por pedido
# qtd_pedidos = pedidos únicos
# peso_medio, volume_medio
cat_agg = df.groupby("categoria").agg(
    receita_total=("price", "sum"),
    qtd_pedidos=("order_id", "nunique"),
    qtd_itens=("order_item_id", "count"),
    tempo_medio_entrega=("tempo_entrega", "mean"),
    peso_medio_g=("product_weight_g", "mean"),
    volume_medio_cm3=("volume_cm3", "mean"),
    preco_medio=("price", "mean"),
    frete_medio=("freight_value", "mean"),
).reset_index()

# Índice de eficiência logística = receita / tempo_medio (R$ por dia de espera)
cat_agg["eficiencia_logistica"] = (
    cat_agg["receita_total"] / cat_agg["tempo_medio_entrega"]
)

# Ordenar por receita
cat_agg = cat_agg.sort_values("receita_total", ascending=False).reset_index(drop=True)

print(f"  Categorias: {len(cat_agg)}")

# ▶ Evolução mensal (para tendência temporal)
df["ano_mes"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
mensal_agg = df.groupby("ano_mes").agg(
    qtd_pedidos=("order_id", "nunique"),
    receita_total=("price", "sum"),
    tempo_medio_entrega=("tempo_entrega", "mean"),
).reset_index().sort_values("ano_mes")

print(f"  Meses: {len(mensal_agg)}")

# ▶ Top 15 categorias mensal (para ver evolução das líderes)
top15_cats = cat_agg.head(15)["categoria"].tolist()
mensal_cat = df[df["categoria"].isin(top15_cats)].groupby(
    ["ano_mes", "categoria"]
).agg(
    qtd_pedidos=("order_id", "nunique"),
    receita_total=("price", "sum"),
).reset_index().sort_values(["ano_mes", "categoria"])

print(f"  Top 15 categorias x meses: {len(mensal_cat)}")

# ── Salvar ──────────────────────────────────────────────────────────────
print("\n[5/5] Salvando CSVs agregados...")
cat_agg.to_csv(os.path.join(OUTPUT_DIR, "insight5_categorias.csv"), index=False)
mensal_agg.to_csv(os.path.join(OUTPUT_DIR, "insight5_mensal.csv"), index=False)
mensal_cat.to_csv(os.path.join(OUTPUT_DIR, "insight5_cat_mensal.csv"), index=False)

print(f"  insight5_categorias.csv    ({len(cat_agg)} linhas)")
print(f"  insight5_mensal.csv        ({len(mensal_agg)} linhas)")
print(f"  insight5_cat_mensal.csv    ({len(mensal_cat)} linhas)")

print("\nDados preparados! Agora rode:")
print("  streamlit run insight5/app.py")
