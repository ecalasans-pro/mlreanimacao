from fastapi.testclient import TestClient
import os
import sys
import pathlib
from api.mlrean_api.main import app

# Instância de teste
client = TestClient(app)


# Testa a rota de raiz
def test_root():
    r = client.get('/')
    assert r.status_code == 200

# Testa saída para casos em que precisa de reanimação
def test_reanimar():
    paciente = {
        "idade_materna": 32,
        "fumo": "n_fumo",
        "alcool": "s_alcool",
        "psicoativas": "n_psico",
        "tpp": "n_tpp",
        "dpp": "n_dpp",
        "oligoamnio": "n_oligo",
        "sifilis": "n_sifilis",
        "hiv": "n_hiv",
        "covid_mae": "n_covid",
        "dheg": "n_dheg",
        "dm": "s_dm",
        "sexo": "Feminino",
    }

    r = client.post('/predict', json=paciente)
    assert r.status_code == 200
    assert r.json() == "Reanimar"


# Testa saída para não reanimação
def test_naoReanimar():
    # Testa saída para casos em que precisa de reanimação
    def test_reanimar():
        paciente = {
            "idade_materna": 32,
            "fumo": "n_fumo",
            "alcool": "s_alcool",
            "psicoativas": "n_psico",
            "tpp": "n_tpp",
            "dpp": "n_dpp",
            "oligoamnio": "n_oligo",
            "sifilis": "n_sifilis",
            "hiv": "n_hiv",
            "covid_mae": "n_covid",
            "dheg": "n_dheg",
            "dm": "s_dm",
            "sexo": "Masculino",
        }

        r = client.post('/predict', json=paciente)
        assert r.status_code == 200
        assert r.json() == "Não Reanimar"

