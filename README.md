Retrtieval-Augmented Generation

This project was part of the school project that aim to utilize AI to answer student queries.

Objectives

As part of the project, we need to develop a system that help to answer question from international student who first want to begin their journey at Western Sydney.
One of the way to start the journey is through the Western Sydney University International College, where they offer a range of Foundation Courses and Diploma degree to help student have a smoother start before going to the Bachelor Courses.
We responsible to develop an AI Chatbot that helps to guide the student through the challenges that they face as a newbie.

To make the chatbot reliable and accurate for answering queries about the University (e.g., tuition fees, application process, requirements, facilities), we’ll use Retrieval-Augmented Generation (RAG). This approach allows us to provide the LLM with up-to-date, university-specific information for generating answers.

Instead of relying solely on the model's base knowledge—which may not include current or specific details about our University—we’ll set up a retrieval system. This system pulls relevant documents or data from a curated knowledge base whenever a question is asked. The retrieved information is then fed into the LLM as context, enabling it to produce accurate and contextually correct responses.

This approach addresses several challenges:

* Reliability: We ensure the model uses verified, university-specific data rather than its potentially outdated or generic training knowledge.
* Accuracy: With targeted information provided as context, the LLM is more likely to generate answers that align with the latest University guidelines.
* Adaptability: The knowledge base can be updated regularly, allowing the model to reflect any changes in University policies or offerings without retraining the LLM itself.

Data

For the data that are going to be used as the context for the LLMs, we are going scrape the University websites to gather all the information in regard of the University. That is also the most reliable source of information on the Internet in regard of this project and the students can also verify the information themselves.

After gathering all the relevant information, we need to chunk the information or documents into appropriate chunk size where each chunk contain important information about one aspect of the Univeristy. Luckily, by scraping the websites, we were able to store each website as a seperate piece of text document that already contain all the important information about a specific aspect. Therefore, we might not need to furthur split the document.

The database that we choose to store our documents is Pinecone, which is a well-knowned database for AI and also support hybrid vector search. The fact the we were able to retrieve the right documents is because of the vector and what we used in this project are both dense vector and sparse vector. For more information you can visit this link: https://aws.amazon.com/marketplace/pp/prodview-xhgyscinlz4jk?gclid=Cj0KCQiA0MG5BhD1ARIsAEcZtwRgdUHqTRkDhr9t4EBgxX06Kvjg5F5kET9Wh8yx-41kTJB__cQlTeEaAljJEALw_wcB&trk=c2a8609f-dca3-4106-ba87-ca86953c6be1&sc_channel=ps&ef_id=Cj0KCQiA0MG5BhD1ARIsAEcZtwRgdUHqTRkDhr9t4EBgxX06Kvjg5F5kET9Wh8yx-41kTJB__cQlTeEaAljJEALw_wcB:G:s&s_kwcid=AL!4422!3!715844273927!p!!g!!vector%20database!21780389725!165637948782



