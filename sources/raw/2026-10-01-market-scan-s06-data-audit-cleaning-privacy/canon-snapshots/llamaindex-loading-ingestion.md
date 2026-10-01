# Written-source snapshot — https://developers.llamaindex.ai/python/framework/understanding/rag/loading/

Fetched 2026-10-01 by the main session (curl; tags stripped). Verbatim text for the s6 digest; see the registry entry for status.

Loading Data (Ingestion) | Developer Documentation Skip to content Overview Getting Started High-Level Concepts Installation and Setup How to read these docs Starter Tutorial (Using OpenAI) Starter Tutorial (Using Local LLMs) Discover LlamaIndex Video Series Frequently Asked Questions (FAQ) Async Programming in Python Learn Building an LLM application Using LLMs Building agents Building an agent Using existing tools Maintaining state Streaming output and events Human in the loop Multi-agent patterns in LlamaIndex Using Structured Output Building a RAG pipeline Introduction to RAG Indexing Indexing Loading Loading Data (Ingestion) Loading from LlamaParse Finding Data Connectors Querying Querying Storing Storing Structured Data Extraction Introduction to Structured Data Extraction Using Structured LLMs Structured Prediction Low-level structured data extraction Structured Input Tracing And Debugging Tracing and Debugging Evaluating Cost Analysis Cost Analysis Usage Pattern Evaluating Putting It All Together Putting It All Together Agents Apps Full-Stack Web Application A Guide to Building a Full-Stack Web App with LLamaIndex A Guide to Building a Full-Stack LlamaIndex Web App with Delphic Chatbots How to Build a Chatbot Q And A Q&A patterns A Guide to Extracting Terms and Definitions Structured Data Structured Data Privacy and Security Use Cases Use Cases Agents Chatbots Structured Data Extraction Fine-tuning Querying Graphs Multi-modal Prompting Question-Answering (RAG) Querying CSVs Parsing Tables and Charts Text to SQL Component Guides Component Guides Deploying Agents Agents Memory Module Guides Tools Chat Engines Chat Engine Module Guides Usage Pattern Query Engine Query Engine Module Guides Response Modes Streaming Supporting Modules Usage Pattern Evaluating Evaluating Contributing A `LabelledRagDataset` Evaluating Evaluators with `LabelledEvaluatorDataset`'s Modules Usage Pattern (Response Evaluation) Usage Pattern (Retrieval) Indexing Indexing Document Management How Each Index Works LlamaCloudIndex + LlamaCloudRetriever Using a Property Graph Index Metadata Extraction Module Guides Using VectorStoreIndex Loading Loading Data Connector Data Connectors LlamaParse Module Guides Usage Pattern Documents And Nodes Documents / Nodes Defining and Customizing Documents Metadata Extraction Usage Pattern Defining and Customizing Nodes Ingestion Pipeline Ingestion Pipeline Transformations Node Parsers Node Parser Usage Pattern Node Parser Modules SimpleDirectoryReader MCP Model Context Protocol (MCP) Converting Existing LlamaIndex Workflows & Tools to MCP LlamaCloud MCP Servers & Tools Using MCP Tools with LlamaIndex Models Models Embeddings Llms Using LLMs Using local models Available LLM integrations Customizing LLMs within LlamaIndex Abstractions Using LLMs as standalone modules Multi-modal models Prompts Prompts Prompt Usage Pattern Rerankers Observability Observability Callbacks Callbacks Token Counting - Migration Guide Instrumentation Querying Querying Node Postprocessors Node Postprocessor Node Postprocessor Modules Response Synthesizers Response Synthesizer Response Synthesis Modules Retriever Retriever Retriever Modes Retriever Modules Router Routers Structured Outputs Structured Outputs Output Parsing Modules Pydantic Programs (Deprecated) Query Engines + Pydantic Outputs Storing Storing Chat Stores Customizing Storage Document Stores Index Stores Key-Value Stores Persisting & Loading Data Vector Stores Supporting Modules Migrating from ServiceContext to Settings Configuring Settings Supporting Modules Open Source Community FAQ Frequently Asked Questions Chat Engines Documents and Nodes Embeddings Large Language Models Query Engines Vector Database Full-Stack Projects Integrations Integrations ChatGPT Plugin Integrations Unit Testing LLMs/RAG With DeepEval Fleet Context Embeddings - Building a Hybrid Search Engine for the Llamaindex Library Using Graph Stores Tracing with Graphsignal Guidance LM Format Enforcer Using Managed Indices Tonic Validate Evaluating and Tracking with TruLens Perform Evaluations on LlamaIndex with UpTrain Using Vector Stores Llama Packs Llama Packs 🦙📦 Integrations Embeddings Aleph Alpha Embeddings
 Anyscale Embeddings
 Baseten Embeddings
 Bedrock Embeddings
 Embeddings with Clarifai
 Cloudflare Workers AI Embeddings
 CohereAI Embeddings
 Custom Embeddings
 DashScope Embeddings
 Databricks Embeddings
 DeepInfra
 Elasticsearch Embeddings
 Qdrant FastEmbed Embeddings
 Fireworks Embeddings
 Google Gemini Embeddings
 GigaChat
 Google GenAI Embeddings
 Google Palm Embeddings
 Heroku LLM Managed Inference Embedding
 Local Embeddings with HuggingFace
 IBM watsonx.ai
 Isaacus Embeddings
 Jina 8K Context Window Embeddings
 Jina Embeddings
 LangChain Embeddings
 Llamafile Embeddings
 LLMRails Embeddings
 MistralAI Embeddings
 Mixedbread AI Embeddings
 ModelScope Embeddings
 Nebius Embeddings
 Netmind AI Embeddings
 Nomic Embedding
 NVIDIA NIMs
 Oracle Cloud Infrastructure (OCI) Data Science Service
 Oracle Cloud Infrastructure Generative AI
 Ollama Embeddings
 OpenAI Embeddings
 Local Embeddings with OpenVINO
 Oracle AI Vector Search: Generate Embeddings
 PremAI Embeddings
 Interacting with Embeddings deployed in Amazon SageMaker Endpoint with LlamaIndex
 Text Embedding Inference
 TextEmbed - Embedding Inference Server
 Together AI Embeddings
 Upstage Embeddings
 Interacting with Embeddings deployed in Vertex AI Endpoint with LlamaIndex
 VoyageAI Embeddings
 YandexGPT
 Llm AI21
 Aleph Alpha
 Anthropic
 Anthropic Prompt Caching
 Anyscale
 Apertis
 ASI LLM
 Azure AI model inference
 Azure OpenAI
 Baseten Cookbook
 Bedrock
 Bedrock Converse
 Cerebras
 Clarifai LLM
 Cleanlab Trustworthy Language Model
 Cohere
 CometAPI
 DashScope LLMS
 Databricks
 DeepInfra
 DeepSeek
 EverlyAI
 Featherless AI LLM
 Fireworks
 Fireworks Function Calling Cookbook
 Friendli
 Gemini
 Google GenAI
 Grok 4
 Groq
 Helicone AI Gateway
 Heroku LLM Managed Inference
 Hugging Face LLMs
 IBM watsonx.ai
 Konko
 LangChain LLM
 LiteLLM
 Replicate - Llama 2 13B
 🦙 x 🦙 Rap Battle
 Llama API
 LlamaCPP 
 llamafile
 LLM Predictor
 LM Studio
 LocalAI
 Maritalk
 MistralRS LLM
 MistralAI
 ModelScope LLMS
 Monster API <> LLamaIndex
 MyMagic AI LLM
 Nebius LLMs
 Netmind AI LLM
 Neutrino AI
 NVIDIA NIMs
 NVIDIA NIMs
 NVIDIA TensorRT-LLM
 NVIDIA LLM Text Completion API
 NVIDIA Triton
 Oracle Cloud Infrastructure Data Science 
 Oracle Cloud Infrastructure Generative AI
 OctoAI 
 Ollama LLM
 Ollama - Gemma
 OpenAI
 OpenAI JSON Mode vs. Function Calling for Data Extraction 
 OpenAI Responses API
 OpenRouter
 OpenVINO LLMs
 OpenVINO GenAI LLMs
 Optimum Intel LLMs optimized with IPEX backend
 Using Opus 4.1 with LlamaIndex
 AlibabaCloud-PaiEas
 PaLM 
 Perplexity
 [Pipeshift](https://pipeshift.com)
 Portkey
 Predibase
 PremAI LlamaIndex
 Client of Baidu Intelligent Cloud's Qianfan LLM Platform
 RunGPT
 Interacting with LLM deployed in Amazon SageMaker Endpoint with LlamaIndex
 SambaNova Systems
 Together AI LLM
 Upstage
 Vercel AI Gateway
 Vertex AI
 Replicate - Vicuna 13B
 vLLM 
 Xorbits Inference
 Yi LLMs
 Retrievers Auto Merging Retriever
 Comparing Methods for Structured Retrieval (Auto-Retrieval vs. Recursive Retrieval)
 Bedrock (Knowledge Bases)
 BM25 Retriever
 Composable Objects
 Activeloop Deep Memory
 Ensemble Retrieval Guide
 Chunk + Document Hybrid Retrieval with Long-Context Embeddings (Together.ai) 
 Pathway Retriever
 Reciprocal Rerank Fusion Retriever
 Recursive Retriever + Node References + Braintrust
 Recursive Retriever + Node References
 Relative Score Fusion and Distribution-Based Score Fusion
 Router Retriever
 Simple Fusion Retriever
 Auto-Retrieval from a Vectara Index
 Vertex AI Search Retriever
 connect to VideoDB
 You.com Retriever
 Vector stores Alibaba Cloud MySQL
 Alibaba Cloud OpenSearch Vector Store
 Google AlloyDB for PostgreSQL - `AlloyDBVectorStore`
 Amazon Neptune - Neptune Analytics vector store
 AnalyticDB
 ApertureDB as a Vector Store with LlamaIndex.
 Astra DB
 Simple Vector Store - Async Index Creation
 Awadb Vector Store
 Test delete
 Azure AI Search
 Azure CosmosDB MongoDB Vector Store
 Azure Cosmos DB No SQL Vector Store
 Azure Postgres Vector Store
 Bagel Vector Store
 Bagel Network
 Baidu VectorDB
 Cassandra Vector Store
 Auto-Retrieval from a Vector Database
 Chroma Vector Store
 Chroma + Fireworks + Nomic with Matryoshka embedding
 Chroma
 ClickHouse Vector Store
 Google Cloud SQL for PostgreSQL - `PostgresVectorStore`
 Couchbase Vector Store
 DashVector Vector Store
 Databricks Vector Search
 IBM Db2 Vector Store and Vector Search
 Deep Lake Vector Store Quickstart
 DocArray Hnsw Vector Store
 DocArray InMemory Vector Store
 Dragonfly and Vector Store
 DuckDB
 Auto-Retrieval from a Vector Database
 Elasticsearch
 Elasticsearch Vector Store
 Epsilla Vector Store
 Existing data Guide: Using Vector Store Index with Existing Pinecone Vector Store
 Guide: Using Vector Store Index with Existing Weaviate Vector Store
 Faiss Vector Store
 Firestore Vector Store
 Gel Vector Store
 Hnswlib
 Hologres
 Jaguar Vector Store
 Advanced RAG with temporal filters using LlamaIndex and KDB.AI vector store
 LanceDB Vector Store
 Lantern Vector Store (auto-retriever)
 Lantern Vector Store
 Lindorm
 Milvus Vector Store with Async API
 Milvus Vector Store with Full-Text Search
 Milvus Vector Store With Hybrid Search
 Milvus Vector Store
 Milvus Vector Store - Metadata Filter
 MongoDB Atlas Vector Store
 MongoDB Atlas + Fireworks AI RAG Example
 MongoDB Atlas + OpenAI RAG Example
 Moorcheh Vector Store Demo
 MyScale Vector Store
 Neo4j Vector Store - Metadata Filter
 Neo4j vector store
 Nile Vector Store (Multi-tenant PostgreSQL)
 ObjectBox VectorStore Demo
 OceanBase Vector Store
 Opensearch Vector Store
 Oracle AI Vector Search: Vector Store
 pgvecto.rs
 A Simple to Advanced Guide with Auto-Retrieval (with Pinecone + Arize Phoenix)
 Pinecone Vector Store - Metadata Filter
 Pinecone Vector Store
 Pinecone Vector Store - Hybrid Search
 Postgres Vector Store
 Hybrid Search with Qdrant BM42
 Qdrant Hybrid Search
 Hybrid RAG with Qdrant: multi-tenancy, custom sharding, distributed setup
 Qdrant Vector Store - Metadata Filter
 Qdrant Vector Store - Default Qdrant Filters
 Qdrant Vector Store
 Redis Vector Store
 Relyt
 Rockset Vector Store
 S3VectorStore Integration
 Simple Vector Store
 Local Llama2 + VectorStoreIndex
 Llama2 + VectorStoreIndex
 Simple Vector Stores - Maximum Marginal Relevance Retrieval
 S3/R2 Storage
 Supabase Vector Store
 TablestoreVectorStore
 Tair Vector Store
 Tencent Cloud VectorDB
 TiDB Vector Store
 Timescale Vector Store (PostgreSQL)
 txtai Vector Store
 Typesense Vector Store
 Upstash Vector Store
 load documents
 1. Installation
 Google Vertex AI Vector Search
 Google Vertex AI Vector Search v2.0
 Vespa Vector Store demo
 Auto-Retrieval from a Weaviate Vector Database
 Weaviate Vector Store Metadata Filter
 Weaviate Vector Store
 Weaviate Vector Store - Hybrid Search
 **WordLift** Vector Store
 Zep Vector Store
 ChangeLog Framework Reference 🔗 For AI Agents 
MCP servers, skills & plugins
 LlamaParse Platform MCP 
Copy MCP URL

Install in Cursor

Copy Claude Code command

Copy Codex config
 Documentation search MCP 
Copy MCP URL

Install in Cursor

Copy Claude Code command

Copy Codex config
 Framework Learn Building a RAG pipeline Loading Loading Data (Ingestion) Copy Markdown Open in Claude Open in ChatGPT Open in Cursor Copy Markdown View as Markdown Loading Data (Ingestion) Before your chosen LLM can act on your data, you first need to process the data and load it. This has parallels to data cleaning/feature engineering pipelines in the ML world, or ETL pipelines in the traditional data setting. 
 This ingestion pipeline typically consists of three main stages: 

 Load the data 
 Transform the data 
 Index and store the data 

 We cover indexing/storage in future sections . In this guide we’ll mostly talk about loaders and transformations. 
 Loaders Section titled “Loaders” 
 Before your chosen LLM can act on your data you need to load it. The way LlamaIndex does this is via data connectors, also called Reader . Data connectors ingest data from different data sources and format the data into Document objects. A Document is a collection of data (currently text, and in future, images and audio) and metadata about that data. 
 Loading using SimpleDirectoryReader Section titled “Loading using SimpleDirectoryReader” 
 The easiest reader to use is our SimpleDirectoryReader, which creates documents out of every file in a given directory. It is built in to LlamaIndex and can read a variety of formats including Markdown, PDFs, Word documents, PowerPoint decks, images, audio and video. 
 from llama_index.core import SimpleDirectoryReader 
 documents = SimpleDirectoryReader( "./data" ).load_data() 
 Using Reader integrations Section titled “Using Reader integrations” 
 Because there are so many possible places to get data, they are not all built-in. Instead, you install them as separate packages. See Data Connectors for how to find them. 
 In this example we use the DatabaseReader connector ( pip install llama-index-readers-database ), which runs a query against a SQL database and returns every row of the results as a Document : 
 from llama_index.readers.database import DatabaseReader 
 reader = DatabaseReader( scheme = os.getenv( "DB_SCHEME" ), host = os.getenv( "DB_HOST" ), port = os.getenv( "DB_PORT" ), user = os.getenv( "DB_USER" ), password = os.getenv( "DB_PASS" ), dbname = os.getenv( "DB_NAME" ), ) 
 query = "SELECT * FROM users" documents = reader.load_data( query = query) 
 There are hundreds of connectors to choose from! 
 Creating Documents directly Section titled “Creating Documents directly” 
 Instead of using a loader, you can also use a Document directly. 
 from llama_index.core import Document 
 doc = Document( text = "text" ) 
 Transformations Section titled “Transformations” 
 After the data is loaded, you then need to process and transform your data before putting it into a storage system. These transformations include chunking, extracting metadata, and embedding each chunk. This is necessary to make sure that the data can be retrieved, and used optimally by the LLM. 
 Transformation input/outputs are Node objects (a Document is a subclass of a Node ). Transformations can also be stacked and reordered. 
 We have both a high-level and lower-level API for transforming documents. 
 High-Level Transformation API Section titled “High-Level Transformation API” 
 Indexes have a .from_documents() method which accepts an array of Document objects and will correctly parse and chunk them up. However, sometimes you will want greater control over how your documents are split up. 
 from llama_index.core import VectorStoreIndex 
 vector_index = VectorStoreIndex.from_documents(documents) vector_index.as_query_engine() 
 Under the hood, this splits your Document into Node objects, which are similar to Documents (they contain text and metadata) but have a relationship to their parent Document. 
 If you want to customize core components, like the text splitter, through this abstraction you can pass in a custom transformations list or apply to the global Settings : 
 from llama_index.core.node_parser import SentenceSplitter 
 text_splitter = SentenceSplitter( chunk_size = 512 , chunk_overlap = 10 ) 
 # global from llama_index.core import Settings 
 Settings.text_splitter = text_splitter 
 # per-index index = VectorStoreIndex.from_documents( documents, transformations = [text_splitter] ) 
 Lower-Level Transformation API Section titled “Lower-Level Transformation API” 
 You can also define these steps explicitly. 
 You can do this by either using our transformation modules (text splitters, metadata extractors, etc.) as standalone components, or compose them in our declarative Transformation Pipeline interface . 
 Let’s walk through the steps below. 
 Splitting Your Documents into Nodes Section titled “Splitting Your Documents into Nodes” 
 A key step to process your documents is to split them into “chunks”/Node objects. The key idea is to process your data into bite-sized pieces that can be retrieved / fed to the LLM. 
 LlamaIndex has support for a wide range of text splitters , ranging from paragraph/sentence/token based splitters to file-based splitters like HTML, JSON. 
 These can be used on their own or as part of an ingestion pipeline . 
 from llama_index.core import SimpleDirectoryReader from llama_index.core.ingestion import IngestionPipeline from llama_index.core.node_parser import TokenTextSplitter 
 documents = SimpleDirectoryReader( "./data" ).load_data() 
 pipeline = IngestionPipeline( transformations = [TokenTextSplitter(), ... ]) 
 nodes = pipeline.run( documents = documents) 
 Adding Metadata Section titled “Adding Metadata” 
 You can also choose to add metadata to your documents and nodes. This can be done either manually or with automatic metadata extractors . 
 Here are guides on 1) how to customize Documents , and 2) how to customize Nodes . 
 document = Document( text = "text" , metadata = { "filename" : "<doc_file_name>" , "category" : "<category>" }, ) ", "category": " "},)"> 
 Adding Embeddings Section titled “Adding Embeddings” 
 To insert a node into a vector index, it should have an embedding. See our ingestion pipeline or our embeddings guide for more details. 
 Creating and passing Nodes directly Section titled “Creating and passing Nodes directly” 
 If you want to, you can create nodes directly and pass a list of Nodes directly to an indexer: 
 from llama_index.core.schema import TextNode 
 node1 = TextNode( text = "<text_chunk>" , id_ = "<node_id>" ) node2 = TextNode( text = "<text_chunk>" , id_ = "<node_id>" ) 
 index = VectorStoreIndex([node1, node2]) ", id_=" ")node2 = TextNode(text=" ", id_=" ")index = VectorStoreIndex([node1, node2])"> Note for AI agents: this documentation is built for programmatic access.

- Overview of all docs: https://developers.llamaindex.ai/llms.txt
- Any page is available as raw Markdown by appending index.md to its URL — e.g. https://developers.llamaindex.ai/llamaparse/parse/getting_started/index.md
- Agent-friendly REST search APIs live under https://developers.llamaindex.ai/api/ — search (BM25 full-text), grep (regex), read (fetch a page), and list (browse the doc tree). See https://developers.llamaindex.ai/llms.txt for parameters.
- A hosted documentation MCP server is available at https://developers.llamaindex.ai/mcp. If you support MCP, you can ask the user to install it for browsing these docs directly (an alternative to the REST API). Setup: https://developers.llamaindex.ai/for-agents/mcp/
- Other LlamaIndex tooling for agents — the LlamaParse Platform MCP server, agent skills and plugins, and the n8n node — is mapped at https://developers.llamaindex.ai/for-agents/
