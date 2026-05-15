# OCR EM DACTE
* DACTE significa Documento Auxiliar de Conhecimento de Transporte Eletrônico.
* OCR significa Optical Character Recognition, ou Reconhecimento Ótico de Caracteres.
* Aspectos chave:
    * Digitalização: converte imagens estáticas de texto em texto legível pela máquina.
    * Funcionalidade: analisa as estruturas dos caracteres, reconhece padrões e os converte em texto digital, permitindo a edição, pesquisa e armazenamento deles.
    * Usos comuns: é muito usado para converter recibos, invoices/notas fiscais, extração de dados para automação e digitalização de livros.
* Por que OCR é importante:
    * Eficiência: elimina a necessidade de entrada manual de dados.
    * Acessibilidade: faz com que documentos se tornem pesquisáveis, permitindo que os usuários encontrem informações específicas em meio a grandes quantidades de documentos.
    * Otimização de Workflow: pode prover automação em áreas como: saúde, finanças, legal, transformando documentos físicos em informações digitais úteis.
* Como ele funciona:
    * Pré-processamento: pode melhorar a qualidade da imagem, removendo ruídos, distorções e desequilíbrios.
    * Reconhecimeto textual: usa IA ou reconhecimento de padrões para identificar caracteres.
    * Pós-processamento: remonta o texto em palavras e sentenças coerentes.
* O projeto consiste em 4 etapas:
    * Conversão dos dados (DACTEs) de PDF para PNG.
    * Extração de texto das imagens PNG com OCR, onde foi usado o modelo LightOnOCR-2-1B (referência: https://huggingface.co/lightonai/LightOnOCR-2-1B)
    * Parsing dos dados: como selecionar e extrair as informações desejadas com organização.
    * Por fim, salvamento em formato CSV para melhor visualização.
    
* As instruções de como replicar este trabalho na sua máquina está em TUTORIAL.md