<!-- cv:skip -->
<p align="right"><a href="pdf/cv.pdf">📄 cv (en)</a> · <a href="pdf/cv.pt-BR.pdf">📄 cv (pt-BR)</a> · <a href="pdf/cv.ja.pdf">📄 cv (ja)</a> · <a href="README.pt-BR.md">🇧🇷 português</a> · <a href="README.ja.md">🇯🇵 日本語</a></p>
<!-- cv:end -->

## 👋 me

sr. software engineer with **8 years** of experience building scalable (and occasionally clever) solutions mainly for payment processing & fraud-fighting, now building open-source ocean tech at **[marola-dev](https://github.com/marola-dev)**
<!-- cv:skip -->
<p align="left">
<a href="https://www.linkedin.com/in/mhoffmannbr/" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
</p>
<!-- cv:end -->

## 🌊 open source — [marola-dev](https://github.com/marola-dev)

<a href="https://marola.dev" target="_blank"><img src="marola-qr.svg" alt="QR code for marola.dev" title="scan for marola.dev" align="right" width="120" /></a>

i'm actively building **[marola](https://github.com/marola-dev/marola)** in the open: a citizen-science **ocean intelligence layer**
for the brazilian coast. it answers *"can i swim tomorrow, and when?"* for every beach around florianópolis, rio de janeiro and salvador:
the best hour from swell, wind, tide, uv and the official bathing-water bulletins, with the *why* in plain language, live at **[marola.dev](https://marola.dev)**.

- **water quality first** - every official sampling point (ima/sc, inea, inema) is on the map, coloured by its last bulletin; unfit water zeroes the score in deterministic scala 3 ([kyo](https://getkyo.io)) code, and the llm explains but never overrules
- **the sea in front of you** - tide, swell, wind, uv, jellyfish and whale odds per beach, a sourced *did you know?* about the local sea, and *ask the ocean*: rag with citations on ollama, an mcp tool server and its own small model, [marola-sea](https://huggingface.co/h0ffmann/marola-sea-tiny-GGUF), no account or api key
- **designed in public** - every non-trivial change starts as a public design doc ([MIPs](https://github.com/marola-dev/marola/tree/main/docs/MIPs)); next up: wind, wave, satellite and sea-heat map layers, *ressaca* (storm surf) warnings, wave-model ensembles with WAVEWATCH III and an open data lake of beaches and water quality

<p align="left">
<a href="https://marola.dev" target="_blank"><img src="https://img.shields.io/badge/%F0%9F%8C%8A_marola.dev-0077BE?style=for-the-badge" alt="marola.dev" /></a>
<a href="https://github.com/marola-dev" target="_blank"><img src="https://img.shields.io/badge/FOSS-marola--dev-2EA043?style=for-the-badge&logo=github&logoColor=white" alt="github: marola-dev" /></a>
<a href="https://docs.marola.dev" target="_blank"><img src="https://img.shields.io/badge/docs-docs.marola.dev-0077BE?style=for-the-badge&logo=materialformkdocs&logoColor=white" alt="docs.marola.dev" /></a>
<a href="https://github.com/marola-dev/marola/blob/main/LICENSE" target="_blank"><img src="https://img.shields.io/badge/license-MIT-2EA043?style=for-the-badge" alt="MIT license" /></a>
</p>
<!-- cv:skip -->
<p align="left">
<a href="https://github.com/marola-dev/marola/commits/main"><img src="https://img.shields.io/github/last-commit/marola-dev/marola?style=flat-square&logo=github&label=last%20commit" alt="last commit to marola-dev/marola" /></a>
<a href="https://github.com/marola-dev/marola/graphs/commit-activity"><img src="https://img.shields.io/github/commit-activity/m/marola-dev/marola?style=flat-square&logo=github&label=commits" alt="monthly commits to marola-dev/marola" /></a>
<a href="https://github.com/marola-dev/marola/actions/workflows/ci.yml"><img src="https://github.com/marola-dev/marola/actions/workflows/ci.yml/badge.svg" alt="marola CI" /></a>
<a href="https://github.com/marola-dev/marola-site/actions/workflows/site.yml"><img src="https://github.com/marola-dev/marola-site/actions/workflows/site.yml/badge.svg" alt="marola.dev build + deploy" /></a>
</p>
<!-- cv:end -->

<!-- cv:skip -->
| repo | what |
| --- | --- |
| [marola](https://github.com/marola-dev/marola) | the umbrella: design docs, roadmap and [docs.marola.dev](https://docs.marola.dev), every repo below as a submodule |
| [marola-app](https://github.com/marola-dev/marola-app) | the product: scala 3 + kyo pipeline, score and safety veto, cli, mcp tool server |
| [marola-site](https://github.com/marola-dev/marola-site) | the map at [marola.dev](https://marola.dev), rebuilt every 3 hours |
| [marola-corpus](https://github.com/marola-dev/marola-corpus) | the sourced ocean knowledge every answer cites |
| [marola-ml](https://github.com/marola-dev/marola-ml) | offline python: dspy prompt compile, benchmark gate, the marola-sea model |
| [marola-oods](https://github.com/marola-dev/marola-oods) | open ocean data store: an open data lake of beaches and bathing-water samples (in progress) |
| [marola-devkit](https://github.com/marola-dev/marola-devkit) | shared dev harness: nix tools, hooks, claude code skills, ci workflows |
| [awesome-ocean-science](https://github.com/marola-dev/awesome-ocean-science) | curated list of open ocean models, data, tools and institutes |
| [open-sustainable-technology](https://github.com/marola-dev/open-sustainable-technology) | fork of the community list of open sustainability projects |
| [awesome-open-climate-science](https://github.com/marola-dev/awesome-open-climate-science) | fork of the community list of open climate science |
<!-- cv:end -->

<p align="left">
<a href="https://github.com/topics/civic-tech"><img src="https://img.shields.io/badge/civic--tech-0077BE?style=flat-square" alt="civic-tech" /></a>
<a href="https://github.com/topics/disaster-risk-management"><img src="https://img.shields.io/badge/disaster--risk--management-0077BE?style=flat-square" alt="disaster-risk-management" /></a>
<a href="https://github.com/topics/forecasting"><img src="https://img.shields.io/badge/forecasting-0077BE?style=flat-square" alt="forecasting" /></a>
<a href="https://github.com/topics/meteorology"><img src="https://img.shields.io/badge/meteorology-0077BE?style=flat-square" alt="meteorology" /></a>
<a href="https://github.com/topics/non-profit"><img src="https://img.shields.io/badge/non--profit-0077BE?style=flat-square" alt="non-profit" /></a>
<a href="https://github.com/topics/oceanography"><img src="https://img.shields.io/badge/oceanography-0077BE?style=flat-square" alt="oceanography" /></a>
<a href="https://github.com/topics/water-quality"><img src="https://img.shields.io/badge/water--quality-0077BE?style=flat-square" alt="water-quality" /></a>
</p>

> 🔓 contributors welcome, humans and ai agents alike — no code needed: use the map and tell us where it's wrong, share local sea knowledge, or open an issue or a PR at **[marola-dev/marola](https://github.com/marola-dev/marola)**. or mail me: **mhoffmannfs[at]gmail.com**

## 💼 exp-highlights

- **[itv](https://www.itvplc.com) (uk)** - ml/mlops on aws for channel audience forecasting (2025/aug 2026)
- **[signifyd](https://www.signifyd.com) (us - award winner tenacious feb/2024)** - ml eng. for loss forecasting & risk-analysis on databricks (2023/2024)
- **[elemeno AI](https://github.com/elemeno-ai) (us - br client bvmf: AMER3)** - mlops engineer with k8s on gcp (2021/2022)
- **[broad](https://broad.app) (uk - [YC W21](https://www.ycombinator.com/companies/broad))** - sr. software engineer with scala for digital banking on gcp (2020)
- **[stone](https://www.stone.com.br) (br: nasdaq: STNE)** - ml & software engineer with scala on aws (2017-2019)
- **[LIOC](http://www.lioc.oceanica.ufrj.br) (br: UFRJ/COPPE)** - ocean instrumentation lab - scientific research, ROV, microcontrollers (2016/2017)

<!-- cv:skip -->
## 🧰 stack
<!-- cv:end -->

### 🫀 core
<p align="left">
<img src="https://img.shields.io/badge/Scala-DC322F?style=flat-square&logo=scala&logoColor=white" alt="Scala" />
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Machine_Learning-5C2D91?style=flat-square" alt="Machine Learning" />
<img src="https://img.shields.io/badge/Claude_Code-D97757?style=flat-square&logo=claude&logoColor=white" alt="Claude Code" />
<img src="https://img.shields.io/badge/Nix-5277C3?style=flat-square&logo=nixos&logoColor=white" alt="Nix" />
<img src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=mysql&logoColor=white" alt="SQL" />
<img src="https://img.shields.io/badge/Apache_Airflow-017CEE?style=flat-square&logo=apacheairflow&logoColor=white" alt="Apache Airflow" />

</p>

### ⚡ high-end
<p align="left">
<img src="https://img.shields.io/badge/Apache_Kafka-231F20?style=flat-square&logo=apache-kafka&logoColor=white" alt="Apache Kafka" />
<img src="https://img.shields.io/badge/Apache_Spark-FFFFFF?style=flat-square&logo=apachespark&logoColor=E35A16" alt="Apache Spark" />
<img src="https://img.shields.io/badge/PySpark-E25A1C?style=flat-square&logo=apachespark&logoColor=white" alt="PySpark" /> 
<img src="https://img.shields.io/badge/Delta_Lake-00ADD8?style=flat-square&logo=databricks&logoColor=white" alt="Delta Lake" />
<img src="https://img.shields.io/badge/Databricks-FF3621?style=flat-square&logo=databricks&logoColor=white" alt="Databricks" />
<img src="https://img.shields.io/badge/Akka_%2F_Pekko-15A9CE?style=flat-square" alt="Akka / Apache Pekko" />
<img src="https://img.shields.io/badge/CUDA-76B900?style=flat-square&logo=nvidia&logoColor=white" alt="CUDA" />
</p>

### 🤖 machine learning
<p align="left">
<img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" alt="scikit-learn" />
<img src="https://img.shields.io/badge/MLflow-0194E2?style=flat-square&logo=mlflow&logoColor=white" alt="MLflow" />
<img src="https://img.shields.io/badge/Kubeflow-326CE5?style=flat-square" alt="Kubeflow" />
<img src="https://img.shields.io/badge/Amazon_SageMaker-FF9900?style=flat-square&logo=amazonsagemaker&logoColor=white" alt="Amazon SageMaker" />
<img src="https://img.shields.io/badge/XGBoost-006ACC?style=flat-square&logo=xgboost&logoColor=white" alt="XGBoost" /> 
<img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" alt="PyTorch" />
<img src="https://img.shields.io/badge/Optuna-2FA7BB?style=flat-square&logo=optuna&logoColor=white" alt="Optuna" />
</p>

### 🧠 llm & agents
<p align="left">
<img src="https://img.shields.io/badge/MCP-000000?style=flat-square&logo=modelcontextprotocol&logoColor=white" alt="Model Context Protocol" />
<img src="https://img.shields.io/badge/A2A-4285F4?style=flat-square" alt="Agent2Agent protocol (A2A)" />
<img src="https://img.shields.io/badge/DSPy-B5121B?style=flat-square" alt="DSPy" />
<img src="https://img.shields.io/badge/RAG-6E40C9?style=flat-square" alt="RAG (retrieval-augmented generation)" />
<img src="https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama&logoColor=white" alt="Ollama" />
<img src="https://img.shields.io/badge/OpenCode-000000?style=flat-square" alt="OpenCode" />
<img src="https://img.shields.io/badge/Hugging_Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black" alt="Hugging Face" />
<img src="https://img.shields.io/badge/LoRA_%2F_DPO_fine--tuning-8E44AD?style=flat-square" alt="LoRA / DPO fine-tuning (PEFT, GGUF export)" />
<img src="https://img.shields.io/badge/Langfuse-000000?style=flat-square" alt="Langfuse" />
</p>

### ☁️ cloud & infra & etc
<p align="left">
<img src="https://img.shields.io/badge/AWS-FF9900?style=flat-square&logo=amazon-web-services&logoColor=white" alt="AWS" />
<img src="https://img.shields.io/badge/Amazon_S3-569A31?style=flat-square&logo=amazon-s3&logoColor=white" alt="Amazon S3" />
<img src="https://img.shields.io/badge/Amazon_EC2-FF9900?style=flat-square&logo=amazon-ec2&logoColor=white" alt="Amazon EC2" />
<img src="https://img.shields.io/badge/Amazon_EKS-FF9900?style=flat-square&logo=amazon-eks&logoColor=white" alt="Amazon EKS" />
<img src="https://img.shields.io/badge/Amazon_EMR-FF9900?style=flat-square&logo=amazon-aws&logoColor=white" alt="Amazon EMR" />
<img src="https://img.shields.io/badge/Amazon_Kinesis-FF9900?style=flat-square&logo=amazon-kinesis&logoColor=white" alt="Amazon Kinesis" />
<img src="https://img.shields.io/badge/Amazon_Redshift-FF9900?style=flat-square&logo=amazon-redshift&logoColor=white" alt="Amazon Redshift" />
<img src="https://img.shields.io/badge/Amazon_DynamoDB-4053D6?style=flat-square&logo=amazondynamodb&logoColor=white" alt="Amazon DynamoDB" />
<img src="https://img.shields.io/badge/AWS_Glue-FF9900?style=flat-square&logo=amazon-aws&logoColor=white" alt="AWS Glue" />
<img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white" alt="Kubernetes" />
<img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" />
<img src="https://img.shields.io/badge/OpenTelemetry-000000?style=flat-square&logo=opentelemetry&logoColor=white" alt="OpenTelemetry" />
<img src="https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white" alt="Prometheus" />
<img src="https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white" alt="Grafana" />
<img src="https://img.shields.io/badge/dbt-FF694B?style=flat-square&logo=dbt&logoColor=white" alt="dbt" />
</p>

<!-- cv:skip -->
## 📊 stats

<!-- generated daily by .github/workflows/metrics.yml (lowlighter/metrics) -->

<p align="left">
  <img src="metrics.base.svg" alt="all-time contributions" />
</p>
<p align="left">
  <img src="metrics.languages.svg" alt="most used languages" />
</p>
<!-- cv:end -->

## 🏅 certs

<p align="left">
<img src="https://img.shields.io/badge/AWS-Cloud%20Practitioner-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS Cloud Practitioner" height="24" />
<img src="https://img.shields.io/badge/AWS-ML%20Specialty-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS ML Specialty" height="24" />
<img src="https://img.shields.io/badge/AWS-ML%20Engineer%20Associate-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS ML Engineer Associate" height="24" />
<img src="https://img.shields.io/badge/AWS-Data%20Engineer%20Associate-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS Data Engineer Associate" height="24" />
</p>

## 📚 learning

<a href="https://github.com/h0ffmann/gcp-agentic-architect" target="_blank"><img src="https://img.shields.io/badge/GCP-Professional_Agentic_Architect_(studying)-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white" alt="studying for Google Cloud Professional Agentic Architect" /></a>

## 🏊 misc
<a href="https://strava.com/athletes/144282698" target="_blank"><img src="https://img.shields.io/badge/Strava-open_water_swimming-FC4C02?style=for-the-badge&logo=strava&logoColor=white" alt="strava (open water swimming)" /></a>
<p align="left">
<img src="https://img.shields.io/badge/PADI-Advanced_Open_Water_Diver-0B5FA5?style=for-the-badge" alt="PADI Advanced Open Water Diver" />
<img src="https://img.shields.io/badge/PADI-Enriched_Air_Nitrox_Diver-0B5FA5?style=for-the-badge" alt="PADI Enriched Air (Nitrox) Diver" />
<img src="https://img.shields.io/badge/PADI-Rescue_Diver-0B5FA5?style=for-the-badge" alt="PADI Rescue Diver" />
</p>

<!-- cv:skip -->
<p align="center">
  <img src="https://github.com/user-attachments/assets/c466f2e5-3ace-41ee-8171-f825f00d6939" width="600">
</p>
<!-- cv:end -->

