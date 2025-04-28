# Widget de Cotações em Tempo Real - Versão Multi-Fonte
Um widget elegante e confiável que exibe as cotações atualizadas do Dólar e Euro em relação ao Real brasileiro em tempo real. Este aplicativo combina múltiplas fontes de dados para garantir a precisão das cotações exibidas.

## 📋 Características

- ✅ Interface transparente e moderna
- ✅ Sempre visível sobre outras janelas
- ✅ Múltiplas fontes de dados para maior confiabilidade
- ✅ Seletor de fonte para escolher a origem dos dados
- ✅ Atualizações automáticas a cada 30 segundos
- ✅ Sistema de fallback que alterna entre APIs em caso de falha
- ✅ Possibilidade de arrastar para qualquer posição na tela
- ✅ Baixo consumo de recursos do sistema

## 🛠️ Tecnologias Utilizadas

- **Python 3.7+**
- **PyQt5** para a interface gráfica
- **Requests** para chamadas de API
- **Threading** para operações assíncronas
- **JSON** para processamento de dados

## 📊 Fontes de Dados

Este widget utiliza dados de múltiplas fontes oficiais para garantir a precisão:

1. **AwesomeAPI**: API pública que fornece cotações de diversas moedas em tempo real
   - Endpoint: `https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL`

2. **Banco Central do Brasil**: API oficial do Banco Central para cotação do dólar
   - Endpoint: `https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia`

O sistema calcula a média das cotações quando a opção "Múltiplas Fontes" está selecionada, ou exibe o valor específico de cada fonte quando selecionada individualmente.

## 🚀 Instalação

### Código-fonte (Para desenvolvedores)

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/widget-cotacoes.git
   cd widget-cotacoes
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o aplicativo:
   ```bash
   python cotacao_multi_api.py
   ```

## 📦 Criando seu próprio executável

Para criar um arquivo executável personalizado:

1. Instale o PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Gere o executável:
   ```bash
   pyinstaller --onefile --windowed cotacao_multi_api.py
   ```

3. O executável será gerado na pasta `dist`.

## 🎯 Como Usar

- **Iniciar o Widget**: Execute o arquivo .exe ou rode o script Python
- **Escolher Fonte**: Selecione uma fonte específica ou "Múltiplas Fontes" no menu dropdown
- **Mover o Widget**: Clique e arraste para posicioná-lo onde preferir
- **Fechar o Widget**: Clique no botão "×" no canto superior direito

## 🖥️ Compatibilidade

- ✅ Windows 10/11
- ✅ Windows 7/8 (requer atualização do Python)
- ✅ Linux (requer compilação específica)
- ⚠️ macOS (requer adaptações)

## 📝 Personalização

O widget pode ser facilmente personalizado editando os seguintes parâmetros no código:

- **Tamanho**: Altere `self.setFixedSize(160, 165)` para ajustar as dimensões
- **Cores**: Modifique os valores no método `setStyleSheet` para personalizar o tema
- **Frequência de atualização**: Altere o valor de `time.sleep(30)` para modificar o intervalo de atualização 
- **Fontes de dados**: Adicione ou remova APIs na lista `self.apis` no construtor da classe

## 🔧 Solução de Problemas

Se o widget apresentar problemas com uma fonte específica:

1. O sistema tentará automaticamente usar outras fontes disponíveis
2. Após 5 falhas consecutivas em uma fonte, ela será desativada automaticamente
3. Você pode selecionar manualmente outra fonte no menu dropdown
4. Reinicie o aplicativo para tentar reconectar com todas as fontes

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir um issue ou enviar um pull request.

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## 👏 Agradecimentos

- [AwesomeAPI](https://economia.awesomeapi.com.br/) por fornecer a API de cotações gratuita
- [Banco Central do Brasil](https://dadosabertos.bcb.gov.br/) pela API oficial de cotações
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) pela biblioteca de interface gráfica
- [PyInstaller](https://www.pyinstaller.org/) pela ferramenta de criação de executáveis

---

<p align="center">
  Desenvolvido com ❤️ por Celso Custodio Junior
</p>
