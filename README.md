# OCR em DACTE com LightOnOCR-2-1B via Transformers

* DACTE significa Documento Auxiliar de Conhecimento de Transporte Eletrônico.
* OCR significa Optical Character Recognition, ou Reconhecimento Ótico de Caracteres.
* Aspectos chave de OCR:
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
    * Extração de texto das imagens PNG com OCR, onde foi usado o modelo LightOnOCR-2-1B. Referência: [https://huggingface.co/lightonai/LightOnOCR-2-1B](https://huggingface.co/lightonai/LightOnOCR-2-1B)
    * Parsing dos dados: como selecionar e extrair as informações desejadas com organização.
    * Por fim, salvamento em formato CSV para melhor visualização.
* Sobre o modelo LightOnOCR-2-1B:
    * Ele é um modelo de visão computacional end-to-end, eficiente, de 1 bilhão de parâmetros, para converter documentos (PDFs, escaneamentos, imagens) em texto limpo e naturalmente ordenado sem depender de pipelines frágeis. O LightOnOCRAI-2 atinge uma performance no estado da arte no OlmOCR-Bench, que é um dataset com 1,403 arquivos PDF, além de 7,010 test cases que capturam propriedades de output que um bom sistema de OCR deveria gerar, sendo então, um modelo até ~9x menor e significantemente mais rápido do que seus competidores.
    Fontes: [https://huggingface.co/lightonai/LightOnOCR-2-1B](https://huggingface.co/lightonai/LightOnOCR-2-1B) e [https://huggingface.co/datasets/allenai/olmOCR-bench](https://huggingface.co/datasets/allenai/olmOCR-bench)

* Sobre a abordagem usada:
    * À princípio, há duas maneiras de usar o modelo, uma com Transformers (usada aqui) e outra com vLLM.
    * [Transformers](https://huggingface.co/docs/transformers/index) é uma biblioteca Hugging Face construída para ter flexibilidade e suportar diversas arquiteturas diferentes (BERT, RoBERTa, GPT, ViT). É usada principalmente em pesquisa, fine-tuning e experimentação em pequena escala. Ela usa a alocação de memória padrão do PyTorch, o que pode levar a "fragmentação de memória", pois a Key-Value (KV) cache para longas sequências é armazenada em blocos contíguos.
    * [vLLM](https://vllm.ai/), ou Virtual Large Language Model é um motor de inferência especializado. Ele não se importa com treinamento, apenas com gerar output o mais rápido e eficientemente possível. É usado principal em larga escala em ambientes de deployment rápidos e massivos, com um rendimento de 10 até 20x mais requisições por segundo do que a biblioteca transformers padrão. Seu "segredo" é o PagedAttention, o que resolve o gargalo de memória das LLMs com a ideia de memória virtual.

* As instruções de como replicar este trabalho na sua máquina está em TUTORIAL.md

* Citação: @misc{lightonocr2_2026,
        title        = {LightOnOCR: A 1B End-to-End Multilingual Vision-Language Model for State-of-the-Art OCR},
        author       = {Said Taghadouini and Adrien Cavaill\`{e}s and Baptiste Aubertin},
        year         = {2026},
        howpublished = {\url{[https://arxiv.org/abs/2601.14251](https://arxiv.org/abs/2601.14251)}}
        }