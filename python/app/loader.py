import json
import re
from pypdf import PdfReader
from pathlib import Path
DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"

def clean_txt(text):
    
    #Unificamos saltos de linea
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    #Colapsar espacios y tabs multiples em uno
    text = re.sub(r"[ \t]+", " ", text)
    #Colapsar saltos de linea multiples en maximo 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    #Limpia espacios al inicio y final de cada linea.
    text = "\n".join(line.strip() for line in text.split("\n"))
    #Devuelvo el texto sin espacios al principio o fin del mismo
    return text.strip()

def load_pdf(path):
###
# Lee el contenido de un archivo PDF y lo devuelve como cadena de texto.
###
    
    reader = PdfReader(path)
    pdf_text = "\n".join([page.extract_text() or "" for page in reader.pages])
    return pdf_text


def load_txt(path):
###
# Lee el contenido de un archivo .txt o .md y lo devuelve como cadena de texto.
###

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    return content

def json_item_to_text(item):
###
# 'Aplana' el contenido de un problema representado en json y lo convierte a texto
###
    res = item.get('categoria', '') + '\n' + item.get('titulo', '') + '\n' + item.get('mensaje_usuario', '') + '\n' + item.get('nivel_soporte', '') + '\n'
    res += 'Causas posibles: ' + ', '.join(item.get('causas_posibles', [])) + '\n'
    res += 'Solucion: ' + ', '.join(item.get('solucion', [])) + '\n'
    res += 'Palabras clave: ' + ', '.join(item.get('palabras_clave', [])) + '\n'
    return { "id": item.get('id', ''), "texto": res}

def load_json(path):
###
# Lee el contenido del json, devuelve una lista de problemas representados como texto
###
    res = []
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        contenido = data.get('contenido', [])
        for c in contenido:
            res.append(json_item_to_text(c))
        
    return res


def load_general():

    docs = []
    for documento in DOCS_DIR.iterdir():
        origen = documento.name
        if documento.suffix == '.pdf':
            docs.append({"texto": clean_txt(load_pdf(documento)), "archivo_origen": origen, "id": None})
        elif documento.suffix in ['.txt', '.md']:
            docs.append({"texto": clean_txt(load_txt(documento)), "archivo_origen": origen, "id": None})
        elif documento.suffix == '.json':
            for p in load_json(documento):
                docs.append({"texto": p.get("texto"), "archivo_origen": origen, "id": p.get("id")})
                
    return docs


load_general()
# print(load_pdf(r'python\docs\Documentación 1.pdf'))
# print(clean_txt(load_pdf(r'python\docs\Documentación 1.pdf')))



