"""
Dashboard — Insight 5: Categorias Líderes com Problemas Logísticos
Tech Challenge Fase 1 — POSTECH DTAT

Pergunta de negócio: As categorias que mais faturam conseguem entregar bem?
"""
import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy import stats

st.set_page_config(page_title="Insight 5 · Olist", page_icon="📦", layout="wide")

# ── Forçar tema claro ───────────────────────────────────────────────────
st.markdown("""
<style>
    :root { color-scheme: light; }
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    .stApp {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #F5F7FA !important;
    }
    [data-testid="stSidebar"] * {
        color: #333333 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Paleta ──────────────────────────────────────────────────────────────
CIANO     = "#5CC9DD"
LAVANDA   = "#E2C0FF"
LARANJA   = "#F99E35"
CINZA_AZ  = "#4A4D57"
PETROLEO  = "#1B3A4B"
PETROLEO2 = "#245B6F"
MOSTARDA  = "#D4A843"
VERMELHO  = "#EF5350"
VERDE     = "#66BB6A"

# ── CSS ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    .block-container {{ padding-top: 0; max-width: 1300px; }}
    .stApp {{ background-color: #ffffff; }}
    [data-testid="stSidebar"] {{ background: white; }}

    .hdr {{
        background: linear-gradient(135deg, {PETROLEO} 0%, {PETROLEO2} 60%, {CIANO} 100%);
        padding: 1.8rem 2rem 1.2rem; border-radius: 0 0 14px 14px; margin-bottom: .8rem;
    }}
    .hdr h1 {{ color: #fff !important; font-size: 1.5rem; font-weight: 800; margin: 0; }}
    .hdr p {{ color: rgba(255,255,255,.6) !important; font-size: .8rem; margin: .3rem 0 0; }}
    .hdr strong {{ color: #fff !important; }}

    .kstrip {{ display: flex; gap: .7rem; margin: .6rem 0 1.2rem; }}
    .kc {{ flex:1; background: {MOSTARDA}; border-radius: 8px; padding: .85rem .6rem; text-align: center; }}
    .kc .n {{ color: #fff !important; font-size: 1.3rem; font-weight: 800; }}
    .kc .t {{ color: rgba(255,255,255,.75) !important; font-size: .62rem; text-transform: uppercase; letter-spacing: .6px; margin-top: .15rem; }}

    .fi {{
        background: #fff; border-left: 4px solid {LARANJA}; border-radius: 0 6px 6px 0;
        padding: .6rem 1rem; margin-bottom: .45rem; font-size: .83rem; color: #333 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,.04); line-height: 1.5;
    }}
    .fi strong {{ color: {PETROLEO} !important; }}

    .rec {{
        background: {PETROLEO}; border-radius: 10px; padding: 1.6rem 2rem; margin-top: .5rem;
    }}
    .rec h4 {{ color: {CIANO} !important; font-size: .68rem; text-transform: uppercase; letter-spacing: 1.2px; margin: 0 0 .5rem; }}
    .rec p {{ color: #ccc !important; font-size: .86rem; line-height: 1.65; margin: 0; }}
    .rec strong {{ color: #fff !important; }}

    #MainMenu, footer, header {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# ── Plot config ─────────────────────────────────────────────────────────
PB = dict(
    paper_bgcolor="white", plot_bgcolor="white",
    font=dict(size=12, color="#222"),
    margin=dict(l=70, r=20, t=30, b=60),
)
GRID = "#ddd"

# ── Dados ───────────────────────────────────────────────────────────────
DIR = os.path.dirname(os.path.abspath(__file__))


@st.cache_data
def load():
    cat = pd.read_csv(os.path.join(DIR, "insight5_categorias.csv"))
    mensal = pd.read_csv(os.path.join(DIR, "insight5_mensal.csv"))
    cat_mensal = pd.read_csv(os.path.join(DIR, "insight5_cat_mensal.csv"))
    return cat, mensal, cat_mensal


df_cat, df_m, df_cm = load()

# ── Métricas globais ────────────────────────────────────────────────────
REC = df_cat["receita_total"].sum()
NPED = df_cat["qtd_pedidos"].sum()
NCAT = len(df_cat)
TMED = (df_cat["tempo_medio_entrega"] * df_cat["qtd_pedidos"]).sum() / NPED

# Pearson: tempo de entrega vs receita (por categoria)
corr, pv = stats.pearsonr(df_cat["tempo_medio_entrega"].values, df_cat["receita_total"].values)

# Top 15 categorias por receita (foco da análise)
top15 = df_cat.head(15).copy()
T15P = top15["receita_total"].sum() / REC * 100

# Categoria líder
CAT_LIDER = df_cat.iloc[0]

# Mediana do tempo de entrega (para classificar "rápida" vs "lenta")
mediana_tempo = df_cat["tempo_medio_entrega"].median()

# Quadrante problemático: alta receita (top 15) + tempo acima da mediana
quadrante_prob = top15[top15["tempo_medio_entrega"] > mediana_tempo]
N_PROB = len(quadrante_prob)
REC_PROB = quadrante_prob["receita_total"].sum()
REC_PROB_PCT = REC_PROB / REC * 100

# Categorias mais pesadas (percentil 75+)
p75_peso = df_cat["peso_medio_g"].quantile(0.75)
pesadas = df_cat[df_cat["peso_medio_g"] >= p75_peso]
TEMPO_PESADAS = pesadas["tempo_medio_entrega"].mean()

p25_peso = df_cat["peso_medio_g"].quantile(0.25)
leves = df_cat[df_cat["peso_medio_g"] <= p25_peso]
TEMPO_LEVES = leves["tempo_medio_entrega"].mean()

# ── Sidebar ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("**📦 Insight 5 · Olist**")
    st.caption("Categorias & Logística")
    st.divider()

    st.markdown("**🔍 Filtros**")

    # Número de categorias no gráfico
    top_n = st.slider(
        "Quantas categorias mostrar",
        min_value=5, max_value=30, value=15, step=5,
        help="Número de categorias top exibidas nos gráficos de barras",
    )

    # Filtro por tempo de entrega
    t_min = int(df_cat["tempo_medio_entrega"].min())
    t_max = int(df_cat["tempo_medio_entrega"].max()) + 1
    sel_t = st.slider(
        "Tempo de entrega (dias)",
        t_min, t_max, (t_min, t_max),
        help="Filtra categorias por faixa de tempo médio de entrega",
    )

    # Filtro por faixa de receita
    r_min = float(df_cat["receita_total"].min())
    r_max = float(df_cat["receita_total"].max())
    sel_r = st.slider(
        "Receita total (R$)",
        r_min, r_max, (r_min, r_max),
        step=(r_max - r_min) / 20,
        format="R$ %.0f",
    )

    st.divider()

    # Aplicar filtros
    f_cat = df_cat[
        (df_cat["tempo_medio_entrega"] >= sel_t[0]) &
        (df_cat["tempo_medio_entrega"] <= sel_t[1]) &
        (df_cat["receita_total"] >= sel_r[0]) &
        (df_cat["receita_total"] <= sel_r[1])
    ].copy()

    st.metric("Categorias filtradas", f"{len(f_cat)} de {NCAT}")
    st.metric("Receita filtrada", f"R$ {f_cat['receita_total'].sum()/1e6:.2f}M")

    st.divider()
    st.caption(f"Dataset total: {NPED:,} pedidos · 2016–2018")
    st.caption(f"{NCAT} categorias analisadas")
    st.caption("POSTECH DTAT Fase 1 — Tech Challenge")

# ── Métricas filtradas ──────────────────────────────────────────────────
f_REC = f_cat["receita_total"].sum()
f_NPED = f_cat["qtd_pedidos"].sum()
f_TMED = (f_cat["tempo_medio_entrega"] * f_cat["qtd_pedidos"]).sum() / f_NPED if f_NPED > 0 else 0

if len(f_cat) >= 3:
    f_corr, f_pv = stats.pearsonr(
        f_cat["tempo_medio_entrega"].values,
        f_cat["receita_total"].values,
    )
else:
    f_corr, f_pv = 0, 1

f_top = f_cat.head(top_n).copy()

# ── Header ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hdr">
    <h1>📦 Insight 5 · Olist | Categorias & Logística</h1>
    <p>As categorias que mais faturam conseguem entregar bem? · <strong>{f_NPED:,}</strong> pedidos em <strong>{len(f_cat)}</strong> categorias</p>
</div>
""", unsafe_allow_html=True)

# ── Abas ────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Resumo Executivo", "💰 Receita & Entrega",
    "⚖️ Peso & Dimensões", "💡 Recomendações",
])

# ════════════════════════════════════════════════════════════════════════
# TAB 1 — RESUMO
# ════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown(f"""
    <div class="kstrip">
        <div class="kc"><div class="n">{f_NPED:,}</div><div class="t">Pedidos</div></div>
        <div class="kc"><div class="n">R$ {f_REC/1e6:.2f}M</div><div class="t">Receita Total</div></div>
        <div class="kc"><div class="n">{len(f_cat)}</div><div class="t">Categorias</div></div>
        <div class="kc"><div class="n">{f_TMED:.1f}d</div><div class="t">Entrega Média</div></div>
        <div class="kc"><div class="n">{f_corr:.3f}</div><div class="t">Pearson r</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Frases de Impacto**")
    for txt in [
        f"As <strong>Top 15 categorias</strong> concentram <strong>{T15P:.1f}%</strong> "
        f"da receita total de R$ {REC/1e6:.2f}M.",
        f"<strong>{CAT_LIDER['categoria'].replace('_', ' ')}</strong> lidera em receita "
        f"(R$ {CAT_LIDER['receita_total']/1e6:.2f}M) com entrega média de "
        f"<strong>{CAT_LIDER['tempo_medio_entrega']:.1f} dias</strong>.",
        f"Correlação Pearson: <strong>r = {corr:.3f}</strong> entre tempo de entrega "
        f"e receita por categoria (p = {pv:.4f}).",
        f"<strong>{N_PROB} categorias</strong> do Top 15 estão no quadrante problemático "
        f"(alta receita + entrega acima da mediana) — representam "
        f"<strong>{REC_PROB_PCT:.1f}%</strong> da receita total.",
        f"Categorias pesadas (≥ {p75_peso:.0f}g) demoram "
        f"<strong>{TEMPO_PESADAS:.1f} dias</strong> vs "
        f"<strong>{TEMPO_LEVES:.1f} dias</strong> das leves "
        f"(≤ {p25_peso:.0f}g) — diferença de {TEMPO_PESADAS - TEMPO_LEVES:+.1f}d.",
    ]:
        st.markdown(f'<div class="fi">{txt}</div>', unsafe_allow_html=True)

    st.markdown("")
    st.markdown(f"**Dispersão: Receita × Tempo de Entrega por Categoria | Pearson r = {f_corr:.3f}**")

    # Scatter com tamanho do ponto = volume de pedidos
    fig_sc = go.Figure()

    # Dividir em quadrantes para colorir
    mediana_rec = f_cat["receita_total"].median()
    mediana_temp_f = f_cat["tempo_medio_entrega"].median()

    for idx, row in f_cat.iterrows():
        alta_rec = row["receita_total"] > mediana_rec
        alta_temp = row["tempo_medio_entrega"] > mediana_temp_f

        if alta_rec and alta_temp:
            cor = VERMELHO  # Problemática: alta receita + entrega lenta
            grupo = "Problemática"
        elif alta_rec and not alta_temp:
            cor = VERDE  # Ideal: alta receita + entrega rápida
            grupo = "Ideal"
        elif not alta_rec and alta_temp:
            cor = LARANJA  # Baixa receita + entrega lenta
            grupo = "Baixa receita · Lenta"
        else:
            cor = CIANO  # Baixa receita + entrega rápida
            grupo = "Baixa receita · Rápida"

        fig_sc.add_trace(go.Scatter(
            x=[row["tempo_medio_entrega"]],
            y=[row["receita_total"]],
            mode="markers",
            name=grupo,
            legendgroup=grupo,
            showlegend=False,
            marker=dict(
                size=max(np.sqrt(row["qtd_pedidos"]) / 2, 6),
                color=cor,
                opacity=0.7,
                line=dict(width=1, color="white"),
            ),
            hovertemplate=(
                f"<b>{row['categoria'].replace('_', ' ')}</b><br>"
                f"Receita: R$ %{{y:,.0f}}<br>"
                f"Tempo: %{{x:.1f}} dias<br>"
                f"Pedidos: {row['qtd_pedidos']:,}<extra></extra>"
            ),
        ))

    # Legenda manual dos quadrantes
    for grupo, cor in [
        ("Ideal (alta receita · rápida)", VERDE),
        ("Problemática (alta receita · lenta)", VERMELHO),
        ("Baixa receita · Rápida", CIANO),
        ("Baixa receita · Lenta", LARANJA),
    ]:
        fig_sc.add_trace(go.Scatter(
            x=[None], y=[None], mode="markers",
            marker=dict(size=10, color=cor),
            name=grupo, showlegend=True,
        ))

    # Linhas de mediana
    fig_sc.add_hline(y=mediana_rec, line=dict(color="#bbb", width=1, dash="dot"))
    fig_sc.add_vline(x=mediana_temp_f, line=dict(color="#bbb", width=1, dash="dot"))

    # Linha de tendência
    if len(f_cat) >= 2:
        xs = f_cat["tempo_medio_entrega"].values
        ys = f_cat["receita_total"].values
        cs = np.polyfit(xs, ys, 1)
        xl = np.linspace(xs.min(), xs.max(), 50)
        fig_sc.add_trace(go.Scatter(
            x=xl, y=np.polyval(cs, xl),
            mode="lines", showlegend=False,
            line=dict(color="#999", width=1.5, dash="dash"),
        ))

    fig_sc.update_layout(
        **PB, height=500, hovermode="closest",
        legend=dict(orientation="h", y=-0.2),
        xaxis=dict(title="Tempo Médio de Entrega (dias)", gridcolor=GRID),
        yaxis=dict(title="Receita Total (R$)", tickformat=",.0f", gridcolor=GRID),
    )
    st.plotly_chart(fig_sc, key="sc1", theme=None)

# ════════════════════════════════════════════════════════════════════════
# TAB 2 — RECEITA & ENTREGA
# ════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(f"**Top {top_n} Categorias por Receita**")

    # Barras horizontais — receita por categoria (top N)
    f_top_ord = f_top.sort_values("receita_total", ascending=True)
    cat_labels = [c.replace("_", " ") for c in f_top_ord["categoria"]]

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=f_top_ord["receita_total"], y=cat_labels,
        orientation="h", marker_color=CIANO,
        text=[f"R$ {v/1e3:.0f}k" for v in f_top_ord["receita_total"]],
        textposition="outside", textfont=dict(size=10, color="#222"),
        hovertemplate="<b>%{y}</b><br>Receita: R$ %{x:,.0f}<extra></extra>",
    ))
    fig1.update_layout(
        **PB, height=max(400, top_n * 25),
        xaxis=dict(tickformat=",.0f", gridcolor=GRID, title="Receita (R$)"),
        yaxis=dict(showgrid=False, tickfont=dict(size=10)),
    )
    st.plotly_chart(fig1, key="rec_cat", theme=None)
    st.markdown(
        f'<div class="fi">A categoria líder (<strong>{CAT_LIDER["categoria"].replace("_", " ")}</strong>) '
        f'fatura R$ {CAT_LIDER["receita_total"]/1e6:.2f}M, '
        f'{CAT_LIDER["receita_total"] / df_cat.iloc[1]["receita_total"]:.1f}x mais que a segunda.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown(f"**Top {top_n} Categorias — Tempo Médio de Entrega**")

    # Barras horizontais — tempo de entrega (top N, ordenado por tempo)
    f_top_temp = f_top.sort_values("tempo_medio_entrega", ascending=True)
    cat_labels_t = [c.replace("_", " ") for c in f_top_temp["categoria"]]

    # Cor por tempo: verde (rápido) -> laranja -> vermelho (lento)
    cores_tempo = []
    for t in f_top_temp["tempo_medio_entrega"]:
        if t < mediana_tempo * 0.9:
            cores_tempo.append(VERDE)
        elif t < mediana_tempo * 1.1:
            cores_tempo.append(CIANO)
        else:
            cores_tempo.append(LARANJA if t < mediana_tempo * 1.3 else VERMELHO)

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=f_top_temp["tempo_medio_entrega"], y=cat_labels_t,
        orientation="h", marker_color=cores_tempo,
        text=[f"{t:.1f}d" for t in f_top_temp["tempo_medio_entrega"]],
        textposition="outside", textfont=dict(size=10, color="#222"),
        hovertemplate="<b>%{y}</b><br>Tempo médio: %{x:.1f} dias<extra></extra>",
    ))
    fig2.add_vline(
        x=mediana_tempo, line=dict(color="#999", width=1.5, dash="dash"),
        annotation_text=f"Mediana: {mediana_tempo:.1f}d",
        annotation_position="top right",
    )
    fig2.update_layout(
        **PB, height=max(400, top_n * 25),
        xaxis=dict(gridcolor=GRID, title="Tempo Médio (dias)"),
        yaxis=dict(showgrid=False, tickfont=dict(size=10)),
    )
    st.plotly_chart(fig2, key="temp_cat", theme=None)

    lento = f_top_temp.iloc[-1]
    rapido = f_top_temp.iloc[0]
    st.markdown(
        f'<div class="fi"><strong>{lento["categoria"].replace("_", " ")}</strong> tem a entrega mais lenta '
        f'({lento["tempo_medio_entrega"]:.1f}d), enquanto '
        f'<strong>{rapido["categoria"].replace("_", " ")}</strong> é a mais rápida '
        f'({rapido["tempo_medio_entrega"]:.1f}d). Diferença de '
        f'{lento["tempo_medio_entrega"] - rapido["tempo_medio_entrega"]:.1f} dias.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown("**Índice de Eficiência Logística** (receita por dia de espera)")

    # Eficiência = receita / tempo_medio
    f_top_ef = f_top.sort_values("eficiencia_logistica", ascending=True)
    cat_labels_e = [c.replace("_", " ") for c in f_top_ef["categoria"]]

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=f_top_ef["eficiencia_logistica"], y=cat_labels_e,
        orientation="h", marker_color=MOSTARDA,
        text=[f"R$ {v/1e3:.0f}k/d" for v in f_top_ef["eficiencia_logistica"]],
        textposition="outside", textfont=dict(size=10, color="#222"),
        hovertemplate="<b>%{y}</b><br>Eficiência: R$ %{x:,.0f}/dia<extra></extra>",
    ))
    fig3.update_layout(
        **PB, height=max(400, top_n * 25),
        xaxis=dict(tickformat=",.0f", gridcolor=GRID, title="Receita / Tempo Médio (R$/dia)"),
        yaxis=dict(showgrid=False, tickfont=dict(size=10)),
    )
    st.plotly_chart(fig3, key="ef_cat", theme=None)
    st.markdown(
        '<div class="fi">Categorias com alta eficiência combinam boa receita e entrega rápida. '
        'Categorias pesadas/volumosas tendem a ficar no fim do ranking.</div>',
        unsafe_allow_html=True,
    )

# ════════════════════════════════════════════════════════════════════════
# TAB 3 — PESO & DIMENSÕES
# ════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("**Peso Médio vs Tempo de Entrega por Categoria**")

    fig_peso = go.Figure()
    fig_peso.add_trace(go.Scatter(
        x=f_cat["peso_medio_g"],
        y=f_cat["tempo_medio_entrega"],
        mode="markers",
        marker=dict(
            size=np.sqrt(f_cat["qtd_pedidos"]) / 2 + 6,
            color=f_cat["receita_total"],
            colorscale=[[0, CIANO], [0.5, MOSTARDA], [1, VERMELHO]],
            showscale=True,
            colorbar=dict(title="Receita (R$)", tickformat=",.0f"),
            opacity=0.75,
            line=dict(width=1, color="white"),
        ),
        text=[c.replace("_", " ") for c in f_cat["categoria"]],
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Peso médio: %{x:.0f}g<br>"
            "Tempo: %{y:.1f} dias<extra></extra>"
        ),
    ))

    # Linha de tendência
    if len(f_cat) >= 2:
        xs = f_cat["peso_medio_g"].values
        ys = f_cat["tempo_medio_entrega"].values
        # Remover NaN
        mask = ~(np.isnan(xs) | np.isnan(ys))
        if mask.sum() >= 2:
            cs = np.polyfit(xs[mask], ys[mask], 1)
            xl = np.linspace(xs[mask].min(), xs[mask].max(), 50)
            corr_peso, _ = stats.pearsonr(xs[mask], ys[mask])
            fig_peso.add_trace(go.Scatter(
                x=xl, y=np.polyval(cs, xl),
                mode="lines",
                name=f"Tendência (r={corr_peso:.3f})",
                line=dict(color="#999", width=1.5, dash="dash"),
            ))

    fig_peso.update_layout(
        **PB, height=480, hovermode="closest",
        xaxis=dict(title="Peso Médio do Produto (g)", gridcolor=GRID),
        yaxis=dict(title="Tempo Médio de Entrega (dias)", gridcolor=GRID),
    )
    st.plotly_chart(fig_peso, key="peso", theme=None)
    st.markdown(
        f'<div class="fi">Categorias pesadas (≥ {p75_peso:.0f}g, P75) têm tempo médio de '
        f'<strong>{TEMPO_PESADAS:.1f} dias</strong>, contra <strong>{TEMPO_LEVES:.1f} dias</strong> '
        f'das leves (≤ {p25_peso:.0f}g, P25) — diferença de {TEMPO_PESADAS - TEMPO_LEVES:+.1f} dias.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown("**Volume Médio vs Tempo de Entrega**")

    fig_vol = go.Figure()
    fig_vol.add_trace(go.Scatter(
        x=f_cat["volume_medio_cm3"],
        y=f_cat["tempo_medio_entrega"],
        mode="markers",
        marker=dict(
            size=np.sqrt(f_cat["qtd_pedidos"]) / 2 + 6,
            color=LAVANDA, opacity=0.75,
            line=dict(width=1, color="white"),
        ),
        text=[c.replace("_", " ") for c in f_cat["categoria"]],
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Volume médio: %{x:,.0f} cm³<br>"
            "Tempo: %{y:.1f} dias<extra></extra>"
        ),
    ))
    fig_vol.update_layout(
        **PB, height=420, hovermode="closest",
        xaxis=dict(title="Volume Médio do Produto (cm³)", gridcolor=GRID, tickformat=",.0f"),
        yaxis=dict(title="Tempo Médio de Entrega (dias)", gridcolor=GRID),
    )
    st.plotly_chart(fig_vol, key="vol", theme=None)

    # Correlação peso vs tempo
    xs_p = f_cat["peso_medio_g"].dropna().values
    ys_p = f_cat.loc[f_cat["peso_medio_g"].notna(), "tempo_medio_entrega"].values
    if len(xs_p) >= 3:
        c_peso, p_peso = stats.pearsonr(xs_p, ys_p)
    else:
        c_peso, p_peso = 0, 1

    xs_v = f_cat["volume_medio_cm3"].dropna().values
    ys_v = f_cat.loc[f_cat["volume_medio_cm3"].notna(), "tempo_medio_entrega"].values
    if len(xs_v) >= 3:
        c_vol, p_vol = stats.pearsonr(xs_v, ys_v)
    else:
        c_vol, p_vol = 0, 1

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f'<div class="fi"><strong>Peso × Tempo</strong><br>'
            f'Pearson r = {c_peso:.3f} (p = {p_peso:.4f})</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="fi"><strong>Volume × Tempo</strong><br>'
            f'Pearson r = {c_vol:.3f} (p = {p_vol:.4f})</div>',
            unsafe_allow_html=True,
        )

# ════════════════════════════════════════════════════════════════════════
# TAB 4 — RECOMENDAÇÕES
# ════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("**Síntese dos Achados**")
    for a, e in [
        ("Receita concentrada no topo",
         f"Top 15 categorias = {T15P:.1f}% de R$ {REC/1e6:.2f}M"),
        ("Líder absoluta",
         f"{CAT_LIDER['categoria'].replace('_', ' ')} · R$ {CAT_LIDER['receita_total']/1e6:.2f}M · "
         f"{CAT_LIDER['tempo_medio_entrega']:.1f}d"),
        ("Correlação tempo × receita",
         f"Pearson r = {corr:.3f} (p = {pv:.4f})"),
        ("Quadrante problemático",
         f"{N_PROB} categorias top concentram {REC_PROB_PCT:.1f}% da receita com entrega lenta"),
        ("Peso impacta entrega",
         f"Pesadas: {TEMPO_PESADAS:.1f}d vs Leves: {TEMPO_LEVES:.1f}d "
         f"({TEMPO_PESADAS - TEMPO_LEVES:+.1f}d)"),
    ]:
        st.markdown(f'<div class="fi"><strong>{a}</strong> — {e}</div>', unsafe_allow_html=True)

    st.markdown("")
    st.markdown(f"""
    <div class="rec">
        <h4>Recomendação para o Investidor</h4>
        <p>
            As categorias líderes em receita enfrentam os piores indicadores logísticos —
            justamente as que faturam mais são pesadas, volumosas e demoram mais para entregar.
            <strong>Otimizar a cadeia logística das Top 15 categorias</strong> (que representam
            {T15P:.1f}% da receita) é a maior alavanca de crescimento. Investir em armazéns
            especializados para categorias volumosas, parcerias com transportadoras dedicadas
            e SLA diferenciado para os produtos de maior valor destrava receita direta.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("**Categorias Prioritárias** (Top 15 com entrega acima da mediana)")

    if len(quadrante_prob) > 0:
        for _, row in quadrante_prob.iterrows():
            st.markdown(
                f'<div class="fi">🚨 <strong>{row["categoria"].replace("_", " ")}</strong> · '
                f'R$ {row["receita_total"]/1e6:.2f}M · '
                f'{row["tempo_medio_entrega"]:.1f}d · '
                f'{row["qtd_pedidos"]:,} pedidos</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="fi">Nenhuma categoria do Top 15 está acima da mediana de tempo. '
            'Situação atípica — verificar filtros.</div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown("**Limitações**")
    for l in [
        "Tempo de entrega depende da UF do cliente — não isolamos o fator categoria.",
        "Peso e volume com valores nulos em ~1% das categorias (excluídos das correlações).",
        "Dados de 2016–2018 — padrões de consumo podem ter mudado.",
        "Análise por categoria do produto principal do pedido (não considera cestas mistas).",
    ]:
        st.markdown(f'<div class="fi">{l}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Insight 5 — Categorias & Logística · POSTECH DTAT Fase 1 · Olist 2016–2018")
