import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from market_analysis_crew import MarketAnalysisCrew, LLM_PROVIDERS, get_available_providers
from datetime import datetime
import json
from typing import Any

st.set_page_config(
    page_title="AI Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

INVESTMENT_TERMS = {
    "RSI": "Relative Strength Index - A momentum indicator that measures the magnitude of recent price changes to evaluate overbought or oversold conditions.",
    "MACD": "Moving Average Convergence Divergence - A trend-following momentum indicator that shows the relationship between two moving averages of a security's price.",
    "Moving Average": "A calculation used to analyze data points by creating a series of averages of different subsets of the full data set.",
    "Volume Profile": "A visualization of trading activity over a specified period that shows the price levels where the most trading activity occurred.",
    "Beta": "A measure of a stock's volatility in relation to the overall market.",
    "Value at Risk (VaR)": "A statistical measure of the potential loss in value of a portfolio over a defined period.",
    "Sharpe Ratio": "A measure that indicates the average return minus the risk-free return divided by the standard deviation of return on an investment.",
    "DCF Valuation": "Discounted Cash Flow - A valuation method that estimates the value of an investment based on its expected future cash flows.",
    "P/E Ratio": "Price-to-Earnings Ratio - A valuation measure that compares a company's stock price to its earnings per share.",
    "Market Cap": "The total value of a company's shares of stock, calculated by multiplying the price of a stock by its total number of outstanding shares.",
    "Economic Moat": "A company's competitive advantage that allows it to maintain profitability and market share over time.",
    "ESG": "Environmental, Social, and Governance - A set of standards for a company's operations that socially conscious investors use to screen potential investments."
}

# ---------------------------------------------------------------------------
# Styling — uses Streamlit's own theme variables so it looks right in both
# light and dark mode, instead of hardcoding white/light colors.
# ---------------------------------------------------------------------------
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        .app-header {
            background: linear-gradient(90deg, #1f77b4 0%, #4facfe 100%);
            padding: 1.6rem 2rem;
            border-radius: 14px;
            margin-bottom: 1.5rem;
        }
        .app-header h1 {
            color: white;
            margin: 0;
            font-size: 1.8rem;
        }
        .app-header p {
            color: rgba(255,255,255,0.85);
            margin: 0.25rem 0 0 0;
            font-size: 0.95rem;
        }

        .term-tooltip {
            text-decoration: underline dotted;
            cursor: help;
        }

        .agent-message {
            padding: 12px 16px;
            margin: 8px 0;
            border-radius: 10px;
            border-left: 4px solid #1f77b4;
            background-color: rgba(31, 119, 180, 0.07);
        }
        .agent-name {
            font-weight: 600;
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
        }
        .agent-timestamp {
            font-size: 0.75em;
            opacity: 0.6;
        }
        .agent-thinking {
            font-style: italic;
            opacity: 0.75;
        }
        .agent-result {
            margin-top: 8px;
            padding: 10px;
            border-radius: 6px;
            background-color: rgba(127, 127, 127, 0.08);
        }

        .glossary-card {
            padding: 10px 14px;
            border-radius: 8px;
            margin-bottom: 10px;
            background-color: rgba(127, 127, 127, 0.08);
        }

        .risk-pill {
            display: inline-block;
            padding: 4px 14px;
            border-radius: 999px;
            font-weight: 700;
            font-size: 0.85rem;
        }
    </style>
""", unsafe_allow_html=True)


def format_json_output(data: dict) -> str:
    return json.dumps(data, indent=2)


def add_tooltips_to_text(text: str) -> str:
    for term, definition in INVESTMENT_TERMS.items():
        if term in text:
            text = text.replace(term, f'<span class="term-tooltip" title="{definition}">{term}</span>')
    return text


def create_candlestick_chart(stock_data):
    dates = pd.to_datetime(stock_data["dates"])
    prices = stock_data["price_history"]
    volumes = stock_data["volume_history"]

    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        vertical_spacing=0.03, subplot_titles=('Price', 'Volume'),
        row_heights=[0.7, 0.3]
    )

    fig.add_trace(go.Scatter(
        x=dates, y=prices, mode='lines', name='Price',
        line=dict(color='#1f77b4', width=2)
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=dates, y=volumes, name='Volume', marker_color='#2ca02c'
    ), row=2, col=1)

    ma_data = stock_data["technical_indicators"]["moving_averages"]
    for ma_name, ma_values in ma_data.items():
        fig.add_trace(go.Scatter(
            x=dates, y=ma_values, name=ma_name, line=dict(dash='dash', width=1.3)
        ), row=1, col=1)

    fig.update_layout(
        height=650,
        showlegend=True,
        margin=dict(l=10, r=10, t=40, b=10),
        template="plotly_dark",
        xaxis_rangeslider_visible=False
    )
    return fig


def create_technical_indicators_chart(stock_data):
    dates = pd.to_datetime(stock_data["dates"])

    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        vertical_spacing=0.06, subplot_titles=('RSI', 'MACD')
    )

    rsi_values = stock_data["technical_indicators"]["rsi"]
    fig.add_trace(go.Scatter(
        x=dates, y=rsi_values, name='RSI', line=dict(color='#1f77b4')
    ), row=1, col=1)

    macd_data = stock_data["technical_indicators"]["macd"]
    fig.add_trace(go.Scatter(
        x=dates, y=macd_data["macd"], name='MACD', line=dict(color='#1f77b4')
    ), row=2, col=1)
    fig.add_trace(go.Scatter(
        x=dates, y=macd_data["signal"], name='Signal', line=dict(color='#ff7f0e')
    ), row=2, col=1)

    fig.add_hline(y=70, line_dash="dash", line_color="red", row=1, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=1, col=1)

    fig.update_layout(
        height=550,
        showlegend=True,
        margin=dict(l=10, r=10, t=40, b=10),
        template="plotly_dark"
    )
    return fig


def display_metrics_dashboard(metrics):
    cols = st.columns(3)
    sections = [
        ("📈 Profitability", metrics.get("profitability", {}), True),
        ("💰 Valuation", metrics.get("valuation", {}), False),
        ("🚀 Growth", metrics.get("growth", {}), True),
    ]
    for col, (title, data, is_pct) in zip(cols, sections):
        with col:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                for key, value in data.items():
                    if value is not None:
                        st.metric(
                            label=key.replace('_', ' ').title(),
                            value=f"{value:.2%}" if is_pct and isinstance(value, float) else (
                                f"{value:.2f}" if isinstance(value, float) else value
                            )
                        )


def display_risk_metrics(risk_metrics):
    st.markdown("### 🎯 Risk Analysis")
    with st.container(border=True):
        cols = st.columns(4)

        with cols[0]:
            volatility = risk_metrics.get("volatility")
            if volatility:
                st.metric("Annualized Volatility", f"{volatility:.2%}")

        with cols[1]:
            var = risk_metrics.get("value_at_risk")
            if var:
                st.metric("Daily VaR (95%)", f"{var:.2%}")

        with cols[2]:
            sharpe = risk_metrics.get("sharpe_ratio")
            if sharpe:
                st.metric("Sharpe Ratio", f"{sharpe:.2f}")

        with cols[3]:
            risk_level = risk_metrics.get("risk_assessment", "").upper()
            if risk_level:
                color = {"LOW": "#2ca02c", "MEDIUM": "#ff9f1c", "HIGH": "#e63946"}.get(risk_level, "#888")
                st.markdown(
                    f"<div style='text-align:center;'>"
                    f"<div style='opacity:0.7; font-size:0.85rem; margin-bottom:4px;'>Risk Level</div>"
                    f"<span class='risk-pill' style='background-color:{color}22; color:{color};'>{risk_level}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )


def display_educational_page():
    st.markdown("## 📚 Investment Terms Glossary")
    st.markdown(
        "Understanding financial terms is crucial for making informed investment decisions. "
        "Here's a glossary of the terms used throughout this analysis."
    )
    cols = st.columns(3)
    terms = list(INVESTMENT_TERMS.items())
    terms_per_col = len(terms) // 3 + (len(terms) % 3 > 0)

    for i, col in enumerate(cols):
        with col:
            start_idx = i * terms_per_col
            end_idx = min((i + 1) * terms_per_col, len(terms))
            for term, definition in terms[start_idx:end_idx]:
                st.markdown(
                    f"<div class='glossary-card'><strong>{term}</strong><br><small>{definition}</small></div>",
                    unsafe_allow_html=True
                )


def format_timestamp(timestamp: str) -> str:
    dt = datetime.fromisoformat(timestamp)
    return dt.strftime("%I:%M:%S %p")


def display_agent_message(agent_name: str, message: str, timestamp: str = None, status: str = "progress", result: Any = None):
    timestamp_str = format_timestamp(timestamp) if timestamp else datetime.now().strftime("%I:%M:%S %p")
    st.markdown(f"""
        <div class="agent-message">
            <div class="agent-name">
                <span>{agent_name}</span>
                <span class="agent-timestamp">{timestamp_str}</span>
            </div>
            <div class="{'agent-thinking' if status == 'progress' else ''}">{message}</div>
            {f'<div class="agent-result">{result}</div>' if result else ''}
        </div>
    """, unsafe_allow_html=True)


def display_agent_log():
    """Show the full log of agent messages collected during the run."""
    if st.session_state.get('agent_messages'):
        with st.expander("🧠 Agent activity log", expanded=False):
            for msg in st.session_state.agent_messages:
                display_agent_message(
                    agent_name=msg["agent"],
                    message=msg["message"],
                    timestamp=msg["timestamp"],
                    status=msg["status"],
                    result=msg["result"] if msg["status"] == "complete" else None
                )


def display_ai_analysis(results: dict):
    if not results:
        return

    if isinstance(results, dict) and "raw_analysis" in results:
        st.markdown(add_tooltips_to_text(results["raw_analysis"]), unsafe_allow_html=True)
        return

    analysis_mapping = {
        "market_research": "🔎 Market Research",
        "technical_analysis": "📊 Technical Analysis",
        "fundamental_analysis": "🧾 Fundamental Analysis",
        "risk_analysis": "⚠️ Risk Analysis",
        "investment_strategy": "🎯 Investment Strategy"
    }

    for key, content in results.items():
        if key == "risk_metrics":
            continue

        display_name = analysis_mapping.get(key, key.replace('_', ' ').title())
        with st.expander(display_name, expanded=(key == "investment_strategy")):
            if isinstance(content, dict):
                formatted_content = format_json_output(content)
                st.markdown(f"```json\n{formatted_content}\n```")

                if key == "investment_strategy":
                    st.markdown("**Key points to look for:**")
                    st.markdown("- **Investment Thesis** — the core reasoning behind the recommendation")
                    st.markdown("- **Position Strategy** — sizing and portfolio allocation guidance")
                    st.markdown("- **Execution Plan** — entry/exit points and timing")
                    st.markdown("- **Risk Management** — position limits and monitoring")
            else:
                st.markdown(add_tooltips_to_text(str(content)), unsafe_allow_html=True)


def run_analysis(ticker: str, selected_model: str):
    """Run the crew analysis with a clean, real progress display."""
    steps = [
        "Gathering market data",
        "Running market intelligence research",
        "Running technical analysis",
        "Running fundamental analysis",
        "Assessing risk",
        "Building final investment strategy",
    ]

    with st.status("Running multi-agent analysis...", expanded=True) as status_box:
        crew = MarketAnalysisCrew(model_provider=selected_model)

        status_box.write(f"Step 1/{len(steps)}: {steps[0]}")
        analysis_results = crew.analyze_stock(ticker)

        if isinstance(analysis_results, dict) and "error" in analysis_results:
            status_box.update(label="Analysis failed", state="error")
            reason = analysis_results.get("reason", "unknown")
            if reason == "missing_api_key":
                st.error("🔑 **API Key Missing** — set your API key as an environment variable.")
                st.code("export GOOGLE_API_KEY=your_api_key_here")
                st.info("Get a free key from [Google AI Studio](https://makersuite.google.com/app/apikey)")
            elif reason == "configuration_error":
                st.error("⚙️ **Configuration Error**\n\n" + analysis_results["error"])
            else:
                st.error("❌ **Analysis Failed**\n\n" + analysis_results["error"])
            return

        status_box.write("Fetching stock data snapshot...")
        stock_data_raw = crew.tools["stock_data"]._run(ticker)
        stock_data = json.loads(stock_data_raw) if isinstance(stock_data_raw, str) else stock_data_raw
        if isinstance(stock_data, dict) and stock_data.get("error"):
            status_box.update(label="Analysis failed", state="error")
            st.error(stock_data["error"])
            return

        status_box.write("Fetching financial metrics...")
        financial_metrics_raw = crew.tools["financial_metrics"]._run(ticker)
        financial_metrics = json.loads(financial_metrics_raw) if isinstance(financial_metrics_raw, str) else financial_metrics_raw
        if isinstance(financial_metrics, dict) and financial_metrics.get("error"):
            status_box.update(label="Analysis failed", state="error")
            st.error(financial_metrics["error"])
            return

        # Pull the full agent message log for the activity expander
        st.session_state.agent_messages = crew.get_agent_messages()

        st.session_state.analysis_results = analysis_results
        st.session_state.stock_data = stock_data
        st.session_state.financial_metrics = financial_metrics
        st.session_state.analyzed_ticker = ticker

        status_box.update(label=f"Analysis complete for {ticker}", state="complete", expanded=False)


def main():
    with st.sidebar:
        st.markdown("### 📈 Navigation")
        page = st.radio("Go to:", ["Dashboard", "Educational Resources"], label_visibility="collapsed")
        st.markdown("---")

        st.markdown("### ⚙️ Stock Analysis Settings")
        ticker = st.text_input("Stock Ticker", value="AAPL").upper()

        st.markdown("##### AI Model")
        available_providers = get_available_providers()

        if not available_providers:
            st.warning("⚠️ No LLM providers configured")
            with st.expander("Quick setup"):
                st.markdown("""
1. Copy `.env.example` to `.env`
2. Add your API key to `.env`
3. Restart the app

**Free options:**
- [OpenAI](https://platform.openai.com/signup) — $5 free credit
- [Anthropic](https://console.anthropic.com/) — free tier
- [Google AI](https://makersuite.google.com/app/apikey) — free API key
- [Ollama](https://ollama.ai/) — free local models
                """)

        provider_options = []
        model_options = {}
        for provider in available_providers:
            provider_config = LLM_PROVIDERS[provider]
            for model in provider_config["models"]:
                display_name = f"{provider.upper()} - {model}"
                provider_options.append(display_name)
                model_options[display_name] = f"{provider}/{model}"

        selected_model = None
        if provider_options:
            selected_display = st.selectbox("Select model", provider_options, index=0, label_visibility="collapsed")
            selected_model = model_options[selected_display]
            st.caption(f"🤖 Using {selected_model.split('/')[0].upper()}")

        st.markdown("##### Time Period")
        time_period = st.select_slider(
            "Time Period",
            options=["1mo", "3mo", "6mo", "1y"],
            value="1y",
            label_visibility="collapsed"
        )
        st.caption("📅 Sets the historical window used for trends, moving averages, and volatility.")

        st.markdown("---")
        analyze_clicked = st.button("🚀 Analyze Stock", type="primary", use_container_width=True)

        if analyze_clicked:
            if not available_providers:
                st.error("No LLM providers available — configure an API key in `.env` first.")
            else:
                try:
                    run_analysis(ticker, selected_model)
                except ValueError as e:
                    if "api key" in str(e).lower():
                        st.error("🔑 **API Key Missing**")
                        st.code("export GOOGLE_API_KEY=your_api_key_here")
                    else:
                        st.error(f"⚙️ Configuration Error: {e}")
                except Exception as e:
                    st.error(f"❌ Unexpected Error: {e}")

    if page == "Educational Resources":
        display_educational_page()
        return

    st.markdown(
        """
        <div class="app-header">
            <h1>📈 AI Stock Analysis Dashboard</h1>
            <p>Multi-agent research, technical, fundamental, and risk analysis — powered by CrewAI</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if 'analysis_results' in st.session_state:
        stock_data = st.session_state.stock_data
        ticker_label = st.session_state.get('analyzed_ticker', '')

        st.subheader(f"Overview — {ticker_label}")
        with st.container(border=True):
            cols = st.columns(4)
            cols[0].metric("Current Price", f"${stock_data['current_price']:.2f}")
            cols[1].metric("Market Cap", f"${stock_data['market_cap']:,.0f}")
            cols[2].metric("52-Week High", f"${stock_data['52_week_high']:.2f}")
            cols[3].metric("52-Week Low", f"${stock_data['52_week_low']:.2f}")

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Price", "📊 Technical", "💵 Financials", "🎯 Risk", "🤖 AI Insights"
        ])

        with tab1:
            st.plotly_chart(create_candlestick_chart(stock_data), use_container_width=True)

        with tab2:
            st.plotly_chart(create_technical_indicators_chart(stock_data), use_container_width=True)

        with tab3:
            display_metrics_dashboard(st.session_state.financial_metrics)

        with tab4:
            display_risk_metrics(st.session_state.analysis_results.get("risk_metrics", {}))

        with tab5:
            display_ai_analysis(st.session_state.analysis_results)
            display_agent_log()
    else:
        st.info("👈 Enter a stock ticker in the sidebar and click **Analyze Stock** to begin.")


if __name__ == "__main__":
    main()