import pandas as pd

def load_matches():
    url = 'https://raw.githubusercontent.com/SkillCorner/opendata/refs/heads/master/data/matches.json'
    try:
        df = pd.read_json(url)
        print(f"✅ matches.json carregado com sucesso! Total de partidas: {len(df)}")
        return df
    except Exception as e:
        print(f"❌ Erro ao carregar matches.json: {e}")
        return None
    
print(load_matches())