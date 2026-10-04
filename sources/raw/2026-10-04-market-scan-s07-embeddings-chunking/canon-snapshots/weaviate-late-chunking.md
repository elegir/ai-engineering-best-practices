# Snapshot — https://weaviate.io/blog/late-chunking

Fetched 2026-10-04 by the main session with curl (HTML stripped to text; verbatim words).

Late Chunking: Balancing Precision and Cost in Long Context Retrieval | Weaviate

Skip to main content

Inside Weaviate's MCP Ecosystem - Register for the webinar 

ContactLog inTry now
☰
Late Chunking: Balancing Precision and Cost in Long Context Retrieval
September 5, 2024 · 13 min read
Charles PierseHead of Weaviate LabsConnor ShortenProduct ResearcherAkanksha SharmaProduct Management Intern

Large-scale RAG applications that require long context retrieval deal with a unique set of challenges. The volume of data is often huge, while the precision of the retrieval system is critical. However, ensuring high-quality retrieval in such systems is often at odds with cost and performance. For users this can present a difficult balancing act. But there may be a new solution that can even the scales.

Two weeks ago, JinaAI announced a new methodology to aid in long-context retrieval called late chunking. This article explores why late chunking may just be the happy medium between naive (but inexpensive) solutions and more sophisticated (but costly) solutions like ColBERT for users looking to build high-quality retrieval systems on long documents.

What is Late Chunking?​

note
The similarity between the names "late chunking" and "late interaction" is intentional—the authors of late chunking chose the name to reflect its connection with late interaction.

Late chunking is a novel approach that aims to preserve contextual information across large documents by inverting the traditional order of embedding and chunking. The key distinction lies in when the chunking occurs:

Traditional approach: Chunk first, then embed each chunk separately.

Late chunking: Embed the entire document first, then chunk the embeddings.

This method utilizes a long context embedding model to create token embeddings for every token in a document. These token-level embeddings are then broken up and pooled into multiple embeddings representing each chunk in the text.

In typical setups, all token embeddings would be pooled (mean, cls, etc.) into a single vector representation for the entire document. However, with the rise of RAG applications, there's growing concern that a single vector for long documents doesn't preserve enough contextual information, potentially sacrificing precision during retrieval.

Late chunking addresses this by maintaining the contextual relationships between tokens across the entire document during the embedding process, and only afterwards dividing these contextually-rich embeddings into chunks. This approach aims to strike a balance between the precision of full-document embedding and the granularity needed for effective retrieval.

Additionally, this method can help mitigate issues associated with very long documents, such as expensive LLM calls, increased latency, and a higher chance of hallucination.

Current Approaches to Long Context Retrieval​

Naive Chunking​

This approach breaks up a long document into chunks (for which there exist numerous chunking strategies) and individually embeds each of those chunks. While this solution can work in some setups it inherently does not account for any contextual dependencies that may exist between chunks because their embeddings are generated independently. Take for example the below paragraph:

Alice went for a walk in the woods one day and on her walk, she spotted something. She saw a rabbit hole at the base of a large tree. She fell into the hole and found herself in a strange new world.

If we were to chunk this paragraph by sentences we would get:

Alice went for a walk in the woods one day and on her walk, she spotted something.

She saw a rabbit hole at the base of a large tree.

She fell into the hole and found herself in a strange new world.

Now imagine that a user has populated their vector database with multiple documents, paragraphs from a book, or even multiple books. If they were to ask "Where did Alice fall" we as humans can intuitively understand that the coreference of "she" in sentence 3 refers to Alice from sentence 1. However, since these embeddings were created independently of one another there is no way for the model representation of sentence 3 to account for this relationship to the name Alice.

Late Interaction and ColBERT​

On the other side of this is the ColBERT approach which utilizes late interaction. Unlike the naive approach described above, late interaction performs no pooling step on the token embeddings belonging to the query and document. Instead, each query token is compared with all document tokens. In a retrieval setup each document has its token-level representations stored in a vector index and then at query time they can be compared via late interaction.

While ColBERT was not initially designed to work with long context, recent extensions to the underlying model have successfully extended the capabilities (via a sliding window approach) to achieve this. It is worth noting that this sliding window approach itself may actually result in the loss of important contextual information as it is a heuristic approach to creating overlaps in chunks and does not guarantee that all tokens have the ability to attend to all other tokens in the document.

Late interaction's core benefit is through the contextual information stored in each individual token representation being compared directly with each token representation in the query, without any pooling method being applied ahead of retrieval. While this approach is highly performant it can become expensive for users from a storage and cost perspective depending on their use case.

For example, let's compare the storage requirements for a long context model that outputs 8000 token-level embeddings and either uses late interaction or naive chunking:

note
This comparison assumes a fixed chunking strategy of 512 tokens for the naive approach. Where the text is split into chunks of 512 tokens, and each of those text chunks are individually embedded.
Storage requirements are calculated assuming 32-bit float precision with vector dimension size of 768.

ApproachTotal embeddings required per documentNumber of DocumentsTotal Vectors StoredStorage Required
Late Interaction (no pooling)8,000100,000800 million~2.46 TB
Naive Approach (chunking before inference)16 ( 8,000 / 512 )100,000~1.6 million~4.9 GB

Key Takeaway:

The naive approach requires only 1/500th of the storage resources compared to late interaction.

Late interaction, while more precise, demands significantly more storage capacity.

As we will see later, late chunking can offer the same reduction in storage requirements as the naive approach while preserving the contextual information that late interaction offers.

Too hot, too cold, just right?​

It appears we have a goldilocks problem, the naive approach may be more cost-effective but can reduce precision, while on the other hand, late interaction and ColBERT offer us increased precision at extreme costs. Surely there must be something in the middle that's just right? Well, late chunking may exactly that.

How Late Chunking Works​

As mentioned earlier late chunking origins are linked closely with late interaction in that both utilise the token-level vector representations that are produced during the forward pass of an embedding model.

Unlike late interaction, there is a pooling step that occurs after the initial inference. This pooling differs from traditional embedding models that pool all representations from every token into a single representation. In late chunking, this pooling is done on segments of the text according to some predetermined chunking strategy that can be aligned based on token spans or boundary cues, thus the term late chunking.

The result is that a long document is still represented by numerous embeddings but critically those embeddings are primed with contextual information relevant to their neighboring chunks.

What's required​

Late chunking requires a relatively simple alteration to the pooling step of the embedding model that can be implemented in under 30 lines of code and its vectors can be ingested as individual chunks into a vector database without any modification to the retrieval pipeline.

There are however some requirements needed ahead of performing late chunking:

Long context models are a requirement as we need token representation for the entirety of the long document to make them contextually aware. Notably, JinaAI tested using their model jina-embeddings-v2-small-en which has the highest performance to parameter ratio on MTEB's long embed retrieval benchmark. This model supports up to 8192 tokens which is roughly equivalent to 10 standard pages of text. This model also uses a mean pooling strategy in typical behavior which is a requirement for any model looking to take advantage of late interaction.

Chunking logic: being able to chunk text ahead of inference as well as associating each chunk with its corresponding token spans is also critical to making late chunking work. Luckily there are many ways to create chunks in this manner and given late chunking's ability to condition each chunk on previous ones chunking approaches like fixed-size chunking without any overlap may be all that is needed.

Late Chunking in Action​

In the below head-to-head comparison, we used our recent blog as a sample to test late chunking vs naive chunking against. Using a fixed token chunking strategy (num tokens = 128) resulted in the following sentence being split across two different chunks:

Weaviate's native, multi-tenant architecture shines for customers who need to prioritize data privacy while maintaining fast retrieval and accuracy.

The two chunks that sentence was split between are:

 Chunk 1 Chunk 2 
...tech stacks to evolve. This optionality, combined with ease of use,
helps teams scale AI prototypes into production faster. Flexibility is
also vital when it comes to architecture. Different use cases have
different requirements. For example, we work with many software companies
and those operating in regulated industries. They often require
multi-tenancy to isolate data and maintain compliance. When building a
Retrieval Augmented Generation (RAG) application, using account or
user-specific data to contextualize results, data must remain within a
dedicated tenant for its user group. 
Weaviate’s native, multi-tenant architecture shines for customers who
need to prioritize...
...data privacy while maintaining fast retrieval and accuracy. On
the other hand, we support some very large scale single-tenant use cases
that orient toward real-time data access. Many of these are in e-commerce
and industries that compete on speed and customer experience.

Head to Head Comparison​

note
The comparison below compares a naive chunking approach with late chunking using the same long context model (jina-embeddings-v2-base-en) and the same chunking strategy (num tokens = 128).
We do not include ColBERT in this comparison as for this qualitative experiment there is only a single document, therefore ColBERT in a retrieval setup would only have one document it can return and would not be useful in comparison.
Check out the notebook here

To answer the query:

what do customers need to prioritise?

We need to return both of the above chunks for a gold standard answer. However, with the naive approach we end up with two separate chunks that are not neighboring one another.

But when we apply late chunking we end returning the two exact paragraphs over which the query is most relevant.

Naive Approach (Top 2)Late Chunking (Top 2)

Chunk 8 (Similarity: 0.756): "product updates, join our upcoming
webinar."

Chunk 2 (Similarity: 0.701): "data privacy while maintaining
fast retrieval and accuracy. On the other hand, we support some very large
scale single-tenant use cases that orient toward real-time data access.
Many of these are in e-commerce and industries that compete on speed and
customer experience..."

Chunk 3 (Similarity: 0.748): "diverse use cases and the evolving
needs of developers. Introducing hot, warm, and cold storage tiers. It's
amazing to see our customers' products gain popularity, attracting more
users, and in many cases, tenants. However, as multi-tenant use cases
scale, infrastructure costs can quickly become prohibitive..."

Chunk 1 (Similarity: 0.689): "tech stacks to evolve. This
optionality, combined with ease of use, helps teams scale AI prototypes
into production faster. Flexibility is also vital when it comes to
architecture. Different use cases have different requirements. For
example, we work with many software companies and those operating in
regulated industries. They often require multi-tenancy to isolate data and
maintain compliance. When building a Retrieval Augmented Generation (RAG)
application, using account or user-specific data to contextualize results,
data must remain within a dedicated tenant for its user group. Weaviate’s
native, multi-tenant architecture shines for customers who need to
prioritize"

Intuitively we as readers understand the link between the two correlated chunks, however with the naive approach there is no ability to condition the two separate embeddings with information about their neighboring chunks.

However, when we apply late chunking this contextual conditioning is preserved and we are able to return the two exact paragraphs needed to answer the query in a RAG application.

Let's revisit our theoretical storage comparison from earlier:

ApproachTotal embeddings required per documentNumber of DocumentsTotal Vectors StoredStorage Required
Late Interaction (no pooling)8,000100,000800 million~2.46 TB
Naive Approach (chunking before inference)16 ( 8,000 / 512 )100,0001.6 million~4.9 GB
Late Chunking (chunking after inference)16 ( 8,000 / 512 )100,0001.6 million~4.9 GB

As we can see late chunking offers the same reduction in storage requirements as the naive approach while giving stronger preservation of the contextual information that late interaction offers.

If interested in more examples, here is another great notebook from Danny Williams exploring Late Chunking with quesitons about Berlin!

What this means for users building RAG applications?​

We believe that late chunking is extremely promising for a number of reasons:

It lessens the requirement for very tailored chunking strategies

It provides a cost-effective path forward for users doing long context retrieval

Its additions can be implemented in under 30 lines of code and require no modification to the retrieval pipeline

It can result in a reduction of the total number of documents required to be returned at query time

It can enable more efficient calls to LLMs by passing less context that is more relevant.

Conclusion​

In retrieval, there is no one-size-fits-all solution and the best approach will always be that which solves the user's problem given their specific constraints. However, if you want to avoid the pitfalls of naive chunking and the high potential costs of ColBERT, late chunking may be a great alternative for you to explore when you need to strike a balance between cost and performance.

Late chunking is a new approach and as such there is limited data available on its performance in benchmarks, which for long context retrieval are already scarcely available. The initial quantitative benchmarks from JinaAI are promising showing improved results across the board against naive chunking. Specifically the relative uplift in performance from late chunking was also shown to improve as the document length in characters increased, which makes sense given where the late chunking operation comes into effect.

We are keen to test late chunking out in further detail, particularly in benchmarks designed for assessing performance in long embedding retrieval. So stay tuned for more on this topic as we continue to explore the benefits of late chunking and integrate it into Weaviate.

Ready to start building?​

Check out the Quickstart tutorial, or sign up for a free Weaviate Cloud account.

Table of contents
What is Late Chunking?
Current Approaches to Long Context RetrievalNaive Chunking
Late Interaction and ColBERT
Too hot, too cold, just right?

How Late Chunking WorksWhat's required

Late Chunking in ActionHead to Head Comparison

What this means for users building RAG applications?
Conclusion
Ready to start building?

Tags
concepts

Share
Xin

Continue reading
September 22, 2026 · 15 min read
how-toagentsconcepts
Agent Memory with Engram: A Practical Guide
Learn how to use Engram effectively, from writing topic descriptions that control extraction to choosing bounded topics and scopes, selecting a retrieval mode, and placing memories in your prompt without hurting prompt-cache efficiency.
September 9, 2026 · 13 min read
engineeringconceptssearch
HFresh: Memory-Efficient Vector Search
HFresh is Weaviate's disk-based vector index for memory-efficient vector search, combining low heap usage with incremental background maintenance.
July 21, 2026 · 8 min read
conceptsengineeringsearch
Query Profiling: See Where a Slow Query Spends Its Time
When a Weaviate query is slow, the first question is where the time went. Query profiling returns a per-stage, per-shard timing breakdown, making query performance issues visible.

Don't want to miss another blog post?
Sign up for our bi-weekly newsletter to stay updated!

Follow us