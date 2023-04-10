import requests
import csv
import re
import argparse

headers = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "Referer": "https://escolasegura.mj.gov.br/",
}

url = "https://rs.safernet.org.br/external/report_kit"

parser = argparse.ArgumentParser(
    prog="Reporter",
    description="Script para reportar URLs em massa para o programa Escola Segura",
)
parser.add_argument(
    "filename",
    help="Nome do arquivo CSV a ser utilizado (Exemplo: 'python reporter.py data.csv url')",
)
parser.add_argument(
    "column",
    help="Nome da coluna que possui as URLs dentro do arquivo CSV a ser utilizado (Exemplo: 'python reporter.py data.csv url')",
)
arguments = parser.parse_args()


def getAuth():
    response = requests.request("GET", url, headers=headers)
    result = re.search(
        "([0-9,a-z]{40})",
        response.text,
    )
    if result.group(1):
        print(f"[!] Token obtido com sucesso '{result.group(1)}'")
        return result.group(1)
    else:
        print(f"[X] Não foi possível obter o token")
        return False


def sendReport(authToken, reportUrl):
    formData = f"feature_319=229954&authenticity_token={authToken}&report%5Burl%5D={reportUrl}&report%5Bcomment%5D=&&partner%5Bpath%5D=https%3A%2F%2Fescolasegura.mj.gov.br%2Fenviado_sucesso.html&report_kit_last_option=229954"
    try:
        response = requests.request("POST", url, data=formData, headers=headers)
        if (
            response.status_code == 200
            and "Sua denúncia foi registrada com sucesso." in response.text
        ):
            print(f"[+] Denúncia registrada com sucesso | {reportUrl}")
        else:
            print(f"[-] Não foi possível registrar a denúncia! | {reportUrl}")
    except Exception as e:
        print(f"[-] Ocorreu um erro ao registrar a denúncia | {reportUrl}")
        print(f"  | {repr(e)}")


def readExcel(filename, column):
    with open(filename, encoding="cp850") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        urlList = []
        for row in reader:
            urlList.append(row[column])
        print(f"[+] {len(urlList)} URL(s) carregada(s) do arquivo '{filename}'")
        return urlList


authToken = getAuth()
if arguments.filename and arguments.column:
    urlList = readExcel(arguments.filename, arguments.column)
    for reportUrl in urlList:
        sendReport(authToken, reportUrl)
