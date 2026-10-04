# Snapshot — https://arxiv.org/abs/2409.04701

Fetched 2026-10-04 by the main session with curl (HTML stripped to text; verbatim words).

[2409.04701] Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models

 Skip to main content

 Search arXiv

 Press Enter to search · Advanced search

-->

 Computer Science > Computation and Language

 arXiv:2409.04701 (cs)

 [Submitted on 7 Sep 2024 (v1), last revised 7 Jul 2025 (this version, v3)]

 Title:Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models

 Authors:Michael Günther, Isabelle Mohr, Daniel James Williams, Bo Wang, Han Xiao
 View a PDF of the paper titled Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models, by Michael G\"unther and 4 other authors

 View PDF
 HTML (experimental)

 Abstract:Many use cases require retrieving smaller portions of text, and dense vector-based retrieval systems often perform better with shorter text segments, as the semantics are less likely to be over-compressed in the embeddings. Consequently, practitioners often split text documents into smaller chunks and encode them separately. However, chunk embeddings created in this way can lose contextual information from surrounding chunks, resulting in sub-optimal representations. In this paper, we introduce a novel method called late chunking, which leverages long context embedding models to first embed all tokens of the long text, with chunking applied after the transformer model and just before mean pooling - hence the term late in its naming. The resulting chunk embeddings capture the full contextual information, leading to superior results across various retrieval tasks. The method is generic enough to be applied to a wide range of long-context embedding models and works without additional training. To further increase the effectiveness of late chunking, we propose a dedicated fine-tuning approach for embedding models.

 Comments:
 11 pages, 3rd draft

 Subjects:

 Computation and Language (cs.CL); Information Retrieval (cs.IR)

 MSC classes:
 68T50

 ACM classes:
 I.2.7

 Cite as:
 arXiv:2409.04701 [cs.CL]

 (or 
 arXiv:2409.04701v3 [cs.CL] for this version)

 https://doi.org/10.48550/arXiv.2409.04701

 Focus to learn more

 arXiv-issued DOI via DataCite

 Submission history
 From: Han Xiao [view email] 
 [v1]
 Sat, 7 Sep 2024 03:54:46 UTC (268 KB)

 [v2]
 Wed, 2 Oct 2024 15:07:09 UTC (273 KB)

 [v3]
 Mon, 7 Jul 2025 17:49:51 UTC (203 KB)

 Full-text links:
 Access Paper:

View a PDF of the paper titled Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models, by Michael G\"unther and 4 other authors
View PDF
HTML (experimental)
TeX Source

 view license

 Current browse context:

 cs.CL

 < prev

   |   
 next >

 new
 | 
 recent
 | 2024-09

 Change to browse by:

 cs
 cs.IR

 References & Citations

 NASA ADS
Google Scholar

 Semantic Scholar

 export BibTeX citation
 Loading...

 BibTeX formatted citation

 ×

 loading...

 Data provided by: 

 Bookmark

 Bibliographic Tools

 Bibliographic and Citation Tools

 Bibliographic Explorer Toggle

 Bibliographic Explorer (What is the Explorer?)

 Connected Papers Toggle

 Connected Papers (What is Connected Papers?)

 Litmaps Toggle

 Litmaps (What is Litmaps?)

 scite.ai Toggle

 scite Smart Citations (What are Smart Citations?)

 Code, Data, Media

 Code, Data and Media Associated with this Article

 alphaXiv Toggle

 alphaXiv (What is alphaXiv?)

 Links to Code Toggle

 CatalyzeX Code Finder for Papers (What is CatalyzeX?)

 DagsHub Toggle

 DagsHub (What is DagsHub?)

 GotitPub Toggle

 Gotit.pub (What is GotitPub?)

 Huggingface Toggle

 Hugging Face (What is Huggingface?)

 ScienceCast Toggle

 ScienceCast (What is ScienceCast?)

 Demos

 Demos

 Replicate Toggle

 Replicate (What is Replicate?)

 Spaces Toggle

 Hugging Face Spaces (What is Spaces?)

 Spaces Toggle

 TXYZ.AI (What is TXYZ.AI?)

 Related Papers

 Recommenders and Search Tools

 Link to Influence Flower

 Influence Flower (What are Influence Flowers?)

 Core recommender toggle

 CORE Recommender (What is CORE?)

 Author

 Venue

 Institution

 Topic

 About arXivLabs

 arXivLabs: experimental projects with community collaborators

 arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

 Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

 Have an idea for a project that will add value for arXiv's community? Learn more about arXivLabs.

 Which authors of this paper are endorsers? |
 Disable MathJax (What is MathJax?)