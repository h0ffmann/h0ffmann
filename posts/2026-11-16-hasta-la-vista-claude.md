---
title: "Hasta la vista, Claude"
date: 2026-11-16
skill: asd-ste100 v0.4.0 (STE-flavored mode)
tags: [open-source, qwen, deepseek, astrbot, brazil]
---

I am ending my Claude subscription. Since 2024, I maintain several open-source projects in good faith. It does not make sense to build my tools using closed, non-open-source models.

I will now test only Chinese models. Qwen and DeepSeek are the best existing contenders. I see many comments about GLM. However, I do not trust Z.ai yet. I also had a poor experience with Kimi one month ago.

I am proudly using Qwen to finish my current projects. I am integrating Brazilian data sources into a cool repository I found recently: [AstrBot](https://github.com/astrbotdevs/astrbot). I am also using the [disaster warning plugin](https://github.com/Pancakes-Labs/astrbot_plugin_disaster_warning).

The main idea is a bot for Brazilian disasters. It will use authoritative sources. These include [CEMADEN](https://www.gov.br/cemaden/pt-br) and regional Civil Defense alerts. Brazil has 27 federative units (26 states and 1 Federal District). Aggregating data from these diverse regions is an interesting challenge.

I will also publish my closed-source work on Leanpub. Links to these projects are in this repository. I will use Chinese models for this process too.

For posting harness tools, I now use DSH, OMP, and Pi. I also added compiled support for code snippets. This ensures published code is not broken. I use a `justfile` and `snippets-check.py` to verify C/C++, Python, Bash, and JS snippets before publishing.

You can see the ASD-STE100 writing rules in action here: [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill). This skill enforces structural and lexical rules for clear documentation.

P.S. The best thing I noticed is that Qwen does not let you type while it is thinking.

peace
