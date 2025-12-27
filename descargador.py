import requests
import sys
import os
import zipfile

def ejecutar_proceso(inicio, fin, nombre_carpeta):
    # --- TUS COOKIES (Si fallan, actualízalas aquí) ---
    cookies = {
        '.AspNetCore.Antiforgery.k2mmBe4OU3k': 'CfDJ8CDi7FB5A4JOg46h67opVR4InkZWFO5DIj9TiboLOB60fOncaxbY2_wzebgR0tPy3hH5lBQKe0xP8zqcwPUlzvKHU5T3g-h2aQXd_Hx8e7-j13FkMRhpvCr4n9yQuKijgA3K0cx1go1Ak1WM56Dvy5Y',
        '.AspNetCore.Identity.Application': 'CfDJ8CDi7FB5A4JOg46h67opVR45DwWb8Nx9ac_9oeSiyHLT1POP5spdX4Kz_25Z7Bl-SJidtYltc5dnfzR9AuuS39WqNY6cNxUKoMRzPWmoHFM1gaE3CginnKyNMEgeVas5xC-nriF9K7lqinLJgwwrTF6wQYlMB1REdoZtMqplABaJ2zeBcJhpFodEd3xaos6n-LbqriBbfe9sXnnZBpud5H45uVqzvi8F7qS-f2hPV31zfWKM-wgk-C1EgOIeB9Fehkm7RJpTz1OFLUtM9Uvt16PKGm2KAGyaBQ5rhytAOqYQvhRs4MqQF1LZaHNWt9dbjNCYxI--VIVcCiXA-rIKsL_qOQckSUGiUq54NVmdTh7esmlLoB3GY4lE1jXzsG_fjV3FijGm7m8Dn3uz4t04GqPKmNSIe3I-YjZVSWzDchSoM5ygAZYTcG4jDWgzmTRMiM6UIMN-9VM_SOR-GusHhkwoe3ncJWwVafXJV8a_hATgLKnCB_Cz96xaR6fv9GEW-HClXgGTYtwrOP4pia9l9U8vqD2yjPTUZk19WhrwsiqHRgml3MNvUg_YJ0PrK5lZy8RSMcEeaNZI6p84FFvoFd1-k3-taa2FVbUj5xgK2Yzcmp82bBfvEsbNMScm1LPoJnqFofmj9PXq9NDug_6YxUH9MYTSHuMcD41iAJK7OnhtMF_bQL8xYM_sVkM4L8pa9tlfHlBtoqXHZCIGAu2dlpyKU2OC1or-1eX6Q0XEHvQWz5QdlWE3uOOk4UtNDUQd_WSV8veebtQQgpxTvYJl4duu2YaLmAfSZV3AEpbmGfay2b8mfR7GqJsacVhWkhEgJfY83YtkTldCvBMfqWgSjPgt83n8AmPq0YjH6_ujBqCM53K_IWMxDl9p0QWlq8CfcF4vjNag',
        '.AspNetCore.Session': 'CfDJ8CDi7FB5A4JOg46h67opVR6jNsOlI%2BnLCVagMSyZAlAwG9eFfMcRk0ZcY7OrOaIbdnxAFz5I5YevI0%2Bbd2qBUqBcRYP48M9R9TbEzxDLlHJmPStorao77giUCzbjiZY6kPHIpozDXomReFmSsLWZe1c0T2dvpfKMzez4AMxP%2F%2FE4'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'Referer': 'https://ccytemconvocatorias.morelos.gob.mx/ResponderPreguntasView/1078'
    }

    if not os.path.exists(nombre_carpeta):
        os.makedirs(nombre_carpeta)

    exitos = 0
    fallos = []

    print(f"Iniciando descarga en carpeta: {nombre_carpeta}")

    for i in range(inicio, fin + 1):
        url = f"https://ccytemconvocatorias.morelos.gob.mx/api/DownloadFile/DownloadFileAnswer/{i}"
        nombre_archivo = f"documento_{i}.pdf"
        ruta_archivo = os.path.join(nombre_carpeta, nombre_archivo)

        try:
            r = requests.get(url, cookies=cookies, headers=headers, timeout=15)
            if r.status_code == 200:
                with open(ruta_archivo, 'wb') as f:
                    f.write(r.content)
                exitos += 1
                print(f"? Descargado ID {i}")
            else:
                print(f"? Error {r.status_code} en ID {i}")
                fallos.append(f"ID {i} (Error {r.status_code})")
        except Exception as e:
            print(f"?? Error conexión ID {i}: {e}")
            fallos.append(f"ID {i} (Conexión)")

    # Comprimir todo
    zip_name = f"{nombre_carpeta}.zip"
    print(f"\nComprimiendo en {zip_name}...")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(nombre_carpeta):
            for file in files:
                zipf.write(os.path.join(root, file), file)

    print(f"Resumen: {exitos} exitosos, {len(fallos)} fallidos.")
    return zip_name, fallos

def subir_a_gofile(archivo_zip):
    print(f"Subiendo {archivo_zip} a GoFile...")
    try:
        server = requests.get("https://api.gofile.io/servers").json()["data"]["servers"][0]["name"]
        with open(archivo_zip, 'rb') as f:
            res = requests.post(f"https://{server}.gofile.io/contents/uploadfile", files={'file': f}).json()
        
        if res["status"] == "ok":
            print(f"\n?? ENLACE PARA TU AMIGO: {res['data']['downloadPage']}")
        else:
            print("Error en respuesta de GoFile")
    except Exception as e:
        print(f"Error subiendo a GoFile: {e}")

if __name__ == "__main__":
    ini = int(sys.argv[1])
    fin = int(sys.argv[2])
    nom = sys.argv[3]
    debe_subir = sys.argv[4].lower()

    zip_final, errores = ejecutar_proceso(ini, fin, nom)
    
    if errores:
        print("\nIDs que fallaron:", errores)

    if debe_subir == "si":
        subir_a_gofile(zip_final)
