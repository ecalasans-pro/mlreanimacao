from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
import pandas as pd
import joblib
import os
import wandb
import sys
from api.mlrean_api.pipeline import FeatureSelector, CategoricalTransformer, NumericalTransformer

# Variáveis globais
setattr(sys.modules['__main__'], 'FeatureSelector', FeatureSelector)
setattr(sys.modules["__main__"], "CategoricalTransformer", CategoricalTransformer)
setattr(sys.modules["__main__"], "NumericalTransformer", NumericalTransformer)

#  Artefato do wandb a ser utilizado
artifact_model_name = 'mlreanimacao/model_export:latest'

# Inicia o projeto no wandb
run = wandb.init(project='mlreanimacao', job_type='api')


# Cria a API
app = FastAPI()

# Classe que configura o objeto para requisição
class Paciente(BaseModel):
    idade_materna: float
    fumo: str
    alcool: str
    psicoativas: str
    tpp: str
    dpp: str
    oligoamnio: str
    sifilis: str
    hiv: str
    covid_mae: str
    dheg: str
    dm: str
    sexo: str
    apgar_1_minuto: float

    class Config:
        schema_extra = {
            'example': {
                'idade_materna': 32,
                'fumo': 'n_fumo',
                'alcool': 's_alcool',
                'psicoativas': 'n_psico',
                'tpp': 'n_tpp',
                'dpp': 'n_dpp',
                'oligoamnio': 'n_oligo',
                'sifilis': 'n_sifilis',
                'hiv': 'n_hiv',
                'covid_mae': 'n_covid',
                'dheg': 'n_dheg',
                'dm': 's_dm',
                'sexo': 'Feminino',
                'apgar_1_minuto': 7
            }
        }

@app.get('/', response_class=HTMLResponse)
async def root():
    return """
        <h1><span style="font-style: italic;">Machine Learning</span> em Reanimação Neonatal</h1>
    <h3>Exemplo de API para auxiliar no Projeto 1 da Disciplina de Aprendizagem de Máquina do PPgEEC-UFRN</h3>
    <p style="margin-top: 15px;">
        Esta API enviará dados referentes ao paciente para o modelo e obterá como resultado a necessidade ou não
        de reanimação neonatal do referido paciente.
    </p>
    """

@app.post('/predict')
async def get_inference(patient: Paciente):
    model_export_path = run.use_artifact(artifact_model_name).file()
    pipe = joblib.load(model_export_path)
    df = pd.DataFrame([patient.dict()])
    predict = pipe.predict(df)

    return "Não Reanimar" if predict[0] == 0 else "Reanimar"