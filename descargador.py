import requests
import sys
import os
import zipfile
import mimetypes

def ejecutar_proceso(inicio, fin, nombre_carpeta):
    # --- TUS COOKIES (Asegúrate de que sigan activas) ---
    cookies = {
        '.AspNetCore.Antiforgery.k2mmBe4OU3k': 'CfDJ8CDi7FB5A4JOg46h67opVR4InkZWFO5DIj9TiboLOB60fOncaxbY2_wzebgR0tPy3hH5lBQKe0xP8zqcwPUlzvKHU5T3g-h2aQXd_Hx8e7-jQVzxaairw1qt3DmU6MziZrDvnDcN7hbYdb6FNDcARU',
        '.AspNetCore.Identity.Application': 'CfDJ8CDi7FB5A4JOg46h67opVR45DwWb8Nx9ac_9oeSiyHLT1POP5spdX4Kz_25Z7Bl-SJidtYltc5dnfzR9AuuS1N39KVvVK8itaGr7odbrTKnBdbwt4n7PoYyNMEgeVas5xC-nriF9K7lqinLREe7WaYE2NUB9kgYce79AH4B79YbSPjJicJhpFodEd3xaos6n-LRupe23NQaEoWU2sGtRssDxFrGsEzpvRzi-f2hPV31zfWKM-wgk-C1N39KVvVK8itaGr7odbrTKnBdbwt4n7PoYGm2KAGyaBQ5rhytAOqYQvhRs4MqQF1LZaHNWt9dbjNCYxI--VIVcCiXA-rIKsL_qOQckSUGiUq54NVmdTh7esmlLoB3GY4lE1jXzsG_fjV3FijGm7m8Dn3uz4t04GqPKmNSIe3I-YjZVSWzDchSoM5ygAZYTcG4jDWgzmTRMiM6UIMN-9VM_SOR-GusHhkwoe3ncJWwVafXJV8a_hATgLKnCB_Cz96xaR6fv9GEW-HClXgGTBWUnddB2J5cckALZenPo6KQJwLzysEohEiqHRgml3MNvUg_YJ0PrK5lZy8RSMcEeaNZI6p84FFvoFd1-k3-taa2FVbUj5xgK2Yzcmp82bBfvEsbNMScm1LPoJnqFofmj9PXq9NDug_6YxUH9MYTSHuMcD41iAJK7OnhtMF_bQL8xYM_sVkLREe7WaYE2NUB9kgYce79AH4B79YbSPjJi1or-1eX6Q0XEHvQWz5QdlWE3uOOk4UtNDUQd_WSV8veebtQQgpxTBWUnddB2J5cckALZenPo6KQJwLzysEohER7GqJsacVhWkhEgJfY83YtkTldCvBMfqWgSjPgt83n8AmPq0YjH6_ujBqCM53K_IWMxDl9p0QWlq8CfcF4vjNag',
        '.AspNetCore.Session': 'CfDJ8CDi7FB5A4JOg46h67opVR6jNsOlI%2BnLREe7WaYE2NUB9kgYce79AH4B79YbSPjJinxAFz5I5YevI0%2Bbd2qBUqBcRYP48LREe7WaYE2NUB9kgYce79AH4B79YbSPjJi6kPHIpozDXomReFmSsLWZe1c0T2dvpfKMzez4AMxP%2F%2FE4'
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/143.0.0.0 Safari/537.36'}

    os.makedirs(nombre_carpeta, exist_ok=True)
    exitos = 0
    fallos = []

    for i in range(inicio, fin + 1):
        url = f"https://ccytemconvocatorias.morelos.gob.mx/api/DownloadFile/DownloadFileAnswer/{i}"
        
        try:
            r = requests.get(url, cookies=cookies, headers=headers, timeout=20)
            if r.status_code == 200:
                # DETECTAR EXTENSIÓN (pdf, jpg, png, etc.)
                content_type = r.headers.get('content-type')
                ext = mimetypes.guess_extension(content_type) or '.dat'
                
                # Si el servidor no envía el tipo, probamos detectar por los primeros bytes
                if ext == '.obj': ext = '.pdf' # Corrección común en algunos servidores
                
                nombre_archivo = f"archivo_{i}{ext}"
                file_path = os.path.join(nombre_carpeta, nombre_archivo)

                with open(file_path, 'wb') as f:
                    f.write(r.content)
                exitos += 1
                print(f"? ID {i} detectado como {ext}")
            else:
                fallos.append(f"ID {i} -> Error {r.status_code}")
        except Exception as e:
            fallos.append(f"ID {i} -> Error: {str(e)}")

    zip_name = f"{nombre_carpeta}.zip"
    print(f"\n?? Comprimiendo en {zip_name}...")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(nombre_carpeta):
            for file in files:
                zipf.write(os.path.join(root, file), file)
    
    return zip_name

def subir_gofile(archivo):
    print(f"?? Enviando a GoFile...")
    srv = requests.get("https://api.gofile.io/servers").json()["data"]["servers"][0]["name"]
    with open(archivo, 'rb') as f:
        res = requests.post(f"https://{srv}.gofile.io/contents/uploadfile", files={'file': f}).json()
    if res["status"] == "ok":
        print(f"\n? ENLACE FINAL: {res['data']['downloadPage']}")

if __name__ == "__main__":
    ini, f_in, nom, sub = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4].lower()
    archivo_final = ejecutar_proceso(ini, f_in, nom)
    if sub == 'si':
        subir_gofile(archivo_final)
