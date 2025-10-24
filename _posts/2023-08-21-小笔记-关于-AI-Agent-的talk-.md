---
layout: post
title: "#小笔记-关于 AI Agent 的talk ..."
author: "Lucca"
comments: false
tags: Life
excerpt_separator: <!--more-->
sticky: false
hidden: false
source: jike
topic: "AI探索站"
date: 2023-08-21 05:15:01 +0800
---

#小笔记-关于 AI Agent 的talk

<!--more-->



之前做了一个AI feature，算是比较高强度地做了一个 AI 产品能力的实验。现在完成度其实我感觉是一般，还是有很多可以优化的点，当然一方面是模型本身的限制（token 的数量和目前的理解能力），另一方面则是本身的产品复杂度很高，导致 prompt 非常复杂。

我做的这个 feature 也是建立在 Agent 的整体架构上，因此实际上来说那个feature 是整体 Agent 的架构中一个 specific 的 tool。

我其实一直还蛮好奇，海外对 Agent 模式应用的进展——毕竟感觉让 chatGPT 能精准地调用 tool，并且做 multitask 的调用，听起来就是难度很大，实际看起来应用上的效果也一般。

周末的时候，我听了 OnBoard! 播客的新一期节目《对话Deepmind, 英伟达大语言模型专家：AI Agent 智能体与开源应用 LLM 的应用、挑战与未来》。

这期节目的嘉宾，一位是 Nvidia 资深研究员 Jim Fan，另一位是 Google Deepmind 的自身研究院戴俊，两位都曾经在 OpenAI 工作过，是大语言模型的深度参与者，也都是比较一线的在干事的人。感觉是整体对于 Agent 未来的应用非常确信，但是也对于其目前的能力限制做了很多说明。非常推荐。

总结和摘录一些比较有启发的 points： 

1. 目前而言从落地的角度讲，agent 模式落地还是比较远。虽然今年 3 月份，autoGPT 突然很火，但是如果真的去用这个模式做一些 serious 的东西，其实还没有人真的做出来什么。

很多人都在询问到底什么是 agent 的 actual use case。因为现在很多所谓的企业常见的 agent，似乎就是一个更聪明的 RPA。

其中的难点可能包括：

 - 时间问题。
autoGPT 能让模型自己去调用预设的 tool，而完成一个事情通常多个步骤，需要较长的时间，这个 latency 是一个非常大的问题。
 
- 中间步骤的 Evaluation。
如果让 agent 去做一个订机票这件事，最后有没有订到正确的机票是容易 verify 的事情。但是中间的订机票的过程其实需要分解为好几个步骤，而大模型常常会产生幻觉，如何去给到模型不同的 action 之后的不同的 evaluation 是很重要。这样才会增加 agent 最终成功完成任务的概率。

- 基础模型的限制。
现在给 GPT4一个API，然后让它要完全按照这个 API 来，它有些时候还是会有hallucination，然后它可能 API 用的并不是特别对。

但这一块如果 GPT 5 和 6 能够很精准地用 API 的话，那其实很多这里面的问题就能解决。比如说如果我们要一个 AI 来控制Browser，然后来订个机票或者什么的，这块万一输错了一个信用卡什么，这问题就特别的大。这块 GPT4 可能还没有那么可靠，所以可能 5 和 6 会解决很多这样的问题。

可能 GPT4 仍然是一个类似于 iphone1、2、3 的 very early version that no one even talked about it。可能最终的 milestone 还会是 GPT5、6。

2. 在企业的机器人或者无人驾驶的领域，安全性和可靠性都非常重要。目前的 AI 可能只有 80% 的到位，但在这种容错率低的场景下，不是 90%甚至 95%到位的情况下，都是很难落地的。

3. 生成式的 AI，最近几年或者最近一两年最做的最好的还是像 Jasper 那个 midjourney 这样的，就是说做出来的东西 creativity 更重要，至于说是差一点或者差10%，这不是很重要。

像 Character.AI 这种，比如说他作为情感陪伴或者是作为模拟一个动画人物，或者是模拟一个 celebrity 跟你对话其实中间说错话或者是乱说什么，其实你也不会太care。

不过  Character.AI 和 midjourney 是 creative，但并不是agent，因为他们没有在做决策。因此，目前而言，容易落地的智能体应用技术在游戏里面，容错率高一些，因为游戏里面说错话，大家会觉得还蛮有娱乐性。

4. 但这并不代表这个 direction 是错的，任何一件事情都需要一些时间去 mature。非常相信这个 agent 的这个direction。以后要做一件事情，可以用大语言模型把一些事情给分解成为小的步骤，然后直接去调一些API，然后直接去把一些事情做成，这是能做的，而且应该做的，但今天还做不到。

今天比如说如果说要落地去做一个客服，你去看客服的东西，很多时候他的问题不只是说是，回答一个问题很多时候是需要去改变，比如说去 update 一些record，今天要用 agent 去做一些 change record。这些东西肯定是不成熟的。但两年、三年、四年以后的那个客服，完全是可以去用 agent 去做。今天还很远，但是这个很远不代表时间很远，而是说这个落地还有很多的落差。

5. 大公司控制生态系统和API的优势。因为他们可以了解自己所有产品的代码和 API，他们可以定制专属于自己产品的语言模型，实现更高的自动化水平。

6. 一个 future scenario prediction：以后的 iphone 手机上 siri 或许可以调用一切 app，完成所有任务，而不需要人对于应用的交互。
