# 🦋 Hawkmoth Effect Demonstrator

This interactive [Streamlit](https://streamlit.io) app demonstrates the difference between the **Hawkmoth Effect** and the **Butterfly Effect** — two phenomena that help explain why predictions in complex systems like weather, finance, or ecosystems can break down, but for very different reasons.

You can interactively explore the effects of:
- 🔧 **Structural model errors** (Hawkmoth Effect)
- 🐛 **Tiny changes in initial conditions** (Butterfly Effect)
- 🔊 **Random noise** in the model dynamics

---

## 🌪️ What Are the Effects?

### 🦋 Butterfly Effect

> *"A butterfly flapping its wings in Brazil can cause a tornado in Texas."*

Small changes in initial conditions can grow exponentially in chaotic systems — this is the **Butterfly Effect**, a key idea in chaos theory. Even if your model is perfect, starting just a bit off can eventually lead to very different outcomes.

### 🐦‍⬛ Hawkmoth Effect

> *"Even a perfect start can't save you if your model is slightly wrong."*

The **Hawkmoth Effect** highlights sensitivity to the model **itself**, not just the starting point. Even when two models look nearly identical (e.g., differing only in a tiny term), their long-term predictions can diverge dramatically. This undermines overconfidence in seemingly well-calibrated simulations.

---

## 🚀 Run Locally with Docker Compose

This project is Dockerized for easy and reproducible use.

### 📦 Requirements

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 🏁 Run appliction


```bash
   docker compose up
```
   
## 📬 Interested in Modeling, Uncertainty, or Decision Support Tools?

This demo was built by [Solytics](https://www.solytics.de), a team passionate about helping people make better decisions under uncertainty.

👉 Visit [https://www.solytics.de](https://www.solytics.de) if you're interested in:
- Custom analytics or simulation tools  
- Forecasting, risk modeling, or decision intelligence  
- Data-driven product development  

We’d love to hear from you.

