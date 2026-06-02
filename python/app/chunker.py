import re
### Si modificamos el CHUNK_SIZE, es probable que los chunks generados cambien. 
# En ese caso hay que limpiar la base de datos porque los vectores pueden quedar huerfanos.

CHUNK_SIZE = 700
CHUNK_OVERLAP = 1
TOPE = 600
SECCION_RE = re.compile(r'(?m)^(?=\d+\.\d+\s|#{1,6}\s)')

def chunk_text(texto):
###
# Divide texto en parrafos y genera los chunks, teniendo en cuenta el tamaño maximo (CHUNK_SIZE) y solapamiento (CHUNK_OVERLAP)
###
    secciones = [s for s in SECCION_RE.split(texto) if s.strip()]
    unidades = []
    
    for s in secciones:
        if len(s) > TOPE:
            unidades.extend(p for p in s.split('\n\n') if p.strip())  # cae al separador chico
        else:
            unidades.append(s)                                         # queda entera
        chunks = []
        actual = ''
        
    for p in unidades:
        if actual and len(actual) + len(p) > CHUNK_SIZE:
            chunks.append(actual)
            cola = actual[0]
            actual = (cola + '\n\n' + p).strip()
        else:
            actual = (actual + '\n\n' + p).strip() if actual else p
    if actual:
        chunks.append(actual)
        
    return chunks

def chunk_docs(docs):
    chunks = []
    for d in docs:
        partes = chunk_text(d["texto"])
        for i, parte in enumerate(partes):
            chunks.append({"texto": parte, "archivo_origen": d["archivo_origen"], 
                           "id": f"{d['id'] if d['id'] is not None else d['archivo_origen']}#{i}"})
            
    return chunks


if __name__ == "__main__":
    from loader import load_general
    docs = load_general()
    chunks = chunk_docs(docs)
    print("num chunks: ", len(chunks))
    print("ids únicos:", len(set(c["id"] for c in chunks)))
    for c in chunks:
      print(len(c["texto"]), '- - -  ', c["id"])
      palabras = c["texto"].split()
    #   if c["id"] == "Documentación 1.pdf#4":
    #       print(palabras)    
      inicio = " ".join(palabras[:5])      # primeras 5
      fin = " ".join(palabras[-5:])        # últimas 5
      print(f"{c['id']}: {inicio} ... {fin}")