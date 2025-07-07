import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Hawkmoth vs Butterfly Effect", layout="centered")

st.title("🦋 Hawkmoth vs Butterfly Effect Demonstrator")
st.markdown("""
This app shows how:
- **Hawkmoth Effect** = small structural model error → large divergence
- **Butterfly Effect** = small change in initial conditions → large divergence
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
    return r * x * (1 - x + epsilon * np.sin(np.pi * x))


def simulate(model_func, x0, r, epsilon=0.0, noise=0.0, steps=50):
    x = [x0]
    for _ in range(steps):
        last = x[-1]
        next_val = (
            model_func(last, r)
            if epsilon == 0 else
            model_func(last, r, epsilon)
        )
        if noise > 0:
            next_val += np.random.normal(0, noise)
        next_val = np.clip(next_val, 0, 1)
        x.append(next_val)
    return x


# --- Tabs for Comparison ---
tab1, tab2 = st.tabs(["🪰 Hawkmoth Effect", "🦋 Butterfly Effect"])

with tab1:
    st.subheader("Hawkmoth Effect (same initial, different model)")
    x_true = simulate(true_model, x0, r, noise=noise_level, steps=steps)
    x_approx = simulate(approx_model, x0, r, epsilon=epsilon,
                        noise=noise_level, steps=steps)

    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(x_true, label="True Model", linewidth=2)
    ax1.plot(x_approx, label=f"Approx Model (ε={epsilon})", linestyle='--')
    ax1.set_title("Hawkmoth Effect")
    ax1.set_xlabel("Time Step")
    ax1.set_ylabel("x")
    ax1.grid(True)
    ax1.legend()
    st.pyplot(fig1)

    fig1b, ax1b = plt.subplots(figsize=(10, 2.5))
    ax1b.plot(np.abs(np.array(x_true) - np.array(x_approx)), color='red')
    ax1b.set_title("Divergence |True - Approx|")
    ax1b.set_xlabel("Time Step")
    ax1b.set_ylabel("Difference")
    ax1b.grid(True)
    st.pyplot(fig1b)

with tab2:
    st.subheader("Butterfly Effect (different initial, same model)")
    x_base = simulate(true_model, x0, r, noise=noise_level, steps=steps)
    x_shift = simulate(true_model, x0 + delta, r,
                       noise=noise_level, steps=steps)

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(x_base, label=f"x₀ = {x0:.3f}", linewidth=2)
    ax2.plot(x_shift, label=f"x₀ + δ = {x0 + delta:.3f}", linestyle='--')
    ax2.set_title("Butterfly Effect")
    ax2.set_xlabel("Time Step")
    ax2.set_ylabel("x")
    ax2.grid(True)
    ax2.legend()
    st.pyplot(fig2)

    fig2b, ax2b = plt.subplots(figsize=(10, 2.5))
    ax2b.plot(np.abs(np.array(x_base) - np.array(x_shift)), color='purple')
    ax2b.set_title("Divergence |x₀ - (x₀+δ)|")
    ax2b.set_xlabel("Time Step")
    ax2b.set_ylabel("Difference")
    ax2b.grid(True)
    st.pyplot(fig2b)
