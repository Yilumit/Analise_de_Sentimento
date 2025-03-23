# Análise de Sentimento com Azure Cognitive Services

Este projeto realiza a análise de sentimento e mineração de opiniões de um documento de texto utilizando o serviço **Azure Text Analytics**, salva os resultados em um arquivo com formato JSON e exibe uma saída amigável para visualização do usuário.

## Funcionalidades

- Autenticação com Azure Cognitive Services utilizando chave e endpoint via arquivo `.env`.
- Detecção automática de idioma.
- Análise de sentimentos detalhada (documento, sentenças e opiniões).
- Geração de relatório da análise estruturado em JSON.
- Impressão dos resultados no console.

## Tecnologias Utilizadas

- Python 3.8
- Azure AI Text Analytics SDK
- python-dotenv (Opcional)
- JSON

### Restrições

Para criar um objeto cliente autenticado e conseguir utilizar os recursos de solução Azure AI, é necessário:

1. Ter uma [assinatura Azure][assinatura_azure] e [criar um recurso do Language Service][criar_recurso_linguagem] estando logado no Portal do Azure.
2. Através do recurso criado, obter uma `key`e um `endpoint` do recurso para a conexão com a API.

#### Exemplo de código para autenticação utilizando o arquivo `.env`
```python
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

key= os.getenv('LANGUAGE_KEY')
endpoint = os.getenv('LANGUAGE_ENDPOINT')

text_analytics_client = TextAnalyticsClient(endpoint, AzureKeyCredential(key))
```

Também é possível configurar uma variável de ambiente do próprio sistema, nesse caso o pacote `python-dotenv` não é necessário.

#### Exemplo de código para autenticação com variáveis de ambiente do sistema
```python
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

key= os.environ.get('LANGUAGE_KEY')
endpoint = os.environ.get('LANGUAGE_ENDPOINT')

text_analytics_client = TextAnalyticsClient(endpoint, AzureKeyCredential(key))
```
Caso já tenha uma chave de autenticação e um endpoint configurado nas variáveis de ambiente do sistema, mas deseja utilizar o `python-dotenv` e configurar suas variáveis em `.env` com o mesmo nome, utilize o senguinte comando:

```python
from dotenv import load_dotenv

load_dotenv(override=True)
```

## Como Executar

1. Instale as dependências:

    ```bash
    pip install azure-ai-textanalytics 
    pip install python-dotenv
    ```

2. Configure o arquivo `.env`:
    ```env
    LANGUAGE_KEY=YOUR_AZURE_KEY
    LANGUAGE_ENDPOINT=YOUR_AZURE_ENDPOINT
    ```

3. Adicione o arquivo de entrada na pasta /inputs:

    - Nome do arquivo esperado: `sentencas.txt`

4. Execute o script principal:
    ```bash
    python ./src/analise_de_sentenca.py
    ```

## Saída
O resultado será salvo automaticamente em formato `JSON` em:
```
./outputs/analise_sentimentos.json
```
Exemplo de saida em formato `JSON`:
```json
[
    {
        "sentimento_documento": "mixed",
        "score_geral": {
            "positivo": 0.36,
            "neutro": 0.15,
            "negativo": 0.48
        },
        "sentencas": [
            {
                "texto": "As ruas desta cidade estão muito esburacadas.\n",
                "sentimento": "negative",
                "score": {
                    "positivo": 0.02,
                    "neutro": 0.1,
                    "negativo": 0.89
                },
                "opinions": [
                    {
                        "alvo": {
                            "texto": "ruas",
                            "sentimento": "negative",
                            "score": {
                                "positivo": 0.04,
                                "negativo": 0.96
                            }
                        },
                        "avaliacoes": [
                            {
                                "texto": "esburacadas",
                                "sentimento": "negative",
                                "score": {
                                    "positivo": 0.04,
                                    "negativo": 0.96
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
]
```

## Observações
- O script sobrescreve o arquivo JSON de saída a cada execução.

- A análise usa `show_opinion_mining=True` para trazer insights mais detalhados, como alvos (targets) e avaliações (assessments) nas sentenças

## Insights e Possibilidades
 - Um ótimo jeito de analisar reviews, feedbacks e sugestões em fóruns de conversas, comentários de produtos e serviços entre outras inúmeras possibilidades.
- Existem diversas outras funcionalidades que podem ser exploradas, como detecção de linguagem e extração de informações.
 
|![interferencia](https://imgur.com/z1It3rD.png)|![pontuacao](https://imgur.com/ZMF1whe.png)|
|----------------------|------------------------|
|Foi observado que não há interferência das frases antecessoras nas sucessoras.| A pontuação correta nas frases tem um impacto significativo para o resultado da análise.|

## Licença
Este projeto está sob a licença [MIT][mit_link]. Sinta-se à vontade para utilizar e adaptar conforme necessário.

<!-- links -->
[assinatura_azure]: https://azure.microsoft.com/pt-br/pricing/purchase-options/azure-account?icid=ai-services
[criar_recurso_linguagem]: https://portal.azure.com/#create/Microsoft.CognitiveServicesTextAnalytics
[mit_link]: https://choosealicense.com/licenses/mit/