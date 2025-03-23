import os
import json
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def autenticacao_cliente():
    load_dotenv(override=True) #Possibilita a sobrescrita das variaveis de ambiente pelas variaveis de .env

    key= os.getenv('LANGUAGE_KEY')
    endpoint = os.getenv('LANGUAGE_ENDPOINT')

    return TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key) )


def analise_de_sentenca(sessao: TextAnalyticsClient):
    #Buscar arquivo para analise
    caminho_documento = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../inputs/sentencas.txt"))

    with open(caminho_documento, ) as fd:
        sentencas = [fd.read()]

    #Analise do texto
    resultado = sessao.analyze_sentiment(sentencas, show_opinion_mining=True) #Fornece analise mais detalhada do sentimento
    doc_result = [doc for doc in resultado if not doc.is_error] #Filtra para extrair somente analises que nao houveram erro

    analise_json = []

    #Saida
    for documento in doc_result:
        print(f"Sentimento do Documento: {documento.sentiment}")
        print(f"""Score Geral:"
Positivo={documento.confidence_scores.positive:.2f}
Neutro={documento.confidence_scores.neutral:.2f}
Negativo={documento.confidence_scores.negative:.2f}
        """)

        #json
        doc_data = {
            "sentimento_documento": documento.sentiment,
            "score_geral": {
                "positivo": round(documento.confidence_scores.positive, 2),
                "neutro": round(documento.confidence_scores.neutral, 2),
                "negativo": round(documento.confidence_scores.negative, 2)
            },
            "sentencas": []
        }

        for sentenca in documento.sentences:
            print(f"Texto: {sentenca.text}")
            print(f"Sentimento do texto: {sentenca.sentiment}")
            print(f"""Score do texto:
Positivo={sentenca.confidence_scores.positive:.2f}
Neutro={sentenca.confidence_scores.neutral:.2f}
Negativo={sentenca.confidence_scores.negative:.2f}
            """)

            sentenca_data = {
                "texto": sentenca.text,
                "sentimento": sentenca.sentiment,
                "score": {
                    "positivo": round(sentenca.confidence_scores.positive, 2),
                    "neutro": round(sentenca.confidence_scores.neutral, 2),
                    "negativo": round(sentenca.confidence_scores.negative, 2)
                },
                "opinions": []
            }
            for opiniao in sentenca.mined_opinions:
                target = opiniao.target
                print(f"......{target.sentiment} alvo {target.text}")
                print(f"Score do alvo:\nPositivo={target.confidence_scores.positive:.2f}\nNegativo={target.confidence_scores.negative:.2f}", end='\n\n')
                
                opin_data = {
                    "alvo": {
                        "texto": opiniao.target.text,
                        "sentimento": opiniao.target.sentiment,
                        "score": {
                            "positivo": round(target.confidence_scores.positive, 2),
                            "negativo": round(target.confidence_scores.negative, 2)
                        }
                    },
                    "avaliacoes": []
                }

                for avaliacao in opiniao.assessments:
                    print("......'{}' assessment '{}'".format(avaliacao.sentiment, avaliacao.text))
                    print(f"Score da avaliacao:\nPositivo={avaliacao.confidence_scores.positive:.2f}\nNegativo={avaliacao.confidence_scores.negative:.2f}", end='\n\n')

                    opin_data["avaliacoes"].append({
                        "texto": avaliacao.text,
                        "sentimento": avaliacao.sentiment,
                        "score": {
                            "positivo": round(avaliacao.confidence_scores.positive, 2),
                            "negativo": round(avaliacao.confidence_scores.negative, 2)
                        }
                    })
                    print()

                print()
                sentenca_data["opinions"].append(opin_data)
                
            print()
            doc_data["sentencas"].append(sentenca_data)

        analise_json.append(doc_data)

        print(end='\n\n')
    print(end='\n\n')

    #Arquivo de saida
    arquivo_json = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../outputs/analise_sentimentos.json"))  

    with open(arquivo_json, mode='w') as f: #Foi optado por sobrescrever o arquivo a cada analise
        json.dump(analise_json, f, ensure_ascii=False, indent=4)



sessao = autenticacao_cliente()

if __name__ == "__main__":
    analise_de_sentenca(sessao)
    