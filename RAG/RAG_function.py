from pinecone_text.sparse import BM25Encoder
from pinecone import Pinecone
from langchain_openai import ChatOpenAI
from langchain_community.retrievers import PineconeHybridSearchRetriever
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
import getpass
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    PromptTemplate
)
import typing

class Retrieve:
    def __init__(self):
        self.setup_environment()
        self.initialize_components()

    def setup_environment(self):
        # Set up environment variables
        os.environ["COHERE_API_KEY"] = '6vrypvmzEMJd9gZvgGTVi7uIblcmcxy91qMtG83E'
        self.api_key = "34f8f800-fe59-46d5-916a-a80cde76e225"

    def initialize_components(self):
        # Initialize BM25 encoder and Pinecone index
        bm25 = BM25Encoder().default()
        self.pc = Pinecone(api_key=self.api_key)
        self.pinecone_index = self.pc.Index("handbook")

        # Initialize custom embeddings
        embedding_client = HuggingFaceEmbeddings(model_name='sentence-transformers/msmarco-bert-base-dot-v5')
        retriever = PineconeHybridSearchRetriever(
            embeddings=embedding_client,
            sparse_encoder=bm25,
            index=self.pinecone_index,
            alpha=0.5,
            top_k=100
        )

        # Set up contextual compression
        compressor = CohereRerank(model="rerank-english-v3.0", top_n=1)
        self.compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=retriever
        )

        # Initialize language model (LLM)
        self.llm = ChatOllama(model="llama3")

        # Initialize retrieval and combination chains
        self.combine_docs_chain = create_stuff_documents_chain(self.llm, self.create_chat_prompt())
        self.rag_chain = create_retrieval_chain(self.compression_retriever, self.combine_docs_chain)

    def create_chat_prompt(self):
        # Define the chat prompt template
        return ChatPromptTemplate(
            input_variables=['context', 'input'],
            optional_variables=['chat_history'],
            input_types={'chat_history': typing.List[typing.Any]},
            # Adjust this if necessary based on actual message types
            partial_variables={'chat_history': []},
            messages=[
                SystemMessagePromptTemplate(
                    prompt=PromptTemplate(
                        input_variables=['context', 'input'],
                        template="You are a program advisor at Western Sydney. Based strictly on the provided context, answer the query in a clear, accurate, and concise manner. Only use the information from the retrieved context to ensure relevance.Using the information provided in the context, respond to student inquiries with accurate and relevant details. Focus on providing concise answers specific to their queries about the program structure, subjects, program sequence or admission requirement. \nContext: {context}\nUser Query:{input}.\nRespond with precise and clear information, keeping the focus on the program/subjects."
                    )
                ),
                MessagesPlaceholder(variable_name='chat_history', optional=True),
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate(
                        input_variables=['input'],
                        template='User Query: {input}'
                    )
                )
            ]
        )

    def query(self, input_text):
        # Invoke the RAG chain with the provided input text
        result = self.rag_chain.invoke({"input": input_text})
        for i in (result.get('context')):
            print(i)
        return print(f'Answer:\n {result.get('answer')}')