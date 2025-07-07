import streamlit as st
import polars as pl
import altair as alt
import math

st.set_page_config(
    page_title="Hawkmoth vs Butterfly Effect", layout="centered")

st.title("🦋 Hawkmoth vs Butterfly Effect Demonstrator")
st.markdown("""
This app shows how:
- **Hawkmoth Effect** = small structural model error → large divergence
- **Butterfly Effect** = small change in initial conditions → large divergence
""")

# Copyright and link
st.markdown("""
© 2024 Jens Laufer | [Solytics.de](https://www.solytics.de/)
""")

# --- Sidebar ---
st.sidebar.header("Model Parameters")
r = st.sidebar.slider("Growth rate (r)", 2.5, 4.0, 3.7, 0.01)
x0 = st.sidebar.slider("Initial value (x₀)", 0.0, 1.0, 0.2, 0.01)
steps = st.sidebar.slider("Steps", 10, 200, 100, 10)

st.sidebar.header("Hawkmoth Settings")
epsilon = st.sidebar.slider("Structural error (ε)", 0.0, 0.1, 0.01, 0.001)

st.sidebar.header("Butterfly Settings")
delta = st.sidebar.slider(
    "Initial condition error (δ)", 0.0, 0.1, 0.001, 0.001)

st.sidebar.header("Noise Settings")
noise_on = st.sidebar.checkbox("Add noise?", value=False)
noise_level = st.sidebar.slider(
    "Noise std dev", 0.0, 0.1, 0.01, 0.001) if noise_on else 0.0

# --- Models ---


def true_model(x, r):
    return r * x * (1 - x)


def approx_model(x, r, epsilon):
    return r * x * (1 - x + epsilon * math.sin(math.pi * x))


def simulate(model_func, x0, r, epsilon=0.0, noise=0.0, steps=50):
    import random
    x = [x0]
    for _ in range(steps):
        last = x[-1]
        next_val = (
            model_func(last, r)
            if epsilon == 0 else
            model_func(last, r, epsilon)
        )
        if noise > 0:
            next_val += random.gauss(0, noise)
        next_val = max(0, min(next_val, 1))
        x.append(next_val)
    return x


# --- Tabs for Comparison ---
tab1, tab2 = st.tabs(["🪰 Hawkmoth Effect", "🦋 Butterfly Effect"])

with tab1:
    st.subheader("Hawkmoth Effect (same initial, different model)")
    x_true = simulate(true_model, x0, r, noise=noise_level, steps=steps)
    x_approx = simulate(approx_model, x0, r, epsilon=epsilon,
                        noise=noise_level, steps=steps)

    # Create dataframe for time series
    df_hawkmoth = pl.DataFrame({
        'Time Step': list(range(len(x_true))) + list(range(len(x_approx))),
        'x': x_true + x_approx,
        'Model': ['True Model'] * len(x_true) + [f'Approx Model (ε={epsilon})'] * len(x_approx)
    })

    chart1 = alt.Chart(df_hawkmoth).mark_line(strokeWidth=2).encode(
        x=alt.X('Time Step:O', title='Time Step'),
        y=alt.Y('x:Q', title='x'),
        color=alt.Color('Model:N',
                        scale=alt.Scale(range=['#2E86AB', '#F24236']),
                        legend=alt.Legend(title="Model")),
        strokeDash=alt.StrokeDash(
            'Model:N', scale=alt.Scale(range=[[1, 0], [5, 5]]))
    ).properties(
        width=600,
        height=400,
        title="Hawkmoth Effect"
    )

    st.altair_chart(chart1, use_container_width=True)

    # Divergence plot
    df_div1 = pl.DataFrame({
        'Time Step': range(len(x_true)),
        'Difference': [abs(a - b) for a, b in zip(x_true, x_approx)]
    })

    chart1b = alt.Chart(df_div1).mark_line(color='red', strokeWidth=2).encode(
        x=alt.X('Time Step:O', title='Time Step'),
        y=alt.Y('Difference:Q', title='Difference')
    ).properties(
        width=600,
        height=400,
        title="Divergence |True - Approx|"
    )

    st.altair_chart(chart1b, use_container_width=True)

with tab2:
    st.subheader("Butterfly Effect (different initial, same model)")
    x_base = simulate(true_model, x0, r, noise=noise_level, steps=steps)
    x_shift = simulate(true_model, x0 + delta, r,
                       noise=noise_level, steps=steps)

    # Create dataframe for time series
    df_butterfly = pl.DataFrame({
        'Time Step': list(range(len(x_base))) + list(range(len(x_shift))),
        'x': x_base + x_shift,
        'Initial': [f'x₀ = {x0:.3f}'] * len(x_base) + [f'x₀ + δ = {x0 + delta:.3f}'] * len(x_shift)
    })

    chart2 = alt.Chart(df_butterfly).mark_line(strokeWidth=2).encode(
        x=alt.X('Time Step:O', title='Time Step'),
        y=alt.Y('x:Q', title='x'),
        color=alt.Color('Model:N',
                        scale=alt.Scale(range=['#2E86AB', '#F24236']),
                        legend=alt.Legend(title="Model")),
        strokeDash=alt.StrokeDash(
            'Initial:N', scale=alt.Scale(range=[[1, 0], [5, 5]]))
    ).properties(
        width=600,
        height=400,
        title="Butterfly Effect"
    )

    st.altair_chart(chart2, use_container_width=True)

    # Divergence plot
    df_div2 = pl.DataFrame({
        'Time Step': range(len(x_base)),
        'Difference': [abs(a - b) for a, b in zip(x_base, x_shift)]
    })

    chart2b = alt.Chart(df_div2).mark_line(color='purple', strokeWidth=2).encode(
        x=alt.X('Time Step:O', title='Time Step'),
        y=alt.Y('Difference:Q', title='Difference')
    ).properties(
        width=600,
        height=400,
        title="Divergence |x₀ - (x₀+δ)|"
    )

    st.altair_chart(chart2b, use_container_width=True)
