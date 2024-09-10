from RAG_function import Retrieve

if __name__ == "__main__":
    advisor = Retrieve()
    response = advisor.query("tell me about the bachelor of data science at Western Sydney")