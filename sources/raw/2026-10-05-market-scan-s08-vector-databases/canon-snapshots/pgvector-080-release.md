# Snapshot — https://www.postgresql.org/about/news/pgvector-080-released-2952/

Fetched 2026-10-05 by the main session with curl (HTML stripped to text; verbatim words).

PostgreSQL: pgvector 0.8.0 Released!

 September 24, 2026: PostgreSQL 19 Beta 4 Released!

 Quick Links

 About

 Governance

 Policies

 Feature Matrix

 Donate

 History

 Sponsors

 Contributing

 Financial

 Servers

 Latest News

 Upcoming Events

 Past events

 Press

 Licence

pgvector 0.8.0 Released!

Posted on 2024-11-11 by pgvector

 Related Open Source

pgvector, an open-source PostgreSQL extension that provides vector similarity search capabilities, has released v0.8.0. This release includes features that improve query performance and usability when using filters (e.g. the WHERE clause), and performance improvements for searching and building HNSW indexes.

This latest version of pgvector has a variety of improvements for filtering. This includes an update to how PostgreSQL estimates when to scan a approximate nearest neighbor (ANN) index like HNSW and IVFFlat, which could lead PostgreSQL to select a B-tree or other index that more efficiently executes the query. If you can achieve the same query performance without using an ANN index, this is usually preferable as it lets you achieve 100% recall, or high relevancy searches.

Additionally, this pgvector release adds iterative index scans, which is a technique to prevent "overfiltering" or not returning enough results to satisfy the conditions of a query. You can enable iterative scanning with the hnsw.iterative_scan and ivfflat.iterative_scan parameters for HNSW and IVFFlat indexes respectively, and if an initial index scan doesn't satisfy the query conditions, pgvector will continue to search the index until it hits a configurable threshold (hnsw.max_scan_tuples and ivfflat.max_probes). 

For more information, please see the CHANGELOG for 0.8.0:

https://github.com/pgvector/pgvector/blob/master/CHANGELOG.md#080-2024-10-30

For more information about pgvector, including how to get started, please visit the project repository on GitHub:

https://github.com/pgvector/pgvector