from django.shortcuts import render
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader


api_key = "key"
os.environ["GROQ_API_KEY"] = api_key

chat = ChatGroq(model="llama-3.3-70b-versatile")


def home(request):
    link = ""
    instrucao = ""
    resposta = ""

    if request.method == "POST":
        link = request.POST.get("link")
        instrucao = request.POST.get("instrucao")

        loader = WebBaseLoader(link)
        lista_documentos = loader.load()

        documento = ""
        for doc in lista_documentos:
            documento += doc.page_content

        template = ChatPromptTemplate.from_messages([
            ("system", "Você é uma assistente explicativa que tem acesso às seguintes informações para responder: {documentos_informados}"),
            ("user", "{input}")
        ])

        chain = template | chat

        resposta_obj = chain.invoke({
            "documentos_informados": documento,
            "input": instrucao
        })

        resposta = resposta_obj.content

    return render(request, "home.html", {
        "link": link,
        "instrucao": instrucao,
        "resposta": resposta
    })