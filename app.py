from flask import Flask, Response
import pandas as pd
import requests
import json

app = Flask(__name__)

API_URL_realisasi = "https://dashboard.mahkotagroup.com/api/dashboard/realisasi-terekam"
API_URL_akun_analitik = "https://dashboard.mahkotagroup.com/api/dashboard/realisasi-akun-analitik-terekam"
API_URL_processing_labour = "https://dashboard.mahkotagroup.com/api/dashboard/processing-labour"
API_URL_production = "https://dashboard.mahkotagroup.com/api/dashboard/production"

# @app.route("/realisasi")
# def get_data_realisasi():
#     responses = requests.get(API_URL_realisasi)
#     result = responses.json()

#     df = pd.DataFrame(result["data"])

#     # Balik tanda nominal untuk Pendapatan dan Pendapatan Lain-lain
#     mask_pendapatan = df["Deskripsi"].isin(["Pendapatan", "Pendapatan Lain-lain"])
#     df.loc[mask_pendapatan, "Nominal"] = df.loc[mask_pendapatan, "Nominal"] * -1

#     # Susun kolom akhir
#     final_cols = [
#         "Tanggal", "Tahun", "Bulan", "Overview", "Deskripsi",
#         "No Akun", "Nama Akun",
#         "No Akun Analitik", "Nama Akun Analitik",
#         "Kode Induk Analitik", "Kode Detail Analitik", "Tipe Unit",
#         "Nominal"
#     ]

#     df = df[final_cols].copy()

#     records = df.to_dict(orient="records")

#     return Response(
#         json.dumps(records, ensure_ascii=False),
#         mimetype="application/json"
#     )

@app.route("/realisasi-akun-analitik")
def get_data_akun_analitik():
    responses = requests.get(API_URL_akun_analitik)
    result = responses.json()

    df = pd.DataFrame(result["data"])

    # Balik tanda nominal untuk Pendapatan dan Pendapatan Lain-lain
    mask_pendapatan = df["Deskripsi"].isin(["Pendapatan", "Pendapatan Lain-lain"])
    df.loc[mask_pendapatan, "Nominal"] = df.loc[mask_pendapatan, "Nominal"] * -1

    # Susun kolom akhir
    final_cols = [
        "Tanggal", "Tahun", "Bulan", "Overview", "Deskripsi",
        "No Akun", "Nama Akun",
        "No Akun Analitik", "Nama Akun Analitik",
        "Kode Induk Analitik", "Kode Detail Analitik", "Tipe Unit",
        "Nominal"
    ]

    df = df[final_cols].copy()

    records = df.to_dict(orient="records")

    return Response(
        json.dumps(records, ensure_ascii=False),
        mimetype="application/json"
    )

if __name__ == "__main__":
    app.run(debug=True)