# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Club Player Performance Analyzer",
    layout="wide"
)

st.title("⚽ Club Player Performance Dashboard")

# ---------------- Load data ----------------
@st.cache_data
def load_data():
    return pd.read_csv("club-analyzer.csv")

df = load_data()

# Create full player name
df["Player"] = df["Name"] + " " + df["Lastname"]

# Ensure numeric columns
stats_cols = ["Games Played", "Goals", "Assists", "Red Cards"]
for col in stats_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Goals per game
df["Goals per Game"] = (df["Goals"] / df["Games Played"]).replace(
    [float("inf")], 0
).round(2)

# ---------------- Controls ----------------
top_n = st.slider("Select number of top players", 5, 30, 10)

# ---------------- Tables ----------------
st.subheader("⚽ Top Goal Scorers")
top_goals = df.sort_values("Goals", ascending=False).head(top_n)
st.dataframe(
    top_goals[["Player", "Goals", "Goals per Game", "Games Played"]]
)

st.subheader("🎯 Top Assist Providers")
top_assists = df.sort_values("Assists", ascending=False).head(top_n)
st.dataframe(
    top_assists[["Player", "Assists", "Games Played"]]
)

st.subheader("🏟 Most Used Players (Games Played)")
most_used = df.sort_values("Games Played", ascending=False).head(top_n)
st.dataframe(
    most_used[["Player", "Games Played", "Goals", "Assists"]]
)

st.subheader("🟥 Most Red Cards")
top_reds = df.sort_values("Red Cards", ascending=False).head(top_n)
st.dataframe(
    top_reds[["Player", "Red Cards", "Games Played"]]
)

# ---------------- Graphs ----------------
st.subheader("📊 Graphs")

# Goals per Game graph
st.markdown("### ⚽ Goals per Game (Top Players)")
gpg_data = df[df["Games Played"] > 5].sort_values(
    "Goals per Game", ascending=False
).head(top_n)

fig1, ax1 = plt.subplots()
ax1.barh(gpg_data["Player"], gpg_data["Goals per Game"])
ax1.invert_yaxis()
ax1.set_xlabel("Goals per Game")
ax1.set_ylabel("Player")

st.pyplot(fig1)

# Most used players graph
st.markdown("### 🏟 Most Used Players")
fig2, ax2 = plt.subplots()
ax2.barh(most_used["Player"], most_used["Games Played"])
ax2.invert_yaxis()
ax2.set_xlabel("Games Played")
ax2.set_ylabel("Player")

st.pyplot(fig2)
S