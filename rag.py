

from uuid import uuid4
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Constants
CHUNK_SIZE = 1000
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
COLLECTION_NAME = "real_estate"

llm = None
vector_store = None


def initialize_components():
    global llm, vector_store

    if llm is None:
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.9, max_tokens=500)

    if vector_store is None:
        ef = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"trust_remote_code": True}
        )

        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=ef,
            persist_directory=str(VECTORSTORE_DIR)
        )


def process_urls(urls):
    """
    This function scraps data from a url and stores it in a vector db
    :param urls: input urls
    :return:
    """
    yield "Initializing Components"
    initialize_components()

    yield "Resetting vector store...✅"
    vector_store.reset_collection()

    yield "Loading data...✅"
    # Add comprehensive headers to bypass anti-scraping measures
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Cache-Control": "max-age=0"
    }
    
    try:
        loader = UnstructuredURLLoader(
            urls=urls, 
            headers=headers,
            ssl_verify=True  # Keep SSL verification for security
        )
        data = loader.load()
        
        # Check if we got actual content or just error pages
        if not data:
            yield "⚠️ Warning: No data retrieved. The website might be blocking access."
        elif all(len(doc.page_content) < 500 for doc in data):
            yield "⚠️ Warning: Retrieved content seems very short. The website might be blocking access."
        else:
            yield f"Successfully loaded {len(data)} document(s) ✅"
    except Exception as e:
        yield f"❌ Error loading URLs: {str(e)}"
        yield "💡 Tip: Try using Wikipedia, Investopedia, or government sites (.gov)"
        return

    yield "Splitting text into chunks...✅"
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "],
        chunk_size=CHUNK_SIZE
    )
    docs = text_splitter.split_documents(data)

    yield "Add chunks to vector database...✅"
    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(docs, ids=uuids)

    yield "Done adding docs to vector database...✅"

def generate_answer(query):
    if not vector_store:
        raise RuntimeError("Vector database is not initialized ")

    # Create retriever
    retriever = vector_store.as_retriever()
    
    # Create prompt template
    template = """Answer the question based only on the following context. Include the source URLs if available.

Context: {context}

Question: {question}

Answer: """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Format documents function
    def format_docs(docs):
        sources = set()
        context_text = []
        for doc in docs:
            context_text.append(doc.page_content)
            if hasattr(doc, 'metadata') and 'source' in doc.metadata:
                sources.add(doc.metadata['source'])
        return "\n\n".join(context_text), list(sources)
    
    # Create the chain using LCEL
    retrieved_docs = retriever.invoke(query)
    context, sources = format_docs(retrieved_docs)
    
    # Generate answer
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": context, "question": query})
    
    return answer, "\n".join(sources) if sources else ""


if __name__ == "__main__":
    urls = [
        "https://www.cnbc.com/2024/12/21/how-the-federal-reserves-rate-policy-affects-mortgages.html",
        "https://www.cnbc.com/2024/12/20/why-mortgage-rates-jumped-despite-fed-interest-rate-cut.html"
    ]

    # Process URLs and consume the generator
    for status in process_urls(urls):
        print(status)
    
    # Now generate answer
    answer, sources = generate_answer("Tell me what was the 30 year fixed mortagate rate along with the date?")
    print(f"\nAnswer: {answer}")
    print(f"Sources: {sources}")