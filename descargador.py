import requests
import sys

def transferir_a_gofile(url_archivo):
    nombre_archivo = url_archivo.split("/")[-1]
    print(f"Descargando {nombre_archivo} desde la fuente...")
    
    # Descarga el archivo en el servidor de GitHub
    with requests.get(url_archivo, stream=True) as r:
        r.raise_for_status()
        with open(nombre_archivo, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    # Sube a GoFile
    print("Subiendo a GoFile...")
    server_resp = requests.get("https://api.gofile.io/servers").json()
    server = server_resp["data"]["servers"][0]["name"]
    
    url_subida = f"https://{server}.gofile.io/contents/uploadfile"
    with open(nombre_archivo, 'rb') as f:
        response = requests.post(url_subida, files={'file': f}).json()

    if response["status"] == "ok":
        print(f"\nENLACE PARA TU AMIGO: {response['data']['downloadPage']}")
    else:
        print("Error en la subida.")

if __name__ == "__main__":
    transferir_a_gofile(sys.argv[1])
