import requests
import sys

def transferir():
    url_archivo = sys.argv[1]
    nombre = url_archivo.split("/")[-1]
    
    # 1. GitHub descarga el archivo
    print(f"Descargando: {nombre}")
    r = requests.get(url_archivo, stream=True)
    with open(nombre, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    # 2. GitHub lo sube a GoFile
    print("Subiendo a GoFile...")
    server = requests.get("https://api.gofile.io/servers").json()["data"]["servers"][0]["name"]
    res = requests.post(f"https://{server}.gofile.io/contents/uploadfile", files={'file': open(nombre, 'rb')}).json()
    
    if res["status"] == "ok":
        print(f"\n✅ ENLACE LISTO: {res['data']['downloadPage']}")
    else:
        print("Error en la subida.")

if __name__ == "__main__":
    transferir()
