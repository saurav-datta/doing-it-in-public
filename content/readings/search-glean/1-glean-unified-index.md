---
title: glean-unified-index
draft: false
tags:
  - glean
  - search
  - unified-index
description: How does Glean process enterprise data
---

# Need of a unified index when we have  agent/tool driven federated search ?
Yes! Indexed search has multiple advantages:

- **Speed and Performance**<br>
	Indexed search is faster, unlike federated search, which is "only as fast as the slowest system”.  Instead of waiting for individual responses from Google Drive, Jira, and Salesforce simultaneously for a query, a unified index allows for near-instantaneous retrieval of results from all these sources combined<br><br>
- **Comprehensive and Context-Rich Data Access**<br> 
    A federated search is often limited by the access permission of the user and misses broader organizational context. For instance, when searching for information about a project, a unified index can surface not only documents the user created but also related documents popular among colleagues, discussions in Slack channels, and relevant Jira tickets<br><br>
- **Advanced and Consistent Ranking**<br>
    With a centralized index, it's possible to "normalize data across sources" and apply "consistent ranking model" that can "reason across heterogeneous data formats." This moves beyond the "simplistic, rule-based logic" of federated search, which can exclude relevant results from lower-priority sources.<br>For instance, comments in a document might be ranked lower or decay faster over time compared to formal project documentation, and title-less messages in Slack can be intelligently contextualized, leading to more relevant search results<br><br>
- **Disambiguation**<br> (WIP)
