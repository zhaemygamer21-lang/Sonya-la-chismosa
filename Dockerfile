DEPython: 3.10-slim

DIRECTORIO DE TRABAJO/aplicación

COPIARrequisitos.txt .
CORRERpip install --no-cache-dir -r requirements.txt

COPIAR . .

# Abre el puerto para enlazarlo con Render
EXPOSE 8080

#Esta es la orden que le dice a Render que usa tu script directamente
CMD["pitón", "bot.py"]
