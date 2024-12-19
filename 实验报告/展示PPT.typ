#import "@preview/touying:0.5.3": *
#import themes.university: *
#import "@preview/cetz:0.2.2"
#import "@preview/fletcher:0.5.1" as fletcher: node, edge
#import "@preview/ctheorems:1.1.2": *
#import "@preview/numbly:0.1.0": numbly

// cetz and fletcher bindings for touying
#let cetz-canvas = touying-reducer.with(reduce: cetz.canvas, cover: cetz.draw.hide.with(bounds: true))
#let fletcher-diagram = touying-reducer.with(reduce: fletcher.diagram, cover: fletcher.hide)

// Pdfpc configuration
// typst query --root . ./example.typ --field value --one "<pdfpc-file>" > ./example.pdfpc
#pdfpc.config(
  duration-minutes: 30,
  start-time: datetime(hour: 14, minute: 10, second: 0),
  end-time: datetime(hour: 14, minute: 40, second: 0),
  last-minutes: 5,
  note-font-size: 12,
  disable-markdown: false,
  default-transition: (
    type: "push",
    duration-seconds: 2,
    angle: ltr,
    alignment: "vertical",
    direction: "inward",
  ),
)

// Theorems configuration by ctheorems
#show: thmrules.with(qed-symbol: $square$)
#let theorem = thmbox("theorem", "Theorem", fill: rgb("#eeffee"))
#let corollary = thmplain(
  "corollary",
  "Corollary",
  base: "theorem",
  titlefmt: strong
)
#let definition = thmbox("definition", "Definition", inset: (x: 1.2em, top: 1em))
#let example = thmplain("example", "Example").with(numbering: none)
#let proof = thmproof("proof", "Proof")

#show: university-theme.with(
  aspect-ratio: "16-9",
  // config-common(handout: true),
  config-info(
    title: [AGENT-LLM],
    subtitle: [数据库大作业展示],
    author: [胡瑞康,莫子昊,陈俊帆],
    // date: datetime.today(),
    // institution: [Institution],
    // logo: image("./img/logo.png", width: 1.5em, height: 1.5em),
  ),
)

#set heading(numbering: numbly("{1}.", default: "1.1"))

#title-slide()

== 大纲 <touying:hidden>

#components.adaptive-columns(outline(title: none, indent: 1em))

= 团队成员

#slide[

- 胡瑞康:整体项目结构设计,知识库RAG搜索,模仿OpenAI API实现,前端修改

- 莫子昊,陈俊帆：表格增删改查实现,后台测试,知识上传功能实现
]


= 技术概览


== 后端

=== 概述

- 基于Python fastapi开发,使用非阻塞式协程

- 用`psycopg3`协程链接数据库

- 封装统一`Model`接口对接数据表,减少重复sql撰写

- 通过`AsyncOpenAI`库链接兼容OpenAI接口的国产大模型平台`DeepSeek`,`智谱`

- 根据OpenAI接口规范,模拟出了他们的`chat`接口,方便任何支持对接OpenAI的项目使用我们API


#slide()[
=== FastAPI优势

  对比来源：https://www.techempower.com/

#figure(
  image("./img/round21.png", width: 60%),
  caption: [22年结果],
)
#figure(
  image("./img/round22.png", width: 60%),
  caption: [23年结果],
)
]

#slide()[
=== RAG原理

生成式语言模型（如GPT、BART等）在多种文本生成任务中表现卓越，尤其在语言生成和上下文理解方面。然而，纯生成模型在处理事实类任务时存在一些固有的局限性。

例如，由于这些模型依赖于固定的预训练数据，它们在回答需要最新或实时信息的问题时，可能会出现“编造”信息的现象，导致生成结果不准确或缺乏事实依据。

]

#slide()[
检索模型（Retriever）能够通过在海量文档中快速找到相关信息，解决事实查询的问题。然而，传统检索模型（如BM25）在面对模糊查询或跨域问题时，往往只能返回孤立的结果，无法生成连贯的自然语言回答。

检索增强生成（Retrieval-Augmented Generation，RAG）应运而生。RAG通过结合生成模型和检索模型的优势，实时从外部知识库中获取相关信息，并将其融入生成任务中，确保生成的文本既具备上下文连贯性，又包含准确的知识。
]

#slide()[

当用户提问时，先将用户问题在知识库中进行向量搜索，通过语义相似度匹配的方式查询到相关的内容，然后再将用户问题和搜索到的相关知识提供给大模型，使得大模型获得足够完备的知识来回答问题，以此获得更可靠的问答结果。

][
#figure(
  image("./img/rag.png", width: 100%),
  caption: [RAG],
)
]


== 数据库

#slide()[
使用安装了DataVec向量引擎插件的openGauss数据库

DataVec是一个基于openGauss的向量引擎，目前支持的向量功能有：精确和近似的最近邻搜索、L2距离&余弦距离&内积、向量索引、向量操作函数和操作符。作为openGauss的内核特性，DataVec使用熟悉的SQL语法操作向量，简化了用户使用向量数据库的过程。

]


#slide()[

#figure(
  image("./img/er.png", width: 100%),
  caption: [数据库ER图],
)
]

== 前端

- 后台使用`LayuiAdmin`配合`Jinja2`模板引擎

- 前台使用Github上的`chatgpt-web`做了一定修改对接后端API,传递对话id

= 效果展示

== 前台


各位同学可以使用校园网访问`db.dorm.skyw.cc`预览网页

目前导入了网络中心的一些QA做知识库,可以问该类型问题测试,比如校园网,电子邮箱等问题.

#figure(
  image("./img/frontend.png", width: 50%),
  caption: [前台],
)

== 使用其他前台程序

由于我们支持openai接口，所以可以使用任何支持openai接口的前台程序，比如`nextchat`。

可以访问`nextweb.sysumsc.cn`体验，输入`db.dorm.skyw.cc`作为API地址,`sk-123`为密钥，即可使用

#figure(
  image("./img/nextchat.png", width: 50%),
  caption: [nextchat],
)


== 后台


#slide()[

=== 表格增删改查

表格增伤改查，在业界一般称为CRUD操作，是指对数据库中的数据进行增加、查询、修改和删除操作。

借助LayuiAdmin，实现了搜索，分页，添加，修改，删除，批量删除等功能。

][

#figure(
  image("./img/message.png", width: 60%),
  caption: [消息内容],
)
]

#slide()[

#figure(
  image("./img/agent.png", width: 60%),
  caption: [智能体管理],
)

#figure(
  image("./img/model.png", width: 60%),
  caption: [模型管理],
)
][

#figure(
  image("./img/knowledgecontent.png", width: 60%),
  caption: [知识内容],
)
#figure(
  image("./img/knowledgebase.png", width: 60%),
  caption: [知识库],
)
]

#slide()[

=== 知识上传
知识上传导入功能主要包括文件上传、文件导入任务的提交、导入任务的异步处理以及文件内容的拆分和保存。

管理员可以在后台将外部文件中的知识内容导入到系统中，并自动生成嵌入向量，以便后续的知识检索和应用
][
#figure(
  image("./img/shangchuan.png", width: 60%),
  caption: [知识库],
)

]

#slide()[
=== 其余页面
#figure(
  image("./img/console.png", width: 80%),
  caption: [后台首页],
)
][
#figure(
  image("./img/setting.png", width: 80%),
  caption: [平台设置],
)
#figure(
  image("./img/pwd.png", width: 80%),
  caption: [密码设置],
)
]



== 模型封装

#slide()[
为了方便后台增删改查的实现，创建了BaseModel，封装了数据库的增删改查操作。

每个表的模型类继承自BaseModel类，可以直接调用父类的方法，减少了重复代码的编写。

][
#figure(
  image("./img/BaseModel.png", width: 80%),
  caption: [基类模型],
)
]

== 兼容Openai API


#slide()[
兼容Openai格式可以方便被各种第三方应用调用，第三方开发者无需对已有功能做修改
][
#figure(
  image("./img/api.png", width: 100%),
  caption: [API回答],
)
]

#slide()[
SSE（Server-Sent Events）是一种Web技术，它允许服务器实时向客户端推送数据。

相比于传统的轮询和长轮询机制，SSE提供了一种更高效且实时的数据推送方式。

用于给前端实现API对话。
][
#figure(
  image("./img/api-sse.png", width: 100%),
  caption: [API-SSE支持],
)
]

== 知识库RAG搜索

用户问题会先被大模型扩展为更多问题，之后调用接口Embedding，然后把向量在数据库中匹配相似的TopN个结果

由于FastAPI特性，链接数据库，调用大模型接口均使用协程
使得我们的搜索速度非常快
#figure(
  image("./img/quick-search.png", width: 50%),
  caption: [RAG搜索],
)