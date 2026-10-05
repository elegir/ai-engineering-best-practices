# Snapshot — https://docs.weaviate.io/weaviate/benchmarks/ann

Fetched 2026-10-05 by the main session with curl (HTML stripped to text; verbatim words).

ANN Benchmark | Weaviate Documentation

LLM/AI Agent Notice: For the most important and up-to-date Weaviate information, see https://weaviate.io/llms.txt
Skip to main content

Introducing Engram — managed memory for AI agents, built on Weaviate

Go to documentation:
⌘U
✕

Weaviate DatabaseDevelop AI applications using Weaviate's APIs and tools

DeployDeploy, configure, and maintain Weaviate Database

Query AgentRun agentic search over your Weaviate Cloud collections

Weaviate CloudManage and scale Weaviate in the cloud

EngramPersistent memory for LLM agents and applications

Additional resources
Integrations
Weaviate Academy

Need help?
Ask AI Assistant⌘K
Support
Community Forum
Contributor guide

Copy page

On this page
ANN Benchmark

This vector database benchmark is designed to measure and illustrate Weaviate's Approximate Nearest Neighbor (ANN) performance for a range of real-life use cases.

To make the most of this vector database benchmark, you can look at it from different perspectives:

The overall performance – Review the benchmark results to draw conclusions about what to expect from Weaviate in a production setting.

Expectation for your use case – Find the dataset closest to your production use case, and estimate Weaviate's expected performance for your use case.

Fine Tuning – If you don't get the results you expect. Find the optimal combinations of the configuration parameters (efConstruction, maxConnections and ef) to achieve the best results for your production configuration. (See HNSW Configuration Tips)

Measured Metrics​

For each benchmark test, we set these HNSW parameters:

efConstruction - Controls the search quality at build time.

maxConnections - The number of outgoing edges a node can have in the HNSW graph.

ef - Controls the search quality at query time.

HNSW Parameter Configuration Guide
For good starting point values and performance tuning advice, see HNSW Configuration Tips.

For each set of parameters, we've run 10,000 requests, and we measured the following metrics:

The Recall@10 and Recall@100 - by comparing Weaviate's results to the ground truths specified in each dataset.

Multi-threaded Queries per Second (QPS) - The overall throughput you can
achieve with each configuration.

Individual Request Latency (mean) - The mean latency over all 10,000 requests.

P99 Latency - 99% of all requests (9,900 out of 10,000) have a latency that is lower than or equal to this number

Import time - Since varying build parameters has an effect on import time, the import time is also included.

By request, we mean:
An unfiltered vector search across the entire dataset for the given test. All
latency and throughput results represent the end-to-end time that your
users would also experience. In particular, these means:

Each request time includes the network overhead for sending the results over the
wire. In the test setup, the client and server machines were located in the
same VPC.

Each request includes retrieving all the matched objects from disk. This is
a significant difference from ann-benchmarks, where the embedded libraries
only return the matched IDs.

info
This benchmark is open source, so you can reproduce the results yourself.

Benchmark Results​

This section contains datasets modeled after the ANN Benchmarks. Pick a dataset that is closest to your production workload:

DatasetNumber of ObjectsVector DimensionsDistance metricUse case
SIFT1M1 M128l2-squaredSIFT is a common ANN test dataset generated from image data
DBPedia OpenAI1 M1536cosineDBPedia dataset from MTEB embedded with OpenAI's ada002 model
MSMARCO Snowflake8.8 M768l2-squaredMSMARCO dataset embedded with Snowflake's Arctic Embed M v1.5 model
Sphere DPR10 M768dotMeta's Sphere dataset (10M sample)

Benchmark Datasets​

These are the results for each dataset:

DBPedia OpenAI
SIFT1M
MSMARCO Snowflake
Sphere DPR
QPS vs Recall for DBPedia OpenAI​
Limit 10
Limit 100

How to read the results tableChoose the desired limit using the tab selector above the table. 

The limit describes how many objects are returned for a query.
Different use cases require different levels of QPS
and returned objects per query. 

For example, at 100 QPS and limit 100 (100 objects per query) 10,000 objects will be returned in total.
At 1,000 QPS and limit 10 (10 objects per query), you
will also receive 10,000 objects in total as each request contains fewer
objects, but you can send more requests in the same timespan. 

Pick the value that matches your desired limit in production most closely.

Pick the desired configuration 

The first three columns represent the different input parameters to configure the HNSW index. These inputs lead to the results shown in columns four through six.

Recall/Throughput Trade-Off at a glance 

The highlighted columns (Recall, QPS) reflect the Recall/QPS trade-off.
Generally, as the Recall improves, the throughput drops. Pick the row
that represents a combination that satisfies your requirements. Since
the benchmark is multi-threaded and running on a 30-core machine, the
QPS/vCore columns shows the throughput per single CPU core. You can use
this column to extrapolate what the throughput would be like on a
machine of different size. See also this section below
outlining what changes to expect when running on different hardware.

Latencies 

Besides the overall throughput, columns seven and eight show the
latencies for individual requests. The Mean Latency columns shows the
mean over all 10,000 test queries. The p99 Latency shows the maximum
latency for the 99th-percentile of requests. In other words, 9,900 out
of 10,000 queries will have a latency equal to or lower than the
specified number. The difference
between mean and p99 helps you get an impression how stable the
request times are in a highly concurrent setup.

Import times 

Changing the configuration parameters can also have an effect on the
time it takes to import the dataset. This is shown in the last column.

Recommended configuration for DBPedia OpenAI ada002​
This is the recommended configuration for this dataset. It balances recall, latency, and throughput to give you a good overview of Weaviate's performance.
efConstructionmaxConnectionsefRecall@10QPS (Limit 10)Mean Latency (Limit 10)p99 Latency (Limit 10)
256169697.24%56392.80ms4.43ms

QPS vs Recall for SIFT1M​
Limit 10
Limit 100

How to read the results tableChoose the desired limit using the tab selector above the table. 

The limit describes how many objects are returned for a query.
Different use cases require different levels of QPS
and returned objects per query. 

For example, at 100 QPS and limit 100 (100 objects per query) 10,000 objects will be returned in total.
At 1,000 QPS and limit 10 (10 objects per query), you
will also receive 10,000 objects in total as each request contains fewer
objects, but you can send more requests in the same timespan. 

Pick the value that matches your desired limit in production most closely.

Pick the desired configuration 

The first three columns represent the different input parameters to configure the HNSW index. These inputs lead to the results shown in columns four through six.

Recall/Throughput Trade-Off at a glance 

The highlighted columns (Recall, QPS) reflect the Recall/QPS trade-off.
Generally, as the Recall improves, the throughput drops. Pick the row
that represents a combination that satisfies your requirements. Since
the benchmark is multi-threaded and running on a 30-core machine, the
QPS/vCore columns shows the throughput per single CPU core. You can use
this column to extrapolate what the throughput would be like on a
machine of different size. See also this section below
outlining what changes to expect when running on different hardware.

Latencies 

Besides the overall throughput, columns seven and eight show the
latencies for individual requests. The Mean Latency columns shows the
mean over all 10,000 test queries. The p99 Latency shows the maximum
latency for the 99th-percentile of requests. In other words, 9,900 out
of 10,000 queries will have a latency equal to or lower than the
specified number. The difference
between mean and p99 helps you get an impression how stable the
request times are in a highly concurrent setup.

Import times 

Changing the configuration parameters can also have an effect on the
time it takes to import the dataset. This is shown in the last column.

Recommended configuration for SIFT1M​
This is the recommended configuration for this dataset. It balances recall, latency, and throughput to give you a good overview of Weaviate's performance.
efConstructionmaxConnectionsefRecall@10QPS (Limit 10)Mean Latency (Limit 10)p99 Latency (Limit 10)
256326498.35%109401.44ms3.13ms

QPS vs Recall for MSMARCO Snowflake​
Limit 10
Limit 100

How to read the results tableChoose the desired limit using the tab selector above the table. 

The limit describes how many objects are returned for a query.
Different use cases require different levels of QPS
and returned objects per query. 

For example, at 100 QPS and limit 100 (100 objects per query) 10,000 objects will be returned in total.
At 1,000 QPS and limit 10 (10 objects per query), you
will also receive 10,000 objects in total as each request contains fewer
objects, but you can send more requests in the same timespan. 

Pick the value that matches your desired limit in production most closely.

Pick the desired configuration 

The first three columns represent the different input parameters to configure the HNSW index. These inputs lead to the results shown in columns four through six.

Recall/Throughput Trade-Off at a glance 

The highlighted columns (Recall, QPS) reflect the Recall/QPS trade-off.
Generally, as the Recall improves, the throughput drops. Pick the row
that represents a combination that satisfies your requirements. Since
the benchmark is multi-threaded and running on a 30-core machine, the
QPS/vCore columns shows the throughput per single CPU core. You can use
this column to extrapolate what the throughput would be like on a
machine of different size. See also this section below
outlining what changes to expect when running on different hardware.

Latencies 

Besides the overall throughput, columns seven and eight show the
latencies for individual requests. The Mean Latency columns shows the
mean over all 10,000 test queries. The p99 Latency shows the maximum
latency for the 99th-percentile of requests. In other words, 9,900 out
of 10,000 queries will have a latency equal to or lower than the
specified number. The difference
between mean and p99 helps you get an impression how stable the
request times are in a highly concurrent setup.

Import times 

Changing the configuration parameters can also have an effect on the
time it takes to import the dataset. This is shown in the last column.

Recommended configuration for MSMARCO Snowflake​
This is the recommended configuration for this dataset. It balances recall, latency, and throughput to give you a good overview of Weaviate's performance.
efConstructionmaxConnectionsefRecall@10QPS (Limit 10)Mean Latency (Limit 10)p99 Latency (Limit 10)
384324897.36%73632.15ms3.69ms

QPS vs Recall for Sphere DPR​
Limit 10
Limit 100

How to read the results tableChoose the desired limit using the tab selector above the table. 

The limit describes how many objects are returned for a query.
Different use cases require different levels of QPS
and returned objects per query. 

For example, at 100 QPS and limit 100 (100 objects per query) 10,000 objects will be returned in total.
At 1,000 QPS and limit 10 (10 objects per query), you
will also receive 10,000 objects in total as each request contains fewer
objects, but you can send more requests in the same timespan. 

Pick the value that matches your desired limit in production most closely.

Pick the desired configuration 

The first three columns represent the different input parameters to configure the HNSW index. These inputs lead to the results shown in columns four through six.

Recall/Throughput Trade-Off at a glance 

The highlighted columns (Recall, QPS) reflect the Recall/QPS trade-off.
Generally, as the Recall improves, the throughput drops. Pick the row
that represents a combination that satisfies your requirements. Since
the benchmark is multi-threaded and running on a 30-core machine, the
QPS/vCore columns shows the throughput per single CPU core. You can use
this column to extrapolate what the throughput would be like on a
machine of different size. See also this section below
outlining what changes to expect when running on different hardware.

Latencies 

Besides the overall throughput, columns seven and eight show the
latencies for individual requests. The Mean Latency columns shows the
mean over all 10,000 test queries. The p99 Latency shows the maximum
latency for the 99th-percentile of requests. In other words, 9,900 out
of 10,000 queries will have a latency equal to or lower than the
specified number. The difference
between mean and p99 helps you get an impression how stable the
request times are in a highly concurrent setup.

Import times 

Changing the configuration parameters can also have an effect on the
time it takes to import the dataset. This is shown in the last column.

Recommended configuration for Sphere DPR​
This is the recommended configuration for this dataset. It balances recall, latency, and throughput to give you a good overview of Weaviate's performance.
efConstructionmaxConnectionsefRecall@10QPS (Limit 10)Mean Latency (Limit 10)p99 Latency (Limit 10)
384329696.06%35234.49ms7.73ms

Benchmark Setup​

Scripts​

This benchmark is open source, so you can reproduce the results yourself.

Hardware​

This benchmark test uses one GCP instances to run both Weaviate and the Benchmark scripts:

a n4-highmem-16 instance with 16 vCPU cores and 128 GB memory.

Here's why we chose the n4-highmem-16:

It is large enough to show that Weaviate is a highly concurrent vector search engine.

It scales well while running thousands of searches across multiple threads.

It is small enough to represent a typical production case without inducing
high costs.

Based on your throughput requirements, it is very likely that you will run Weaviate
on a considerably smaller or larger machine in production.

We have outlined in the Benchmark FAQs
what you should expect when altering the configuration or
setup parameters.

Experiment Setup​

We modeled our dataset selection after
ann-benchmarks. The same test
queries are used to test speed, throughput, and recall. The provided ground
truths are used to calculate the recall.

We use Weaviate's Golang client to import data.
We use Go to measure the concurrent (multi-threaded) queries.
Each language has its own performance characteristics.
You may get different results if you use a different language to send your queries.

For maximum throughput, we recommend using the Go or
Java client libraries.

The complete import and test scripts are available here.

Benchmark FAQ​

How can I get the most performance for my use case?​

If your use case is similar to one of the benchmark tests, use the recommended HNSW parameter configurations to start tuning.

For more instructions on how to tune your configuration for best performance, see HNSW Configuration Tips.

What is the difference between latency and throughput?​

The latency refers to the time it takes to complete a single request. This
is typically measured by taking a mean or percentile distribution of all
requests. For example, a mean latency of 5ms means that a single request takes, on average, 5ms to complete. This does not say anything about how many queries
can be answered in a given timeframe.

If Weaviate were single-threaded, the throughput per second would roughly equal
to 1s divided by mean latency. For example, with a mean latency of 5ms, this
would mean that 200 requests can be answered in a second.

However, in reality, you often don't have a single user sending one query after
another. Instead, you have multiple users sending queries. This makes the
querying side concurrent. Similarly, Weaviate can handle concurrent incoming
requests. We can identify how many concurrent requests can be served by measuring
the throughput.

We can take our single-thread calculation from before and multiply it with the
number of server CPU cores. This will give us a rough estimate of what the
server can handle concurrently. However, it would be best never to trust this
calculation alone and continuously measure the actual throughput. This is because
such scaling may not always be linear. For example, there may be synchronization
mechanisms used to make concurrent access safe, such as locks. Not only do
these mechanisms have a cost themselves, but if implemented incorrectly, they
can also lead to congestion, which would further decrease the concurrent
throughput. As a result, you cannot perform a single-threaded benchmark and
extrapolate what the numbers would be like in a multi-threaded setting.

All throughput numbers ("QPS") outlined in this benchmark are actual
multi-threaded measurements on a 30-core machine, not estimations.

What is a p99 latency?​

The mean latency gives you an average value of all requests measured. This is a
good indication of how long a user will have to wait on average for
their request to be completed. Based on this mean value, you cannot make any
promises to your users about wait times. 90 out of 100 users might see a
considerably better time, but the remaining 10 might see a significantly worse
time.

Percentile-based latencies are used to give a more precise indication. A
99th-percentile latency - or "p99 latency" for short - indicates the slowest
request that 99% of requests experience. In other words, 99% of your users will
experience a time equal to or better than the stated value. This is a much
better guarantee than a mean value.

In production settings, requirements - as stated in support plans - are often a
combination of throughput and a percentile latency. For example, the statement
"3000 QPS at p95 latency of 20ms" conveys the following meaning.

3000 requests need to be successfully completed per second

95% of users must see a latency of 20ms or lower.

There is no assumption about the remaining 5% of users, implicitly tolerating
that they will experience higher latencies than 20ms.

The higher the percentile (e.g. p99 over p95) the "safer" the quoted
latency becomes. We have thus decided to use p99-latencies instead of
p95-latencies in our measurements.

What happens if I run with fewer or more CPU cores than on the example test machine?​

The benchmark outlines a QPS per core measurement. This can help you make a
rough estimation of how the throughput would vary on smaller or larger
machines. If you do not need the stated throughput, you can run with fewer CPU
cores. If you need more throughput, you can run with more CPU cores.

Adding more CPUs reaches a point of diminishing returns because of synchronization mechanisms, disk, and memory bottlenecks. Beyond that point, you should scale horizontally instead of vertically. Horizontal scaling with replication is also available.

What are ef, efConstruction, and maxConnections?​

These parameters refer to the HNSW build and query
parameters.
They represent a trade-off between recall, latency & throughput, index size, and
memory consumption. This trade-off is highlighted in the benchmark results.

I can't match the same latencies/throughput in my own setup. How can I debug this?​

If you are encountering other numbers in your own dataset, here are a couple of
hints to look at:

What CPU architecture are you using? The benchmarks above were run on a GCP
c2 CPU type, which is based on amd64 architecture. Weaviate also supports
arm64 architecture, but not all optimizations are present. If your machine
shows maximum CPU usage but you cannot achieve the same throughput, consider
switching the CPU type to the one used in this benchmark.

Are you using an actual dataset or random vectors? HNSW is known to perform
considerably worse with random vectors than with real-world datasets. This is due
to the distribution of points in real-world datasets compared to randomly
generated vectors. If you cannot achieve the performance (or recall)
outlined above with random vectors, switch to an actual dataset.

Are your disks fast enough? While the ANN search itself is CPU-bound, the objects
must be read from disk after the search has been completed. Weaviate
uses memory-mapped files to speed this process up. However, if not enough
memory is present or the operating system has allocated the cached pages
elsewhere, a physical disk read needs to occur. If your disk is slow,
it could then be that your benchmark is bottlenecked by those disks.

Are you using more than 2 million vectors? If yes, make sure to set the
vector cache large enough
for maximum performance.

Where can I find the scripts to run this benchmark myself?​

The repository is located here.

Questions and feedback​

Have a question or feedback? Here's how to reach us.
Community Forum
Ask questions and connect with other developers on our Community forum.
Support
Weaviate Cloud user or customer? Find the right channel on the Support page.

Measured Metrics
Benchmark Results
Benchmark SetupScripts
Hardware
Experiment Setup

Benchmark FAQHow can I get the most performance for my use case?
What is the difference between latency and throughput?
What is a p99 latency?
What happens if I run with fewer or more CPU cores than on the example test machine?
What are ef, efConstruction, and maxConnections?
I can't match the same latencies/throughput in my own setup. How can I debug this?
Where can I find the scripts to run this benchmark myself?

Questions and feedback

Was this page helpful?
YesNo