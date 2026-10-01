# Written-source snapshot — https://docs.unstructured.io/concepts/chunking

Fetched 2026-10-01 by the main session (curl; tags stripped). Verbatim text for the s6 digest; see the registry entry for status.

Unstructured chunking - Unstructured Documentation Index Fetch the complete documentation index at: /llms.txt Use this file to discover all available pages before exploring further. Skip to main content 
 After partitioning, chunking rearranges the resulting document elements into manageable “chunks” to stay within
the limits of an embedding model and to improve retrieval precision. The goal is to retrieve only parts of documents
that contain only the information that is relevant to a user’s query. You can specify if and how Unstructured chunks
those elements, based on your intended end use. 
 During chunking, Unstructured uses a basic chunking strategy that attempts to combine two or more consecutive text elements
into each chunk that fits together within the max characters setting. To determine the best max characters setting, see the documentation
for the embedding model that you want to use. 
 You can further control this behavior with by title , by page , and by similarity chunking strategies.
In all cases, Unstructured will only split individual elements if they exceed the specified max characters length.
After chunking, you will have document elements of only the following types: 

 CompositeElement : Any text element will become a CompositeElement after chunking. A composite element can be a
combination of two or more original text elements that together fit within the max characters setting. It can also be a single
element that doesn’t leave room in the chunk for any others but fits by itself. Or it can be a fragment of an original
text element that was too big to fit in one chunk and required splitting. 
 Table : A table element is not combined with other elements, and if it fits within the max characters setting it will remain as is. 
 TableChunk : Large tables that exceed the max characters setting are split into special TableChunk elements. 

 Here are a few examples: 
 { 
 "type" : "CompositeElement" , 
 "element_id" : "3e891e70121efac5f8374e4f1d41f25c" , 
 "text" : "PORTABLE DOCUMENT FORMAT (PDF) SPECIFICATIONS...<full-content-redacted-for-brevity>..." , 
 "metadata" : { 
 "filetype" : "application/pdf" , 
 "languages" : [ 
 "eng" 
 ], 
 "page_number" : 1 , 
 "orig_elements" : "eJy...<full-content-redacted-for-brevity>...tY0=" , 
 "filename" : "Portable-Document-Format-Specifications.pdf" 
 } 
 } 

 { 
 "type" : "Table" , 
 "element_id" : "2abca97d9f7dde6557cda4731f5e1d01" , 
 "text" : "Date 2005-04-08 2008-06-04 2011-12-20 2012-1-13 2014-9-26 2016-9-14...<full-content-redacted-for-brevity>..." , 
 "metadata" : { 
 "text_as_html" : "<table><thead><tr><th>Date</th><th>Version</th><th>Summary of Revisions</th></tr></thead><tbody>...<full-content-redacted-for-brevity>..." , 
 "filetype" : "application/pdf" , 
 "languages" : [ 
 "eng" 
 ], 
 "page_number" : 3 , 
 "orig_elements" : "eJz...<full-content-redacted-for-brevity>...r8=" , 
 "filename" : "Portable-Document-Format-Specifications.pdf" 
 } 
 } 

 { 
 "type" : "TableChunk" , 
 "element_id" : "57602d200f123a317637eb57596ab488" , 
 "text" : "Term Definition Team A team is defined as a social" , 
 "metadata" : { 
 "filetype" : "application/pdf" , 
 "languages" : [ 
 "eng" 
 ], 
 "orig_elements" : "eJy...<full-content-redacted-for-brevity>...Ys=" , 
 "page_number" : 5 
 }, 

 }, 
 { 
 "type" : "TableChunk" , 
 "element_id" : "4fe0a26a9f38c16b1ac2eedb4460db61" , 
 "text" : "unit of more than two people with specified roles" , 
 "metadata" : { 
 "filetype" : "application/pdf" , 
 "is_continuation" : true , 
 "languages" : [ 
 "eng" 
 ], 
 "orig_elements" : "eJy...<full-content-redacted-for-brevity>...w==" , 
 "page_number" : 5 
 } 
 } 

 If the option to include original elements is specified, during chunking the orig_elements field is added to the metadata field of each chunked element.
The orig_elements field is a list of the original elements that were used to create the current chunked element. This list is output in
gzip compressed, Base64-encoded format. To get back to the original content for this list, Base64-decode the list’s bytes, and then gzip decompress them as UTF-8. 
 After chunking, Image elements are not preserved in the output. However,
if High Res partitioning is used and the option to include original elements is also specified, the orig_elements field of each chunked element will contain
an image_base64 field for each detected image and table associated with the original elements listed within orig_elements . To get back to the
original content for an image_base64 field, Base64-decode the field’s bytes. 
 The following sections provide information about the available chunking strategies and their settings. 
 You can change a workflow’s preconfigured strategy only through Custom workflow settings. 
 ​ Basic chunking strategy 
 The basic chunking strategy uses only the max characters setting (an absolute or “hard” limit) and
 new after n characters setting (an approximate or “soft” limit) to combine sequential elements to maximally
fill each chunk. 
 This strategy adds elements to a chunk until the new after n characters limit is reached. A new chunk is then started.
No chunk will exceed the max characters limit. For elements larger than the “max characters” limit, the text is split into
multiple chunks at spaces or new lines to avoid cutting words. 
 Table elements are always treated as standalone chunks. If a table is too large, the table is chunked by rows. 
 This strategy does not use section boundaries, page boundaries, or content similarities to determine
the chunks’ contents. 
 The following diagram illustrates conceptually how a candidate element is chunked to fit within the max characters (hard) and
new after n characters (soft) limits. 

 In scenario 1, the candidate element exceeds the hard limit, and so the candidate element will become the first element in the next chunk. 
 In scenario 2, the first candidate element exceeds the soft limit but remains within the hard limit. Because the second candidate element begins
after the soft limit has been reached, the second candidate element will become the first element in the next chunk. 
 In scenario 3, the first two candidate elements exceed the soft limit but remain within the hard limit. Even though the third candidate element
remains within the hard limit, because it begins after the soft limit has been reached, the third candidate element will become the first element in the next chunk. 

 The following two conceptual diagrams show how a basic chunking strategy with a max characters setting of 200 would chunk the following text and table elements. 
 In this first conceptual diagram, each chunk of text gets as close as possible to the 200-character hard limit without going over, and lexical constructs such as sentence endings are not recognized: 

 In this second conceptual diagram, each chunk for the table also gets as close as possible to the 200-character hard limit without going over. However, for tables,
row endings are also considered in determining chunk boundaries. For this table, the first chunk is close to the 200-character hard limit and also a row ending.
The second chunk is well short of the 200-character hard limit because of a row (and, in this case, also the table) ending: 

 Context between chunks can be maintained by using the overlap and overlap all settings.
The overlap setting repeats the specified number of characters from the end of the previous chunk at the beginning of the next chunk.
By default, overlap all is applied only to relatively large elements. If overlap all is set to true, the overlap is applied to all chunks, regardless. 
 The overlap setting is based on the number of characters, so words might be split.
The overlap setting’s character count is included in the chunk size; nonetheless, the chunk’s total size must not exceed the max characters setting. 
 The following conceptual diagram illustrates conceptually how chunks are calculated by setting overlap all to true or false. In this diagram, setting overlap all to true results in a portion at the end of each chunk always being copied over to the beginning of the next chunk. 
 By default (or by setting overalp all to false), only a portion at the end of Element 6 Part 1 in Chunk 2 being is copied over
to the beginning of Element 6 Part 2 in Chunk 3, because Element 6 is larger than the max characters setting. 

 The following diagram shows how a basic chunking strategy with a max characters setting of 200, an overlap of 25 characters, and
overlap all set to true would chunk the following text. Note that some of the text is split in the middle of a word: 

 To use this chunking strategy, specify Chunk by character for a Chunker node in a workflow. 
 ​ Chunk by title strategy 
 The by-title chunking strategy attempts to preserve section boundaries when determining the chunks’ contents, primarily when
a Title element is encountered. The title is used as the section header for the chunk. The max characters and new after n
characters settings are still respected. 
 The following conceptual diagram illustrates conceptually how elements are chunked when Title elements are encountered (see
Chunks 1, 4, and 6), while still respecting the max characters and new after n characters settings (see Chunks 2 and 3): 

 A single chunk should not contain text that occurred in two different sections. When a new section starts, the existing
chunk is closed and a new one is started, even if the next element would fit in the prior chunk. 
 The following conceptual diagram illustrates this point, in that many Title elements can produce many relatively small chunks. 

 To reduce the number of chunks, you can use the combine text under n characters setting. This
setting attempts to combine elements into a single chunk until the combine text under n characters limit is reached, as shown in the
following conceptual diagram. In this case, multiple Title elements are combined into a single chunk. However, when the
combine text under n characters limit is reached, the chunk is closed and a new one is started. In any case, the new chunk must start with a Title element.
For instance, if Element 3 exceeded the combine text under n characters limit, the chunk would be closed and a new one would be started, beginning
with Title 2, followed by Element 3. 

 The following diagram shows how a chunk by title strategy with a max characters setting of 200 would chunk the following text.
Although the first chunk is close to the 200-character hard limit, the second chunk is well short of this limit due to encountering the
title immediately after it, which starts a new chunk: 

 To use this chunking strategy, specify Chunk by title for a Chunker node in a workflow. 
 ​ Chunk by page strategy 
 The by-page chunking strategy attempts to preserve page boundaries when determining the chunks’ contents.
A single chunk should not contain text that occurred in two different page. When a new page starts, the existing
chunk is closed and a new one is started, even if the next element would fit in the prior chunk. 
 The following diagram shows how a chunk by page strategy with a max characters setting of 200 would chunk the following text.
Notice that due to the page break, the second chunk is very small, as it could not fit into the first chunk’s hard character limit. 
 Nonetheless, the second chunk is still part of same page as the first chunk: 

 To use this chunking strategy, specify Chunk by page for a Chunker node in a workflow. 
 ​ Chunk by similarity strategy 
 The by-similarity chunking strategy uses the
 sentence-transformers/multi-qa-mpnet-base-dot-v1 embedding model
to identify topically similar sequential elements and combines them into chunks. 
 As with the other chunking strategies, chunks will never exceed the absolute maximum chunk size set by Max characters . For this reason,
not all elements that share a topic will necessarily appear in the same chunk. However, with this strategy you can
guarantee that two elements with low similarity will not be combined in a single chunk. 
 To use this chunking strategy, specify Chunk by similarity for a Chunker node in a workflow. 
 You can control the level of topic similarity you require for elements to have by setting Similarity threshold . 
 The following diagram shows how a chunk by similarity strategy with a max characters setting of 1000 and similarity threshold of 0.5 would chunk the following text.
Notice that the two chunks are well short of the 1000-character hard limit, as the paragraph break introduces a convenient lexical construct for
helping determinine the similarities of sentences to each other: 

 ​ Max characters setting 
 Specifies the absolute maximum number of characters in a chunk. 
 To specify this setting, specify a number for Max characters . 
 This setting applies to all of the chunking strategies. 
 ​ Combine text under n characters setting 
 Combines elements from a section into a chunk until a section reaches a length of this many characters. 
 To specify this setting, specify a number for Combine text under n chars . 
 This setting applies only to the chunking strategy Chunk by title . 
 ​ Include original elements setting 
 If Include original elements is enabled, the elements that were used to form a chunk appear in the metadata field’s orig_elements field for that chunk. 
 This setting applies to all of the chunking strategies. 
 ​ Multipage sections setting 
 If Multipage sections is enabled, this allows sections to span multiple pages. 
 This setting applies only to the chunking strategy Chunk by title . 
 ​ New after n characters setting 
 Closes new sections after reaching a length of this many characters. This is an approximate limit. 
 To specify this setting, specify a number for New after n characters . 
 This setting applies only to the chunking strategies Chunk by character , Chunk by title , and Chunk by page . 
 ​ Overlap setting 
 Applies a prefix of this many trailing characters from the prior text-split chunk to second and later chunks formed from oversized elements by text-splitting. 
 To specify this setting, specify a number for Overlap . 
 This setting applies only to the chunking strategies Chunk by character , Chunk by title , and Chunk by page . 
 ​ Overlap all setting 
 If Overlap all box is enabled, applies overlap to “normal” chunks formed by combining whole elements. Use with caution as this can introduce noise into otherwise clean semantic units. 
 This setting applies only to the chunking strategies Chunk by character , Chunk by title , and Chunk by page . 
 ​ Similarity threshold setting 
 Specifies the minimum similarity that text in consecutive elements must have to be included in the same chunk.
This must be a value between 0.0 and 1.0 , exclusive ( 0.01 to 0.99 ). The default is 0.5 if not otherwise specified. 
 To specify this setting, specify a number for Similarity threshold . 
 This setting applies only to the chunking strategy Chunk by similarity . 
 ​ Contextual chunking 
 A technique known as contextual chunking prepends chunk-specific explanatory context to each chunk.
Contextual chunking has been shown to enhance traditional RAG solutions by yielding
significant improvements in retrieval accuracy, which directly translates to better performance in downstream tasks.
 Contextual retrieval overview from Anthropic . 
 To apply contextual chunking, add a Contextual Chunker node (subtype chunk_by_contextual ) to your workflow, placed after your chunking node. Contextual chunking runs as a separate enrichment step on the chunks your chunker already produced, so chunk count and chunk IDs are preserved. 
 Deprecated: Earlier releases exposed contextual chunking as a contextual_chunking_strategy: v1 setting on the other chunking strategies. That option is no longer available in the workflow designer and is not recommended. Use the Contextual Chunker node instead. 
 This chunk-specific explanatory context information is typically a couple of sentences in length.
Contextual chunking happens before any embeddings are generated. 
 When contextual chunking is applied, the contextual information in each chunk begins with Prefix: and ends with a semicolon ( ; ).
The chunk’s original content begins with Original: . 
 For example, without contextual chunking applied, elements would for instance be generated similar to the following.
Line breaks have been inserted here for readability. The output will not contain these line breaks: 
 { 
 "type" : "CompositeElement" , 
 "element_id" : "aa482034de5ade41b7223bb3beeb6a22" , 
 "text" : "THE \n\n CONSTITUTION of the United States \n\n G \n\n NATIONAL 
 CONSTITUTION CENTER \n\n We the People of the United States, in 
 Order to form a more perfect Union, establish Justice, insure 
 ...<full-content-redacted-for-brevity>..." , 
 "metadata" : { 
 "filename" : "constitution.pdf" , 
 "filetype" : "application/pdf" , 
 "languages" : [ 
 "eng" 
 ], 
 "page_number" : 1 
 } 
 }, 
 { 
 "type" : "CompositeElement" , 
 "element_id" : "59fbfcfb51e52c426df4c48a620c6031" , 
 "text" : "SECTION. 2 \n\n The House of Representatives shall be 
 composed of Mem- bers chosen every second Year by the People 
 of the several States, and the Electors in each State shall 
 ...<full-content-redacted-for-brevity>..." , 
 "metadata" : { 
 "filename" : "constitution.pdf" , 
 "filetype" : "application/pdf" , 
 "languages" : [ 
 "eng" 
 ], 
 "page_number" : 2 
 } 
 }, 

 Applying contextual chunking to those same elements would result in the following output.
Line breaks and blank lines have been inserted here for readability. The output will not contain these line breaks and blank lines: 
 { 
 "type" : "CompositeElement" , 
 "element_id" : "063ed41d2a989191f2281b2d35c4b4ae" , 
 "text" : "Prefix: This is the opening preamble and first section of 
 Article I of the U.S. Constitution, establishing the fundamental 
 purpose of the document and the basic structure of legislative 
 power in Congress. It appears at the very beginning of the main 
 constitutional text, before all other articles and amendments.; 

 Original: THE \n\n CONSTITUTION of the United States \n\n G \n\n NATIONAL 
 CONSTITUTION CENTER \n\n We the People of the United States, in 
 Order to form a more perfect Union, establish Justice, insure 
 ...<full-content-redacted-for-brevity>..." , 
 "metadata" : { 
 "filename" : "constitution.pdf" , 
 "filetype" : "application/pdf" , 
 "languages" : [ 
 "eng" 
 ], 
 "page_number" : 1 
 } 
 }, 
 { 
 "type" : "CompositeElement" , 
 "element_id" : "2270f6b8c8b4afc668f6277789370ffd" , 
 "text" : "Prefix: This chunk appears in Article I, Section 2 of the 
 U.S. Constitution, which establishes the structure, composition, 
 and powers of the House of Representatives as one of the two 
 chambers of Congress. It follows Section 1's establishment of 
 Congress and precedes Section 3's establishment of the Senate.; 

 Original: SECTION. 2 \n\n The House of Representatives shall be 
 composed of Mem- bers chosen every second Year by the People 
 of the several States, and the Electors in each State shall 
 ...<full-content-redacted-for-brevity>..." , 
 "metadata" : { 
 "filename" : "constitution.pdf" , 
 "filetype" : "application/pdf" , 
 "languages" : [ 
 "eng" 
 ], 
 "page_number" : 2 
 } 
 } 

 ​ Implementing chunking 
 To have Unstructured perform chunking, do the following: 

 For Unstructured Pipelines users, add a Chunker node 
to an Unstructured custom workflow . 
 For Unstructured API users, add a Chunker node 
as either as an object in a workflow_nodes array
(for curl) or as a WorkflowNode in a WorkflowNodes collection (for Python) whenever you
 create a workflow ,
 update a workflow , or
 create a workflow job that processes local files . 

 ​ Learn more 

   “Breaking It Down: Chunking Strategies” in Level Up Your GenAI Apps: Essential Data Preprocessing for Any RAG System 
    Contextual Chunking in Unstructured Platform: Boost Your RAG Retrieval Accuracy 
    Chunking for RAG: best practices . 
 Was this page helpful? Yes No
