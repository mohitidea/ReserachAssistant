from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from app.services.vectorstore import get_vectorstore
from typing import Iterator

_llm= ChatOllama(
    model=settings.llm_model, 
    base_url=settings.ollama_base_url,
    tempreture= 0.1
    )

_prompt= ChatPromptTemplate.from_template(
    """you are a precise research assistant. Answer the question using ONLY the 
    context below. If the context does not contain the answer, say 
    "I don't know." 
    Question: {question}
    Answer: """
)

def _format_docs(docs) -> str:
    return "\n\n".join(d.page_content for d in docs)

def answer_question(question: str, K:int =4):
    retriever= get_vectorstore().as_retriever(search_kwargs={"k": K})
    docs= retriever.invoke(question)
    chain= _prompt | _llm | StrOutputParser()
    answer= chain.invoke({"context": _format_docs(docs), "question": question})
    sources= [
        {
            "source": d.metadata.get("source", "unknown"),
            "snippet": d.page_content[:200].replace("\n", " ")
        }
        for d in docs
    ]
    return answer, sources


def stream_answer(question: str, k: int =4) -> Iterator[str]:
    retriever= get_vectorstore().as_retriever(search_kwargs={"k": k})
    docs= retriever.invoke(question)
    chain= _prompt | _llm | StrOutputParser()
    for token in chain.stream({"context": _format_docs(docs), "question": question}):
        yield token







