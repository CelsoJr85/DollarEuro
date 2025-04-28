""" COTAÇÃO DOLLAR EURO COM USO DE APIs """
import sys
import time
import threading
import requests
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QPushButton, QHBoxLayout, QDesktopWidget, QComboBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon


class CotacaoWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Remover bordas da janela e definir como sempre visível
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Lista de APIs para consulta
        self.apis = [
            {"nome": "AwesomeAPI", "url": "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL", "ativa": True},
            {"nome": "Banco Central",
             "url": "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{}'&$format=json",
             "ativa": True}
        ]

        # Inicializa as cotações
        self.dolar_valores = {"AwesomeAPI": "0.00", "Banco Central": "0.00"}
        self.euro_valores = {"AwesomeAPI": "0.00"}
        self.dolar_valor_exibir = "0.00"
        self.euro_valor_exibir = "0.00"
        self.fonte_atual = "Múltiplas Fontes"
        self.ultima_atualizacao = "00:00:00"
        self.contador_falhas = {api["nome"]: 0 for api in self.apis}

        # Configurações iniciais
        self.iniciar_ui()
        self.posicionar_widget()

        # Iniciar thread para buscar cotações
        self.thread_ativa = True
        self.thread_cotacao = threading.Thread(target=self.atualizar_cotacoes)
        self.thread_cotacao.daemon = True
        self.thread_cotacao.start()

        # Timer para atualizar a interface
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_interface)
        self.timer.start(1000)  # Atualiza a cada 1 segundo

        # Variável para rastrear se está arrastando a janela
        self.dragging = False
        self.offset = None

    def iniciar_ui(self):
        """Inicializa a interface do usuário"""
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Layout para botão de fechar e fonte
        top_layout = QHBoxLayout()

        # Seletor de fonte
        self.fonte_combo = QComboBox()
        self.fonte_combo.addItem("Múltiplas Fontes")
        for api in self.apis:
            self.fonte_combo.addItem(api["nome"])
        self.fonte_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 30);
                color: white;
                border-radius: 5px;
                padding: 2px;
                font-size: 8pt;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.fonte_combo.currentTextChanged.connect(self.mudar_fonte)
        top_layout.addWidget(self.fonte_combo)

        # Botão de fechar
        self.fechar_btn = QPushButton("×")
        self.fechar_btn.setFixedSize(20, 20)
        self.fechar_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 30);
                color: white;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 150);
            }
        """)
        self.fechar_btn.clicked.connect(self.fechar_aplicativo)
        top_layout.addWidget(self.fechar_btn)

        main_layout.addLayout(top_layout)

        # Título
        self.titulo_label = QLabel("Cotações")
        self.titulo_label.setAlignment(Qt.AlignCenter)
        self.titulo_label.setStyleSheet("color: white; font-weight: bold;")
        main_layout.addWidget(self.titulo_label)

        # Informações do Dólar
        self.dolar_label = QLabel(f"USD: R$ {self.dolar_valor_exibir}")
        self.dolar_label.setAlignment(Qt.AlignCenter)
        self.dolar_label.setStyleSheet("color: white;")
        self.dolar_label.setFont(QFont("Arial", 12))
        main_layout.addWidget(self.dolar_label)

        # Informações do Euro
        self.euro_label = QLabel(f"EUR: R$ {self.euro_valor_exibir}")
        self.euro_label.setAlignment(Qt.AlignCenter)
        self.euro_label.setStyleSheet("color: white;")
        self.euro_label.setFont(QFont("Arial", 12))
        main_layout.addWidget(self.euro_label)

        # Última atualização
        self.atualizacao_label = QLabel(f"Fonte: {self.fonte_atual}")
        self.atualizacao_label.setAlignment(Qt.AlignCenter)
        self.atualizacao_label.setStyleSheet("color: white; font-size: 8pt;")
        main_layout.addWidget(self.atualizacao_label)

        # Status da última atualização
        self.status_label = QLabel(f"Atualizado: {self.ultima_atualizacao}")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: white; font-size: 8pt;")
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)
        self.setFixedSize(160, 165)  # Tamanho fixo para o widget

        # Estilo da janela
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(40, 40, 40, 180);
                border-radius: 10px;
            }
        """)

    def posicionar_widget(self):
        """Posiciona o widget no canto inferior direito da tela"""
        tela = QDesktopWidget().availableGeometry()
        self.move(tela.width() - self.width() - 20, tela.height() - self.height() - 40)

    def atualizar_cotacoes(self):
        """Thread que busca as cotações de moedas usando múltiplas APIs"""
        while self.thread_ativa:
            try:
                # Atualizar usando todas as APIs ativas
                for api in self.apis:
                    if api["ativa"]:
                        try:
                            if api["nome"] == "AwesomeAPI":
                                self.buscar_awesome_api()
                            elif api["nome"] == "Banco Central":
                                self.buscar_banco_central()

                            # Resetar contador de falhas para API bem-sucedida
                            self.contador_falhas[api["nome"]] = 0
                        except Exception as e:
                            print(f"Erro ao buscar cotações na {api['nome']}: {e}")
                            self.contador_falhas[api["nome"]] += 1

                            # Desativar API após 5 falhas consecutivas
                            if self.contador_falhas[api["nome"]] >= 5:
                                api["ativa"] = False

                # Calcular valores a serem exibidos (média ou valor único)
                self.calcular_valores_exibicao()

                # Atualizar horário
                self.ultima_atualizacao = time.strftime("%H:%M:%S")

                # Esperar antes da próxima atualização (30 segundos)
                time.sleep(30)

            except Exception as e:
                print(f"Erro geral ao buscar cotações: {e}")
                time.sleep(10)  # Tentar novamente após 10 segundos

    def buscar_awesome_api(self):
        """Busca cotações na AwesomeAPI"""
        response = requests.get(self.apis[0]["url"], timeout=5)

        if response.status_code == 200:
            data = response.json()

            # Extrair as cotações
            if 'USDBRL' in data:
                self.dolar_valores["AwesomeAPI"] = data['USDBRL']['bid']

            if 'EURBRL' in data:
                self.euro_valores["AwesomeAPI"] = data['EURBRL']['bid']

    def buscar_banco_central(self):
        """Busca cotações no Banco Central do Brasil"""
        # Formatando a data atual no formato requerido (MM-DD-YYYY)
        hoje = datetime.now().strftime('%m-%d-%Y')

        # Construindo a URL com a data formatada
        url = self.apis[1]["url"].format(hoje)

        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()

            # Verificar se há valores retornados
            if 'value' in data and len(data['value']) > 0:
                # O BC retorna cotação de venda
                self.dolar_valores["Banco Central"] = str(data['value'][0]['cotacaoVenda'])

    def calcular_valores_exibicao(self):
        """Calcula os valores a serem exibidos baseado na fonte selecionada"""
        fonte_selecionada = self.fonte_combo.currentText()

        if fonte_selecionada == "Múltiplas Fontes":
            # Calcula média dos valores disponíveis para dólar
            valores_disponiveis = [float(valor) for fonte, valor in self.dolar_valores.items()
                                   if valor != "0.00" and self.apis_esta_ativa(fonte)]

            if valores_disponiveis:
                self.dolar_valor_exibir = "{:.4f}".format(sum(valores_disponiveis) / len(valores_disponiveis))

            # Para o euro, só temos AwesomeAPI por enquanto
            if self.euro_valores["AwesomeAPI"] != "0.00" and self.apis_esta_ativa("AwesomeAPI"):
                self.euro_valor_exibir = self.euro_valores["AwesomeAPI"]

            self.fonte_atual = "Múltiplas Fontes"

        else:
            # Exibe valores da fonte específica selecionada
            if fonte_selecionada in self.dolar_valores and self.dolar_valores[fonte_selecionada] != "0.00":
                self.dolar_valor_exibir = self.dolar_valores[fonte_selecionada]

            if fonte_selecionada in self.euro_valores and self.euro_valores[fonte_selecionada] != "0.00":
                self.euro_valor_exibir = self.euro_valores[fonte_selecionada]
            else:
                self.euro_valor_exibir = "N/D"  # Não disponível

            self.fonte_atual = fonte_selecionada

    def apis_esta_ativa(self, nome_api):
        """Verifica se uma API específica está ativa"""
        for api in self.apis:
            if api["nome"] == nome_api:
                return api["ativa"]
        return False

    def mudar_fonte(self, texto):
        """Altera a fonte de dados exibida"""
        self.calcular_valores_exibicao()
        self.atualizar_interface()

    def atualizar_interface(self):
        """Atualiza os valores na interface"""
        self.dolar_label.setText(f"USD: R$ {self.dolar_valor_exibir}")
        self.euro_label.setText(f"EUR: R$ {self.euro_valor_exibir}")
        self.atualizacao_label.setText(f"Fonte: {self.fonte_atual}")
        self.status_label.setText(f"Atualizado: {self.ultima_atualizacao}")

    def fechar_aplicativo(self):
        """Fecha o aplicativo"""
        self.thread_ativa = False
        self.close()
        sys.exit()

    # Eventos para permitir arrastar a janela
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging and self.offset:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = CotacaoWidget()
    widget.show()
    sys.exit(app.exec_())