from collections import defaultdict 
from typing import Dict, List, Tuple
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.services.rag import _llm, _format_docs
from app.services.vectorstore import get_vectorstore

#session_id -> List of (role, text)
_history: Dict[str, List[Tuple[str, str]]]= defaultdict(list)
_condense= ChatPromptTemplate.from_template(
    """Given the chat history and follow up question, rewrite the follow up as standalone question. Return only the rewritten question.
    Chat history: {history}
    Follow-up: {question}
    Standalone question: """
)

_answer= ChatPromptTemplate.from_template(
    """ Answer using ONLY the context. If Unknown say so
    Context: {context}
    Answer: """
)

def _format_history(turns: List[Tuple[str, str]]) -> str:
    return "\n".join(f"{role}: {text}" for role, text in turns) or "(empty)"

def chat(session_id: str, question: str, k: int =4):
    turns= _history[session_id]
    # step-1 : Condense follow-up into standalone question(skip on first turn)
    if turns:
        condense_chain= _condense | _llm | StrOutputParser()
        standalone= condense_chain.invoke(
            {"history": _format_history(turns), "question": question}
            )
    else:
        standalone= question

    #step-2 Retrieve + Answer
    docs= get_vectorstore().as_retriever(
        search_kwargs= {}
    ).invoke(standalone)
    answer_chain= _answer | _llm | StrOutputParser()
    answer= answer_chain.invoke(
        {"context": _format_docs(docs), "question": standalone}
    )
    
    #step-3 Save turn
    turns.append(("User", question))
    turns.append(("Assistant", answer))
    return answer, standalone

def reset(session_id: str):
    _history.pop(session_id, None)
