# Asistente de soporte que consume documentación privada
## Arquitectura
                                                                                        
                           ┌─────────┐                                  
                           │ chromaDB│                                  
                           └──▲───┬──┘                                  
                    pregunta  │   │devuelve top_k                       
                    vectorizada   │vectores cercanos                    
  ┌──────────┐             ┌──┼───▼──┐                                  
  │          │ search      │         │    ┌──────────┐                  
  │          │(pregunta)   │         │docs│          │                  
  │ Webhook  ┼────────────►│ Python  ┼────► code node│                  
  │          │             │   API   │    │          │                  
  │          │             │         │    └────┬─────┘                  
  └──────────┘             └─────────┘         │system_prompt           
                                               │query                   
                                               │docs                    
                                               │                        
                                               │       system_prompt    
                                          ┌────┴──────┐query  ┌────┐    
                                          │if len(docs)──────►│    │    
                                          │   > 0     │docs   │LLM │    
                                          └───┬───────┘       └─┬──┘    
                                              │                 │       
                                              │else             ▼       
                                              ▼             respuesta   
                                          respuesta                     
                                                                        

## Stack
Python/FastAPI, ChromaDB, sentence-transformers (e5-base), n8n, GLM-5.1 provisto por NVIDIA build

## Requisitos
Docker + Docker Compose + API key de NVIDIA BUILD

## Levantamiento 
1. crear .env, guardar dentro la NVIDIA_API_KEY (ver .env.example)
2. ejecutar docker compose up -d en la raiz del repo.
3. el repositorio ya contiene docs genericos, en caso de querer utilizar otros documentos subirlos a la carpeta /python/docs (soporta .PDF, .TXT, .MD, .JSON).
4. correr /ingest por primera vez para llenar chroma con los embeddings (:8000/docs).
5. abrir :5678, loggearse en n8n, importar workflow.json (n8n/workflow.json) y activarlo (boton arriba a la derecha)

## Uso
1. Cargue archivos masivamente y me dio error. 
   Hay documentación explicita para este error.
```powershell
$body = '{"pregunta":"Cargue archivos masivamente y me dio error"}'
Invoke-RestMethod -Uri "http://localhost:5678/webhook/pregunta" -Method Post -ContentType "application/json; charset=utf-8" -Body $body | ConvertTo-Json -Depth 10
```
RESPONSE
```json
{
"respuesta":  "Según la documentación proporcionada, si te dio error al realizar una carga masiva, el mensaje que se muestra es **\"No se pudo procesar el archivo de importación\"**. \n\nLas posibles causas y la solución según la fuente son:\n\n**Causas posibles:**\n* Plantilla incorrecta.\n* Columnas faltantes.\n* Datos incompatibles.\n* Códigos repetidos.\n* Formato de fecha inválido.\n\n**Solución:**\nDescargar la plantilla oficial del sistema, completar los datos respetando el formato requerido y volver a cargar el archivo.\n\n*Información extraída de la Fuente: Documentación 2.txt (Sección 3.6 Error: carga masiva fallida).*",
    
"fuentes":  ["Documentación 2.txt", "Documentación 1.pdf"]
}       
``` 
2. El sistema devuelve error 502, ¿qué significa?:
   En la documentación no hay nada que describa un error 502.
   
```powershell
$body = '{"pregunta":"El sistema devuelve error 502, ¿qué significa?"}'
Invoke-RestMethod -Uri "http://localhost:5678/webhook/pregunta" -Method Post -ContentType "application/json; charset=utf-8" -Body $body | ConvertTo-Json -Depth 10
```

RESPONSE
```json
{
    "respuesta":  "No tengo la información suficiente para responder a tu pregunta. La documentación proporcionada no contiene referencias ni explicaciones sobre el error 502.",
    "fuentes":  ["Documentación 3.md", "Documentación 2.txt"]
}       
```        
3. Olvide mis credenciales de inicio
   Hay información sobre errores con credenciales de inicio.
```powershell

$body = '{"pregunta":"Olvide mis credenciales de inicio"}'
Invoke-RestMethod -Uri "http://localhost:5678/webhook/pregunta" -Method Post -ContentType "application/json; charset=utf-8" -Body $body | ConvertTo-Json -Depth 10
```
RESPONSE
```json
{
"respuesta":  "No tengo información suficiente para responder cómo recuperar o restablecer credenciales olvidadas. \n\nLa documentación proporcionada solo explica qué hacer frente al error de credenciales incorrectas (Código ERR-AUTH-001), donde se recomienda: \"1. Verificar que el usuario y la contraseña sean correctos. 2. Comprobar si la cuenta está activa. 3. Revisar si la cuenta se encuentra bloqueada. 4. Solicitar al administrador el restablecimiento de la contraseña si el error continúa\" (Fuente: Documentación 3.md).",

"fuentes":  ["Documentación 3.md","Documentación 2.txt"]
     }       
```            

## ADRs
1. Teniendo en cuenta que los documentos tenian un formato bastante uniforme, se decidio aplicar chunking por seccion (intentando mantener siempre un chunk por error).
2. Se eligio el modelo e5-base porque presento mejor rendimiento que otros modelos (e5-small, MiniLM)
3. Umbral + system prompt: El umbral de decision sobre si un chunk es o no una solucion del problema es permisivo, el LLM se encarga de una segunda revision de la documentación recuperada.
4. Se utilizo modelo LLM provisto por NVIDIA build porque OpenAi no tiene freetier.
5. El modelo provisto por Nvidia no era compatible con el nodo 'Message a model' de OpenAi, se utilizo HTTP request.

## Manejo de errores
  - input vacío → 400 (API)
  - sin respuesta → rama if / system prompt → "no encontrado"
  - timeout → timeout en el nodo + retry
  - error de API → salida de error → 503

                                                                                        
                                                                                        
                                                                                        
                                                                                        