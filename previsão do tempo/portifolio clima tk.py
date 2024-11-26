import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

# Função para buscar os dados do clima
def buscar_clima():
    try:
        url = "https://www.google.com/search?q=clima+em+sao+paulo"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        
        temperatura = soup.find("span", {"id": "wob_tm"}).text
        descricao = soup.find("span", {"id": "wob_dc"}).text
        umidade = soup.find("span", {"id": "wob_hm"}).text

        resultado_label.config(
            text=f"Clima em São Paulo:\n"
                 f"Temperatura: {temperatura}°C\n"
                 f"Umidade: {umidade}\n"
                 f"Descrição: {descricao}"
        )
        return {
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "cidade": "São Paulo",
            "temperatura": temperatura,
            "umidade": umidade,
            "descricao": descricao,
        }
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao obter dados: {e}")

# Função para salvar os dados em um arquivo JSON
def salvar_dados():
    dados = buscar_clima()
    if dados:
        try:
            try:
                with open("historico_clima.json", "r", encoding="utf-8") as arquivo:
                    historico = json.load(arquivo)
            except FileNotFoundError:
                historico = []
                
            historico.append(dados)

            # Salva o arquivo JSON com os novos dados
            with open("historico_clima.json", "w", encoding="utf-8") as arquivo:  # Mudei para "w"
                json.dump(historico, arquivo, indent=4, ensure_ascii=False)

            messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados: {e}")


# Interface gráfica com Tkinter
app = tk.Tk()
app.title("Captador de Clima - São Paulo")

titulo_label = tk.Label(app, text="Captador de Clima de São Paulo", font=("Helvetica", 16))
titulo_label.pack(pady=10)

resultado_label = tk.Label(app, text="Clique no botão para buscar o clima.", font=("Helvetica", 12))
resultado_label.pack(pady=10)

buscar_btn = tk.Button(app, text="Buscar Clima", command=buscar_clima, bg="blue", fg="white")
buscar_btn.pack(pady=5)

salvar_btn = tk.Button(app, text="Salvar Dados", command=salvar_dados, bg="green", fg="white")
salvar_btn.pack(pady=5)

app.mainloop()