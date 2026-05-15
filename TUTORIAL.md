# Tutorial: OCR em DACTEs com LightOnOCR-2-1B

> Este tutorial foi escrito para guiar qualquer pessoa — inclusive iniciantes — a replicar este projeto do zero em sua própria máquina.

---

## Sumário

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Requisitos de Hardware](#2-requisitos-de-hardware)
3. [Instalando o Python](#3-instalando-o-python)
4. [Instalando o Git](#4-instalando-o-git)
5. [Clonando o Repositório](#5-clonando-o-repositório)
6. [Criando e Ativando o Ambiente Virtual](#6-criando-e-ativando-o-ambiente-virtual)
7. [Instalando as Dependências](#7-instalando-as-dependências)
8. [Estrutura do Projeto](#8-estrutura-do-projeto)
9. [Como Executar](#9-como-executar)
10. [Saídas Esperadas](#10-saídas-esperadas)
11. [Solução de Problemas Comuns](#11-solução-de-problemas-comuns)

---

## 1. Visão Geral do Projeto

Este projeto realiza **OCR (Reconhecimento Ótico de Caracteres)** em **DACTEs** (Documentos Auxiliares de Conhecimento de Transporte Eletrônico) utilizando o modelo **LightOnOCR-2-1B** da biblioteca Hugging Face Transformers.

O pipeline é composto por **4 etapas**:

```
PDFs de DACTE
      │
      ▼
[1] Conversão: PDF → PNG
      │
      ▼
[2] Extração de texto via OCR (LightOnOCR-2-1B)
      │
      ▼
[3] Parsing e organização dos dados extraídos
      │
      ▼
[4] Exportação para CSV
```

**Principais bibliotecas utilizadas:**

| Biblioteca | Finalidade |
|---|---|
| `torch` | Backend de deep learning (GPU/CPU) |
| `transformers` | Carregamento e inferência do modelo OCR |
| `PyMuPDF` | Conversão de PDF para imagem |
| `Pillow` | Manipulação de imagens |
| `pandas` | Organização e exportação dos dados |
| `BeautifulSoup4` | Parsing do texto extraído |

---

## 2. Requisitos de Hardware

> ⚠️ **Atenção:** O modelo LightOnOCR-2-1B possui **1 bilhão de parâmetros**. O uso de uma **GPU NVIDIA** é fortemente recomendado para um tempo de inferência aceitável.

### Configuração recomendada

| Componente | Mínimo | Recomendado |
|---|---|---|
| RAM | 16 GB | 32 GB |
| VRAM (GPU) | 8 GB | 16 GB+ |
| Espaço em disco | 10 GB livres | 20 GB livres |
| GPU | NVIDIA (CUDA 12+) | NVIDIA RTX 3080 / A100 ou superior |

### Verificando se sua GPU é compatível

Abra um terminal e execute:

```bash
nvidia-smi
```

Se o comando retornar informações sobre sua GPU e a versão do driver CUDA, você está pronto para continuar. Caso o comando não seja reconhecido, o projeto ainda pode ser executado **via CPU**, porém será significativamente mais lento.

---

## 3. Instalando o Python

O projeto requer **Python 3.10 ou superior**.

### Verificando se o Python já está instalado

Abra um terminal (Prompt de Comando no Windows, Terminal no macOS/Linux) e execute:

```bash
python --version
```

ou

```bash
python3 --version
```

Se a versão exibida for `3.10.x` ou superior, pule para a [próxima seção](#4-instalando-o-git).

### Instalando o Python (caso necessário)

#### Windows

1. Acesse [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Clique em **"Download Python 3.x.x"** (versão mais recente)
3. Execute o instalador baixado
4. ✅ **IMPORTANTE:** Marque a opção **"Add Python to PATH"** antes de clicar em *Install Now*
5. Conclua a instalação e reabra o terminal

#### macOS

```bash
# Instalar via Homebrew (recomendado)
brew install python@3.11
```

Se não tiver o Homebrew, instale-o primeiro em [https://brew.sh/](https://brew.sh/).

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip -y
```

---

## 4. Instalando o Git

O Git é necessário para clonar (baixar) o repositório.

### Verificando se o Git já está instalado

```bash
git --version
```

Se retornar uma versão, pule para a [próxima seção](#5-clonando-o-repositório).

### Instalando o Git (caso necessário)

#### Windows

Baixe e instale em: [https://git-scm.com/download/win](https://git-scm.com/download/win)

Durante a instalação, mantenha as opções padrão.

#### macOS

```bash
brew install git
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install git -y
```

---

## 5. Clonando o Repositório

Navegue até a pasta onde deseja salvar o projeto e execute o comando abaixo no terminal, substituindo `<URL_DO_REPOSITORIO>` pela URL do repositório:

```bash
git clone <URL_DO_REPOSITORIO>
```

Em seguida, entre na pasta do projeto:

```bash
cd <NOME_DA_PASTA_DO_PROJETO>
```

> 💡 **Dica:** Para navegar entre pastas no terminal, use `cd nome-da-pasta`. Para listar os arquivos de uma pasta, use `ls` (macOS/Linux) ou `dir` (Windows).

---

## 6. Criando e Ativando o Ambiente Virtual

Um **ambiente virtual** isola as dependências deste projeto das demais instalações do seu sistema, evitando conflitos entre versões de bibliotecas.

### Criando o ambiente virtual

Dentro da pasta do projeto, execute:

```bash
python3 -m venv venv
```

Isso criará uma pasta chamada `venv/` no diretório do projeto.

### Ativando o ambiente virtual

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

Após a ativação, você verá `(venv)` no início da linha do terminal, indicando que o ambiente está ativo:

```
(venv) C:\Users\seu-usuario\projeto>
```

> ⚠️ **Lembre-se:** O ambiente virtual precisa estar **ativo** sempre que for instalar dependências ou executar os scripts. Se fechar o terminal, ative-o novamente antes de continuar.

---

## 7. Instalando as Dependências

Com o ambiente virtual ativo, instale todas as dependências do projeto de uma vez:

```bash
pip install -r requirements.txt
```

> ⏳ Este processo pode levar alguns minutos, pois inclui bibliotecas grandes como `torch` e os pacotes CUDA da NVIDIA.

### Verificando a instalação

Após a conclusão, verifique se as principais bibliotecas foram instaladas corretamente (lembre-se de estar com o ambiente ativo para esse tipo de ação):

```bash
python -c "import torch; import transformers; import fitz; import PIL; import pandas; print('Todas as dependências instaladas com sucesso!')"
```

Se a mensagem `Todas as dependências instaladas com sucesso!` aparecer, você está pronto para executar o projeto.

### Verificando se o PyTorch detecta sua GPU

```bash
python -c "import torch; print('GPU disponível:', torch.cuda.is_available()); print('Dispositivo:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

- Se retornar `GPU disponível: True`, o modelo utilizará a GPU automaticamente.
- Se retornar `GPU disponível: False`, o modelo rodará na CPU (mais lento, mas funcional).

---

## 8. Estrutura do Projeto

Após clonar o repositório, você encontrará a seguinte estrutura de arquivos:

```
OCR_DACTE/
│
├── pdfs_para_conversao/    # Pasta para os PDFs de entrada (DACTEs)
├── imgs_convertidas/       # PNGs gerados a partir dos PDFs
├── DACTEsCSV/              # Arquivos CSV com os dados extraídos
├── LOG/                    # Logs gerados durante a execução
│
├── src/                    # Scripts Python do projeto
│   ├── script_principal.py # Pipeline completo (conversão + OCR + parsing + exportação)
│   ├── script_ocr.py       # Módulo de OCR (carregamento do modelo e inferência)
│   └── script_utils.py     # Funções utilitárias (logging, timers, helpers)
│
├── .gitignore
├── requirements.txt        # Lista de dependências do projeto
├── README.md               # Descrição geral do projeto
└── TUTORIAL.md             # Este arquivo
```

> 📁 **Antes de executar**, coloque seus arquivos PDF de DACTE dentro da pasta `pdfs_para_conversao/`.

---

## 9. Como Executar

Com o ambiente virtual ativo e os PDFs na pasta correta, execute o script principal:

```bash
python script_principal.py
```

### O que acontece durante a execução

O terminal exibirá logs informando o progresso de cada etapa:

```
[INFO] Iniciando conversão de PDFs para PNG...
[INFO] dacte_001.pdf → dacte_001.png ✓
[INFO] Carregando modelo LightOnOCR-2-1B...
[INFO] Processando imagem 1/N...
[INFO] Parsing dos dados extraídos...
[INFO] Exportando resultados para CSV...
[INFO] Concluído. Arquivo salvo em: saidas/resultados/resultado.csv
```

> 💡 O **primeiro carregamento do modelo** pode demorar mais, pois o Hugging Face fará o download dos pesos automaticamente (~2 GB). Nas execuções seguintes, o modelo será carregado do cache local.

---

## 10. Saídas Esperadas

Ao final da execução, os seguintes arquivos serão gerados:

| Pasta | Conteúdo |
|---|---|
| `saidas/imagens/` | Arquivos `.png` de cada página dos PDFs processados |
| `saidas/resultados/` | Arquivo `.csv` com os dados extraídos e organizados de cada DACTE |

O arquivo CSV terá colunas correspondentes aos campos extraídos dos DACTEs, permitindo fácil visualização em ferramentas como Excel, LibreOffice Calc ou Google Sheets.

---

## 11. Solução de Problemas Comuns

### ❌ `python` não é reconhecido no terminal

**Causa:** Python não foi adicionado ao PATH durante a instalação.

**Solução (Windows):** Tente usar `python3` no lugar de `python`. Se não funcionar, reinstale o Python marcando a opção **"Add Python to PATH"**.

---

### ❌ `pip install -r requirements.txt` falha com erros CUDA

**Causa:** Os pacotes NVIDIA do `requirements.txt` são compatíveis com CUDA 12+. Se sua GPU ou driver for mais antigo, pode haver incompatibilidade.

**Solução:** Atualize os drivers da sua GPU em [https://www.nvidia.com/drivers](https://www.nvidia.com/drivers) e tente novamente.

---

### ❌ `CUDA out of memory` durante a inferência

**Causa:** Sua GPU não tem VRAM suficiente para carregar o modelo completo.

**Solução:** Reduza o número de imagens processadas por vez ou execute via CPU adicionando a seguinte variável de ambiente antes de rodar o script:

```bash
# Linux/macOS
CUDA_VISIBLE_DEVICES="" python script_principal.py

# Windows
set CUDA_VISIBLE_DEVICES=
python script_principal.py
```

---

### ❌ O modelo não é baixado automaticamente

**Causa:** Problema de conexão com o Hugging Face Hub.

**Solução:** Verifique sua conexão com a internet. Se estiver atrás de um proxy corporativo, configure as variáveis `HTTP_PROXY` e `HTTPS_PROXY`. Você também pode baixar o modelo manualmente em [https://huggingface.co/lightonai/LightOnOCR-2-1B](https://huggingface.co/lightonai/LightOnOCR-2-1B) e apontar o caminho local no script.

---

### ❌ `ModuleNotFoundError` ao executar os scripts

**Causa:** O ambiente virtual não está ativo, ou as dependências não foram instaladas corretamente.

**Solução:** Certifique-se de que o `(venv)` aparece no início do terminal. Se não aparecer, ative o ambiente virtual novamente (veja a [Seção 6](#6-criando-e-ativando-o-ambiente-virtual)) e reinstale as dependências.

---

## Referências

- Modelo LightOnOCR-2-1B: [https://huggingface.co/lightonai/LightOnOCR-2-1B](https://huggingface.co/lightonai/LightOnOCR-2-1B)
- Benchmark OlmOCR-Bench: [https://huggingface.co/datasets/allenai/olmOCR-bench](https://huggingface.co/datasets/allenai/olmOCR-bench)
- Documentação Transformers: [https://huggingface.co/docs/transformers/index](https://huggingface.co/docs/transformers/index)
- Artigo do modelo: [https://arxiv.org/abs/2601.14251](https://arxiv.org/abs/2601.14251)


