import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# --- Dados ---
periodos = ["Jan-Jul/2025", "Ago-Dez/2025", "Jan-Mar/2026", "Abril/2026", "Mai-Dez/2026"]
custo_total = [73.5, 77.5, 66.5, 49.5, 51.0]

periodos_run_rate = ["Jan-Jul/2025", "Ago-Dez/2025", "Atual\n(Mai-Dez/2026)"]
run_rate = [40.5, 44.5, 34.5]

comparacoes = ["vs Jan-Jul/2025", "vs Ago-Dez/2025"]
economia_mensal = [22.5, 26.5]
reducao_pct = [30.6, 34.2]

# --- Paleta de cores ---
COR_PRIMARIA   = "#1a3a5c"   # azul escuro
COR_DESTAQUE   = "#e63946"   # vermelho
COR_POSITIVO   = "#2dc653"   # verde
COR_NEUTRO     = "#457b9d"   # azul médio
COR_CLARO      = "#a8dadc"   # azul claro
COR_FUNDO      = "#f8f9fa"
COR_LINHA      = "#dee2e6"

def cor_barra(val, lista):
    """Retorna cor mais escura para o valor máximo."""
    return [COR_DESTAQUE if v == max(lista) else COR_NEUTRO for v in lista]

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Custo Mensal por Período (R$ mil)",
        "Run Rate Mensal – Estrutura (R$ mil)",
        "Economia Mensal vs. Mai-Dez/2026 (R$ mil)",
        "Redução Percentual vs. Mai-Dez/2026 (%)",
    ),
    vertical_spacing=0.18,
    horizontal_spacing=0.12,
)

# ── 1. Evolução custo total ──────────────────────────────────────────────────
cores_total = [COR_DESTAQUE if v == max(custo_total) else COR_NEUTRO for v in custo_total]
cores_total[-1] = COR_POSITIVO  # último período em verde (menor custo futuro)

fig.add_trace(
    go.Bar(
        x=periodos,
        y=custo_total,
        marker_color=cores_total,
        text=[f"R$ {v} mil" for v in custo_total],
        textposition="outside",
        textfont=dict(size=11, color=COR_PRIMARIA),
        name="Custo Total",
        showlegend=False,
    ),
    row=1, col=1,
)

# Linha de tendência
fig.add_trace(
    go.Scatter(
        x=periodos,
        y=custo_total,
        mode="lines+markers",
        line=dict(color=COR_PRIMARIA, width=2, dash="dot"),
        marker=dict(size=8, color=COR_PRIMARIA),
        name="Tendência",
        showlegend=False,
    ),
    row=1, col=1,
)

# ── 2. Run rate ──────────────────────────────────────────────────────────────
cores_rr = [COR_NEUTRO, COR_NEUTRO, COR_POSITIVO]

fig.add_trace(
    go.Bar(
        x=periodos_run_rate,
        y=run_rate,
        marker_color=cores_rr,
        text=[f"R$ {v} mil" for v in run_rate],
        textposition="outside",
        textfont=dict(size=11, color=COR_PRIMARIA),
        name="Run Rate",
        showlegend=False,
    ),
    row=1, col=2,
)

# ── 3. Economia mensal absoluta ──────────────────────────────────────────────
fig.add_trace(
    go.Bar(
        x=comparacoes,
        y=economia_mensal,
        marker_color=[COR_POSITIVO, COR_POSITIVO],
        text=[f"R$ {v} mil/mês" for v in economia_mensal],
        textposition="outside",
        textfont=dict(size=11, color=COR_PRIMARIA),
        name="Economia",
        showlegend=False,
    ),
    row=2, col=1,
)

# ── 4. Redução percentual ────────────────────────────────────────────────────
fig.add_trace(
    go.Bar(
        x=comparacoes,
        y=reducao_pct,
        marker_color=[COR_CLARO, COR_POSITIVO],
        text=[f"{v}%" for v in reducao_pct],
        textposition="outside",
        textfont=dict(size=12, color=COR_PRIMARIA, family="Arial Black"),
        name="Redução %",
        showlegend=False,
    ),
    row=2, col=2,
)

# ── Layout geral ─────────────────────────────────────────────────────────────
fig.update_layout(
    title=dict(
        text=(
            "<b>Visão Executiva – Custos com Pessoas da Área</b><br>"
            "<span style='font-size:13px;color:#457b9d'>"
            "Evolução Jan/2025 → Mai-Dez/2026 | Redução de R$ 26,5 mil/mês (−34,2% vs. Ago-Dez/2025)"
            "</span>"
        ),
        x=0.5,
        xanchor="center",
        font=dict(size=20, color=COR_PRIMARIA, family="Arial"),
    ),
    paper_bgcolor=COR_FUNDO,
    plot_bgcolor="white",
    height=720,
    width=1200,
    margin=dict(t=130, b=60, l=60, r=60),
    font=dict(family="Arial", size=12, color="#333"),
)

# Ajustes de eixos
for row, col in [(1,1),(1,2),(2,1),(2,2)]:
    fig.update_xaxes(
        showgrid=False,
        tickfont=dict(size=10),
        row=row, col=col,
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=COR_LINHA,
        zeroline=False,
        tickfont=dict(size=10),
        row=row, col=col,
    )

# Títulos dos subplots em negrito
for ann in fig.layout.annotations:
    ann.font = dict(size=13, color=COR_PRIMARIA, family="Arial Black")

# ── Anotação de insight estratégico ─────────────────────────────────────────
fig.add_annotation(
    xref="paper", yref="paper",
    x=0.5, y=-0.09,
    text=(
        "<b>Leitura estratégica:</b> Mesmo com o aumento da remuneração da Malu (+R$ 1,5 mil), "
        "a área saiu de R$ 77,5 mil/mês (Ago-Dez/2025) para <b>R$ 51 mil/mês</b> em 2026 — "
        "<b>economia anualizada de R$ 318 mil</b>, mantendo liderança e capacidade operacional."
    ),
    showarrow=False,
    font=dict(size=11, color="#555"),
    align="center",
    bgcolor="#e9f5ff",
    bordercolor=COR_NEUTRO,
    borderwidth=1,
    borderpad=8,
)

fig.write_html("custos_pessoas.html")
print("Arquivo gerado: custos_pessoas.html")
