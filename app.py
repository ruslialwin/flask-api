from flask import Flask, Response
import pandas as pd
import requests
import json

app = Flask(__name__)

COMPANIES = {
    "bimp": {
        "realisasi": "https://dashboard.mahkotagroup.com/api/dashboard/realisasi-bimp",
        "analitik": "https://dashboard.mahkotagroup.com/api/dashboard/realisasi-akun-analitik-bimp",
        "processing": "https://dashboard.mahkotagroup.com/api/dashboard/processing-labour-bimp",
        "production": "https://dashboard.mahkotagroup.com/api/dashboard/production-bimp"
    },
    "bimr": {
        "realisasi": "https://dashboard.mahkotagroup.com/api/dashboard/realisasi-bimr",
        "analitik": "https://dashboard.mahkotagroup.com/api/dashboard/realisasi-akun-analitik-bimr",
        "processing": "https://dashboard.mahkotagroup.com/api/dashboard/processing-labour-bimr",
        "production": "https://dashboard.mahkotagroup.com/api/dashboard/production-bimr"
    },
    "bims": {
        "realisasi": "https://dashboard.mahkotagroup.com/api/dashboard/realisasi-bims",
        "analitik": "https://dashboard.mahkotagroup.com/api/dashboard/realisasi-akun-analitik-bims",
        "processing": "https://dashboard.mahkotagroup.com/api/dashboard/processing-labour-bims",
        "production": "https://dashboard.mahkotagroup.com/api/dashboard/production-bims"
    },
    "mul": {
        "realisasi": "https://dashboard.mahkotagroup.com/api/dashboard/realisasi-mul",
        "analitik": "https://dashboard.mahkotagroup.com/api/dashboard/realisasi-akun-analitik-mul",
        "processing": "https://dashboard.mahkotagroup.com/api/dashboard/processing-labour-mul",
        "production": "https://dashboard.mahkotagroup.com/api/dashboard/production-mul"
    },
    "kpnj": {
        "realisasi": "https://dashboard.mahkotagroup.com/api/dashboard/realisasi-kpnj",
        "analitik": "https://dashboard.mahkotagroup.com/api/dashboard/realisasi-akun-analitik-kpnj",
        "processing": "https://dashboard.mahkotagroup.com/api/dashboard/processing-labour-kpnj",
        "production": "https://dashboard.mahkotagroup.com/api/dashboard/production-kpnj"
    }
}

# Data Helper
def get_dataframe(url):
    response = requests.get(url)
    result = response.json()
    return pd.DataFrame(result["data"])

@app.route("/realisasi/<company>")
def get_data_realisasi(company):

    df = get_dataframe(COMPANIES[company]["realisasi"])

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

@app.route("/realisasi-akun-analitik/<company>")
def get_data_akun_analitik(company):
    df = get_dataframe(COMPANIES[company]["analitik"])

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

@app.route("/processing-labour/<company>")
def get_data_processing_labour(company):
    df = get_dataframe(COMPANIES[company]["processing"])

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

@app.route("/production/<company>")
def get_data_production(company):
    df = get_dataframe(COMPANIES[company]["production"])

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