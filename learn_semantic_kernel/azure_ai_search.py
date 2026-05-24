import os

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import (
    QueryAnswerType,
    QueryCaptionType,
    VectorizableTextQuery,
)
from dotenv import load_dotenv

# 自动加载 .env 文件
load_dotenv()

# TODO: 不能正确的创建索引
# client = SearchIndexClient(
#     endpoint=os.getenv("AI_SEARCH_ENDPOINT"),
#     credential=AzureKeyCredential(os.getenv("AI_SEARCH_API_KEY")),
# )

# # 1. 先删旧索引（谨慎！）
# client.delete_index("test")

# # 2. 建索引，IsActive 设为 filterable=True
# index = SearchIndex(
#     name="test",
#     fields=[
#         # 1. 主键（SimpleField，正确）
#         SimpleField(name="Id", type="Edm.String", key=True),
#         # 2. 需要全文搜索的字段 → 必须用 SearchableField
#         SearchableField(name="ProductName", type="Edm.String"),
#         SearchableField(name="chunk", type="Edm.String"),
#         # 3. 普通字段
#         SimpleField(name="Price", type="Edm.Double"),
#         # 4. 需要过滤的字段 → SimpleField + filterable=True
#         SimpleField(name="IsActive", type="Edm.Boolean", filterable=True),
#     ],
# )
# client.create_index(index)


client = SearchClient(
    endpoint=os.getenv("AI_SEARCH_ENDPOINT"),
    index_name="rag-1779625951554",
    credential=AzureKeyCredential(os.getenv("AI_SEARCH_API_KEY")),
)

results = client.search(
    search_mode="any",  # 搜索模式，any=匹配任意一个词，all=必须匹配所有词
    search_text="AI",
    top=5,  # 最多5条
    search_fields=["visitor", "visit_address", "chunk"],  # 只搜这两个字段
    # filter="IsActive eq true",  # 只搜上架商品
    select=["chunk", "visitor", "visit_address"],  # 只返回需要的字段
    query_type="semantic",  # 语义重排，更准确
    # extractive 是摘抄的意思，从查询出来的问题当中摘抄出最相关的内容作为摘要。count-3 是指最多摘抄3条内容。highlight-true 是指在摘抄的内容中高亮显示查询词。
    # 最稳定、最准确、不会胡说八道
    # query_answer="extractive|count-3,highlight-true",  # 开启自动摘要和高亮，最多3条摘要。 注意：query_answer 只能和 query_type="semantic" 一起用，且必须放在 query_type 后面，否则会报错。
    # query_caption="extractive|count-3,highlight-true",  # 开启自动摘要和高亮，最多3条摘要。 注意：query_caption 只能和 query_type="semantic" 一起用，且必须放在 query_type 后面，否则会报错。
    query_caption=QueryCaptionType.EXTRACTIVE,
    query_answer=QueryAnswerType.NONE,
    vector_queries=[
        # VectorizedQuery(
        #     text="医疗AI诊断系统",
        #     fields="contentVector",
        #     k_nearest_neighbors=200,
        # ),
        VectorizableTextQuery(
            text="AI",
            fields="text_vector",
            k_nearest_neighbors=50,
        ),
    ],
)

for idx, doc in enumerate(results):
    print(f"---------- 第{idx + 1}条结果 ----------\n")
    captions = doc.get("@search.captions", [])
    # for c in captions:
    #     print("TEXT:", c.text)
    #     print("HIGHLIGHTS:", c.highlights)

    for key, value in doc.items():
        # chunk_id = c5226d058b51_12_pages_0        → 【分块ID，AI 自动切分文档时生成】
        # IsActive = True                          → 【是否上架/启用】你自己的业务字段
        # Stock = 30                               → 【库存】你自己的业务字段
        # ProductName = 超薄便携笔记本电脑          → 【产品名称】你自己的业务字段
        # Price = 4299                             → 【价格】你自己的业务字段
        # Category = 电脑办公                       → 【分类】你自己的业务字段
        # parent_id = 12                           → 【父级ID/关联ID】你自己的业务字段
        # UpdatedAt = 2026-04-22T05:43:00.403Z      → 【更新时间】你自己的业务字段
        # chunk = 14英寸全面屏，轻薄机身，办公学习通用 → 【文本分块内容】AI 检索的核心内容
        # Id = 12                                  → 【文档唯一ID】你自己的业务字段
        # @search.score = 5.2665815                → 【Azure 搜索相关性得分】越高越匹配，search_text 关键词的BM25得分
        # @search.reranker_score = None             → 【语义重排得分】没开语义搜索就是 None
        # @search.highlights = None                 → 【关键词高亮】没开启就是 None
        # @search.captions = None                   → 【自动摘要】没开启就是 None
        print(f"{key} = {value}")
