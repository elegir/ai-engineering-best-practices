# Snapshot — https://arxiv.org/abs/1603.09320

Fetched 2026-10-05 by the main session with curl (HTML stripped to text; verbatim words).

[1603.09320] Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs

 Skip to main content

 Search arXiv

 Press Enter to search · Advanced search

-->

 Computer Science > Data Structures and Algorithms

 arXiv:1603.09320 (cs)

 [Submitted on 30 Mar 2016 (v1), last revised 14 Aug 2018 (this version, v4)]

 Title:Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs

 Authors:Yu. A. Malkov, D. A. Yashunin
 View a PDF of the paper titled Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs, by Yu. A. Malkov and 1 other authors

 View PDF

 Abstract:We present a new approach for the approximate K-nearest neighbor search based on navigable small world graphs with controllable hierarchy (Hierarchical NSW, HNSW). The proposed solution is fully graph-based, without any need for additional search structures, which are typically used at the coarse search stage of the most proximity graph techniques. Hierarchical NSW incrementally builds a multi-layer structure consisting from hierarchical set of proximity graphs (layers) for nested subsets of the stored elements. The maximum layer in which an element is present is selected randomly with an exponentially decaying probability distribution. This allows producing graphs similar to the previously studied Navigable Small World (NSW) structures while additionally having the links separated by their characteristic distance scales. Starting search from the upper layer together with utilizing the scale separation boosts the performance compared to NSW and allows a logarithmic complexity scaling. Additional employment of a heuristic for selecting proximity graph neighbors significantly increases performance at high recall and in case of highly clustered data. Performance evaluation has demonstrated that the proposed general metric space search index is able to strongly outperform previous opensource state-of-the-art vector-only approaches. Similarity of the algorithm to the skip list structure allows straightforward balanced distributed implementation.

 Comments:
 13 pages, 15 figures

 Subjects:

 Data Structures and Algorithms (cs.DS); Computer Vision and Pattern Recognition (cs.CV); Information Retrieval (cs.IR); Social and Information Networks (cs.SI)

 Cite as:
 arXiv:1603.09320 [cs.DS]

 (or 
 arXiv:1603.09320v4 [cs.DS] for this version)

 https://doi.org/10.48550/arXiv.1603.09320

 Focus to learn more

 arXiv-issued DOI via DataCite

 Submission history
 From: Yury Malkov A [view email] 
 [v1]
 Wed, 30 Mar 2016 19:29:44 UTC (1,613 KB)

 [v2]
 Sat, 21 May 2016 07:27:25 UTC (1,590 KB)

 [v3]
 Sun, 30 Jul 2017 12:07:54 UTC (2,481 KB)

 [v4]
 Tue, 14 Aug 2018 19:29:07 UTC (2,575 KB)

 Full-text links:
 Access Paper:

View a PDF of the paper titled Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs, by Yu. A. Malkov and 1 other authors
View PDF

 view license

 Current browse context:

 cs.DS

 < prev

   |   
 next >

 new
 | 
 recent
 | 2016-03

 Change to browse by:

 cs
 cs.CV
 cs.IR
 cs.SI

 References & Citations

 NASA ADS
Google Scholar

 Semantic Scholar

 3 blog links
 (what is this?)

 DBLP - CS Bibliography

 listing | bibtex 

Yury A. Malkov
D. A. Yashunin 

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