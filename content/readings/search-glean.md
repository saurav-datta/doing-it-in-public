---
title: search-glean
draft: false
tags:
  - glean
  - search
description: How does Glean process enterprise data
---

**Do we still need a index when we have  federated search using LLM agents?**
Yes! Indexed search has multiple advantages:

- **Speed and Performance**
	Indexed search is faster, unlike federated search, which is "only as fast as the slowest system," a centralized index avoids waiting for multiple API calls. Instead of waiting for individual responses from Google Drive, Jira, and Salesforce simultaneously for a query, a unified index allows for near-instantaneous retrieval of results from all these sources combined

- **Comprehensive and Context-Rich Data Access** 
    A federated search is often limited by the access permission of the user and misses broader organizational context. For instance, when searching for information about a project, a unified index can surface not only documents the user created but also related documents popular among colleagues, discussions in Slack channels, and relevant Jira tickets, providing a complete picture that federated search might miss due to siloed data access

- **Enhanced Relevance and Ranking:** With a centralized index, it's possible to "normalize data across sources" and apply "consistent ranking model[s]" that can "reason across heterogeneous data formats." This moves beyond the "simplistic, rule-based logic" of federated search, which can exclude relevant results from lower-priority sources.
- **Foundation for AI and Knowledge Graphs:** A unified index is described as "the foundation for the next-generation AI data platform" and "makes all your data searchable—providing the foundation for the next-generation AI data platform." It is explicitly stated that "indexing helps AI understand content; knowledge graphs help it understand relationships."

"*Many enterprises are now asking: have LLMs found a shortcut to grounding agents in enterprise context, fundamentally changing the need for an index?*" [1](https://www.glean.com/blog/federated-indexed-enterprise-ai)
- Federated search is prone to latencies. Imagine searching across Google Drive, Box, each with its own latency.
	- Each source executes the query independently and returns separate results
	- Leads to a sub-optimal experience in an enterprise application
- "*You can't get to that seamless experience without a centralized index across all horizontal enterprise data. Forgetting that index means recreating for AI the same data siloes that occurred in SaaS*"
-

# Reference

<div style="font-size:0.85em;">
  <ol>
    <li><a href="https://www.glean.com/blog/federated-indexed-enterprise-ai">https://www.glean.com/blog/federated-indexed-enterprise-ai</a></li>
    <li><a href="https://www.glean.com/blog/why-a-great-crawler-is-essential-for-building-a-workplace-chatgpt">https://www.glean.com/blog/why-a-great-crawler-is-essential-for-building-a-workplace-chatgpt</a></li>
    <li><a href="https://www.glean.com/product/system-of-context">https://www.glean.com/product/system-of-context</a></li>
    <li><a href="https://www.glean.com/blog/knowledge-graph-agentic-engine">https://www.glean.com/blog/knowledge-graph-agentic-engine</a></li>
  </ol>
</div>
