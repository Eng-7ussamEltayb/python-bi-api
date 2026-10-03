#!/usr/bin/env python3
from __future__ import annotations

from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)
DF = pd.read_csv("data/kpis.csv")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/kpis")
def kpis():
    region = request.args.get("region")
    df = DF.copy()
    if region:
        df = df[df["region"].str.lower() == region.lower()]
    payload = {
        "revenue_total": float(df["revenue"].sum()),
        "work_orders_closed": int(df["work_orders_closed"].sum()),
        "mttr_avg": float(df["mttr_hours"].mean()) if len(df) else 0,
        "rows": df.to_dict(orient="records"),
    }
    return jsonify(payload)


@app.get("/api/kpis/by-region")
def by_region():
    grouped = (
        DF.groupby("region", as_index=False)
        .agg(revenue=("revenue", "sum"), wo=("work_orders_closed", "sum"), mttr=("mttr_hours", "mean"))
        .to_dict(orient="records")
    )
    return jsonify({"data": grouped})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
