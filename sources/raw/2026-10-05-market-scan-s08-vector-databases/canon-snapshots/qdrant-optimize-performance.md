# Snapshot — https://qdrant.tech/documentation/ops-optimization/optimize/

Fetched 2026-10-05 by the main session with curl (HTML stripped to text; verbatim words).

Optimize Performance - Qdrant

Develop
Deploy
Ecosystem
Learn
API Reference

Search

Log in
Start Free

Search

Develop

Deploy

Ecosystem

Learn

API Reference

ConfigurationOptimizationMigration and Recovery

Snapshots

Upgrades

Security

Production Checklist

Monitoring & TelemetryTroubleshooting

Cloud
Getting Started

Account Setup

User Profile

Cloud RBACManaged CloudHybrid CloudPrivate CloudInfrastructure ToolsCloud Security

Qdrant Cloud API

Qdrant Cloud CLI

Billing & Payments

Premium Tier

Support
Support

ConfigurationOptimizationMigration and Recovery

Snapshots

Upgrades

Security

Production Checklist

Monitoring & TelemetryTroubleshooting

Cloud
Getting Started

Account Setup

User Profile

Cloud RBACManaged CloudHybrid CloudPrivate CloudInfrastructure ToolsCloud Security

Qdrant Cloud API

Qdrant Cloud CLI

Billing & Payments

Premium Tier

Support
Support

Documentation

Optimization

Optimize Performance
Optimizing Qdrant Performance: Three Scenarios
Different use cases require different balances between memory usage, search speed, and precision. Qdrant is designed to be flexible and customizable so you can tune it to your specific needs.
This guide will walk you three main optimization strategies:
High Speed Search & Low Memory Usage
High Precision & Low Memory Usage
High Precision & High Speed Search

This page covers the memory parameter introduced in Qdrant v1.19. If you're using an older version, see the Legacy Settings section for how to map the new parameter to the old ones.An agent can work through this with you. The Diagnose high memory usage prompt makes it find which component is actually using the memory before it suggests any changes.
Agent Prompt
Diagnose high memory usageMy Qdrant memory usage is higher than I expected, or a node was killed for running out of memory. Read https://skills.qdrant.tech/qdrant-performance-optimization/memory-usage-optimization/SKILL.md first, then ask me for my collection configuration before proposing anything. Tell me which component is actually consuming the memory, whether that is the vectors, the HNSW index, or the payload indexes, and give me the fixes in order of impact. Say which ones need a reindex, and what recall I would lose if I quantize.
Uses the
qdrant-performance-optimization/memory-usage-optimization
agent skill.
What are agent skills?

1. High-Speed Search with Low Memory Usage
To achieve high search speed with minimal memory usage, you can store vectors on disk while minimizing the number of disk reads. Vector quantization is a technique that compresses vectors, allowing more of them to be stored in memory, thus reducing the need to read from disk.
To configure in-memory quantization, with on-disk original vectors, you need to create a collection with the following parameters:
memory: Set to cold to store the original vectors on disk.
datatype: Set to turbo4 to efficiently store vectors as compact 4-bits representation per dimension on disk (instead of a 32-bits floating point number).
quantization_config: Compresses quantized vectors to 1 bit using the turboquant method.
quantization_config.memory: Set to pinned to keep the quantized vectors in RAM.
PUT /collections/{collection_name}
{
 "vectors": {
 "size": 768,
 "distance": "Cosine",
 "memory": "cold",
 "datatype": "turbo4"
 },
 "quantization_config": {
 "turbo": {
 "bits": "bits1",
 "memory": "pinned"
 }
 }
}

from qdrant_client import QdrantClient, models

client.create_collection(
 collection_name="{collection_name}",
 vectors_config=models.VectorParams(
 size=768,
 distance=models.Distance.COSINE,
 memory=models.Memory.COLD,
 datatype=models.Datatype.TURBO4,
 ),
 quantization_config=models.TurboQuantization(
 turbo=models.TurboQuantQuantizationConfig(
 bits=models.TurboQuantBitSize.BITS1,
 memory=models.Memory.PINNED,
 ),
 ),
)

import { QdrantClient } from "@qdrant/js-client-rest";

client.createCollection("{collection_name}", {
 vectors: {
 size: 768,
 distance: "Cosine",
 memory: "cold",
 datatype: "turbo4"
 },
 quantization_config: {
 turbo: {
 bits: "bits1",
 memory: "pinned",
 },
 },
});

use qdrant_client::qdrant::{
 CreateCollectionBuilder, Datatype, Distance, Memory, TurboQuantBitSize, TurboQuantizationBuilder,
 VectorParamsBuilder,
};
use qdrant_client::Qdrant;

client
 .create_collection(
 CreateCollectionBuilder::new("{collection_name}")
 .vectors_config(
 VectorParamsBuilder::new(768, Distance::Cosine)
 .memory(Memory::Cold)
 .datatype(Datatype::Turbo4),
 )
 .quantization_config(
 TurboQuantizationBuilder::default()
 .bits(TurboQuantBitSize::Bits1)
 .memory(Memory::Pinned),
 ),
 )
 .await?;

import io.qdrant.client.QdrantClient;
import io.qdrant.client.QdrantGrpcClient;
import io.qdrant.client.grpc.Collections.CreateCollection;
import io.qdrant.client.grpc.Collections.Datatype;
import io.qdrant.client.grpc.Collections.Distance;
import io.qdrant.client.grpc.Collections.Memory;
import io.qdrant.client.grpc.Collections.OptimizersConfigDiff;
import io.qdrant.client.grpc.Collections.QuantizationConfig;
import io.qdrant.client.grpc.Collections.TurboQuantBitSize;
import io.qdrant.client.grpc.Collections.TurboQuantization;
import io.qdrant.client.grpc.Collections.VectorParams;
import io.qdrant.client.grpc.Collections.VectorsConfig;

client
 .createCollectionAsync(
 CreateCollection.newBuilder()
 .setCollectionName("{collection_name}")
 .setVectorsConfig(
 VectorsConfig.newBuilder()
 .setParams(
 VectorParams.newBuilder()
 .setSize(768)
 .setDistance(Distance.Cosine)
 .setMemory(Memory.Cold)
 .setDatatype(Datatype.Turbo4)
 .build())
 .build())
 .setQuantizationConfig(
 QuantizationConfig.newBuilder()
 .setTurboquant(
 TurboQuantization.newBuilder()
 .setMemory(Memory.Pinned)
 .setBits(TurboQuantBitSize.Bits1)
 .build())
 .build())
 .build())
 .get();

using Qdrant.Client;
using Qdrant.Client.Grpc;

await client.CreateCollectionAsync(
 collectionName: "{collection_name}",
 vectorsConfig: new VectorParams {
 Size = 768, Distance = Distance.Cosine, Memory = Memory.Cold, Datatype = Datatype.Turbo4
 },
 quantizationConfig: new QuantizationConfig
 {
 Turboquant = new TurboQuantization { Memory = Memory.Pinned, Bits = TurboQuantBitSize.Bits1 }
 }
);

import (
 "context"

 "github.com/qdrant/go-client/qdrant"
)

client.CreateCollection(context.Background(), &qdrant.CreateCollection{
 CollectionName: "{collection_name}",
 VectorsConfig: qdrant.NewVectorsConfig(&qdrant.VectorParams{
 Size: 768,
 Distance: qdrant.Distance_Cosine,
 Memory: qdrant.Memory_Cold.Enum(),
 Datatype: qdrant.Datatype_Turbo4.Enum(),
 }),
 QuantizationConfig: qdrant.NewQuantizationTurbo(
 &qdrant.TurboQuantization{
 Memory: qdrant.Memory_Pinned.Enum(),
 Bits: qdrant.TurboQuantBitSize_Bits1.Enum(),
 },
 ),
})

Note: These examples use the turbo4 datatype. turbo4 stores each vector dimension as a 4-bit value instead of the full 32-bit value, which improves storage efficiency but can reduce recall and search quality. Weigh these trade-offs before you use turbo4 in your vector search setup.
Disable Rescoring for Faster Search (optional)
This is completely optional, and only applicable if using binary quantization or TurboQuant with 1, 1.5 and 2 bits (other methods do not rescore by default). Disabling rescoring with search params can further reduce the number of disk reads. Note that this might slightly decrease precision.
POST /collections/{collection_name}/points/query
{
 "query": [0.2, 0.1, 0.9, 0.7],
 "params": {
 "quantization": {
 "rescore": false
 }
 },
 "limit": 10
}

from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

client.query_points(
 collection_name="{collection_name}",
 query=[0.2, 0.1, 0.9, 0.7],
 search_params=models.SearchParams(
 quantization=models.QuantizationSearchParams(rescore=False)
 ),
)

import { QdrantClient } from "@qdrant/js-client-rest";

const client = new QdrantClient({ host: "localhost", port: 6333 });

client.query("{collection_name}", {
 query: [0.2, 0.1, 0.9, 0.7],
 params: {
 quantization: {
 rescore: false,
 },
 },
});

use qdrant_client::qdrant::{
 QuantizationSearchParamsBuilder, QueryPointsBuilder, SearchParamsBuilder,
};
use qdrant_client::Qdrant;

let client = Qdrant::from_url("http://localhost:6334").build()?;

client
 .query(
 QueryPointsBuilder::new("{collection_name}")
 .query(vec![0.2, 0.1, 0.9, 0.7])
 .limit(3)
 .params(
 SearchParamsBuilder::default()
 .quantization(QuantizationSearchParamsBuilder::default().rescore(false)),
 ),
 )
 .await?;

import static io.qdrant.client.QueryFactory.nearest;

import io.qdrant.client.QdrantClient;
import io.qdrant.client.QdrantGrpcClient;
import io.qdrant.client.grpc.Points.QuantizationSearchParams;
import io.qdrant.client.grpc.Points.QueryPoints;
import io.qdrant.client.grpc.Points.SearchParams;

QdrantClient client =
 new QdrantClient(QdrantGrpcClient.newBuilder("localhost", 6334, false).build());

client.queryAsync(
 QueryPoints.newBuilder()
 .setCollectionName("{collection_name}")
 .setQuery(nearest(0.2f, 0.1f, 0.9f, 0.7f))
 .setParams(
 SearchParams.newBuilder()
 .setQuantization(
 QuantizationSearchParams.newBuilder().setRescore(false).build())
 .build())
 .setLimit(3)
 .build())
 .get();

using Qdrant.Client;
using Qdrant.Client.Grpc;

var client = new QdrantClient("localhost", 6334);

await client.QueryAsync(
 collectionName: "{collection_name}",
 query: new float[] { 0.2f, 0.1f, 0.9f, 0.7f },
 searchParams: new SearchParams
 {
 Quantization = new QuantizationSearchParams { Rescore = false }
 },
 limit: 3
);

import (
 "context"

 "github.com/qdrant/go-client/qdrant"
)

client, err := qdrant.NewClient(&qdrant.Config{
 Host: "localhost",
 Port: 6334,
})

client.Query(context.Background(), &qdrant.QueryPoints{
 CollectionName: "{collection_name}",
 Query: qdrant.NewQuery(0.2, 0.1, 0.9, 0.7),
 Params: &qdrant.SearchParams{
 Quantization: &qdrant.QuantizationSearchParams{
 Rescore: qdrant.PtrOf(false),
 },
 },
})

2. High Precision with Low Memory Usage
If you require high precision but have limited RAM, you can store both vectors and the HNSW index on disk. This setup reduces memory usage while maintaining search precision.
To move the vectors to the cold memory tier, you need to configure both the vectors and the HNSW index:
PUT /collections/{collection_name}
{
 "vectors": {
 "size": 768,
 "distance": "Cosine",
 "memory": "cold"
 },
 "hnsw_config": {
 "memory": "cold"
 }
}

from qdrant_client import QdrantClient, models

client.create_collection(
 collection_name="{collection_name}",
 vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE, memory=models.Memory.COLD),
 hnsw_config=models.HnswConfigDiff(memory=models.Memory.COLD),
)

import { QdrantClient } from "@qdrant/js-client-rest";

client.createCollection("{collection_name}", {
 vectors: {
 size: 768,
 distance: "Cosine",
 memory: "cold",
 },
 hnsw_config: {
 memory: "cold",
 },
});

use qdrant_client::qdrant::{
 CreateCollectionBuilder, Distance, HnswConfigDiffBuilder, Memory,
 VectorParamsBuilder,
};
use qdrant_client::Qdrant;

client
 .create_collection(
 CreateCollectionBuilder::new("{collection_name}")
 .vectors_config(VectorParamsBuilder::new(768, Distance::Cosine).memory(Memory::Cold))
 .hnsw_config(HnswConfigDiffBuilder::default().memory(Memory::Cold)),
 )
 .await?;

import io.qdrant.client.QdrantClient;
import io.qdrant.client.QdrantGrpcClient;
import io.qdrant.client.grpc.Collections.CreateCollection;
import io.qdrant.client.grpc.Collections.Distance;
import io.qdrant.client.grpc.Collections.HnswConfigDiff;
import io.qdrant.client.grpc.Collections.Memory;
import io.qdrant.client.grpc.Collections.VectorParams;
import io.qdrant.client.grpc.Collections.VectorsConfig;

client
 .createCollectionAsync(
 CreateCollection.newBuilder()
 .setCollectionName("{collection_name}")
 .setVectorsConfig(
 VectorsConfig.newBuilder()
 .setParams(
 VectorParams.newBuilder()
 .setSize(768)
 .setDistance(Distance.Cosine)
 .setMemory(Memory.Cold)
 .build())
 .build())
 .setHnswConfig(HnswConfigDiff.newBuilder().setMemory(Memory.Cold).build())
 .build())
 .get();

using Qdrant.Client;
using Qdrant.Client.Grpc;

await client.CreateCollectionAsync(
 collectionName: "{collection_name}",
 vectorsConfig: new VectorParams { Size = 768, Distance = Distance.Cosine, Memory = Memory.Cold },
 hnswConfig: new HnswConfigDiff { Memory = Memory.Cold }
);

import (
 "context"

 "github.com/qdrant/go-client/qdrant"
)

client.CreateCollection(context.Background(), &qdrant.CreateCollection{
 CollectionName: "{collection_name}",
 VectorsConfig: qdrant.NewVectorsConfig(&qdrant.VectorParams{
 Size: 768,
 Distance: qdrant.Distance_Cosine,
 Memory: qdrant.Memory_Cold.Enum(),
 }),
 HnswConfig: &qdrant.HnswConfigDiff{
 Memory: qdrant.Memory_Cold.Enum(),
 },
})

Improving Precision
Increase the ef and m parameters of the HNSW index to improve precision, even with limited RAM:
...
"hnsw_config": {
 "m": 64,
 "ef_construct": 512,
 "memory": "cold"
}
...

Note: The speed of this setup depends on the disk’s IOPS (Input/Output Operations Per Second).You can use fio to measure disk IOPS.
Inline Storage in HNSW Index
Available as of v1.16.0
Inline storage can increase the HNSW index size significantly. Only use it when the HNSW index is in the cold memory tier. To keep the index size to roughly 3–6 times the original float32 vectors, apply a quantization method that compresses to at most 4 bits per dimension, such as TurboQuant.When vectors and the HNSW index are in the cold memory tier, you can improve search performance by enabling the inline_storage option in the hnsw_config.
With inline storage, Qdrant stores copies of vectors directly within the HNSW index file.
It makes searches faster by reducing the number of IO operations, at the cost of increased storage usage.
To enable inline storage, quantization must be enabled.
PUT /collections/{collection_name}
{
 "vectors": {
 "size": 768,
 "distance": "Cosine",
 "memory": "cold",
 "datatype": "turbo4"
 },
 "quantization_config": {
 "turbo": {
 "memory": "cold",
 "bits": "bits1"
 }
 },
 "hnsw_config": {
 "memory": "cold",
 "inline_storage": true
 }
}

from qdrant_client import QdrantClient, models

client.create_collection(
 collection_name="{collection_name}",
 vectors_config=models.VectorParams(
 size=768,
 distance=models.Distance.COSINE,
 memory=models.Memory.COLD,
 datatype=models.Datatype.TURBO4,
 ),
 quantization_config=models.TurboQuantization(
 turbo=models.TurboQuantQuantizationConfig(
 bits=models.TurboQuantBitSize.BITS1,
 memory=models.Memory.COLD,
 )
 ),
 hnsw_config=models.HnswConfigDiff(memory=models.Memory.COLD, inline_storage=True),
)

import { QdrantClient } from "@qdrant/js-client-rest";

client.createCollection("{collection_name}", {
 vectors: {
 size: 768,
 distance: "Cosine",
 memory: "cold",
 datatype: "turbo4",
 },
 quantization_config: {
 turbo: {
 memory: "cold",
 bits: "bits1",
 },
 },
 hnsw_config: {
 memory: "cold",
 inline_storage: true,
 },
});

use qdrant_client::Qdrant;
use qdrant_client::qdrant::{
 CreateCollectionBuilder, Datatype, Distance, HnswConfigDiffBuilder, Memory,
 TurboQuantBitSize, TurboQuantizationBuilder, VectorParamsBuilder,
};

client
 .create_collection(
 CreateCollectionBuilder::new("{collection_name}")
 .vectors_config(VectorParamsBuilder::new(768, Distance::Cosine).memory(Memory::Cold).datatype(Datatype::Turbo4))
 .quantization_config(TurboQuantizationBuilder::default().memory(Memory::Cold).bits(TurboQuantBitSize::Bits1))
 .hnsw_config(
 HnswConfigDiffBuilder::default()
 .memory(Memory::Cold)
 .inline_storage(true),
 ),
 )
 .await?;

import io.qdrant.client.QdrantClient;
import io.qdrant.client.QdrantGrpcClient;
import io.qdrant.client.grpc.Collections.CreateCollection;
import io.qdrant.client.grpc.Collections.Datatype;
import io.qdrant.client.grpc.Collections.Distance;
import io.qdrant.client.grpc.Collections.HnswConfigDiff;
import io.qdrant.client.grpc.Collections.Memory;
import io.qdrant.client.grpc.Collections.QuantizationConfig;
import io.qdrant.client.grpc.Collections.TurboQuantBitSize;
import io.qdrant.client.grpc.Collections.TurboQuantization;
import io.qdrant.client.grpc.Collections.VectorParams;
import io.qdrant.client.grpc.Collections.VectorsConfig;

client
 .createCollectionAsync(
 CreateCollection.newBuilder()
 .setCollectionName("{collection_name}")
 .setVectorsConfig(
 VectorsConfig.newBuilder()
 .setParams(
 VectorParams.newBuilder()
 .setSize(768)
 .setDistance(Distance.Cosine)
 .setMemory(Memory.Cold)
 .setDatatype(Datatype.Turbo4)
 .build())
 .build())
 .setQuantizationConfig(
 QuantizationConfig.newBuilder()
 .setTurboquant(
 TurboQuantization.newBuilder().
 setMemory(Memory.Cold).
 setBits(TurboQuantBitSize.Bits1)
 .build())
 .build())
 .setHnswConfig(HnswConfigDiff.newBuilder().setMemory(Memory.Cold).setInlineStorage(true).build())
 .build())
 .get();

using Qdrant.Client;
using Qdrant.Client.Grpc;

await client.CreateCollectionAsync(
 collectionName: "{collection_name}",
 vectorsConfig: new VectorParams { Size = 768, Distance = Distance.Cosine, Memory = Memory.Cold, Datatype = Datatype.Turbo4 },
 quantizationConfig: new QuantizationConfig
 {
 Turboquant = new TurboQuantization { Memory = Memory.Cold, Bits = TurboQuantBitSize.Bits1 }
 },
 hnswConfig: new HnswConfigDiff { Memory = Memory.Cold, InlineStorage = true }
);

import (
 "context"

 "github.com/qdrant/go-client/qdrant"
)

client.CreateCollection(context.Background(), &qdrant.CreateCollection{
 CollectionName: "{collection_name}",
 VectorsConfig: qdrant.NewVectorsConfig(&qdrant.VectorParams{
 Size: 768,
 Distance: qdrant.Distance_Cosine,
 Memory: qdrant.Memory_Cold.Enum(),
 Datatype: qdrant.Datatype_Turbo4.Enum(),
 }),
 QuantizationConfig: qdrant.NewQuantizationTurbo(
 &qdrant.TurboQuantization{
 Bits: qdrant.TurboQuantBitSize_Bits1.Enum(),
 Memory: qdrant.Memory_Cold.Enum(),
 },
 ),
 HnswConfig: &qdrant.HnswConfigDiff{
 Memory: qdrant.Memory_Cold.Enum(),
 InlineStorage: qdrant.PtrOf(true),
 },
})

3. High Precision with High-Speed Search
For scenarios requiring both high speed and high precision, keep as much data in RAM as possible. Apply quantization with re-scoring for tunable accuracy.
Here is how you can configure TurboQuant quantization for a collection:
PUT /collections/{collection_name}
{
 "vectors": {
 "size": 768,
 "distance": "Cosine",
 "datatype": "turbo4"
 },
 "quantization_config": {
 "turbo": {
 "bits": "bits1",
 "memory": "pinned"
 }
 }
}

from qdrant_client import QdrantClient, models

client.create_collection(
 collection_name="{collection_name}",
 vectors_config=models.VectorParams(
 size=768,
 distance=models.Distance.COSINE,
 datatype=models.Datatype.TURBO4
 ),
 quantization_config=models.TurboQuantization(
 turbo=models.TurboQuantQuantizationConfig(
 bits=models.TurboQuantBitSize.BITS1,
 memory=models.Memory.PINNED,
 ),
 ),
)

import { QdrantClient } from "@qdrant/js-client-rest";

client.createCollection("{collection_name}", {
 vectors: {
 size: 768,
 distance: "Cosine",
 datatype: "turbo4",
 },
 quantization_config: {
 turbo: {
 type: "bits4",
 memory: "pinned",
 },
 },
});

use qdrant_client::qdrant::{
 CreateCollectionBuilder, Datatype, Distance, Memory, TurboQuantBitSize,
 TurboQuantizationBuilder, VectorParamsBuilder,
};
use qdrant_client::Qdrant;

client
 .create_collection(
 CreateCollectionBuilder::new("{collection_name}")
 .vectors_config(VectorParamsBuilder::new(768, Distance::Cosine).datatype(Datatype::Turbo4))
 .quantization_config(
 TurboQuantizationBuilder::default()
 .bits(TurboQuantBitSize::Bits1)
 .memory(Memory::Pinned),
 ),
 )
 .await?;

import io.qdrant.client.QdrantClient;
import io.qdrant.client.QdrantGrpcClient;
import io.qdrant.client.grpc.Collections.CreateCollection;
import io.qdrant.client.grpc.Collections.Datatype;
import io.qdrant.client.grpc.Collections.Distance;
import io.qdrant.client.grpc.Collections.Memory;
import io.qdrant.client.grpc.Collections.OptimizersConfigDiff;
import io.qdrant.client.grpc.Collections.QuantizationConfig;
import io.qdrant.client.grpc.Collections.TurboQuantBitSize;
import io.qdrant.client.grpc.Collections.TurboQuantization;
import io.qdrant.client.grpc.Collections.VectorParams;
import io.qdrant.client.grpc.Collections.VectorsConfig;

client
 .createCollectionAsync(
 CreateCollection.newBuilder()
 .setCollectionName("{collection_name}")
 .setVectorsConfig(
 VectorsConfig.newBuilder()
 .setParams(
 VectorParams.newBuilder()
 .setSize(768)
 .setDistance(Distance.Cosine)
 .setDatatype(Datatype.Turbo4)
 .build())
 .build())
 .setQuantizationConfig(
 QuantizationConfig.newBuilder()
 .setTurboquant(
 TurboQuantization.newBuilder()
 .setMemory(Memory.Pinned)
 .setBits(TurboQuantBitSize.Bits1)
 .build())
 .build())
 .build())
 .get();

using Qdrant.Client;
using Qdrant.Client.Grpc;

await client.CreateCollectionAsync(
 collectionName: "{collection_name}",
 vectorsConfig: new VectorParams { Size = 768, Distance = Distance.Cosine, Datatype = Datatype.Turbo4},
 quantizationConfig: new QuantizationConfig
 {
 Turboquant = new TurboQuantization { Memory = Memory.Pinned, Bits = TurboQuantBitSize.Bits1 }
 }
);

import (
 "context"

 "github.com/qdrant/go-client/qdrant"
)

client.CreateCollection(context.Background(), &qdrant.CreateCollection{
 CollectionName: "{collection_name}",
 VectorsConfig: qdrant.NewVectorsConfig(&qdrant.VectorParams{
 Size: 768,
 Distance: qdrant.Distance_Cosine,
 }),
 QuantizationConfig: qdrant.NewQuantizationTurbo(
 &qdrant.TurboQuantization{
 Memory: qdrant.Memory_Pinned.Enum(),
 Bits: qdrant.TurboQuantBitSize_Bits1.Enum(),
 },
 ),
})

Note that, by default, vectors are stored using the cached memory tier, thus there is no need to configure it explicitly.
Fine-Tuning Search Parameters
You can adjust search parameters like hnsw_ef and exact to balance between speed and precision:
Key Parameters:
hnsw_ef: Number of neighbors to visit during search (higher value = better accuracy, slower speed).
exact: Set to true for exact search, which is slower but more accurate. You can use it to compare results of the search with different hnsw_ef values versus the ground truth.
POST /collections/{collection_name}/points/query
{
 "query": [0.2, 0.1, 0.9, 0.7],
 "params": {
 "hnsw_ef": 128,
 "exact": false
 },
 "limit": 3
}

from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

client.query_points(
 collection_name="{collection_name}",
 query=[0.2, 0.1, 0.9, 0.7],
 search_params=models.SearchParams(hnsw_ef=128, exact=False),
 limit=3,
)

import { QdrantClient } from "@qdrant/js-client-rest";

const client = new QdrantClient({ host: "localhost", port: 6333 });

client.query("{collection_name}", {
 query: [0.2, 0.1, 0.9, 0.7],
 params: {
 hnsw_ef: 128,
 exact: false,
 },
 limit: 3,
});

use qdrant_client::qdrant::{QueryPointsBuilder, SearchParamsBuilder};
use qdrant_client::Qdrant;

let client = Qdrant::from_url("http://localhost:6334").build()?;

client
 .query(
 QueryPointsBuilder::new("{collection_name}")
 .query(vec![0.2, 0.1, 0.9, 0.7])
 .limit(3)
 .params(SearchParamsBuilder::default().hnsw_ef(128).exact(false)),
 )
 .await?;

import static io.qdrant.client.QueryFactory.nearest;

import io.qdrant.client.QdrantClient;
import io.qdrant.client.QdrantGrpcClient;
import io.qdrant.client.grpc.Points.QueryPoints;
import io.qdrant.client.grpc.Points.SearchParams;

QdrantClient client =
 new QdrantClient(QdrantGrpcClient.newBuilder("localhost", 6334, false).build());

client.queryAsync(
 QueryPoints.newBuilder()
 .setCollectionName("{collection_name}")
 .setQuery(nearest(0.2f, 0.1f, 0.9f, 0.7f))
 .setParams(SearchParams.newBuilder().setHnswEf(128).setExact(false).build())
 .setLimit(3)
 .build())
 .get();

using Qdrant.Client;
using Qdrant.Client.Grpc;

var client = new QdrantClient("localhost", 6334);

await client.QueryAsync(
 collectionName: "{collection_name}",
 query: new float[] { 0.2f, 0.1f, 0.9f, 0.7f },
 searchParams: new SearchParams { HnswEf = 128, Exact = false },
 limit: 3
);

import (
 "context"

 "github.com/qdrant/go-client/qdrant"
)

client, err := qdrant.NewClient(&qdrant.Config{
 Host: "localhost",
 Port: 6334,
})

client.Query(context.Background(), &qdrant.QueryPoints{
 CollectionName: "{collection_name}",
 Query: qdrant.NewQuery(0.2, 0.1, 0.9, 0.7),
 Params: &qdrant.SearchParams{
 HnswEf: qdrant.PtrOf(uint64(128)),
 Exact: qdrant.PtrOf(false),
 },
})

Balancing Latency and Throughput
When optimizing search performance, latency and throughput are two main metrics to consider:
Latency: Time taken for a single request.
Throughput: Number of requests handled per second.
The following optimization approaches are not mutually exclusive, but in some cases it might be preferable to optimize for one or another.
Minimizing Latency
To minimize latency, you can set up Qdrant to use as many cores as possible for a single request.
You can do this by setting the number of segments in the collection to be equal to the number of cores in the system.
In this case, each segment will be processed in parallel, and the final result will be obtained faster.
PUT /collections/{collection_name}
{
 "vectors": {
 "size": 768,
 "distance": "Cosine"
 },
 "optimizers_config": {
 "default_segment_number": 16
 }
}

from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

client.create_collection(
 collection_name="{collection_name}",
 vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
 optimizers_config=models.OptimizersConfigDiff(default_segment_number=16),
)

import { QdrantClient } from "@qdrant/js-client-rest";

const client = new QdrantClient({ host: "localhost", port: 6333 });

client.createCollection("{collection_name}", {
 vectors: {
 size: 768,
 distance: "Cosine",
 },
 optimizers_config: {
 default_segment_number: 16,
 },
});

use qdrant_client::qdrant::{
 CreateCollectionBuilder, Distance, OptimizersConfigDiffBuilder, VectorParamsBuilder,
};
use qdrant_client::Qdrant;

let client = Qdrant::from_url("http://localhost:6334").build()?;

client
 .create_collection(
 CreateCollectionBuilder::new("{collection_name}")
 .vectors_config(VectorParamsBuilder::new(768, Distance::Cosine))
 .optimizers_config(
 OptimizersConfigDiffBuilder::default().default_segment_number(16),
 ),
 )
 .await?;

import io.qdrant.client.QdrantClient;
import io.qdrant.client.QdrantGrpcClient;
import io.qdrant.client.grpc.Collections.CreateCollection;
import io.qdrant.client.grpc.Collections.Distance;
import io.qdrant.client.grpc.Collections.OptimizersConfigDiff;
import io.qdrant.client.grpc.Collections.VectorParams;
import io.qdrant.client.grpc.Collections.VectorsConfig;

QdrantClient client =
 new QdrantClient(QdrantGrpcClient.newBuilder("localhost", 6334, false).build());

client
 .createCollectionAsync(
 CreateCollection.newBuilder()
 .setCollectionName("{collection_name}")
 .setVectorsConfig(
 VectorsConfig.newBuilder()
 .setParams(
 VectorParams.newBuilder()
 .setSize(768)
 .setDistance(Distance.Cosine)
 .build())
 .build())
 .setOptimizersConfig(
 OptimizersConfigDiff.newBuilder().setDefaultSegmentNumber(16).build())
 .build())
 .get();

using Qdrant.Client;
using Qdrant.Client.Grpc;

var client = new QdrantClient("localhost", 6334);

await client.CreateCollectionAsync(
 collectionName: "{collection_name}",
 vectorsConfig: new VectorParams { Size = 768, Distance = Distance.Cosine },
 optimizersConfig: new OptimizersConfigDiff { DefaultSegmentNumber = 16 }
);

import (
 "context"

 "github.com/qdrant/go-client/qdrant"
)

client, err := qdrant.NewClient(&qdrant.Config{
 Host: "localhost",
 Port: 6334,
})

client.CreateCollection(context.Background(), &qdrant.CreateCollection{
 CollectionName: "{collection_name}",
 VectorsConfig: qdrant.NewVectorsConfig(&qdrant.VectorParams{
 Size: 768,
 Distance: qdrant.Distance_Cosine,
 }),
 OptimizersConfig: &qdrant.OptimizersConfigDiff{
 DefaultSegmentNumber: qdrant.PtrOf(uint64(16)),
 },
})

Maximizing Throughput
To maximize throughput, configure Qdrant to use as many cores as possible to process multiple requests in parallel.
To do that, use fewer segments (usually 2) of larger size (default 200Mb per segment) to handle more requests in parallel.
Large segments benefit from the size of the index and overall smaller number of vector comparisons required to find the nearest neighbors. However, they will require more time to build the HNSW index.
PUT /collections/{collection_name}
{
 "vectors": {
 "size": 768,
 "distance": "Cosine"
 },
 "optimizers_config": {
 "default_segment_number": 2,
 "max_segment_size": 5000000
 }
}

from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

client.create_collection(
 collection_name="{collection_name}",
 vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
 optimizers_config=models.OptimizersConfigDiff(default_segment_number=2, max_segment_size=5000000),
)

import { QdrantClient } from "@qdrant/js-client-rest";

const client = new QdrantClient({ host: "localhost", port: 6333 });

client.createCollection("{collection_name}", {
 vectors: {
 size: 768,
 distance: "Cosine",
 },
 optimizers_config: {
 default_segment_number: 2,
 max_segment_size: 5000000,
 },
});

use qdrant_client::qdrant::{
 CreateCollectionBuilder, Distance, OptimizersConfigDiffBuilder, VectorParamsBuilder,
};
use qdrant_client::Qdrant;

let client = Qdrant::from_url("http://localhost:6334").build()?;

client
 .create_collection(
 CreateCollectionBuilder::new("{collection_name}")
 .vectors_config(VectorParamsBuilder::new(768, Distance::Cosine))
 .optimizers_config(
 OptimizersConfigDiffBuilder::default().default_segment_number(2).max_segment_size(5000000),
 ),
 )
 .await?;

import io.qdrant.client.QdrantClient;
import io.qdrant.client.QdrantGrpcClient;
import io.qdrant.client.grpc.Collections.CreateCollection;
import io.qdrant.client.grpc.Collections.Distance;
import io.qdrant.client.grpc.Collections.OptimizersConfigDiff;
import io.qdrant.client.grpc.Collections.VectorParams;
import io.qdrant.client.grpc.Collections.VectorsConfig;

QdrantClient client =
 new QdrantClient(QdrantGrpcClient.newBuilder("localhost", 6334, false).build());

client
 .createCollectionAsync(
 CreateCollection.newBuilder()
 .setCollectionName("{collection_name}")
 .setVectorsConfig(
 VectorsConfig.newBuilder()
 .setParams(
 VectorParams.newBuilder()
 .setSize(768)
 .setDistance(Distance.Cosine)
 .build())
 .build())
 .setOptimizersConfig(
 OptimizersConfigDiff.newBuilder()
 .setDefaultSegmentNumber(2)
 .setMaxSegmentSize(5000000)
 .build()
 )
 .build())
 .get();

using Qdrant.Client;
using Qdrant.Client.Grpc;

var client = new QdrantClient("localhost", 6334);

await client.CreateCollectionAsync(
 collectionName: "{collection_name}",
 vectorsConfig: new VectorParams { Size = 768, Distance = Distance.Cosine },
 optimizersConfig: new OptimizersConfigDiff { DefaultSegmentNumber = 2, MaxSegmentSize = 5000000 }
);

import (
 "context"

 "github.com/qdrant/go-client/qdrant"
)

client, err := qdrant.NewClient(&qdrant.Config{
 Host: "localhost",
 Port: 6334,
})

client.CreateCollection(context.Background(), &qdrant.CreateCollection{
 CollectionName: "{collection_name}",
 VectorsConfig: qdrant.NewVectorsConfig(&qdrant.VectorParams{
 Size: 768,
 Distance: qdrant.Distance_Cosine,
 }),
 OptimizersConfig: &qdrant.OptimizersConfigDiff{
 DefaultSegmentNumber: qdrant.PtrOf(uint64(2)),
 MaxSegmentSize: qdrant.PtrOf(uint64(5000000)),
 },
})

Note: max_segment_size is expressed in kilobytes, so the example above corresponds to ~5GB.
Summary
By adjusting configurations like vector storage, quantization, and search parameters, you can optimize Qdrant for different use cases:
Low Memory + High Speed: Use vector quantization.
High Precision + Low Memory: Store vectors and HNSW index in the cold memory tier.
High Precision + High Speed: Keep data in RAM, use quantization with re-scoring.
Latency vs. Throughput: Adjust segment numbers based on the priority.
Choose the strategy that best fits your use case to get the most out of Qdrant’s performance capabilities.
Was this page useful?

Yes

No
Thank you for your feedback! 🙏
We are sorry to hear that. 😔 You can edit this page on GitHub, or create a GitHub issue.

On this page:

View as Markdown

Edit on Github

Create an issue

Ready to try Qdrant?