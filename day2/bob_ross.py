import bs4
from typing import Dict, Any
from colorama import Fore, init
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Constants
MIN_RELEVANCE_SCORE = 5
MIN_HALLUCINATION_SCORE = 7

# Initialize colorama
init(autoreset=True)

def format_docs(docs: list) -> str:
    """Combine document contents into a single formatted string."""
    return "\n\n".join(doc.page_content for doc in docs)

def evaluate_score(prompt: str) -> int:
    """Invoke the LLM with a prompt and extract the numerical score."""
    response = llm.invoke(prompt)
    response_text = response['content'] if isinstance(response, dict) else response.content
    return int(''.join(filter(str.isdigit, response_text)))

def enhanced_rag_chain(question: str) -> Dict[str, Any]:
    """Perform enhanced retrieval-augmented generation with verification."""
    # Retrieve context
    context = retriever.invoke(question)

    # Check relevance
    relevance_prompt = f"""
    Question: {question}
    Retrieved context: {context}
    Rate the relevance of the retrieved context for answering the question (1-10):

    **Return Only Score (1-10)**
    """
    relevance_score = evaluate_score(relevance_prompt)
    if relevance_score < MIN_RELEVANCE_SCORE:
        return {"error": "Cannot find relevant information to answer the question."}

    hallucination_score = 0
    answer = ""

    # Refine answer until hallucination score meets the threshold
    while hallucination_score < MIN_HALLUCINATION_SCORE:
        answer = rag_chain.invoke(question)
        verify_prompt = f"""
        Question: {question}
        Context: {context}
        Generated Answer: {answer}
        
        Verify if the answer is supported by the context. Identify any hallucinations.

        **Return Only Score (1-10)**
        """
        hallucination_score = evaluate_score(verify_prompt)

    return {
        "answer": answer,
        "hallucination_score": hallucination_score,
        "context_used": context
    }

# LLM and retriever setup
llm = ChatOpenAI(model="gpt-4o-mini")

loader = WebBaseLoader(
    web_paths=[
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
        "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
    ],
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)

docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={'k': 6})

prompt = hub.pull("rlm/rag-prompt")
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

result = enhanced_rag_chain("What is Task Decomposition?")
if "error" in result:
    print(Fore.RED + result["error"])
else:
    print("---------")
    print(Fore.GREEN + "Answer: " + str(result["answer"]))
    print(Fore.YELLOW + "Hallucination Score: " + str(result["hallucination_score"]))
