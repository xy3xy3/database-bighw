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

== 数据库

使用安装了DataVec向量引擎插件的openGauss数据库

#figure(
  image("./img/er.png", width: 70%),
  caption: [数据库ER图],
)

== 后端

- 基于Python fastapi开发,使用非阻塞式协程

- 用`psycopg3`协程链接数据库

- 封装统一`Model`接口对接数据表,减少重复sql撰写

- 通过`AsyncOpenAI`库链接兼容OpenAI接口的国产大模型平台`DeepSeek`,`智谱`

- 根据OpenAI接口规范,模拟出了他们的`chat`接口,方便任何支持对接OpenAI的项目使用我们API

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


== 后台

#slide()[

#figure(
  image("./img/console.png", width: 80%),
  caption: [后台首页],
)

#figure(
  image("./img/knowledgebase.png", width: 80%),
  caption: [知识库],
)
][
#figure(
  image("./img/knowledgecontent.png", width: 80%),
  caption: [知识内容],
)
#figure(
  image("./img/model.png", width: 80%),
  caption: [模型管理],
)
]

#slide()[

#figure(
  image("./img/agent.png", width: 80%),
  caption: [智能体管理],
)

#figure(
  image("./img/message.png", width: 80%),
  caption: [消息内容],
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