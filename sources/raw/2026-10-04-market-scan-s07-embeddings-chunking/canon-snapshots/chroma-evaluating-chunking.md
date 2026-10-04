# Snapshot — https://research.trychroma.com/evaluating-chunking

Fetched 2026-10-04 by the main session with curl (HTML stripped to text; verbatim words).

Evaluating Chunking Strategies for Retrieval | Chroma

Products
SyncDatabaseAgent
DocsResearch
Resources
Use casesUpdatesVideosChangelogDiscordGitHubSupportHidden

Pricing27kLog inSign up

Chroma Technical Report
July 3, 2024

Evaluating Chunking Strategies for Retrieval
Brandon Smith 
Anton Troynikov 

Despite document chunking being virtually ubiquitous as a pre-processing step, little work has been done to investigate its impact on retrieval performance. This is partially due to the structure of commonly used information retrieval benchmarks, which are aimed at whole-document retrieval tasks.
In this work we present an evaluation approach which takes token-level relevance into account, and allows for the evaluation of several popular document chunking strategies. We demonstrate that the choice of chunking strategy can have a significant impact on retrieval performance, with some strategies outperforming others by up to 9% in recall.

Evaluation of various popular chunking strategies on our evaluation, as well as new (★) strategies we propose. We show that the choice of chunking strategy can have significant impact on retrieval performance, in terms of accuracy and efficiency. Size denotes chunk size in tokens, in brackets indicates mean chunk size where it may vary by chunking strategy. Overlap denotes the chunk overlap in tokens. Bold values highlight the best performance in each category. See metrics section for details of each metric.Chunking is a commonly used pre-processing step when ingesting documents for retrieval in the context of AI applications. Chunking serves to divide documents into units of information, with semantic content suitable for embeddings-based retrieval and processing by an LLM.

The purpose of this technical report is to evaluate the impact of the choice of chunking strategy on retrieval performance, in a way representative of how chunking and retrieval is used in the context of AI applications.

While LLM context lengths have grown, and it has become possible to insert entire documents, or even text corpora into the context window, in practice doing so is often inefficient, and can distract the model. For any given query, only a small portion of the text corpus is likely to be relevant, but all tokens in the context window are processed for each inference. Ideally, for each query, the LLM would only need to process only the relevant tokens, and hence one of the primary goals of a retrieval system in AI applications is to identify and retrieve only the relevant tokens for a given query.

Commonly used benchmarks like MTEB take a traditional information retrieval (IR) approach, where retrieval performance is typically evaluated with respect to the relevance of entire documents, rather than at the level of passages or tokens, meaning they cannot take chunking into account.

In AI applications, excerpts containing all tokens relevant to a query may be found within or across many documents. Chunks may contain both relevant and irrelevant tokens, and relevant excerpts may be split across chunks.
Traditional IR benchmarks also often focus on the relative ranking of the retrieved documents, however in practice, LLMs are relatively insensitive to the position of the relevant information within the context window. Additionally, the information relevant to a given query may be spread across multiple documents, making the evaluation of relative ranking between documents ambiguous.

Motivated by these limitations, we propose a new evaluation strategy, evaluating retrieval performance at the token level. Our evaluation uses an LLM to generate, and subsequently filter, a set of queries and associated relevant exerpts from any given text corpus, and subsequently evaluates retrieval performance via precision, recall, and intersection-over-union (Jaccard index) on the basis of retrieved tokens.

Our evaluation takes a fine-grained, token-wise approach to evaluating retrieval accuracy and efficiency, which allows it to take components such as chunking into account. The presence or absence or relevant tokens is more important than their relative ranking in AI applications.
We generate a concrete dataset across various domains with varying data cleanliness, and use this to evaluate the performance of a several popular chunking strategies. We find that the choice of chunking strategy has significant impact on retrieval accuracy and efficiency. Notably, we find that default settings for certain popular chunking strategies can lead to relatively poor performance. We also find that heuristic chunking strategies such as the popular RecursiveCharacterTextSplitter often perform well in practice when parametrized appropriately.

Finally, we propose and evaluate two novel chunking strategies; ClusterSemanticChunker, which uses embedding models directly to compose chunks up to a given size on the basis of semantic similarity, and LLMChunker, which prompts an LLM directly to perform chunking over a text corpus. We find that both produce competitive results on our evaluation.

We provide all code to replicate our results as a GitHub repo, along with useful utilities for similar experiments. We hope that this preliminary work will inspire further research into factors affecting real world performance of retrieval systems for AI applications.

Our in-depth technical report continues below. If you find our work useful, please consider citing us:

plaintext

@techreport{smith2024evaluating,
 title = {Evaluating Chunking Strategies for Retrieval},
 author = {Smith, Brandon and Troynikov, Anton},
 year = {2024},
 month = {July},
 institution = {Chroma},
 url = {https://trychroma.com/research/evaluating-chunking},
}

Thanks to Douwe Kiela and Chris Manning for their feedback on this work.

Interested in working on improving retrieval for AI applications? Chroma is Hiring

Introduction#

Besides answering questions and generating text [1], recently Large Language Models (LLMs) have emerged as a new type of computing primitive, capable of processing unstructured information in a "common sense" way, leading to the creation of AI applications. A key element of AI applications is so-called Retrieval-Augmented Generation (RAG)[2], wherein external data which is semantically relevant to the current task is retrieved for processing. In contrast to traditional IR, retrieval for AI applications often relies on storing and retrieving document parts (chunks), sometimes across several documents, in order to present the most relevant information to the LLM. Thus, in the AI application use-case, which tokens and chunks are returned is often as important as which documents.

Information Retrieval (IR) in general, and passage retrieval in particular, are long-studied problems in natural language processing, with a considerable literature [3][4][5]. However, benchmarks like the Massive Text Embedding Benchmark (MTEB) [6] and MSMARCO[10] do not account for token efficiency, or chunking, and usually evaluate on the basis of the relevance of entire retrieved documents. Additionally, the normalized Discounted Cumulative Gain (nDCG@K) metric, commonly used in IR [7], is less useful in the context of RAG because the rank order of retrieved documents is less important. It has been shown that as long as the relevant tokens are present, and the overall context is of reasonable length, LLMs can accurately process the information regardless of token position [8].

To address these shortcomings, we propose a new evaluation designed to capture the essential details of retrieval performance in the AI application context, consisting of a generative dataset, and a new performance measure. We describe the pipeline that generates the dataset, allowing others to generate domain specific evaluations for their own data and use cases. Because the dataset is generated, in general it should not exist in the training set of any general-purpose embedding model. Along with the dataset, we introduce a new measure of performance, based on the Jaccard similarity coefficient [11] at the token level, which we refer to as Intersection over Union (IoU) for short, as well as evaluating recall and precision at the token rather than document level. By analogy to its use in computer vision, we can think of text chunks as bounding boxes, and the IoU as a measure of how well the bounding boxes of the retrieved chunks overlap with the bounding boxes of the relevant tokens.

As an application of our new evaluation strategy, we compare the performance of popular document chunking methods, such as the RecursiveCharacterTextSplitter. We also develop and evaluate two new chunking methods, the ClusterSemanticChunker which takes the embedding model used for retrieval into account, and LLMChunker, which prompts an LLM directly to perform chunking over a text corpus.

Contributions#

We present the following:

A framework for generating domain specific datasets to evaluate retrieval quality in the context of AI applications, as well as a new measure of retrieval quality which takes chunking strategies into account.

We use this framework to generate a concrete evaluation dataset for a limited set of popular domains, and subsequently we evaluate several commonly-used document chunking strategies according to the proposed measures.

We present and evaluate new chunking strategies, including an embedding-model aware chunking strategy, the ClusterSemanticChunker, which uses any given embedding model to produce a partition of chunks, as well as the LLMChunker which prompts an LLM to perform the chunking task directly.

Finally, we provide the complete codebase for this project.

Related Work#

Current popular Information Retrieval (IR) benchmarks include the Massive Text Embedding Benchmark (MTEB) [6] and Benchmarking-IR (BEIR) [7]. MTEB evaluates text embedding models across 58 datasets and 8 tasks. BEIR includes 18 datasets across 9 retrieval tasks. The MTEB text retrieval datasets contain all publicly available BEIR retrieval datasets. Their primary metric is normalized Discounted Cumulative Gain at rank 10 (nDCG@10), and they both provide Mean Average Precision at rank k (MAP@k), precision@k and recall@k additionally.

The nDCG@K metric evaluates the relevance of K retrieved documents, giving more weight to higher-ranked documents, penalizing relevant results that appear lower in the ranking. Similarly, MAP@K takes the average of the precision at each position in the top K retrieved documents. As mentioned in the introduction, the order of retrieved documents is less important in the context of RAG. Additionally, existing benchmarks evaluate retrieval system performance at the document level, while for AI applications, only a fraction of the tokens in any document may be relevant to a particular query, and relevant tokens may be found across an entire corpus. Our proposed evaluation metrics aim to take this token-level relevance into account.

Along with information retrieval in general, there has been extensive work on passage retrieval [9], including at large scales and in a machine learning context as with the MS MARCO dataset [10]. However, this work has mostly been considered as either an intermediate step to document retrieval, or in the general context of search and retrieval, rather than in the specific context of retrieval for AI applications, and without reference to token efficiency.

More recently, LLMs have been used to directly evaluate retrieval performance, for example by prompting the LLM for a binary classification of relevancy as in ARAGOG [12]. LLMs have also been used to generate synthetic data from a text corpus, as well as evaluating the final generated output of a RAG pipeline as in RAGAS [13]. In contrast, our proposed evaluation focuses only on retrieval, with a limited step to synthesize queries from document corpora, rather than complex multi-step synthesis and evaluation pipelines which may be sensitive to model particulars and prompting. We evaluate retrieval directly, without relying on an LLM. In principle, our proposed approach can be composed with others to produce a more complete evaluation.

Despite the fact that chunking is often the first step of data ingestion in RAG pipelines, the literature on evaluating chunking strategies is sparse. Greg Kamradt's work on semantic chunking was incorporated by LangChain [14], and Aurelio AI developed its own version [15]. Additionally, Unstructured explored chunking in financial contexts, focusing on metadata about chunks based on their document position rather than optimal text partitioning [16]. These efforts highlight the emerging interest evaluations of chunking for RAG, yet there remains a significant gap in comprehensive evaluation, which our works is intended to address.

Evaluating Retrieval for AI Applications#

We introduce our evaluation framework for retrieval in the context of AI applications, consisting of a generative evaluation dataset from a supplied corpus of documents, as well as a new metric based on the well-known Jaccard similarity coefficient, token-wise Intersection over Union (IoU) which takes chunking strategies into account, and corresponds to the token efficiency of the retrieval system. We use this metric alongside other measures such as recall to evaluate the effectiveness of retrieval systems in the AI application context.

This approach to partially synthetic data generation ensures that data generated this way was not available at training time for any general-purpose embedding model, preventing possible bias. Our approach also allows for domain-specific evaluation, making it suitable for evaluating retrieval quality on any dataset. Finally, our approach can be used in combination with other evaluation approaches, including the use of human labels.

Dataset Generation#

For a given text corpus consisting of a set of documents, we sample from an LLM to generate a query relevant to the documents, as well as excerpts from the corpus which are relevant to the generated query. We present the LLM with a prompt consisting of documents from the evaluation corpus, instructions to generate factual queries about the corpus, and to provide excerpts corresponding to the generated questions.

To ensure the queries are unique, we include a random sample of up to 50 previously generated queries in the prompt. We accept only excerpts which have full-text matches within the corpus as valid. We reject any query and all associated excerpts, if any excerpt is invalid.

Query: What were the main characteristics of the armor used on the ship Atlanta?
Excerpts:

"Her armor was backed by 3 inches ( 76 mm ) of oak , vertically oriented , and
two layers of 7 @.@ 5 inches ( 191 mm ) of pine , alternating in direction "

"The upper portion of Atlanta 's hull received two inches of armor "

An example query and set of excerpts generated from the Wikitexts corpus, one of the 474 queries in our generated dataset, sampled from GPT-4-Turbo in JSON mode. Excerpts are exact matches from the Wikitexts corpus.
In order to reduce the instance of compound queries, e.g. "What was the date and significance of the Gettysburg Address?", which may complicate evaluation, we prompt the LLM to avoid using the connecting form of 'and', allowing it only when used as part of a proper noun.

For details of our prompt, see the appendix.

Dataset Prefiltering#

To ensure high quality queries and excerpts we filter the outputs of the initial generation step.

Despite prompting to avoid duplicate generated queries, the LLM will occasionally still generate duplicates or near-duplicates. We de-duplicate the generated dataset by embedding each query, and computing the cosine similarity between the embeddings of all pairs of queries. Subsequently, we filter all queries and associated excerpts where the cosine similarity is above a certain threshold value.

We note that the LLM will occasionally produce excerpts which are out-of-context or irrelevant to the query. In order to mitigate this, we embed each query and its associated excerpts, and compute the cosine similarity from the query to each of them. We filter any query and all its associated excerpts, where the query's cosine similarity with any of its associated excerpts is less than a set threshold.

The choice of threshold values for both duplicate queries and excerpt relevance is dataset dependent. We provide details of the threshold values used in the details of our concrete dataset. We use OpenAI's text-embedding-3-large as the embedding model.

We observe that the latter threshold sets a minimum cosine similarity between a query and its related excerpts. Although this might introduce a sampling bias, it is important to note that each excerpt is part of one or more text chunks, with each chunk being one among many from a given corpus. Additionally, because we perform our evaluation over multiple embedding models, the impact of this bias is negligible in practice.

We note also that although we filter aggressively to ensure generated excerpts are relevant to each query, we do not search for other exceprts in the corpus which might be relevant to the query but were not generated. This is a limitation of our current approach, which future work may mitigate by using supervised or semi-supervised methods.

Metrics#

For a given query related to a specific corpus, only a subset of tokens within that corpus will be relevant. Ideally, for both efficiency and accuracy, the retrieval system should retrieve exactly and only the relevant tokens for each query across the entire corpus.

In practice, the unit of retrieval for AI applications is usually a text chunk containing the relevant excerpt. This chunk will often contain superfluous tokens which require additional compute to process, and which may contain irrelevant distractors which may reduce overall performance of the RAG application [17]. Additionally, where a chunking strategy uses overlapping chunks, the retriever may return redundant tokens, for example if tokens from a relevant excerpt are in more than one chunk due to overlap. Finally, a given retriever may not retrieve all necessary excerpts for a given query.

We therefore seek a metric which can take into account not only whether relevant excerpts are retrieved, but also how many irrelevant, redundant, or distracting tokens are also retrieved. Inspired by a similar metric in computer vision and data mining, the Jaccard similarity [11], we propose the token-wise Intersection over Union (IoU) metric for evaluating the efficiency of a retrieval system [18].

We compute IoU for a given query and chunked corpus 
 as follows. For a query $q$, we denote the set of tokens among all relevant excerpts $t_e$. The set of all retrieved chunks consists of tokens $t_r$.

We compute IoU for a given query in the chunked corpus as:

Note that in the numerator, we count each $t_e$ among $t_r$ only once, while counting all retrieved tokens in $|t_r|$ in the denominator. This accounts for the case where redundant excerpt tokens appear in multiple retrieved chunks, for example where an overlapping chunking strategy is used.

Along with IoU, we propose to use precision and recall metrics in a similar way as they are traditionally used in information retrieval, but at the token rather than the document level.

We define precision as:

And recall as:

When performing our evaluations, we report the mean of IoU, Precision, and Recall, across all queries and all corpora in our dataset. Additionally, we report precision for the case that all chunks containing excerpt tokens are successfully retrieved as Precision$_\Omega$. This gives an upper bound on token efficiency given perfect recall.

We note that we could also compute the F-score ($F_1$) as:

But in practice, IoU provides similar information while preserving a more intuitive 'bounding box' analogy.

Chunking Evaluation Dataset#

We use our evaluation framework to generate a dataset for evaluating chunking strategies for retrieval for AI applications.

Corpora#

We selected five diverse corpora for our dataset, ensuring a mix of both clean and messy text sources. Clean corpora contain well-structured text, while messy corpora reflect the unstructured nature of text typically obtained from web scraping. Each corpus is briefly described below. We provide the length of each corpus in tokens, measured with Tiktoken for "cl100k_base" (the standard used by OpenAI's GPT-4). All Hugging Face corpora are subsets of the full corpora, and the lengths provided refer to the subsets we used. These subsets always start from the beginning of the text as it is on Hugging Face.

While these corpora are relatively small in comparison to most large-scale retreival benchmarks, our aim is to demonstrate the utility of our evaluation framework on representative data, provide easily reproduced results, and to provide a starting point for future work. We do not claim that the concrete dataset we present is comprehensive, but rather that it demonstrates the utility of our evaluation framework.

State of the Union Address 2024 [19]#

This is a plain transcript of the State of the Union Address in 2024. It is well-structured and clear. This corpus is 10,444 tokens long.

Wikitext [20]#

The WikiText language modeling dataset consists of over 100 million tokens from verified Good and Featured articles on Wikipedia. Our subset is the first 26,649 tokens of this text as it appears on Hugging Face.

Chatlogs [21]#

The UltraChat 200k dataset is a high quality filtered subset of UltraChat consisting of 1.4M dialogues generated by ChatGPT. Our corpus includes all surrounding JSON syntax, making it a more accurate representation of real-world raw text. Our subset is the first 7,727 tokens of this text.

Finance [22]#

The ConvFinQA dataset is designed to study numerical reasoning in conversational question answering within the finance domain. This corpus includes complex multi-turn questions and answers based on financial reports, focusing on modeling long-range numerical reasoning paths. Our subset is the first 166,177 tokens of this text.

Pubmed [23]#

The PMC Open Access Subset is a collection of biomedical and life sciences journal literature from the National Library of Medicine. Our subset is the first 117,211 tokens of this text.

Generation & Prefiltering#

To determine the duplicate threshold, we perform a binary search over threshold values by sampling from pairs of generated queries for a given threshold, manually examine the sampled pairs, and adjusting the threshold according to whether the queries in each pair are sufficiently distinct.

Distributions of cosine similarity between queries and their associated excerpts, Pubmed corpus.

Distribution of cosine similarity between all query pairs, Pubmet corpus.

A similar approach is used for the excerpt filter. Future work could automate this process. We note also that in the adopted threshold values are similar across corpora, suggesting a heuristic value could be used in practice.

CorpusNo. of TokensNo. of QueriesEx. Thresh.Dup. Thresh.
State of the Union10,444760.400.70
Wikitext26,6491440.420.73
Chatlogs7,727560.430.71
Finance166,177970.420.70
Pubmed117,211990.400.67
Total328,208472
Number of tokens, number of queries, excerpt threshold and duplicate query threshold for each corpus.
All text excerpts and queries are available in the GitHub repository.

Time & Cost Analysis#

The time required for query generation varied between 3 to 16 seconds per question, averaging around 10 seconds. The longer times were primarily due to the need to disqualify questions based on invalid excerpts, which required additional processing to generate valid questions.

For our base prompt, we used 703 tokens (measured with OpenAI's cl100k Tokenizer). During query generation, we included a random 4,000-character subset from the original corpus and 50 sampled queries from the dataset, resulting in an average prompt size of 2,000 tokens. The average response length was 200 tokens, giving an overall input length of 2,000 tokens and an output length of 200 tokens per question.

At the time of writing, the cost of generating a single question using GPT-4 is approximately \$0.01. Consequently, creating a dataset of 1,000 questions would cost around \$10. Note that this estimate does not account for the subsequent filtering steps, which would reduce the final question count.

Chunking Algorithms#

Below we present the chunking methods used in this report. We evaluate general-purpose, commonly-used chunkers, as well as novel approaches . Any mentions of tokens in this section refer to that within the context of OpenAI's cl100k Tokenizer. The symbol ★ indicates that the subsequent algorithm is a new chunking method we developed for this study.

RecursiveCharacterTextSplitter & TokenTextSplitter [24]#

RecursiveCharacterTextSplitter and TokenTextSplitter are some of the most popular chunking methods, and the default used by many RAG systems. These chunking methods are insensitive to the semantic content of the corpus, relying instead on the position of character sequences to divide documents into chunks, up to a maximum specified length. We follow the implementation of the popular Langchain library.

We found that it was necessary to alter some defaults to achieve fair results. By default, the RecursiveCharacterTextSplitter uses the following separators: ["\n\n", "\n", " ", ""]. We found this would commonly result in very short chunks, which performed poorly in comparison to TokenTextSplitter which produces chunks of a fixed length by default. Therefore we use ["\n\n", "\n", ".", "?", "!", " ", ""] as the set of separators.

KamradtSemanticChunker [14]#

Greg Kamradt proposed a novel semantic chunking algorithm, which was later incorporated into LangChain. The chunker works by first splitting the corpus by sentence. It functions by computing the embedding of a sliding window of tokens over a document, and searching for discontinuities in the cosine distances between consecutive windows. By default, the threshold for detecting a discontinuity is set to any distance above the 95th percentile of all consecutive distances. This is a relative metric and can lead to larger chunks in bigger corpora.

★ KamradtModifiedChunker#

It is desirable for users to be able to set the chunk length directly, in order to ensure that chunks fit within the context window of the embedding model. To address this, we modify the KamradtSemanticChunker by implementing a binary search over discontinuity thresholds such that the largest chunk is shorter than the specified length.

★ ClusterSemanticChunker#

We further extend the principle of embeddings-based semantic chunking by observing that the KamradtSemanticChunker algorithm is greedy in nature, which may not produce the optimal chunking under the objective of preserving chunks with high internal similarity. We propose a new algorithm, the ClusterSemanticChunker, which aims to produce globally optimal chunks by maximizing the sum of cosine similarities within chunks, up to a user-specified maximum length. Intuitively, this preserves as much similar semantic information as possible across the document, while compacting relevant information in each chunk.

Documents are divided into pieces of at most 50 tokens using the RecursiveCharacterTextSplitter, and pieces are individually embedded. Subsequently, we use a dynamic programming approach to maximize the pairwise cosine similarity between all pairs of pieces within any chunk. Code for this algorithm is available in the GitHub repository

A limitation to this method is that the globally optimal packing relies on the global statistics of the corpus, requiring chunks to be re-computed as data is added. This limitation may be improved upon by maintaining an appropriate data-structure over the smaller pieces as data is added or removed; we leave this to future work.

★ LLMSemanticChunker#

In the spirit of "just [ask] the model", we experimented with directly prompting an LLM to chunk the text. We found that a naive approach where the LLM is prompted to repeat the corpus with a <|split|> token was costly, slow, and suffered from hallucinations in the produced text.

To resolve this we broke the text into chunks of size 50 in tokens using a RecursiveCharacterTextSplitter. Then we re-joined the text but surrounded by chunk tags resulting in text like the following:

<start_chunk_0>On glancing over my notes of the seventy odd cases in which I have during the last eight years <end_chunk_0><start_chunk_1>studied the methods of my friend Sherlock Holmes, I find many tragic, some comic, a large number <end_chunk_1><start_chunk_2> . . .

We then instruct the LLM to return the indexes of chunks to split on, in the form

split_after: 3, 5

We found both GPT-4o and Llama 3 8B Instruct consistently adhered to this format. Complete prompts and code for this algorithm are available in the GitHub repository

Results#

We present the mean of Recall, Precision, Precision$_\Omega$, and IoU scores for each chunking method, over all queries and corpora in our evaluation. ± indicates the standard deviation. We report the results for n=5 retrieved chunks, using OpenAI's text-embedding-3-large as the embedding model.

ChunkingSizeOverlapRecallPrecisionPrecision$_\Omega$IoU
Recursive800 (~661)40085.4 ± 34.91.5 ± 1.36.7 ± 5.21.5 ± 1.3
TokenText80040087.9 ± 31.71.4 ± 1.14.7 ± 3.11.4 ± 1.1
Recursive400 (~312)20088.1 ± 31.63.3 ± 2.713.9 ± 10.43.3 ± 2.7
TokenText40020088.6 ± 29.72.7 ± 2.28.4 ± 5.12.7 ± 2.2
Recursive400 (~276)089.5 ± 29.73.6 ± 3.217.7 ± 14.03.6 ± 3.2
TokenText400089.2 ± 29.22.7 ± 2.212.5 ± 8.12.7 ± 2.2
Recursive200 (~137)088.1 ± 30.17.0 ± 5.629.9 ± 18.46.9 ± 5.6
TokenText200087.0 ± 30.85.2 ± 4.121.0 ± 11.95.1 ± 4.1
KamradtN/A (~660)083.6 ± 36.81.5 ± 1.67.4 ± 10.21.5 ± 1.6
★ KamradtMod300 (~397)087.1 ± 31.92.1 ± 2.010.5 ± 12.32.1 ± 2.0
★ Cluster400 (~182)091.3 ± 25.44.5 ± 3.420.7 ± 14.54.5 ± 3.4
★ Cluster200 (~103)087.3 ± 29.88.0 ± 6.034.0 ± 19.78.0 ± 6.0
★ LLM (GPT4o)N/A (~240)091.9 ± 26.53.9 ± 3.219.9 ± 16.33.9 ± 3.2
Results for text-embedding-3-large. Size denotes the chunk size in tokens (cl100k tokenizer). Size in brackets indicates mean chunk size where it may vary by chunking strategy. Overlap denotes the chunk overlap in tokens. Bold values highlight the best performance in each category.
We find that the heuristic RecursiveCharacterTextSplitter with chunk size 200 and no overlap performs well. While it does not achieve the best result, it is consistently high performing across all evaluation metrtics. We note that it outperforms TokenTextSplitter across all metrics for chunk size of 400 or less with no chunk overlap. Interestingly, this does not hold for larger chunk sizes and overlap. Unsurprisingly, reducing chunk overlap improves IoU scores, as this metric penalizes redundant information.

OpenAI Assistants can use file search to improve their response, following the standard Retrieval-Augmented Generation (RAG) process. According to their documentation, the default chunking strategy uses a chunk size of 800 tokens with an overlap of 400 tokens [25]. Assuming the TokenTextSplitter method is employed, we observe that this setting results in slightly below-average recall and the lowest scores across all other metrics, suggesting particularly poor recall-efficiency tradeoffs.

The ClusterSemanticChunker, with a max chunk size set to 400 tokens, achieves the second highest recall of 0.913. Dropping the max chunk size to 200 results in average recall but the highest precision, Precision$_\Omega$ , and IoU. The LLMSemanticChunkers achieves the highest recall of 0.919 while having average scores on the remaining metrics, suggesting LLMs are relatively capable at this task.

The KamradtSemanticChunker with the default settings scores slightly below average across all metrics, with a recall of 0.836. Recall rises to 0.871 with a similar boost in the remaining metrics when the modifications of the KamradtModifiedChunker are applied. We note that recall improved despite the mean chunk length dropping.

We speculate that recall could reach a maximum before relevant information is diluted within chunks, making it more difficult to retrieve, while chunks which are too small fail to capture necessary context within a single unit.

We repeat our experiments with the embedding model changed to the Sentence Transformers 'all-MiniLM-L6-v2'[26].

ChunkingSizeOverlapRecallPrecisionPrecision$_Ω$IoU
Recursive250 (~180)12578.7 ± 39.24.9 ± 4.521.9 ± 14.94.9 ± 4.4
TokenText25012582.4 ± 36.23.6 ± 3.111.4 ± 6.63.5 ± 3.1
Recursive250 (~162)078.5 ± 39.55.4 ± 4.926.7 ± 18.35.4 ± 4.9
TokenText250077.1 ± 39.33.3 ± 3.016.4 ± 10.33.3 ± 3.0
Recursive200 (~128)075.7 ± 40.76.5 ± 6.231.2 ± 18.46.5 ± 6.1
TokenText200076.6 ± 38.84.1 ± 3.719.1 ± 11.04.1 ± 3.6
✒ Cluster250 (~168)077.3 ± 38.66.1 ± 5.128.6 ± 16.76.0 ± 5.1
✒ Cluster200 (~102)075.2 ± 39.97.2 ± 6.133.6 ± 20.07.2 ± 6.0
Results for all-MiniLM-L6-v2. Size denotes the chunk size in tokens (cl100k tokenizer). Size in brackets indicates mean chunk size where it may vary by chunking strategy. Overlap denotes the chunk overlap in tokens. Bold values highlight the best performance in each category.
We find that the ClusterSemanticChunker achieves the highest precision, Precision$_\Omega$ and IoU however has slightly below average recall likely due to its small average chunk size. The TokenTextSplitter achieves the highest recall of 0.824 when configured with chunk size 250 and chunk overlap of 125. This then drops to 0.771 when chunk overlap is set to zero, suggesting that for smaller context, overlapping chunks are necessary for high recall.

Limitations & Future Work#

One limitation in our synthetic evaluation pipeline is that LLMs tend to generate a specific style of question. We attempt to mitigate this by providing it with its previous questions to encourage new ones, but this sometimes exacerbates its lack of creativity. The metric will be more accurate with more realistic and diverse questions. Future work may experiment with various temperature settings and other prompting techniques.

A limitation of the concrete evaluation we present is its relatively small size, and limited diversity. Future work can easily expand on the evaluation we provide by generating larger datasets from larger corpora. Future work may also explore generating excerpt datasets from benchmarks containing existing queries, which are considered to be diverse and widely representative of many retrieval domains. Future work may also blend human-annotated data with synthetic data to improve the evaluation quality.

Finally, our work does not take into account the time required to run these chunking methods, which can vary from almost instantaneous to tens of minutes in the case of the LLMChunker, which is an important consideration in practical retrieval settings.

Conclusion#

In this work, we introduced a comprehensive framework for generating domain and dataset-specific evaluations that accurately capture critical properties, such as information density via IoU (Intersection over Union), for retreival as used in practical AI applications. Using this framework, we created a concrete evaluation across several popular domains, enabling robust comparisons of various chunking methods.

Our evaluation of popular chunking strategies demonstrate that this evaluation effectively captures variations in retrieval performance due to the selected chunking strategye. We developed the ClusterSemanticChunker, an embedding-model aware chunking strategy which produced consistently strong results across the evaluation. We also present a second novel chunking strategy, the LLMSemanticChunker, which also achieves good performance on this evaluation.

References#

[1] Jacob Devlin Maarten Bosma Gaurav Mishra Adam Roberts Paul Barham Hyung Won Chung Charles Sutton
Sebastian Gehrmann et al. Aakanksha Chowdhery, Sharan Narang. Palm: Scaling language modeling with
pathways. Journal of Machine Learning Research, 24(240):1–113, 2023.

[2] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich
Küttler, Mike Lewis, Wen tau Yih, Tim Rocktäschel, Sebastian Riedel, and Douwe Kiela. Retrieval-augmented
generation for knowledge-intensive nlp tasks, 2021

[3] Sergey Brin and Lawrence Page. The anatomy of a large-scale hypertextual web search engine. In Proceedings of
the seventh international conference on World Wide Web 7, pages 107–117. Elsevier, 1998.

[4] C.J. van Rijsbergen. A probability ranking principle in information retrieval. Journal of Documentation, 33(4):334–
354, 1977.

[5] S. E. Robertson, S. Walker, M. Beaulieu, M. Gatford, and A. Payne. Okapi at trec-3. In Proceedings of the Third
Text REtrieval Conference (TREC-3), pages 109–126. NIST, 1995.

[6] Niklas Muennighoff, Nouamane Tazi, Loïc Magne, and Nils Reimers. Mteb: Massive text embedding benchmark,
2022.

[7] Nandan Thakur, Nils Reimers, Andreas Rücklé, Abhishek Srivastava, and Iryna Gurevych. Beir: A heterogenous
benchmark for zero-shot evaluation of information retrieval models, 2021.

[8] Weiyun Wang, Shuibo Zhang, Yiming Ren, Yuchen Duan, Tiantong Li, Shuo Liu, Mengkang Hu, Zhe Chen,
Kaipeng Zhang, Lewei Lu, Xizhou Zhu, Ping Luo, Yu Qiao, Jifeng Dai, Wenqi Shao, and Wenhai Wang. Needle
in a multimodal haystack, 2024.

[9] Marcin Kaszkiel and Justin Zobel. Passage retrieval revisited. In ACM SIGIR Forum, volume 31, pages 178–185.
ACM New York, NY, USA, 1997

[10] Bajaj, P., Campos, D., Craswell, N., Deng, L., Gao, J., Liu, X., Majumder, R., McNamara, A., Mitra, B., Nguyen, T., Rosenberg, M., Song, X., Stoica, A., Tiwary, S., & Wang, T. (2018). MS MARCO: A Human Generated MAchine Reading COmprehension Dataset. arXiv preprint arXiv:1611.09268. https://arxiv.org/abs/1611.09268

[11] Jure Leskovec, Anand Rajaraman, and Jeffrey David Ullman. Mining of massive data sets. Cambridge university
press, 2020.

[12] Matouš Eibich, Shivay Nagpal, and Alexander Fred-Ojala. Aragog: Advanced rag output grading, 2024.

[13] Shahul Es, Jithin James, Luis Espinosa-Anke, and Steven Schockaert. Ragas: Automated evaluation of retrieval
augmented generation, 2023.

[14] Greg Kamradt. 5 levels of text splitting. https://github.com/FullStackRetrieval-com/
RetrievalTutorials/blob/main/tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_
Splitting.ipynb, 2024. Implementation of Semantic Chunking.

[15] Aurelio AI Labs. Semantic chunkers. https://github.com/aurelio-labs/semantic-chunkers, 2024.
Library for semantic text chunking.

[16] Antonio Jimeno Yepes, Yao You, Jan Milczek, Sebastian Laverde, and Renyu Li. Financial report chunking for
effective retrieval augmented generation, 2024.

[17] Freda Shi, Xinyun Chen, Kanishka Misra, Nathan Scales, David Dohan, Ed Chi, Nathanael Schärli, and Denny
Zhou. Large language models can be easily distracted by irrelevant context, 2023.

[18] Md Atiqur Rahman and Yang Wang. Optimizing intersection-over-union in deep neural networks for image
segmentation. In George Bebis, Richard Boyle, Bahram Parvin, Darko Koracin, Fatih Porikli, Sandra Skaff,
Alireza Entezari, Jianyuan Min, Daisuke Iwai, Amela Sadagic, Carlos Scheidegger, and Tobias Isenberg, editors,
Advances in Visual Computing. ISVC 2016. Lecture Notes in Computer Science, volume 10072, pages 234–244.
Springer, Cham, 2016.

[19] The White House. State of the union 2024, 2024. Accessed: 2024-05-02.

[20] Stephen Merity, Caiming Xiong, James Bradbury, and Richard Socher. Pointer sentinel mixture models, 2016.

[21] Ning Ding, Yulin Chen, Bokai Xu, Yujia Qin, Zhi Zheng, Shengding Hu, Zhiyuan Liu, Maosong Sun, and Bowen
Zhou. Enhancing chat language models by scaling high-quality instructional conversations, 2023.

[22] Zhiyu Chen, Shiyang Li, Charese Smiley, Zhiqiang Ma, Sameena Shah, and William Yang Wang. Convfinqa:
Exploring the chain of numerical reasoning in conversational finance question answering. In EMNLP, pages
6279–6292. Association for Computational Linguistics, 2022.

[23] National Library of Medicine. Pmc open access subset. Dataset retrieved from Hugging Face
Datasets (2023). PubMed Central Open Access dataset (Version 2023-06-17.commercial). Available from
https://huggingface.co/datasets/pmc/open_access, 2003–. [cited 2024 May 08].

[24] LangChain. Recursive text splitter, 2023. Accessed: 2024-04-16.

[25] OpenAI. Vector stores. https://platform.openai.com/docs/assistants/tools/file-search/
vector-stores, 2024. Accessed: 2024-06-27.

[26] HuggingFace. Sentence Transformers, all-MiniLM-L6-v2. https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 2024. Accessed: 2024-06-27.

[27] Kristian Georgiev Aleksander Madry Benjamin Cohen-Wang, Harshay Shah. Contextcite: Attributing model
generation to context. https://github.com/MadryLab/context-cite/tree/main, 2024.

Appendices#

Synthetic Dataset Prompt#

text

You are an agent that generates questions from provided text.
Your job is to generate a question and provide the relevant
sections from the text as references.

Instructions:
1. For each provided text, generate a question that can be
 answered solely by the facts in the text.
2. Extract all significant facts that answer the generated
 question.
3. Format the response in JSON format with two fields:
 - 'question': A question directly related to these facts,
 ensuring it can only be answered using the references
 provided.
 - 'references': A list of all text sections that answer
 the generated question. These must be exact copies from
 the original text and should be whole sentences where
 possible.

Notes:
Make the question more specific.
Do not ask a question about multiple topics.
Do not ask a question with over 5 references.

Example:

Text: "Experiment A: The temperature control test showed that
at higher temperatures, the reaction rate increased
significantly, resulting in quicker product formation. However,
at extremely high temperatures, the reaction yield decreased
due to the degradation of reactants.

Experiment B: The pH sensitivity test revealed that the
reaction is highly dependent on acidity, with optimal results
at a pH of 7. Deviating from this pH level in either direction
led to a substantial drop in yield.

Experiment C: In the enzyme activity assay, it was found that
the presence of a specific enzyme accelerated the reaction by
a factor of 3. The absence of the enzyme, however, led to a
sluggish reaction with an extended completion time.

Experiment D: The light exposure trial demonstrated that UV
light stimulated the reaction, making it complete in half the
time compared to the absence of light. Conversely, prolonged
light exposure led to unwanted side reactions that
contaminated the final product."

Response: {
 'oath': "I will not use the word 'and' in the question
unless it is part of a proper noun. I will also make sure the
question is concise.",
 'question': 'What experiments were done in this paper?',
 'references': [
 'Experiment A: The temperature control test showed that at
higher temperatures, the reaction rate increased significantly,
resulting in quicker product formation.',
 'Experiment B: The pH sensitivity test revealed that the
reaction is highly dependent on acidity, with optimal results
at a pH of 7.',
 'Experiment C: In the enzyme activity assay, it was found
that the presence of a specific enzyme accelerated the reaction
by a factor of 3.',
 'Experiment D: The light exposure trial demonstrated that
UV light stimulated the reaction, making it complete in half
the time compared to the absence of light.'
 ]
}

DO NOT USE THE WORD 'and' IN THE QUESTION UNLESS IT IS PART OF
A PROPER NOUN.
YOU MUST INCLUDE THE OATH ABOVE IN YOUR RESPONSE.
YOU MUST ALSO NOT REPEAT A QUESTION THAT HAS ALREADY BEEN
USED."

An interesting observation from the above is the inclusion of an oath. We require these queries to be specific so that the excerpts answer only that query. This generally means the query shouldn't include 'and' unless it is part of a proper noun. Despite this requirement being part of the prompt at many points, GPT would not comply until we required it to include an 'oath': "I will not use the word 'and' in the question unless it is part of a proper noun. I will also make sure the question is concise." in the JSON response. It then consistently included the oath and followed our requirements.

Further Algorithms#

Logit & Attention Based Chunking#

We experimented with next token prediction probabilities and attention values to determine if any signals could be used for chunking. All these experiments were conducted using Llama 3 8B, which provides access to next token logits and attention values.

Token entropy visualization over Wikitext corpus using Llama 3 8B. The color gradient from light blue (under 1 bit) to dark blue (8 bits and over) indicates the entropy in the next token prediction at that token.

Heatmap of attention values from the Llama 3 8B model on the wikitext corpus. This plot shows the max attention values in the last layer across all 32 heads, with x and y axes representing token positions.

We calculate token entropy according to:

Where $Y$ is a random variable representing the next token, $y_t$ is the $t$-th possible token and $P(y_t)$ is the probability assigned to token $(y_t)$. We observe that in general, token entropy rises at the beginning and towards the end of sentences, as well as after a verb after which any noun or adjective could be expected. We initially expected that the entropy would rise as the theme of the text changes, however, we find that the LLM quickly refocuses between topics and so we did not extract a clear signal for semantic boundaries.

We also did not find that there was any clear structure in the attention values which could be used for chunking.

ContextCite Inspired Chunking#

The final algorithm was inspired by ContextCite [27]. Their work leverages next-token prediction to observe how the probability of an LLM generating a response changes as different parts of the input prompt are masked. This allows them to fit weights to each part of the input prompt, determining how much it influences the likelihood of generating a specific response. Essentially, this results in a weighted importance of each part of the input prompt relative to the response.

For our work, we split the Wikitext corpus into 50-token chunks using a RecursiveCharacterTextSplitter and applied the same algorithm, but with each chunk as the 'response' and all previous chunks as the input prompt. This allowed us to fit weights between each chunk. Unfortunately, no clear structure emerged, and we were unable to derive a useful chunking algorithm.

All Results#

We present the mean of Recall, Precision, Precision$_\Omega$, and IoU scores for each chunking method, over all queries and corpora in our evaluation. ± indicates the standard deviation. We vary the number of chunks retrieved: 'Min' retrieves the minimum number of chunks containing excerpts (usually 1-3), while 5 and 10 represent fixed retrieval numbers for all queries. Captions indicate corpus and embedding model.

ChunkingSizeOverlapRetrieveRecallPrecisionPrecision_ΩIoU
Recursive800400Min66.7 ± 46.63.5 ± 4.46.7 ± 5.23.5 ± 4.4
TokenText800400Min75.6 ± 41.82.6 ± 2.44.7 ± 3.12.6 ± 2.4
Recursive400200Min73.3 ± 43.48.5 ± 10.013.9 ± 10.48.4 ± 10.0
TokenText400200Min77.9 ± 39.84.6 ± 3.88.4 ± 5.14.5 ± 3.8
Recursive4000Min61.4 ± 47.710.8 ± 13.217.7 ± 14.010.8 ± 13.2
TokenText4000Min58.1 ± 47.57.2 ± 8.512.5 ± 8.17.1 ± 8.5
Recursive2000Min70.2 ± 42.820.4 ± 20.029.9 ± 18.420.2 ± 20.0
TokenText2000Min66.7 ± 43.313.4 ± 12.921.0 ± 11.913.3 ± 12.9
Cluster4000Min68.6 ± 44.811.8 ± 12.717.8 ± 13.211.7 ± 12.7
Cluster2000Min69.3 ± 43.019.1 ± 18.229.1 ± 17.018.9 ± 18.2
LLMN/A0Min65.4 ± 46.713.1 ± 16.219.9 ± 16.313.0 ± 16.2

Recursive800400585.4 ± 34.91.5 ± 1.36.7 ± 5.21.5 ± 1.3
TokenText800400588.5 ± 30.91.4 ± 1.14.7 ± 3.11.4 ± 1.1
Recursive400200588.3 ± 31.33.3 ± 2.713.9 ± 10.43.3 ± 2.7
TokenText400200587.3 ± 31.32.6 ± 2.28.4 ± 5.12.6 ± 2.2
Recursive4000589.9 ± 29.13.6 ± 3.217.7 ± 14.03.6 ± 3.2
TokenText4000589.7 ± 28.62.7 ± 2.212.5 ± 8.12.7 ± 2.2
Recursive2000588.5 ± 29.57.0 ± 5.629.9 ± 18.47.0 ± 5.6
TokenText2000586.7 ± 31.05.1 ± 4.121.0 ± 11.95.1 ± 4.1
Cluster4000592.1 ± 25.23.7 ± 2.717.8 ± 13.23.7 ± 2.7
Cluster2000589.0 ± 28.96.7 ± 4.929.1 ± 17.06.6 ± 4.9
LLMN/A0591.7 ± 26.83.9 ± 3.219.9 ± 16.33.9 ± 3.2

Recursive8004001091.5 ± 27.50.8 ± 0.76.7 ± 5.20.8 ± 0.7
TokenText8004001094.8 ± 21.70.7 ± 0.64.7 ± 3.10.7 ± 0.6
Recursive4002001094.5 ± 22.01.7 ± 1.313.9 ± 10.41.7 ± 1.3
TokenText4002001092.5 ± 25.01.4 ± 1.18.4 ± 5.11.4 ± 1.1
Recursive40001094.5 ± 21.81.9 ± 1.517.7 ± 14.01.9 ± 1.5
TokenText40001095.1 ± 20.61.5 ± 1.112.5 ± 8.11.5 ± 1.1
Recursive20001092.8 ± 24.33.7 ± 2.729.9 ± 18.43.7 ± 2.7
TokenText20001093.1 ± 23.02.8 ± 2.121.0 ± 11.92.8 ± 2.1
Cluster40001096.2 ± 17.62.0 ± 1.417.8 ± 13.22.0 ± 1.4
Cluster20001093.7 ± 22.43.6 ± 2.529.1 ± 17.03.6 ± 2.5
LLMN/A01095.7 ± 19.82.0 ± 1.519.9 ± 16.32.0 ± 1.5
All corpora, text-embedding-3-large
ChunkingSizeOverlapRetrieveRecallPrecisionPrecision_ΩIoU
Recursive800400Min80.8 ± 39.04.8 ± 4.47.2 ± 4.74.8 ± 4.4
TokenText800400Min89.5 ± 28.63.5 ± 2.55.4 ± 3.53.5 ± 2.5
Recursive400200Min94.3 ± 22.68.0 ± 4.611.4 ± 6.48.0 ± 4.6
TokenText400200Min82.2 ± 37.65.8 ± 4.510.0 ± 5.95.8 ± 4.5
Recursive4000Min76.5 ± 41.413.2 ± 11.216.1 ± 9.513.2 ± 11.2
TokenText4000Min67.1 ± 44.510.2 ± 10.014.1 ± 8.210.2 ± 10.0
Recursive2000Min86.7 ± 30.123.5 ± 14.025.7 ± 12.223.4 ± 14.1
TokenText2000Min77.3 ± 37.719.5 ± 14.824.7 ± 13.219.2 ± 14.7
Cluster4000Min78.5 ± 39.714.2 ± 11.316.7 ± 9.614.2 ± 11.3
Cluster2000Min85.6 ± 31.423.3 ± 14.825.8 ± 12.423.2 ± 14.9
LLMN/A0Min74.0 ± 42.116.1 ± 16.219.3 ± 15.116.0 ± 16.2

Recursive800400594.6 ± 22.51.9 ± 1.67.2 ± 4.71.9 ± 1.6
TokenText800400594.4 ± 21.31.7 ± 1.45.4 ± 3.51.7 ± 1.4
Recursive400200599.6 ± 2.73.9 ± 2.911.4 ± 6.43.9 ± 2.9
TokenText400200587.1 ± 32.23.1 ± 2.910.0 ± 5.93.1 ± 2.9
Recursive40005100.0 ± 0.04.1 ± 3.116.1 ± 9.54.1 ± 3.1
TokenText4000594.4 ± 21.33.5 ± 2.914.1 ± 8.23.5 ± 2.9
Recursive2000599.6 ± 2.78.3 ± 6.625.7 ± 12.28.3 ± 6.5
TokenText2000589.0 ± 30.96.4 ± 5.724.7 ± 13.26.4 ± 5.7
Cluster40005100.0 ± 0.14.1 ± 3.116.7 ± 9.64.1 ± 3.1
Cluster2000599.1 ± 3.87.4 ± 5.525.8 ± 12.47.3 ± 5.5
LLMN/A0595.9 ± 18.85.0 ± 3.919.3 ± 15.15.0 ± 3.9

Recursive8004001094.6 ± 22.51.0 ± 0.87.2 ± 4.71.0 ± 0.8
TokenText8004001098.7 ± 9.51.0 ± 0.75.4 ± 3.51.0 ± 0.7
Recursive40020010100.0 ± 0.02.0 ± 1.511.4 ± 6.42.0 ± 1.5
TokenText4002001089.3 ± 30.91.6 ± 1.510.0 ± 5.91.6 ± 1.5
Recursive400010100.0 ± 0.02.2 ± 1.616.1 ± 9.52.2 ± 1.6
TokenText40001098.2 ± 13.21.9 ± 1.514.1 ± 8.21.9 ± 1.5
Recursive200010100.0 ± 0.04.3 ± 3.225.7 ± 12.24.3 ± 3.2
TokenText20001089.3 ± 30.93.2 ± 2.924.7 ± 13.23.2 ± 2.9
Cluster400010100.0 ± 0.12.5 ± 1.916.7 ± 9.62.5 ± 1.9
Cluster20001099.8 ± 0.83.9 ± 2.925.8 ± 12.43.9 ± 2.9
LLMN/A010100.0 ± 0.12.5 ± 1.819.3 ± 15.12.5 ± 1.8
Chatlogs corpus, text-embedding-3-large
ChunkingSizeOverlapRetrieveRecallPrecisionPrecision_ΩIoU
Recursive800400Min53.8 ± 49.12.9 ± 4.36.9 ± 6.02.9 ± 4.3
TokenText800400Min62.8 ± 47.21.8 ± 2.13.9 ± 3.01.8 ± 2.1
Recursive400200Min64.4 ± 46.95.3 ± 7.412.0 ± 9.25.3 ± 7.4
TokenText400200Min78.1 ± 40.53.3 ± 3.57.0 ± 5.33.3 ± 3.5
Recursive4000Min54.3 ± 48.37.5 ± 12.317.4 ± 18.77.5 ± 12.3
TokenText4000Min55.9 ± 48.84.8 ± 6.610.0 ± 8.04.8 ± 6.6
Recursive2000Min61.5 ± 46.612.8 ± 16.427.1 ± 18.612.8 ± 16.4
TokenText2000Min64.9 ± 45.78.6 ± 11.417.2 ± 13.28.6 ± 11.4
Cluster4000Min58.9 ± 48.36.6 ± 9.314.0 ± 10.86.6 ± 9.3
Cluster2000Min63.5 ± 47.111.6 ± 14.524.4 ± 17.111.6 ± 14.4
LLMN/A0Min49.4 ± 49.55.9 ± 9.713.6 ± 11.65.9 ± 9.7

Recursive800400574.2 ± 43.21.1 ± 1.36.9 ± 6.01.1 ± 1.3
TokenText800400579.3 ± 40.41.0 ± 1.13.9 ± 3.01.0 ± 1.1
Recursive400200581.3 ± 37.52.7 ± 2.512.0 ± 9.22.7 ± 2.5
TokenText400200586.0 ± 34.02.2 ± 2.17.0 ± 5.32.2 ± 2.1
Recursive4000584.0 ± 35.43.4 ± 4.317.4 ± 18.73.4 ± 4.3
TokenText4000583.6 ± 35.52.1 ± 2.110.0 ± 8.02.1 ± 2.1
Recursive2000579.6 ± 38.45.9 ± 5.627.1 ± 18.65.9 ± 5.6
TokenText2000583.7 ± 35.34.2 ± 4.017.2 ± 13.24.2 ± 3.9
Cluster4000585.1 ± 33.92.8 ± 2.314.0 ± 10.82.8 ± 2.3
Cluster2000582.1 ± 37.75.3 ± 4.824.4 ± 17.15.3 ± 4.8
LLMN/A0585.2 ± 35.23.3 ± 3.013.6 ± 11.63.3 ± 3.0

Recursive8004001083.0 ± 37.20.6 ± 0.66.9 ± 6.00.6 ± 0.6
TokenText8004001088.4 ± 31.20.6 ± 0.63.9 ± 3.00.6 ± 0.6
Recursive4002001091.5 ± 27.51.4 ± 1.112.0 ± 9.21.4 ± 1.1
TokenText4002001094.2 ± 22.41.2 ± 1.07.0 ± 5.31.2 ± 1.0
Recursive40001091.0 ± 27.81.7 ± 1.617.4 ± 18.71.7 ± 1.6
TokenText40001086.2 ± 33.01.1 ± 1.110.0 ± 8.01.1 ± 1.1
Recursive20001088.0 ± 31.03.0 ± 2.527.1 ± 18.63.0 ± 2.5
TokenText20001091.1 ± 27.72.3 ± 2.017.2 ± 13.22.3 ± 2.0
Cluster40001095.8 ± 18.61.6 ± 1.114.0 ± 10.81.6 ± 1.1
Cluster20001087.8 ± 31.72.9 ± 2.424.4 ± 17.12.9 ± 2.4
LLMN/A01092.4 ± 26.01.7 ± 1.413.6 ± 11.61.7 ± 1.4
Finance corpus, text-embedding-3-large
ChunkingSizeOverlapRetrieveRecallPrecisionPrecision_ΩIoU
Recursive800400Min51.2 ± 49.14.0 ± 6.59.1 ± 6.64.0 ± 6.5
TokenText800400Min66.0 ± 45.03.2 ± 3.16.1 ± 3.63.2 ± 3.1
Recursive400200Min58.3 ± 47.911.5 ± 14.419.6 ± 13.511.5 ± 14.4
TokenText400200Min68.6 ± 43.05.1 ± 4.410.6 ± 5.45.1 ± 4.4
Recursive4000Min51.6 ± 48.813.0 ± 17.223.3 ± 16.513.0 ± 17.2
TokenText4000Min49.6 ± 46.68.1 ± 10.716.0 ± 9.78.0 ± 10.7
Recursive2000Min54.9 ± 43.721.7 ± 23.236.4 ± 19.521.1 ± 23.3
TokenText2000Min47.2 ± 43.610.8 ± 12.124.3 ± 11.410.5 ± 11.9
Cluster4000Min50.7 ± 46.912.4 ± 17.024.9 ± 19.612.3 ± 17.0
Cluster2000Min61.9 ± 42.822.1 ± 22.136.7 ± 20.021.6 ± 22.1
LLMN/A0Min57.0 ± 48.015.1 ± 20.727.2 ± 20.615.1 ± 20.7

Recursive800400580.3 ± 38.71.9 ± 1.69.1 ± 6.61.9 ± 1.6
TokenText800400581.5 ± 36.21.8 ± 1.46.1 ± 3.61.8 ± 1.4
Recursive400200580.3 ± 38.64.2 ± 3.619.6 ± 13.54.2 ± 3.6
TokenText400200582.5 ± 33.53.3 ± 2.510.6 ± 5.43.3 ± 2.5
Recursive4000583.6 ± 35.34.6 ± 3.623.3 ± 16.54.6 ± 3.5
TokenText4000577.2 ± 38.43.2 ± 2.616.0 ± 9.73.2 ± 2.6
Recursive2000581.1 ± 33.29.0 ± 6.836.4 ± 19.58.9 ± 6.8
TokenText2000575.7 ± 37.15.9 ± 4.624.3 ± 11.45.9 ± 4.6
Cluster4000582.5 ± 35.34.5 ± 3.324.9 ± 19.64.4 ± 3.3
Cluster2000581.7 ± 33.48.1 ± 5.736.7 ± 20.08.0 ± 5.6
LLMN/A0586.3 ± 32.14.6 ± 3.627.2 ± 20.64.6 ± 3.6

Recursive8004001085.9 ± 34.21.1 ± 0.89.1 ± 6.61.1 ± 0.8
TokenText8004001091.4 ± 27.41.0 ± 0.76.1 ± 3.61.0 ± 0.7
Recursive4002001089.8 ± 28.32.3 ± 1.719.6 ± 13.52.3 ± 1.7
TokenText4002001089.6 ± 26.61.8 ± 1.310.6 ± 5.41.8 ± 1.3
Recursive40001089.2 ± 28.72.4 ± 1.723.3 ± 16.52.4 ± 1.7
TokenText40001092.3 ± 24.91.9 ± 1.316.0 ± 9.71.9 ± 1.3
Recursive20001088.2 ± 28.24.9 ± 3.336.4 ± 19.54.8 ± 3.3
TokenText20001090.6 ± 23.23.6 ± 2.324.3 ± 11.43.5 ± 2.3
Cluster40001089.4 ± 29.02.4 ± 1.724.9 ± 19.62.4 ± 1.7
Cluster20001091.1 ± 23.74.5 ± 2.836.7 ± 20.04.5 ± 2.8
LLMN/A01095.4 ± 19.92.5 ± 1.627.2 ± 20.62.5 ± 1.6
Pubmed corpus, text-embedding-3-large
ChunkingSizeOverlapRetrieveRecallPrecisionPrecision_ΩIoU
Recursive800400Min82.9 ± 37.62.2 ± 1.73.6 ± 2.12.2 ± 1.7
TokenText800400Min88.6 ± 31.32.3 ± 1.73.3 ± 2.12.3 ± 1.7
Recursive400200Min93.4 ± 24.85.1 ± 3.27.1 ± 3.95.1 ± 3.2
TokenText400200Min87.2 ± 32.44.1 ± 2.96.2 ± 3.64.1 ± 2.9
Recursive4000Min67.1 ± 46.37.3 ± 8.010.6 ± 6.97.3 ± 8.0
TokenText4000Min71.1 ± 45.37.0 ± 7.29.4 ± 6.27.0 ± 7.2
Recursive2000Min88.9 ± 30.819.5 ± 12.921.3 ± 11.719.5 ± 12.9
TokenText2000Min83.7 ± 35.515.0 ± 11.116.8 ± 9.615.0 ± 11.1
Cluster4000Min88.6 ± 30.714.3 ± 12.115.9 ± 11.414.3 ± 12.1
Cluster2000Min84.3 ± 35.024.1 ± 18.728.5 ± 16.924.0 ± 18.6
LLMN/A0Min84.3 ± 35.815.0 ± 15.218.0 ± 15.415.0 ± 15.2

Recursive800400592.1 ± 27.01.0 ± 0.73.6 ± 2.11.0 ± 0.7
TokenText800400596.1 ± 19.51.0 ± 0.73.3 ± 2.11.0 ± 0.7
Recursive400200597.4 ± 16.02.2 ± 1.47.1 ± 3.92.2 ± 1.4
TokenText400200594.7 ± 22.32.0 ± 1.36.2 ± 3.62.0 ± 1.3
Recursive4000594.7 ± 22.32.1 ± 1.510.6 ± 6.92.1 ± 1.5
TokenText4000598.7 ± 11.42.0 ± 1.39.4 ± 6.22.0 ± 1.3
Recursive2000598.6 ± 11.44.5 ± 2.921.3 ± 11.74.5 ± 2.9
TokenText2000595.7 ± 19.63.9 ± 2.616.8 ± 9.63.9 ± 2.6
Cluster4000598.3 ± 11.53.4 ± 2.315.9 ± 11.43.4 ± 2.3
Cluster2000597.6 ± 12.16.1 ± 4.128.5 ± 16.96.1 ± 4.1
LLMN/A0597.3 ± 16.03.3 ± 3.018.0 ± 15.43.3 ± 3.0

Recursive8004001094.7 ± 22.30.5 ± 0.43.6 ± 2.10.5 ± 0.4
TokenText8004001098.7 ± 11.40.5 ± 0.33.3 ± 2.10.5 ± 0.3
Recursive4002001098.7 ± 11.41.1 ± 0.77.1 ± 3.91.1 ± 0.7
TokenText4002001097.4 ± 16.01.0 ± 0.76.2 ± 3.61.0 ± 0.7
Recursive40001097.3 ± 16.01.1 ± 0.710.6 ± 6.91.1 ± 0.7
TokenText400010100.0 ± 0.01.0 ± 0.69.4 ± 6.21.0 ± 0.6
Recursive20001098.6 ± 11.42.3 ± 1.421.3 ± 11.72.3 ± 1.4
TokenText20001097.4 ± 16.02.0 ± 1.316.8 ± 9.62.0 ± 1.3
Cluster40001098.3 ± 11.51.7 ± 1.115.9 ± 11.41.7 ± 1.1
Cluster20001098.1 ± 11.53.0 ± 2.028.5 ± 16.93.0 ± 2.0
LLMN/A01097.3 ± 16.01.6 ± 1.118.0 ± 15.41.6 ± 1.1
State of the Union corpus, text-embedding-3-large
ChunkingSizeOverlapRetrieveRecallPrecisionPrecision_ΩIoU
Recursive800400Min72.1 ± 44.53.6 ± 3.56.3 ± 3.93.6 ± 3.5
TokenText800400Min78.6 ± 40.52.7 ± 2.04.6 ± 2.42.7 ± 2.0
Recursive400200Min71.0 ± 44.610.4 ± 10.716.0 ± 9.710.4 ± 10.7
TokenText400200Min77.6 ± 40.14.8 ± 3.48.5 ± 4.14.8 ± 3.4
Recursive4000Min64.1 ± 47.212.5 ± 12.618.6 ± 10.612.5 ± 12.6
TokenText4000Min55.1 ± 47.77.1 ± 7.512.8 ± 6.77.0 ± 7.5
Recursive2000Min70.3 ± 43.324.0 ± 23.233.5 ± 19.923.8 ± 23.2
TokenText2000Min68.1 ± 41.815.3 ± 13.021.9 ± 10.315.1 ± 13.0
Cluster4000Min72.8 ± 42.712.5 ± 11.116.8 ± 8.912.4 ± 11.1
Cluster2000Min64.0 ± 44.217.8 ± 16.528.6 ± 14.117.6 ± 16.5
LLMN/A0Min68.5 ± 45.914.3 ± 15.220.3 ± 14.514.2 ± 15.1

Recursive800400589.3 ± 30.71.6 ± 1.16.3 ± 3.91.6 ± 1.1
TokenText800400593.3 ± 24.51.4 ± 0.94.6 ± 2.41.4 ± 0.9
Recursive400200589.4 ± 30.63.4 ± 2.316.0 ± 9.73.4 ± 2.3
TokenText400200587.6 ± 30.82.6 ± 1.78.5 ± 4.12.6 ± 1.7
Recursive4000591.9 ± 26.73.6 ± 2.418.6 ± 10.63.6 ± 2.4
TokenText4000595.7 ± 18.92.8 ± 1.712.8 ± 6.72.8 ± 1.7
Recursive2000590.0 ± 29.07.1 ± 4.633.5 ± 19.97.1 ± 4.6
TokenText2000590.8 ± 25.35.4 ± 3.321.9 ± 10.35.4 ± 3.3
Cluster4000597.1 ± 14.83.8 ± 2.116.8 ± 8.93.8 ± 2.1
Cluster2000590.1 ± 27.96.6 ± 4.228.6 ± 14.16.6 ± 4.2
LLMN/A0595.1 ± 21.53.9 ± 2.420.3 ± 14.53.9 ± 2.4

Recursive8004001098.3 ± 12.30.9 ± 0.56.3 ± 3.90.9 ± 0.5
TokenText8004001097.8 ± 14.40.7 ± 0.44.6 ± 2.40.7 ± 0.4
Recursive4002001095.5 ± 20.31.8 ± 1.116.0 ± 9.71.8 ± 1.1
TokenText4002001091.9 ± 26.21.3 ± 0.98.5 ± 4.11.3 ± 0.9
Recursive40001096.8 ± 16.81.9 ± 1.218.6 ± 10.61.9 ± 1.2
TokenText40001099.2 ± 8.51.5 ± 0.812.8 ± 6.71.5 ± 0.8
Recursive20001093.3 ± 24.43.8 ± 2.333.5 ± 19.93.8 ± 2.3
TokenText20001095.5 ± 17.82.8 ± 1.621.9 ± 10.32.8 ± 1.6
Cluster40001098.7 ± 9.32.0 ± 1.116.8 ± 8.92.0 ± 1.1
Cluster20001094.7 ± 21.53.6 ± 2.228.6 ± 14.13.6 ± 2.2
LLMN/A01095.8 ± 20.02.0 ± 1.320.3 ± 14.52.0 ± 1.3
Wikitext corpus, text-embedding-3-large
ChunkingSizeOverlapRetrieveRecallPrecisionPrecision_ΩIoU
Recursive250125Min60.7 ± 47.410.6 ± 14.121.9 ± 14.910.6 ± 14.0
TokenText250125Min73.4 ± 42.65.6 ± 4.911.4 ± 6.65.6 ± 4.9
Recursive2500Min54.1 ± 47.914.6 ± 19.126.7 ± 18.314.4 ± 19.1
TokenText2500Min52.4 ± 46.78.5 ± 10.616.4 ± 10.38.4 ± 10.6
Recursive2000Min48.5 ± 47.314.5 ± 19.131.2 ± 18.414.3 ± 19.0
TokenText2000Min53.6 ± 46.010.0 ± 11.919.1 ± 11.09.9 ± 11.9
Cluster2500Min55.7 ± 46.514.4 ± 16.928.6 ± 16.714.1 ± 16.8
Cluster2000Min51.9 ± 46.815.8 ± 19.133.6 ± 20.015.5 ± 19.0

Recursive250125578.7 ± 39.24.9 ± 4.521.9 ± 14.94.9 ± 4.4
TokenText250125582.4 ± 36.23.6 ± 3.111.4 ± 6.63.5 ± 3.1
Recursive2500578.5 ± 39.55.4 ± 4.926.7 ± 18.35.4 ± 4.9
TokenText2500577.1 ± 39.33.3 ± 3.016.4 ± 10.33.3 ± 3.0
Recursive2000575.7 ± 40.76.5 ± 6.231.2 ± 18.46.5 ± 6.1
TokenText2000576.6 ± 38.84.1 ± 3.719.1 ± 11.04.1 ± 3.6
Cluster2500577.3 ± 38.66.1 ± 5.128.6 ± 16.76.0 ± 5.1
Cluster2000575.2 ± 39.97.2 ± 6.133.6 ± 20.07.2 ± 6.0

Recursive2501251087.2 ± 32.32.8 ± 2.321.9 ± 14.92.8 ± 2.3
TokenText2501251088.4 ± 30.81.9 ± 1.611.4 ± 6.61.9 ± 1.6
Recursive25001084.7 ± 34.52.9 ± 2.526.7 ± 18.32.9 ± 2.5
TokenText25001085.7 ± 33.11.9 ± 1.616.4 ± 10.31.9 ± 1.6
Recursive20001083.7 ± 35.03.7 ± 3.031.2 ± 18.43.7 ± 3.0
TokenText20001085.4 ± 32.32.4 ± 1.919.1 ± 11.02.4 ± 1.9
Cluster25001084.4 ± 33.33.5 ± 2.728.6 ± 16.73.5 ± 2.7
Cluster20001084.4 ± 32.84.2 ± 3.233.6 ± 20.04.2 ± 3.2
All corpora, all-MiniLM-L6-v2
ChunkingSizeOverlapRetrieveRecallPrecisionPrecision_ΩIoU
Recursive250125Min91.1 ± 24.612.5 ± 6.819.0 ± 9.212.5 ± 6.8
TokenText250125Min92.9 ± 25.88.8 ± 5.513.3 ± 7.98.8 ± 5.5
Recursive2500Min70.5 ± 42.518.7 ± 16.025.0 ± 12.718.5 ± 16.0
TokenText2500Min76.3 ± 37.015.9 ± 13.018.8 ± 11.115.8 ± 13.0
Recursive2000Min67.0 ± 41.122.1 ± 18.932.9 ± 16.321.5 ± 18.8
TokenText2000Min77.0 ± 37.519.6 ± 14.123.0 ± 11.119.5 ± 14.2
Cluster2500Min77.0 ± 37.720.7 ± 16.427.6 ± 14.020.5 ± 16.5
Cluster2000Min68.6 ± 42.222.4 ± 18.834.1 ± 19.621.9 ± 18.8

Recursive250125594.6 ± 17.47.1 ± 4.719.0 ± 9.27.0 ± 4.4
TokenText2501255100.0 ± 0.05.3 ± 4.013.3 ± 7.95.3 ± 4.0
Recursive2500598.2 ± 13.27.6 ± 5.825.0 ± 12.77.6 ± 5.8
TokenText2500597.7 ± 13.55.1 ± 3.918.8 ± 11.15.1 ± 3.9
Recursive2000596.5 ± 15.79.2 ± 7.332.9 ± 16.39.2 ± 7.3
TokenText2000598.7 ± 7.16.5 ± 4.923.0 ± 11.16.4 ± 4.9
Cluster2500595.9 ± 15.08.4 ± 6.427.6 ± 14.08.3 ± 6.4
Cluster2000591.1 ± 23.09.7 ± 6.734.1 ± 19.69.5 ± 6.2

Recursive2501251098.2 ± 13.23.8 ± 3.019.0 ± 9.23.8 ± 3.0
TokenText25012510100.0 ± 0.02.6 ± 2.013.3 ± 7.92.6 ± 2.0
Recursive25001098.2 ± 13.24.0 ± 3.025.0 ± 12.74.0 ± 3.0
TokenText25001097.9 ± 13.42.6 ± 2.118.8 ± 11.12.6 ± 2.1
Recursive200010100.0 ± 0.04.9 ± 3.632.9 ± 16.34.9 ± 3.6
TokenText200010100.0 ± 0.03.3 ± 2.623.0 ± 11.13.3 ± 2.6
Cluster25001099.1 ± 4.54.5 ± 3.227.6 ± 14.04.5 ± 3.2
Cluster20001097.6 ± 9.15.3 ± 4.034.1 ± 19.65.3 ± 4.0
Chatlogs corpus, all-MiniLM-L6-v2
ChunkingSizeOverlapRetrieveRecallPrecisionPrecision_ΩIoU
Recursive250125Min59.0 ± 48.77.1 ± 10.118.8 ± 12.37.1 ± 10.1
TokenText250125Min72.4 ± 43.13.7 ± 3.99.4 ± 6.73.7 ± 3.9
Recursive2500Min50.0 ± 48.59.5 ± 15.823.1 ± 17.99.4 ± 15.8
TokenText2500Min55.5 ± 47.65.3 ± 7.112.8 ± 9.35.3 ± 7.1
Recursive2000Min49.4 ± 47.79.3 ± 12.626.3 ± 16.49.2 ± 12.5
TokenText2000Min57.4 ± 46.65.9 ± 7.414.5 ± 10.45.9 ± 7.3
Cluster2500Min55.3 ± 48.29.0 ± 12.425.2 ± 17.08.9 ± 12.4
Cluster2000Min51.2 ± 47.89.9 ± 13.329.5 ± 21.99.8 ± 13.2

Recursive250125569.3 ± 44.93.7 ± 3.718.8 ± 12.33.7 ± 3.7
TokenText250125579.1 ± 39.33.0 ± 2.99.4 ± 6.73.0 ± 2.9
Recursive2500569.7 ± 44.24.2 ± 4.023.1 ± 17.94.2 ± 4.0
TokenText2500572.8 ± 42.12.7 ± 2.712.8 ± 9.32.7 ± 2.7
Recursive2000571.3 ± 43.15.8 ± 6.026.3 ± 16.45.7 ± 5.8
TokenText2000573.4 ± 41.53.5 ± 3.514.5 ± 10.43.5 ± 3.4
Cluster2500574.9 ± 41.64.9 ± 4.525.2 ± 17.04.9 ± 4.5
Cluster2000569.6 ± 43.75.9 ± 5.729.5 ± 21.95.8 ± 5.7

Recursive2501251079.2 ± 40.42.2 ± 2.018.8 ± 12.32.2 ± 2.0
TokenText2501251087.0 ± 32.91.6 ± 1.59.4 ± 6.71.6 ± 1.5
Recursive25001077.6 ± 40.32.4 ± 2.223.1 ± 17.92.4 ± 2.2
TokenText25001077.0 ± 40.31.5 ± 1.412.8 ± 9.31.4 ± 1.4
Recursive20001079.3 ± 38.73.1 ± 2.826.3 ± 16.43.1 ± 2.8
TokenText20001078.2 ± 38.51.9 ± 1.814.5 ± 10.41.9 ± 1.8
Cluster25001078.7 ± 38.92.6 ± 2.425.2 ± 17.02.6 ± 2.4
Cluster20001079.8 ± 38.83.3 ± 3.029.5 ± 21.93.3 ± 3.0
Finance corpus, all-MiniLM-L6-v2
ChunkingSizeOverlapRetrieveRecallPrecisionPrecision_ΩIoU
Recursive250125Min42.8 ± 46.611.2 ± 18.128.8 ± 18.511.1 ± 18.0
TokenText250125Min61.4 ± 46.35.9 ± 5.514.1 ± 7.15.9 ± 5.5
Recursive2500Min37.2 ± 45.113.4 ± 20.934.0 ± 21.113.1 ± 20.8
TokenText2500Min45.4 ± 45.79.8 ± 12.620.8 ± 12.29.6 ± 12.6
Recursive2000Min31.7 ± 43.112.7 ± 21.038.1 ± 21.512.3 ± 20.7
TokenText2000Min37.5 ± 42.88.6 ± 11.823.0 ± 11.58.4 ± 11.7
Cluster2500Min42.7 ± 44.213.1 ± 16.233.4 ± 17.112.6 ± 15.9
Cluster2000Min35.1 ± 43.711.8 ± 17.938.7 ± 19.811.5 ± 17.8

Recursive250125563.7 ± 45.25.9 ± 6.228.8 ± 18.55.8 ± 6.2
TokenText250125568.4 ± 44.13.9 ± 3.514.1 ± 7.13.9 ± 3.5
Recursive2500562.4 ± 45.36.6 ± 6.634.0 ± 21.16.6 ± 6.6
TokenText2500563.1 ± 44.23.6 ± 3.520.8 ± 12.23.6 ± 3.5
Recursive2000561.0 ± 45.77.9 ± 8.038.1 ± 21.57.8 ± 7.9
TokenText2000561.3 ± 43.34.4 ± 4.123.0 ± 11.54.3 ± 4.1
Cluster2500561.3 ± 43.16.3 ± 5.833.4 ± 17.16.2 ± 5.7
Cluster2000559.8 ± 43.97.1 ± 6.438.7 ± 19.86.9 ± 6.3

Recursive2501251074.6 ± 41.13.5 ± 3.028.8 ± 18.53.5 ± 3.0
TokenText2501251076.8 ± 40.72.3 ± 1.914.1 ± 7.12.3 ± 1.9
Recursive25001069.6 ± 43.43.6 ± 3.234.0 ± 21.13.6 ± 3.2
TokenText25001073.0 ± 41.02.2 ± 1.920.8 ± 12.22.2 ± 1.9
Recursive20001067.2 ± 43.44.3 ± 3.838.1 ± 21.54.3 ± 3.8
TokenText20001073.6 ± 39.62.7 ± 2.223.0 ± 11.52.7 ± 2.2
Cluster25001071.5 ± 40.63.9 ± 3.333.4 ± 17.13.9 ± 3.3
Cluster20001073.5 ± 38.24.5 ± 3.538.7 ± 19.84.4 ± 3.4
Pubmed corpus, all-MiniLM-L6-v2
ChunkingSizeOverlapRetrieveRecallPrecisionPrecision_ΩIoU
Recursive250125Min71.9 ± 44.67.7 ± 7.013.2 ± 7.07.7 ± 7.0
TokenText250125Min78.3 ± 40.84.8 ± 4.18.6 ± 4.94.8 ± 4.1
Recursive2500Min62.5 ± 47.513.2 ± 14.218.7 ± 11.013.1 ± 14.2
TokenText2500Min52.4 ± 47.86.8 ± 8.413.0 ± 8.26.8 ± 8.4
Recursive2000Min51.6 ± 48.712.7 ± 14.923.0 ± 11.612.6 ± 14.8
TokenText2000Min53.1 ± 46.67.8 ± 9.514.2 ± 8.27.7 ± 9.5
Cluster2500Min63.3 ± 45.213.9 ± 15.922.2 ± 14.213.8 ± 15.9
Cluster2000Min55.6 ± 47.414.8 ± 16.527.8 ± 15.714.5 ± 16.4

Recursive250125591.2 ± 27.23.7 ± 2.713.2 ± 7.03.7 ± 2.7
TokenText250125588.7 ± 31.22.6 ± 2.08.6 ± 4.92.6 ± 2.0
Recursive2500582.5 ± 37.63.6 ± 3.018.7 ± 11.03.6 ± 3.0
TokenText2500582.0 ± 36.52.4 ± 2.013.0 ± 8.22.4 ± 2.0
Recursive2000582.7 ± 36.54.6 ± 3.723.0 ± 11.64.6 ± 3.7
TokenText2000580.5 ± 36.52.9 ± 2.514.2 ± 8.22.9 ± 2.5
Cluster2500585.0 ± 32.35.4 ± 4.322.2 ± 14.25.4 ± 4.3
Cluster2000585.0 ± 33.66.9 ± 6.327.8 ± 15.76.9 ± 6.3

Recursive2501251096.4 ± 16.92.0 ± 1.313.2 ± 7.02.0 ± 1.3
TokenText2501251094.7 ± 22.31.4 ± 1.08.6 ± 4.91.4 ± 1.0
Recursive25001087.3 ± 32.41.9 ± 1.418.7 ± 11.01.9 ± 1.4
TokenText25001090.3 ± 28.31.3 ± 1.013.0 ± 8.21.3 ± 1.0
Recursive20001088.7 ± 30.92.5 ± 1.923.0 ± 11.62.5 ± 1.9
TokenText20001089.3 ± 27.01.6 ± 1.214.2 ± 8.21.6 ± 1.2
Cluster25001090.1 ± 27.23.0 ± 2.322.2 ± 14.23.0 ± 2.3
Cluster20001088.5 ± 29.13.7 ± 3.027.8 ± 15.73.7 ± 3.0
State of the Union corpus, all-MiniLM-L6-v2
ChunkingSizeOverlapRetrieveRecallPrecisionPrecision_ΩIoU
Recursive250125Min56.3 ± 48.313.4 ± 17.024.8 ± 15.413.4 ± 17.0
TokenText250125Min72.0 ± 42.85.8 ± 4.411.5 ± 5.25.7 ± 4.4
Recursive2500Min57.7 ± 47.817.9 ± 22.029.1 ± 19.017.8 ± 22.0
TokenText2500Min45.9 ± 46.37.7 ± 9.416.7 ± 8.47.6 ± 9.4
Recursive2000Min50.5 ± 47.817.3 ± 21.833.3 ± 18.617.1 ± 21.8
TokenText2000Min53.3 ± 45.911.0 ± 12.620.5 ± 10.210.9 ± 12.6
Cluster2500Min52.8 ± 47.216.7 ± 19.431.4 ± 16.916.4 ± 19.1
Cluster2000Min55.4 ± 46.220.6 ± 22.335.8 ± 19.720.2 ± 22.3

Recursive250125582.7 ± 36.94.9 ± 3.724.8 ± 15.44.9 ± 3.7
TokenText250125584.2 ± 33.63.6 ± 2.511.5 ± 5.23.6 ± 2.5
Recursive2500585.7 ± 33.55.4 ± 3.829.1 ± 19.05.4 ± 3.8
TokenText2500579.1 ± 37.63.3 ± 2.616.7 ± 8.43.3 ± 2.6
Recursive2000576.9 ± 40.06.0 ± 4.633.3 ± 18.65.9 ± 4.6
TokenText2000578.7 ± 37.14.1 ± 2.920.5 ± 10.24.1 ± 2.9
Cluster2500578.7 ± 38.26.2 ± 4.631.4 ± 16.96.1 ± 4.6
Cluster2000578.1 ± 38.27.5 ± 5.435.8 ± 19.77.4 ± 5.4

Recursive2501251092.1 ± 25.82.8 ± 1.824.8 ± 15.42.8 ± 1.8
TokenText2501251089.5 ± 28.31.9 ± 1.311.5 ± 5.21.9 ± 1.3
Recursive25001093.1 ± 23.83.0 ± 1.929.1 ± 19.03.0 ± 1.9
TokenText25001093.2 ± 23.92.0 ± 1.216.7 ± 8.42.0 ± 1.2
Recursive20001089.0 ± 29.53.7 ± 2.533.3 ± 18.63.7 ± 2.5
TokenText20001090.8 ± 26.52.5 ± 1.620.5 ± 10.22.5 ± 1.6
Cluster25001088.5 ± 28.73.7 ± 2.431.4 ± 16.93.7 ± 2.3
Cluster20001087.6 ± 29.14.3 ± 2.635.8 ± 19.74.3 ± 2.6
Wikitext, all-MiniLM-L6-v2

© 2026

Product
DatabaseSyncEnterprisePackage Search MCPDocsStatusContact
Follow
GitHubXYouTube
Company
AboutChangelogCareers
Legal
PrivacyTermsSecurityDPA