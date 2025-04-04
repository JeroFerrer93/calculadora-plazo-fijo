import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Función para calcular plazo fijo
def calcular_plazo_fijo(capital_inicial, tna, plazo_meses, tipo_interes="simple", reinvertir=True, aporte_mensual=0):
    tasa_mensual = tna / 12 / 100
    historial = []

    capital = capital_inicial
    intereses_acumulados = 0

    for mes in range(1, plazo_meses + 1):
        if tipo_interes == "simple":
            interes_mes = capital_inicial * tasa_mensual
            intereses_acumulados += interes_mes
            capital_total = capital_inicial + intereses_acumulados
        else:
            interes_mes = capital * tasa_mensual
            if reinvertir:
                capital += interes_mes
            else:
                intereses_acumulados += interes_mes
            capital += aporte_mensual
            capital_total = capital

        capital_aportado = capital_inicial + aporte_mensual * mes if tipo_interes == "compuesto" else capital_inicial

        historial.append({
            "Mes": mes,
            "Capital total": round(capital_total, 2),
            "Capital aportado": round(capital_aportado, 2),
            "Interés del mes": round(interes_mes, 2),
            "Aporte mensual": aporte_mensual if tipo_interes == "compuesto" else 0,
            "Intereses no reinvertidos": round(intereses_acumulados, 2) if not reinvertir or tipo_interes == "simple" else 0
        })

    return pd.DataFrame(historial)

# Streamlit UI
st.title("💸 Calculadora de Inversión a Plazo Fijo")

capital_inicial = st.number_input("💰 Capital inicial (ARS)", min_value=0.0, value=100000.0, step=1000.0)
tna = st.number_input("📈 TNA (% anual)", min_value=0.0, value=110.0, step=0.5)
plazo_meses = st.slider("📆 Plazo en meses", 1, 60, 12)

tipo_interes = st.radio("🔁 Tipo de interés", ["simple", "compuesto"])

if tipo_interes == "compuesto":
    reinvertir = st.radio("♻️ ¿Reinvertir intereses?", ["Sí", "No"]) == "Sí"
    aporte_mensual = st.number_input("➕ Aporte mensual (ARS)", min_value=0.0, value=0.0, step=1000.0)
else:
    reinvertir = False
    aporte_mensual = 0.0
    st.info("ℹ️ En interés simple no se reinvierten los intereses ni se hacen aportes.")

# Calcular
df = calcular_plazo_fijo(capital_inicial, tna, plazo_meses, tipo_interes, reinvertir, aporte_mensual)

# Mostrar resultados
st.subheader("📊 Resultados")
st.dataframe(df.style.format({"Capital total": "${:,.2f}", "Capital aportado": "${:,.2f}", "Interés del mes": "${:,.2f}"}))

# Gráfico
st.subheader("📈 Evolución del capital")
st.line_chart(df.set_index("Mes")[["Capital total", "Capital aportado"]])
