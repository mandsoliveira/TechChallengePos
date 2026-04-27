"""
Dashboard — Insight 1: Crescimento Limitado pela Logística
Tech Challenge Fase 1 — POSTECH DTAT
"""
import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy import stats

st.set_page_config(page_title="Insight 1 · Olist", page_icon="📦", layout="wide")

# ── Forçar tema claro (sem precisar de .streamlit/config.toml) ──────────
st.markdown("""
<style>
    :root {
        color-scheme: light;
    }
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

CORES_REG = {
    "Sudeste": CIANO, "Sul": "#66BB6A", "Nordeste": LARANJA,
    "Centro-Oeste": LAVANDA, "Norte": "#EF5350",
}

# ── CSS (só o essencial) ────────────────────────────────────────────────
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

# ── Dados (só agregados = rápido) ──────────────────────────────────────
DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load():
    m = pd.read_csv(os.path.join(DIR, "insight1_mensal.csv"))
    u = pd.read_csv(os.path.join(DIR, "insight1_por_uf.csv"))
    r = pd.read_csv(os.path.join(DIR, "insight1_regiao_mensal.csv"))
    return m, u, r

df_m, df_uf, df_rg = load()

# ── Métricas ────────────────────────────────────────────────────────────
REC = df_uf["receita_total"].sum()
NPED = df_uf["qtd_pedidos"].sum()
TMED = (df_uf["tempo_medio_entrega"] * df_uf["qtd_pedidos"]).sum() / NPED
corr, pv = stats.pearsonr(df_uf["tempo_medio_entrega"].values, df_uf["receita_total"].values)

xi = np.arange(len(df_m), dtype=float)
yi = df_m["qtd_pedidos"].values.astype(float)
tc = np.polyfit(xi, yi, 1)
yt = np.polyval(tc, xi)
pi = int(df_m["qtd_pedidos"].idxmax())
PMES, PVAL = df_m.loc[pi, "ano_mes"], int(df_m.loc[pi, "qtd_pedidos"])

top3 = df_uf.nlargest(3, "receita_total")
T3P = top3["receita_total"].sum() / REC * 100

mu = df_uf["tempo_medio_entrega"].median()
TKR = df_uf.loc[df_uf["tempo_medio_entrega"] < mu, "ticket_medio"].mean()
TKL = df_uf.loc[df_uf["tempo_medio_entrega"] >= mu, "ticket_medio"].mean()
TKD = ((TKR - TKL) / TKL) * 100 if TKL > 0 else 0

pr = df_uf.groupby("regiao")["qtd_pedidos"].sum()
SE_P = pr.get("Sudeste", 0) / pr.sum() * 100
TR = df_uf.groupby("regiao")["tempo_medio_entrega"].mean()

# ── Sidebar ─────────────────────────────────────────────────────────────
all_regioes = sorted(df_uf["regiao"].unique())
all_ufs = sorted(df_uf["customer_state"].unique())
all_meses = df_m["ano_mes"].tolist()

with st.sidebar:
    st.markdown(f"**📦 Insight 1 · Olist**")
    st.caption("Logística & Receita")
    st.divider()

    st.markdown("**🔍 Filtros**")

    # Região
    sel_reg = st.multiselect(
        "Região",
        options=all_regioes,
        default=all_regioes,
        help="Filtra gráficos por região geográfica",
    )

    # Estado
    ufs_disponiveis = sorted(df_uf[df_uf["regiao"].isin(sel_reg)]["customer_state"].unique())
    sel_ufs = st.multiselect(
        "Estado (UF)",
        options=ufs_disponiveis,
        default=ufs_disponiveis,
        help="Filtra por estado do cliente",
    )

    # Período
    st.markdown("")
    mes_ini, mes_fim = st.select_slider(
        "Período",
        options=all_meses,
        value=(all_meses[0], all_meses[-1]),
        help="Filtra gráficos temporais por período",
    )

    # Faixa de entrega
    ent_min = int(df_uf["tempo_medio_entrega"].min())
    ent_max = int(df_uf["tempo_medio_entrega"].max()) + 1
    sel_ent = st.slider("Tempo de entrega (dias)", ent_min, ent_max, (ent_min, ent_max))

    st.divider()

    # Resumo do filtro
    uf_filt = df_uf[
        (df_uf["regiao"].isin(sel_reg)) &
        (df_uf["customer_state"].isin(sel_ufs)) &
        (df_uf["tempo_medio_entrega"] >= sel_ent[0]) &
        (df_uf["tempo_medio_entrega"] <= sel_ent[1])
    ]
    ped_filt = uf_filt["qtd_pedidos"].sum()
    rec_filt = uf_filt["receita_total"].sum()

    st.metric("Pedidos filtrados", f"{ped_filt:,}")
    st.metric("Receita filtrada", f"R$ {rec_filt/1e6:.2f}M")

    st.divider()
    st.caption(f"Dataset total: {NPED:,} pedidos · 2016–2018")
    st.caption("POSTECH DTAT Fase 1 — Tech Challenge")

# ── Dados filtrados ─────────────────────────────────────────────────────
f_uf = uf_filt.copy()
i_ini = all_meses.index(mes_ini)
i_fim = all_meses.index(mes_fim)
meses_sel = all_meses[i_ini:i_fim + 1]
f_m = df_m[df_m["ano_mes"].isin(meses_sel)]
f_rg = df_rg[(df_rg["ano_mes"].isin(meses_sel)) & (df_rg["regiao"].isin(sel_reg))]

# Métricas filtradas
f_REC = f_uf["receita_total"].sum()
f_NPED = f_uf["qtd_pedidos"].sum()
f_TMED = (f_uf["tempo_medio_entrega"] * f_uf["qtd_pedidos"]).sum() / f_NPED if f_NPED > 0 else 0
if len(f_uf) >= 3:
    f_corr, f_pv = stats.pearsonr(f_uf["tempo_medio_entrega"].values, f_uf["receita_total"].values)
else:
    f_corr, f_pv = 0, 1
f_top3 = f_uf.nlargest(3, "receita_total")
f_T3P = f_top3["receita_total"].sum() / f_REC * 100 if f_REC > 0 else 0

# ── Header ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hdr">
    <h1>📦 Insight 1 · Olist | Logística & Receita</h1>
    <p>O crescimento está sendo limitado pela logística? · <strong>{f_NPED:,}</strong> pedidos filtrados de {NPED:,}</p>
</div>
""", unsafe_allow_html=True)

# ── Abas ────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Resumo Executivo", "📈 Análise Temporal",
    "🗺️ Geografia & Logística", "💡 Recomendações",
])

# ════════════════════════════════════════════════════════════════════════
# TAB 1
# ════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown(f"""
    <div class="kstrip">
        <div class="kc"><div class="n">{f_NPED:,}</div><div class="t">Pedidos Entregues</div></div>
        <div class="kc"><div class="n">R$ {f_REC/1e6:.2f}M</div><div class="t">Receita Total</div></div>
        <div class="kc"><div class="n">{f_TMED:.1f}d</div><div class="t">Entrega Média</div></div>
        <div class="kc"><div class="n">{f_corr:.3f}</div><div class="t">Pearson r</div></div>
        <div class="kc"><div class="n">{f_T3P:.1f}%</div><div class="t">Top 3 UFs</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Frases de Impacto**")
    for txt in [
        f"SP, RJ e MG concentram <strong>{T3P:.1f}%</strong> da receita total de R$ {REC/1e6:.2f}M.",
        f"Correlação de Pearson: <strong>r = {corr:.3f}</strong> (p < 0,001) — negativa e significativa.",
        f"Volume cresceu de {int(df_m.iloc[0]['qtd_pedidos']):,} para <strong>{PVAL:,}</strong> (+{tc[0]:.0f}/mês), com desaceleração nos meses finais.",
        f"Sudeste: <strong>{SE_P:.0f}%</strong> dos pedidos ({TR.get('Sudeste',0):.0f}d). Norte: &lt;2% ({TR.get('Norte',0):.0f}d).",
        f"Ticket rápida: R$ {TKR:.2f} vs lenta: R$ {TKL:.2f} ({TKD:+.1f}%).",
    ]:
        st.markdown(f'<div class="fi">{txt}</div>', unsafe_allow_html=True)

    st.markdown("")
    st.markdown(f"**Dispersão: Entrega × Receita | Pearson r = {f_corr:.3f}**")

    fig_sc = go.Figure()
    for reg, cor in CORES_REG.items():
        s = f_uf[f_uf["regiao"] == reg]
        if s.empty:
            continue
        fig_sc.add_trace(go.Scatter(
            x=s["tempo_medio_entrega"], y=s["receita_total"],
            mode="markers+text", name=reg,
            text=s["customer_state"], textposition="top center",
            textfont=dict(size=9, color="#555"),
            marker=dict(
                size=s["qtd_pedidos"] / f_uf["qtd_pedidos"].max() * 45 + 8,
                color=cor, opacity=.75, line=dict(width=1, color="white"),
            ),
            hovertemplate="%{text}: %{x:.1f}d · R$ %{y:,.0f}<extra></extra>",
        ))
    if len(f_uf) >= 2:
        xs, ys = f_uf["tempo_medio_entrega"].values, f_uf["receita_total"].values
        cs = np.polyfit(xs, ys, 1)
        xl = np.linspace(xs.min(), xs.max(), 50)
        fig_sc.add_trace(go.Scatter(x=xl, y=np.polyval(cs, xl), mode="lines", showlegend=False,
                                    line=dict(color="#bbb", width=1.5, dash="dot")))
    fig_sc.update_layout(**PB, height=480, hovermode="closest",
                         legend=dict(orientation="h", y=1.05),
                         xaxis=dict(title="Tempo Médio (dias)", gridcolor=GRID),
                         yaxis=dict(title="Receita (R$)", tickformat=",.0f", gridcolor=GRID))
    st.plotly_chart(fig_sc, key="sc1", theme=None)

# ════════════════════════════════════════════════════════════════════════
# TAB 2 — TEMPORAL
# ════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("**Evolução Mensal de Pedidos**")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=f_m["ano_mes"], y=f_m["qtd_pedidos"],
        mode="lines+markers", name="Pedidos",
        line=dict(color=CIANO, width=2.5), marker=dict(size=5),
        fill="tozeroy", fillcolor="rgba(92,201,221,0.07)",
    ))
    if len(f_m) >= 2:
        fxi = np.arange(len(f_m), dtype=float)
        fyi = f_m["qtd_pedidos"].values.astype(float)
        ftc = np.polyfit(fxi, fyi, 1)
        fyt = np.polyval(ftc, fxi)
        fig1.add_trace(go.Scatter(
            x=f_m["ano_mes"], y=fyt,
            mode="lines", name=f"Tendência (+{ftc[0]:.0f}/mês)",
            line=dict(color=LARANJA, width=2, dash="dash"),
        ))
    fig1.update_layout(**PB, height=420, hovermode="x unified",
                       legend=dict(orientation="h", y=1.05),
                       xaxis=dict(type="category", tickangle=-45, dtick=3, gridcolor=GRID),
                       yaxis=dict(gridcolor=GRID))
    st.plotly_chart(fig1, key="evol", theme=None)
    st.markdown(
        f'<div class="fi">De <strong>{int(df_m.iloc[0]["qtd_pedidos"]):,}</strong> '
        f'({df_m.iloc[0]["ano_mes"]}) para <strong>{PVAL:,}</strong> ({PMES}). '
        f'Tendência: <strong>+{tc[0]:.0f}/mês</strong>. Desaceleração nos meses finais.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown("**Evolução por Região**")
    fig4 = go.Figure()
    for reg in ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]:
        s = f_rg[f_rg["regiao"] == reg]
        if s.empty:
            continue
        fig4.add_trace(go.Scatter(
            x=s["ano_mes"], y=s["qtd_pedidos"],
            mode="lines+markers", name=reg,
            line=dict(color=CORES_REG[reg], width=2), marker=dict(size=3),
        ))
    fig4.update_layout(**PB, height=400, hovermode="x unified",
                       legend=dict(orientation="h", y=1.08, font=dict(size=10)),
                       xaxis=dict(type="category", tickangle=-45, dtick=4, gridcolor=GRID),
                       yaxis=dict(gridcolor=GRID))
    st.plotly_chart(fig4, key="reg", theme=None)
    st.markdown(
        f'<div class="fi">Sudeste: <strong>{SE_P:.0f}%</strong> ({TR.get("Sudeste",0):.0f}d). '
        f'Norte: &lt;2% ({TR.get("Norte",0):.0f}d). Gap cresce ao longo do tempo.</div>',
        unsafe_allow_html=True,
    )

# ════════════════════════════════════════════════════════════════════════
# TAB 3 — GEOGRAFIA
# ════════════════════════════════════════════════════════════════════════
with tab3:
    c1, c2 = st.columns([3, 2])

    with c1:
        st.markdown("**Receita por Estado**")
        uf_s = f_uf.sort_values("receita_total", ascending=True)
        cores_h = [CIANO if u in {"SP","RJ","MG"} else "#c8d0d8" for u in uf_s["customer_state"]]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=uf_s["receita_total"], y=uf_s["customer_state"],
            orientation="h", marker_color=cores_h,
            hovertemplate="%{y}: R$ %{x:,.0f}<extra></extra>",
        ))
        fig2.update_layout(**PB, height=600,
                           xaxis=dict(tickformat=",.0f", gridcolor=GRID),
                           yaxis=dict(showgrid=False, tickfont=dict(size=10)))
        st.plotly_chart(fig2, key="uf", theme=None)
        st.markdown(
            f'<div class="fi"><strong>SP</strong> ({top3.iloc[0]["receita_total"]/1e6:.1f}M) + '
            f'<strong>RJ</strong> ({top3.iloc[1]["receita_total"]/1e6:.1f}M) + '
            f'<strong>MG</strong> ({top3.iloc[2]["receita_total"]/1e6:.1f}M) = '
            f'<strong>{T3P:.1f}%</strong></div>',
            unsafe_allow_html=True,
        )

    with c2:
        f_mu = f_uf["tempo_medio_entrega"].median() if len(f_uf) > 0 else mu
        f_TKR = f_uf.loc[f_uf["tempo_medio_entrega"] < f_mu, "ticket_medio"].mean() if len(f_uf) > 0 else 0
        f_TKL = f_uf.loc[f_uf["tempo_medio_entrega"] >= f_mu, "ticket_medio"].mean() if len(f_uf) > 0 else 0
        f_TKD = ((f_TKR - f_TKL) / f_TKL) * 100 if f_TKL > 0 else 0

        st.markdown("**Ticket Médio: Rápida vs Lenta**")
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(
            x=[f"Rápida (< {f_mu:.0f}d)", f"Lenta (≥ {f_mu:.0f}d)"],
            y=[f_TKR, f_TKL],
            marker_color=[CIANO, LARANJA],
            text=[f"R$ {f_TKR:.2f}", f"R$ {f_TKL:.2f}"],
            textposition="outside", textfont=dict(size=13, color="#222"),
            width=0.5,
        ))
        fig5.update_layout(**PB, height=350, showlegend=False,
                           yaxis=dict(gridcolor=GRID,
                                      range=[0, max(f_TKR, f_TKL, 1) * 1.3]))
        st.plotly_chart(fig5, key="tk", theme=None)
        st.markdown(
            f'<div class="fi">Rápida: <strong>R$ {f_TKR:.2f}</strong> · '
            f'Lenta: <strong>R$ {f_TKL:.2f}</strong> ({f_TKD:+.1f}%)</div>',
            unsafe_allow_html=True,
        )

        st.markdown("")
        st.markdown("**Tempo Médio por Região**")
        f_TR = f_uf.groupby("regiao")["tempo_medio_entrega"].mean()
        tr_df = f_TR.reset_index()
        tr_df.columns = ["regiao", "dias"]
        tr_df = tr_df.sort_values("dias")
        fig_tr = go.Figure()
        fig_tr.add_trace(go.Bar(
            x=tr_df["dias"], y=tr_df["regiao"], orientation="h",
            marker_color=[CORES_REG.get(r, CINZA_AZ) for r in tr_df["regiao"]],
            text=[f"{d:.1f}d" for d in tr_df["dias"]],
            textposition="outside", textfont=dict(size=11, color="#222"),
        ))
        fig_tr.update_layout(**PB, height=230, showlegend=False,
                             xaxis=dict(title="Dias", gridcolor=GRID),
                             yaxis=dict(showgrid=False))
        st.plotly_chart(fig_tr, key="tr", theme=None)

# ════════════════════════════════════════════════════════════════════════
# TAB 4 — RECOMENDAÇÕES
# ════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("**Síntese dos Achados**")
    for a, e in [
        ("Crescimento com desaceleração", f"{int(df_m.iloc[0]['qtd_pedidos']):,} → {PVAL:,} · +{tc[0]:.0f}/mês"),
        ("Receita concentrada", f"SP+RJ+MG = {T3P:.1f}% de R$ {REC/1e6:.2f}M"),
        ("Logística impacta receita", f"Pearson r = {corr:.3f} · p < 0,001"),
        ("Sudeste domina", f"{SE_P:.0f}% dos pedidos · {TR.get('Sudeste',0):.0f}d entrega"),
        ("Ticket varia", f"Rápida R$ {TKR:.2f} vs Lenta R$ {TKL:.2f} ({TKD:+.1f}%)"),
    ]:
        st.markdown(f'<div class="fi"><strong>{a}</strong> — {e}</div>', unsafe_allow_html=True)

    st.markdown("")
    st.markdown(f"""
    <div class="rec">
        <h4>Recomendação para o Investidor</h4>
        <p>
            A demanda cresceu expressivamente, mas a capacidade logística não acompanhou.
            A correlação negativa (<strong>r = {corr:.3f}</strong>) mostra que estados fora
            do eixo SP–RJ–MG possuem potencial subexplorado.
            <strong>Investir em centros de distribuição regionais</strong> (Nordeste e Norte),
            incentivo a sellers com SLA rápido e otimização de rotas é a maior alavanca
            de crescimento.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("**Limitações**")
    for l in [
        "Correlação ≠ causalidade — parte do efeito é geografia, não só eficiência.",
        "payment_value inclui frete — ticket maior em regiões distantes pelo custo logístico.",
        "Dados de 2016–2018 — comportamento pode ter mudado.",
        "Análise por UF do cliente, não do seller.",
    ]:
        st.markdown(f'<div class="fi">{l}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Insight 1 — Logística & Receita · POSTECH DTAT Fase 1 · Olist 2016–2018")
