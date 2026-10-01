# Written-source snapshot — https://supabase.com/docs/guides/ai/rag-with-permissions

Fetched 2026-10-01 by the main session (curl; tags stripped). Verbatim text for the s6 digest; see the registry entry for status.

RAG with Permissions | Supabase Docs Skip to content DOCS Search docs... Ctrl K DOCS Search docs... Ctrl K AI & Vectors Since pgvector is built on top of Postgres, you can implement fine-grained access control on your vector database using Row Level Security (RLS) . This means you can restrict which documents are returned during a vector similarity search to users that have access to them. Supabase also supports Foreign Data Wrappers (FDW) which means you can use an external database or data source to determine these permissions if your user data doesn't exist in Supabase. 
 Use this guide to learn how to restrict access to documents when performing retrieval augmented generation (RAG). 
 Example # 
 In a typical RAG setup, your documents are chunked into small subsections and similarity is performed over those sections: 
 1 -- Track documents/pages/files/etc 2 create table documents ( 3 id bigint primary key generated always as identity , 4 name text not null , 5 owner_id uuid not null references auth . users (id) default auth . uid () , 6 created_at timestamp with time zone not null default now () 7 ); 8 9 -- Store the content and embedding vector for each section in the document 10 -- with a reference to original document (one-to-many) 11 create table document_sections ( 12 id bigint primary key generated always as identity , 13 document_id bigint not null references documents (id), 14 content text not null , 15 embedding extensions . vector ( 384 ) 16 ); 
 Notice the record of owner_id on each document. Create an RLS policy that restricts access to document_sections based on whether or not they own the linked document: 
 1 -- Grant the privileges the roles need 2 GRANT SELECT ON public . document_sections TO authenticated; 3 4 -- enable row level security 5 alter table document_sections enable row level security ; 6 7 -- setup RLS for select operations 8 create policy " Users can query their own document sections " 9 on document_sections for select to authenticated using ( 10 document_id in ( 11 select id 12 from documents 13 where (owner_id = ( select auth . uid () )) 14 ) 15 ); 
 In this example, the current user is determined using the built-in auth.uid() function when the query is executed through your project's auto-generated REST API . If you are connecting to your Supabase database through a direct Postgres connection, see Direct Postgres Connection below for directions on how to achieve the same access control. 
 Now every select query executed on document_sections will implicitly filter the returned sections based on whether or not the current user has access to them. 
 For example, executing: 
 1 select * from document_sections; 
 as an authenticated user will only return rows that they are the owner of (as determined by the linked document). More importantly, semantic search over these sections (or any additional filtering for that matter) will continue to respect these RLS policies: 
 1 -- Perform inner product similarity based on a match_threshold 2 select * 3 from document_sections 4 where document_sections . embedding < # > embedding < - match_threshold 5 order by document_sections . embedding < # > embedding; 
 The above example only configures select access to users. If you wanted, you could create more RLS policies for inserts, updates, and deletes in order to apply the same permission logic for those other operations. See Row Level Security for a more in-depth guide on RLS policies. 
 Alternative scenarios # 
 Every app has its own unique requirements and may differ from the above example. Here are some alternative scenarios we often see and how they are implemented in Supabase. 
 Documents owned by multiple people # 
 Instead of a one-to-many relationship between users and documents , you may require a many-to-many relationship so that multiple people can access the same document. Reimplement this using a join table: 
 1 create table document_owners ( 2 id bigint primary key generated always as identity , 3 owner_id uuid not null references auth . users (id) default auth . uid () , 4 document_id bigint not null references documents (id) 5 ); 
 Then your RLS policy would change to: 
 1 create policy " Users can query their own document sections " 2 on document_sections for select to authenticated using ( 3 document_id in ( 4 select document_id 5 from document_owners 6 where (owner_id = ( select auth . uid () )) 7 ) 8 ); 
 Instead of directly querying the documents table, we query the join table. 
 User and document data live outside of Supabase # 
 You may have an existing system that stores users, documents, and their permissions in a separate database. Consider the scenario where this data exists in another Postgres database. We'll use a foreign data wrapper (FDW) to connect to the external DB from within your Supabase DB: 
 RLS is latency-sensitive, so extra caution should be taken before implementing this method. Use the query plan analyzer to measure execution times for your queries to ensure they are within expected ranges. For enterprise applications, contact enterprise@supabase.io . 
 For data sources other than Postgres, see Foreign Data Wrappers for a list of external sources supported today. If your data lives in a source not provided in the list, contact support and we'll be happy to discuss your use case. 
 Assume your external DB contains a users and documents table like this: 
 1 create table public .users ( 2 id bigint primary key generated always as identity , 3 email text not null , 4 created_at timestamp with time zone not null default now () 5 ); 6 7 create table public .documents ( 8 id bigint primary key generated always as identity , 9 name text not null , 10 owner_id bigint not null references public . users (id), 11 created_at timestamp with time zone not null default now () 12 ); 
 In your Supabase DB, create foreign tables that link to the above tables: 
 1 create schema external ; 2 create extension postgres_fdw with schema extensions; 3 4 -- Setup the foreign server 5 create server foreign_server 6 foreign data wrapper postgres_fdw 7 options (host ' <db-host> ' , port ' <db-port> ' , dbname ' <db-name> ' ); 8 9 -- Map local 'authenticated' role to external 'postgres' user 10 create user mapping for authenticated 11 server foreign_server 12 options (user ' postgres ' , password ' <user-password> ' ); 13 14 -- Import foreign 'users' and 'documents' tables into 'external' schema 15 import foreign schema public limit to (users, documents) 16 from server foreign_server into external ; 
 This example maps the authenticated role in Supabase to the postgres user in the external DB. In production, it's best to create a custom user on the external DB that has the minimum permissions necessary to access the information you need. On the Supabase DB, we use the built-in authenticated role which is automatically used when end users make authenticated requests over your auto-generated REST API. If you plan to connect to your Supabase DB over a direct Postgres connection instead of the REST API, you can change this to any user you like. See Direct Postgres Connection for more info. 
 We'll store document_sections and their embeddings in Supabase so that we can perform similarity search over them via pgvector. 
 1 create table document_sections ( 2 id bigint primary key generated always as identity , 3 document_id bigint not null , 4 content text not null , 5 embedding extensions . vector ( 384 ) 6 ); 
 We maintain a reference to the foreign document via document_id , but without a foreign key reference since foreign keys can only be added to local tables. Be sure to use the same ID data type that you use on your external documents table. 
 Since we're managing users and authentication outside of Supabase, we have two options: 

 Make a direct Postgres connection to the Supabase DB and set the current user every request 
 Issue a custom JWT from your system and use it to authenticate with the REST API 

 Direct Postgres connection # 
 You can directly connect to your Supabase Postgres DB using the connection info on a project page. To use RLS with this method, we use a custom session variable that contains the current user's ID: 
 1 -- enable row level security 2 alter table document_sections enable row level security ; 3 4 -- setup RLS for select operations 5 create policy " Users can query their own document sections " 6 on document_sections for select to authenticated using ( 7 document_id in ( 8 select id 9 from external . documents 10 where owner_id = current_setting( ' app.current_user_id ' ):: bigint 11 ) 12 ); 
 The session variable is accessed through the current_setting() function. We name the variable app.current_user_id here, but you can modify this to any name you like. We also cast it to a bigint since that was the data type of the user.id column. Change this to whatever data type you use for your ID. 
 Now for every request, we set the user's ID at the beginning of the session: 
 1 set app . current_user_id = ' <current-user-id> ' ; 
 Then all subsequent queries will inherit the permission of that user: 
 1 -- Only document sections owned by the user are returned 2 select * 3 from document_sections 4 where document_sections . embedding < # > embedding < - match_threshold 5 order by document_sections . embedding < # > embedding; 
 You might be tempted to discard RLS completely and filter by user within the where clause. Though this will work, we recommend RLS as a general best practice since RLS is always applied even as new queries and application logic is introduced in the future. 
 Custom JWT with REST API # 
 If you would like to use the auto-generated REST API to query your Supabase database using JWTs from an external auth provider, you can get your auth provider to issue a custom JWT for Supabase. 
 See the Clerk Supabase docs for an example of how this can be done. Modify the instructions to work with your own auth provider as needed. 
 Now we can use the same RLS policy from our first example: 
 1 -- enable row level security 2 alter table document_sections enable row level security ; 3 4 -- setup RLS for select operations 5 create policy " Users can query their own document sections " 6 on document_sections for select to authenticated using ( 7 document_id in ( 8 select id 9 from documents 10 where (owner_id = ( select auth . uid () )) 11 ) 12 ); 
 Under the hood, auth.uid() references current_setting('request.jwt.claim.sub') which corresponds to the JWT's sub (subject) claim. This setting is automatically set at the beginning of each request to the REST API. 
 All subsequent queries will inherit the permission of that user: 
 1 -- Only document sections owned by the user are returned 2 select * 3 from document_sections 4 where document_sections . embedding < # > embedding < - match_threshold 5 order by document_sections . embedding < # > embedding; 
 Other scenarios # 
 There are endless approaches to this problem based on the complexities of each system. Luckily Postgres comes with all the primitives needed to provide access control in the way that works best for your project. 
 If the examples above didn't fit your use case or you need to adjust them slightly to better fit your existing system, feel free to reach out to support and we'll be happy to assist you. Is this helpful? No Yes AI Tools Connect your AI agent Copy as Markdown Ask ChatGPT Ask Claude
