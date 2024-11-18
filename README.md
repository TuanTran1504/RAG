Retrtieval-Augmented Generation

This project was part of the school project that aim to utilize AI to answer student queries.

**Objectives**

As part of the project, we need to develop a system that help to answer question from international student who first want to begin their journey at Western Sydney.
One of the way to start the journey is through the Western Sydney University International College, where they offer a range of Foundation Courses and Diploma degree to help student have a smoother start before going to the Bachelor Courses.
We responsible to develop an AI Chatbot that helps to guide the student through the challenges that they face as a newbie.

To make the chatbot reliable and accurate for answering queries about the University (e.g., tuition fees, application process, requirements, facilities), we’ll use Retrieval-Augmented Generation (RAG). This approach allows us to provide the LLM with up-to-date, university-specific information for generating answers.

Instead of relying solely on the model's base knowledge—which may not include current or specific details about our University—we’ll set up a retrieval system. This system pulls relevant documents or data from a curated knowledge base whenever a question is asked. The retrieved information is then fed into the LLM as context, enabling it to produce accurate and contextually correct responses.

This approach addresses several challenges:

* Reliability: We ensure the model uses verified, university-specific data rather than its potentially outdated or generic training knowledge.
* Accuracy: With targeted information provided as context, the LLM is more likely to generate answers that align with the latest University guidelines.
* Adaptability: The knowledge base can be updated regularly, allowing the model to reflect any changes in University policies or offerings without retraining the LLM itself.

**Data**

For the data that are going to be used as the context for the LLMs, we are going scrape the University websites to gather all the information in regard of the University. That is also the most reliable source of information on the Internet in regard of this project and the students can also verify the information themselves.

After gathering all the relevant information, we need to chunk the information or documents into appropriate chunk size where each chunk contain important information about one aspect of the Univeristy. Luckily, by scraping the websites, we were able to store each website as a seperate piece of text document that already contain all the important information about a specific aspect. Therefore, we might not need to furthur split the document.

The database that we choose to store our documents is Pinecone, which is a well-knowned database for AI and also support hybrid vector search. The fact the we were able to retrieve the right documents is because of the vector and what we used in this project are both dense vector and sparse vector. For more information you can visit this link: https://aws.amazon.com/marketplace/pp/prodview-xhgyscinlz4jk?gclid=Cj0KCQiA0MG5BhD1ARIsAEcZtwRgdUHqTRkDhr9t4EBgxX06Kvjg5F5kET9Wh8yx-41kTJB__cQlTeEaAljJEALw_wcB&trk=c2a8609f-dca3-4106-ba87-ca86953c6be1&sc_channel=ps&ef_id=Cj0KCQiA0MG5BhD1ARIsAEcZtwRgdUHqTRkDhr9t4EBgxX06Kvjg5F5kET9Wh8yx-41kTJB__cQlTeEaAljJEALw_wcB:G:s&s_kwcid=AL!4422!3!715844273927!p!!g!!vector%20database!21780389725!165637948782

**Pipeline**

Now we have completed the pre-processing phase in which we have prepared the data that we need for the generation that are being stored in a vectore database (Pinecone). The next step is to invoke the generation with the question.

The framework that we choose here is Langchain, which helps to connect different component of the generation pipeline together as a coherent process. In addition, we use Langgraph to further tailor the pipeline, directing the LLMs to align with our specific objectives.



<img width="1133" alt="image" src="https://github.com/user-attachments/assets/ad2bdb6a-76cf-4fbe-aa97-051b98194b8a">




Langgraph allowed us to connect different nodes together to create a pipeline. For example,in the first step of the generation, we feed the retriver with a question and the retriever will return several relevant documents.



<img width="684" alt="image" src="https://github.com/user-attachments/assets/afc41640-a8ec-4cae-9bc0-2fd1e8bbaf04">



An interesting part of Langgrapth is we can have conditional edges where it will guide the process to different nodes depends on the result of the current nodes. We can use that to create fallback step where one component is not sufficiently perform. For exmaple, if we did not find any relevant information from the database, we can change the path to go to the Web Search. In order to do that, we need to use another LLM to grade the documents that we found and output a binary answer "yes" or "no" which help us to decide where to go next. 



<img width="1092" alt="image" src="https://github.com/user-attachments/assets/1e6738c6-8262-4a62-bc85-b476162946b3">


The ultimate reason why we need to do this is to reduce the hallucination of the LLMs as much as possible, and we dont want the LLMs to generate the answer when we accidentally provide a wrong context to it.

**Evaluation**

In the evaluation step, we’re implementing RAGAS along with its key evaluation metrics: Faithfulness, Response Relevancy, and Factual Correctness. These metrics allow us to gauge how accurately and effectively the LLM responses align with the intended information, directly addressing concerns around consistency, reliability, and user experience.

Faithfulness helps us ensure that responses stay true to the source material, minimizing the risk of hallucinated or inaccurate information. Response Relevancy measures how pertinent and contextually relevant the responses are, which is essential for providing users with answers that align closely with their inquiries. Factual Correctness, perhaps one of the most critical metrics, assesses the factual accuracy of the output, an indispensable factor in establishing trustworthiness and credibility in the responses.

You can read more information about the metrics in this link: https://docs.ragas.io/en/stable/.

The importance of this evaluation step is hard to overstate—it enables us to identify and address fundamental issues in our pipeline that might compromise quality. By rigorously assessing and iterating based on these metrics, we can refine the model's performance, increase user trust, and ensure the pipeline produces responses that are accurate, relevant, and faithful to the intended information.

<img width="1518" alt="image" src="https://github.com/user-attachments/assets/9f62a6ae-5203-4676-bc11-313dc0b9318d">

**Conclusion**

This project’s complexity means we may never truly reach a definitive endpoint, as there will always be room for refinement and improvement. Stay curious, embrace trial and error, and remember there’s always potential to make it better.

