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


