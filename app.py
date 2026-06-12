from flask import Flask, Response
import pandas as pd
import requests
import json

app = Flask(__name__)

API_URL_realisasi_bimp = "https://dashboard.mahkotagroup.com/api/dashboard/realisasi-bimp"
API_URL_analitik_bimp = "https://dashboard.mahkotagroup.com/api/dashboard/realisasi-akun-analitik-bimp"
API_URL_processing_labour_bimp = "https://dashboard.mahkotagroup.com/api/dashboard/processing-labour-bimp"
API_URL_production_bimp = "https://dashboard.mahkotagroup.com/api/dashboard/production-bimp"

@app.route("/realisasi-bimp")
def get_data_realisasi():
    responses = requests.get(API_URL_realisasi_bimp)
    result = responses.json()

    df = pd.DataFrame(result["data"])

    # Balik tanda nominal untuk Pendapatan dan Pendapatan Lain-lain
    mask_pendapatan = df["Deskripsi"].isin(["Pendapatan", "Pendapatan Lain-lain"])
    df.loc[mask_pendapatan, "Realisasi Biaya"] = df.loc[mask_pendapatan, "Realisasi Biaya"] * -1

    # Bulatkan nilai 2 angka di belakang koma
    df["Realisasi Biaya"] = df["Realisasi Biaya"].round(2)

    # Susun kolom akhir
    final_cols = [
        "Tahun", "Bulan", "Overview", "Deskripsi", "No. Akun", "Rincian Deskripsi", "Realisasi Biaya"
    ]

    df = df[final_cols].copy()
    records = df.to_dict(orient="records")

    return Response(
        json.dumps(records, ensure_ascii=False),
        mimetype="application/json"
    )

@app.route("/realisasi-akun-analitik-bimp")
def get_data_akun_analitik():
    responses = requests.get(API_URL_analitik_bimp)
    result = responses.json()

    df = pd.DataFrame(result["data"])

    # Balik tanda nominal untuk Pendapatan dan Pendapatan Lain-lain
    mask_pendapatan = df["Deskripsi"].isin(["Pendapatan", "Pendapatan Lain-lain"])
    df.loc[mask_pendapatan, "Nominal"] = df.loc[mask_pendapatan, "Nominal"] * -1

    # Bulatkan nilai 2 angka di belakang koma
    df["Nominal"] = df["Nominal"].round(2)

    # Susun kolom akhir
    final_cols = [
        "Tanggal", "Tahun", "Bulan", "Overview", "Deskripsi", "No Akun", "Nama Akun", "No Akun Analitik",
        "Nama Akun Analitik", "Kode Induk Analitik", "Kode Detail Analitik", "Tipe Unit", "Nominal"
    ]

    df = df[final_cols].copy()

    records = df.to_dict(orient="records")

    return Response(
        json.dumps(records, ensure_ascii=False),
        mimetype="application/json"
    )

@app.route("/processing-labour-bimp")
def get_data_processing_labour():
    responses = requests.get(API_URL_processing_labour_bimp)
    result = responses.json()

    df = pd.DataFrame(result["data"])

    # Bulatkan nilai 2 angka di belakang koma
    df["Realisasi Biaya"] = df["Realisasi Biaya"].round(2)

    # Susun kolom akhir
    final_cols = [
        "Tahun", "Bulan", "Overview", "Deskripsi", "Tipe", "No. Akun", "Rincian Deskripsi", "Realisasi Biaya"
    ]

    df = df[final_cols].copy()

    df = df[~df["Rincian Deskripsi"].str.contains("Peny", case=False, na=False)]

    records = df.to_dict(orient="records")

    return Response(
        json.dumps(records, ensure_ascii=False),
        mimetype="application/json"
    )

@app.route("/production-bimp")
def get_data_production():
    responses = requests.get(API_URL_production_bimp)
    result = responses.json()

    df = pd.DataFrame(result["data"])

    # format tanggal
    df["Tanggal"] = pd.to_datetime(df["Tanggal"])
    df["Tanggal"] = df["Tanggal"].dt.strftime("%d/%m/%Y")

    # format Total Jam Operasi
    df["Total Jam Operasi"] = (
        df["Total Jam Operasi"]
        .astype(float)
        .round(2)
        .astype(str)
        .str.rstrip("0")
        .str.rstrip(".")
    )

    records = df.to_dict(orient="records")

    return Response(
        json.dumps(records, ensure_ascii=False),
        mimetype="application/json"
    )

if __name__ == "__main__":
    app.run(debug=True)