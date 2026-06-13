import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
import json
import os
from datetime import datetime

ARQUIVO = "medicamentos.json"


class SistemaMedicamentos:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Controle de Medicamentos")
        self.root.geometry("1200x700")

        self.medicamentos = []
        self.historico = []

        self.criar_interface()
        self.carregar_dados()

    def criar_interface(self):

        # TÍTULO
        titulo = ttk.Label(
            self.root,
            text="💊 Sistema de Controle de Medicamentos para Idosos",
            font=("Segoe UI", 20, "bold")
        )
        titulo.pack(pady=10)

        # ==========================
        # DADOS DO PACIENTE
        # ==========================

        frame_paciente = ttk.LabelFrame(
            self.root,
            text="Dados do Paciente"
        )

        frame_paciente.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ttk.Label(
            frame_paciente,
            text="Nome:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.nome_paciente = ttk.Entry(
            frame_paciente,
            width=30
        )

        self.nome_paciente.grid(
            row=0,
            column=1,
            padx=5
        )

        ttk.Label(
            frame_paciente,
            text="Idade:"
        ).grid(row=0, column=2)

        self.idade_paciente = ttk.Entry(
            frame_paciente,
            width=10
        )

        self.idade_paciente.grid(
            row=0,
            column=3,
            padx=5
        )

        ttk.Label(
            frame_paciente,
            text="Telefone:"
        ).grid(row=0, column=4)

        self.telefone_paciente = ttk.Entry(
            frame_paciente,
            width=20
        )

        self.telefone_paciente.grid(
            row=0,
            column=5,
            padx=5
        )
            

        # DASHBOARD
        frame_cards = ttk.Frame(self.root)
        frame_cards.pack(fill="x", padx=20, pady=10)

        self.card_total = ttk.LabelFrame(
            frame_cards,
            text="Medicamentos Cadastrados"
        )
        self.card_total.pack(side="left", padx=10)

        self.lbl_total = ttk.Label(
            self.card_total,
            text="0",
            font=("Segoe UI", 24, "bold")
        )
        self.lbl_total.pack(padx=20, pady=20)

        # FORMULÁRIO
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Label(frame, text="Medicamento").grid(
            row=0, column=0, padx=5
        )
        self.nome_entry = ttk.Entry(frame, width=25)
        self.nome_entry.grid(row=1, column=0, padx=5)

        ttk.Label(frame, text="Dosagem").grid(
            row=0, column=1, padx=5
        )
        self.dosagem_entry = ttk.Entry(frame, width=15)
        self.dosagem_entry.grid(row=1, column=1, padx=5)

        ttk.Label(frame, text="Horário").grid(
            row=0, column=2, padx=5
        )
        self.horario_entry = ttk.Entry(frame, width=15)
        self.horario_entry.grid(row=1, column=2, padx=5)

        ttk.Label(frame, text="Estoque").grid(
            row=0, column=3, padx=5
        )
        self.estoque_entry = ttk.Entry(frame, width=10)
        self.estoque_entry.grid(row=1, column=3, padx=5)

        ttk.Button(
            frame,
            text="Cadastrar",
            command=self.cadastrar,
            bootstyle="success"
        ).grid(row=1, column=4, padx=10)

        # PESQUISA
        frame_pesquisa = ttk.Frame(self.root)
        frame_pesquisa.pack(fill="x", padx=20, pady=10)

        ttk.Label(
            frame_pesquisa,
            text="Pesquisar:"
        ).pack(side="left")

        self.pesquisa = ttk.Entry(
            frame_pesquisa,
            width=40
        )
        self.pesquisa.pack(side="left", padx=10)
        self.pesquisa.bind(
            "<KeyRelease>",
            self.filtrar
        )

        # TABELA
        colunas = (
            "Medicamento",
            "Dosagem",
            "Horário",
            "Estoque"
        )

        self.tabela = ttk.Treeview(
            self.root,
            columns=colunas,
            show="headings",
            height=15
        )

        for coluna in colunas:
            self.tabela.heading(coluna, text=coluna)
            self.tabela.column(
                coluna,
                width=250,
                anchor="center"
            )

        self.tabela.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # BOTÕES
        frame_botoes = ttk.Frame(self.root)
        frame_botoes.pack(pady=10)

        ttk.Button(
            frame_botoes,
            text="Registrar Uso",
            command=self.registrar_uso,
            bootstyle="primary"
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            frame_botoes,
            text="Excluir",
            command=self.excluir,
            bootstyle="danger"
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            frame_botoes,
            text="Verificar Estoque",
            command=self.verificar_estoque,
            bootstyle="warning"
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            frame_botoes,
            text="Histórico",
            command=self.mostrar_historico,
            bootstyle="info"
        ).grid(row=0, column=3, padx=5)

    def cadastrar(self):

        nome = self.nome_entry.get().strip()
        dosagem = self.dosagem_entry.get().strip()
        horario = self.horario_entry.get().strip()

        if not nome:
            messagebox.showwarning(
                "Aviso",
                "Informe o nome do medicamento."
            )
            return

        try:
            estoque = int(
                self.estoque_entry.get()
            )
        except ValueError:
            messagebox.showerror(
                "Erro",
                "Digite um estoque válido."
            )
            return

        medicamento = {
            "nome": nome,
            "dosagem": dosagem,
            "horario": horario,
            "estoque": estoque
        }

        self.medicamentos.append(medicamento)

        self.salvar_dados()
        self.atualizar_tabela()

        self.nome_entry.delete(0, tk.END)
        self.dosagem_entry.delete(0, tk.END)
        self.horario_entry.delete(0, tk.END)
        self.estoque_entry.delete(0, tk.END)

        messagebox.showinfo(
            "Sucesso",
            "Medicamento cadastrado!"
        )

    def atualizar_tabela(self):

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for med in self.medicamentos:

            tag = ""

            if med["estoque"] <= 5:
                tag = "baixo"

            self.tabela.insert(
                "",
                "end",
                values=(
                    med["nome"],
                    med["dosagem"],
                    med["horario"],
                    med["estoque"]
                ),
                tags=(tag,)
            )

        self.tabela.tag_configure(
            "baixo",
            background="#ffb3b3"
        )

        self.lbl_total.config(
            text=str(len(self.medicamentos))
        )

    def filtrar(self, event=None):

        texto = self.pesquisa.get().lower()

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for med in self.medicamentos:

            if texto in med["nome"].lower():

                self.tabela.insert(
                    "",
                    "end",
                    values=(
                        med["nome"],
                        med["dosagem"],
                        med["horario"],
                        med["estoque"]
                    )
                )

    def registrar_uso(self):

        selecionado = self.tabela.selection()

        if not selecionado:
            messagebox.showwarning(
                "Aviso",
                "Selecione um medicamento."
            )
            return

        item = self.tabela.item(selecionado)

        nome = item["values"][0]

        for med in self.medicamentos:

            if med["nome"] == nome:

                if med["estoque"] > 0:

                    med["estoque"] -= 1

                    registro = {
                        "data": datetime.now().strftime(
                            "%d/%m/%Y %H:%M"
                        ),
                        "paciente": self.nome_paciente.get(),
                        "medicamento": nome
                    }

                    self.historico.append(registro)

                    self.salvar_dados()
                    self.atualizar_tabela()

                    messagebox.showinfo(
                        "Sucesso",
                        f"{nome} registrado."
                    )

                else:
                    messagebox.showwarning(
                        "Aviso",
                        "Sem estoque."
                    )

    def excluir(self):

        selecionado = self.tabela.selection()

        if not selecionado:
            return

        item = self.tabela.item(selecionado)

        nome = item["values"][0]

        self.medicamentos = [
            med for med in self.medicamentos
            if med["nome"] != nome
        ]

        self.salvar_dados()
        self.atualizar_tabela()

    def verificar_estoque(self):

        alerta = ""

        for med in self.medicamentos:

            if med["estoque"] <= 5:

                alerta += (
                    f"{med['nome']} possui "
                    f"{med['estoque']} unidades\n"
                )

        if alerta:

            messagebox.showwarning(
                "Estoque Baixo",
                alerta
            )

        else:

            messagebox.showinfo(
                "Estoque",
                "Todos os estoques estão normais."
            )

    def mostrar_historico(self):

            janela = tk.Toplevel(self.root)

            janela.title(
                "Histórico de Medicamentos"
            )

            janela.geometry("700x400")

            texto = tk.Text(
                janela,
                font=("Consolas", 10)
            )

            texto.pack(
                fill="both",
                expand=True
            )

            if not self.historico:

                texto.insert(
                    "end",
                    "Nenhum registro encontrado."
                )

                return

            for item in self.historico:

                texto.insert(
                    "end",
                    f"{item['data']}\n"
                    f"Paciente: {item['paciente']}\n"
                    f"Medicamento: {item['medicamento']}\n"
                    f"{'-'*40}\n"
                )

    def salvar_dados(self):

            dados = {
                "paciente": {
                    "nome": self.nome_paciente.get(),
                    "idade": self.idade_paciente.get(),
                    "telefone": self.telefone_paciente.get()
                },
                "medicamentos": self.medicamentos,
                "historico": self.historico
            }

            with open(
                ARQUIVO,
                "w",
                encoding="utf-8"
            ) as arquivo:

                json.dump(
                    dados,
                    arquivo,
                    indent=4,
                    ensure_ascii=False
                )

    def carregar_dados(self):

        if os.path.exists(ARQUIVO):

            with open(
                ARQUIVO,
                "r",
                encoding="utf-8"
            ) as arquivo:

                dados = json.load(arquivo)

                self.medicamentos = dados.get(
                    "medicamentos",
                    []
                )

                self.historico = dados.get(
                    "historico",
                    []
                )

        self.atualizar_tabela()


if __name__ == "__main__":

    root = ttk.Window(
        title="Controle de Medicamentos",
        themename="darkly",
        size=(1200, 700)
    )

    app = SistemaMedicamentos(root)

    root.mainloop()