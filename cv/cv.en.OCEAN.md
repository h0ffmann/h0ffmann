## Profile

Engineer who has built forecasting systems that run in production since 2017, and the data and
MLOps platforms that keep them running: loss forecasting for an e-commerce fraud platform, churn
forecasting for a payment company, audience forecasting for a broadcaster. More recently that
practice turned to the sea: a bit-for-bit GPU port of the WAVEWATCH III wave model, an open platform
that turns public sea, weather and bathing-water data into a daily signal for three Brazilian coastal
cities, and a proposal for a national benchmark that scores wave forecasts against instruments.
Before that, two years in an ocean instrumentation laboratory at UFRJ. What I offer an ocean-research
group: numerical wave modelling on GPUs, operational forecasting pipelines with verification built in,
data infrastructure that gathers and standardises observations from many sources, and an open-science
practice: each work below has a DOI, a public repository and a pinned, reproducible toolchain.

## Research

**marola** · Hoffmann, M., Valério, B., Soares da Silva Junior, R. K., Oliveira, E., Almeida, L. R. and
Ribeiro, P. (2026). *marola: an open, non-profit platform for sea conditions and bathing-water quality
at Brazilian beaches, built on public data.* Software, v0.2.2.
DOI [10.5281/zenodo.23224155](https://doi.org/10.5281/zenodo.23224155)
<a href="https://github.com/marola-dev/marola"><img src="https://img.shields.io/badge/GitHub-marola--dev%2Fmarola-181717?style=flat-square" alt="GitHub: marola-dev/marola" /></a>\
Scores the beaches of Florianópolis, Rio de Janeiro and Salvador for today and tomorrow from sea, wind,
wave and tide forecasts and the official bathing-water bulletins of three state agencies; plain rules,
not a model, decide anything that concerns a swimmer's safety. Six authors, in three countries.

**ww3-gpu** · Hoffmann, M. (2026). *WW3 GPU Lab: agentic coding and agentic research on a bit-for-bit
GPU port of WAVEWATCH III.* Software, v0.1.3.
DOI [10.5281/zenodo.23221351](https://doi.org/10.5281/zenodo.23221351)
<a href="https://github.com/h0ffmann/ww3-gpu"><img src="https://img.shields.io/badge/GitHub-h0ffmann%2Fww3--gpu-181717?style=flat-square" alt="GitHub: h0ffmann/ww3-gpu" /></a>\
Moves the expensive kernels of the WAVEWATCH III third-generation spectral wave model to GPUs without
changing the answer: a C++/Kokkos port of the nonlinear four-wave interaction term (W3SNL1, DIA) shown
bit-identical to the Fortran on the Serial, OpenMP and CUDA backends, with CPU (OpenMP, MPI) and GPU
(OpenACC, CUDA Fortran) benchmarks that each carry the command that reproduces them.

**marola-bench** · Hoffmann, M. (2026). *marola-bench: a proposal for a WeatherBench for Brazil.*
Proposal, v0.1.0.
DOI [10.5281/zenodo.23352633](https://doi.org/10.5281/zenodo.23352633)
<a href="https://github.com/marola-dev/marola-research/tree/main/marola-bench"><img src="https://img.shields.io/badge/GitHub-marola--dev%2Fmarola--research-181717?style=flat-square" alt="GitHub: marola-dev/marola-research (marola-bench)" /></a>\
Proposes a public benchmark for forecasts on the Brazilian coast in the WeatherBench tradition: a fixed
region, scores for ocean waves, and in-situ instruments as the ground truth, so that any forecaster can
be scored at the same observation points over time.

```{=latex}
{\small\color{muted}Also research on open-source software: \href{https://github.com/h0ffmann/closed-source}{\emph{Closed Source: The God that Failed}} (DOI \href{https://doi.org/10.5281/zenodo.23333656}{10.5281/zenodo.23333656}) \quad\textbar\quad personal website: \href{https://h0ffmann.github.io/h0ffmann/}{h0ffmann.github.io/h0ffmann}\\
Other works with a DOI: \emph{picasso}, the Nix flakes that pin the toolchains the works above build with (\href{https://doi.org/10.5281/zenodo.23311208}{10.5281/zenodo.23311208}); \emph{Nashkell: Rhizomatic experiments}, an open book (\href{https://doi.org/10.5281/zenodo.23356739}{10.5281/zenodo.23356739}).\par}
```

## Experience

### Senior Machine Learning Operations (MLOps) Engineer, TXP / ITV

*July 2025 – August 2026 · London, UK (remote)*

- Re-architected a single-channel audience-forecasting pipeline into an extensible multi-channel ML
  platform, extending the forecasts to ITV2, ITV3 and ITV Quiz
- Owned the pipeline end to end, from data ingestion to the published forecasts: AWS Glue ETL, Amazon
  SageMaker training and MLflow tracking, orchestrated on Apache Airflow (MWAA), served from Amazon
  DynamoDB

### Senior ML Engineer II (L5), Signifyd (via the Legiti acquisition, March 2023)

*June 2022 – November 2024 · San Jose, CA, USA (remote)*

- Loss forecasting: cut model experimentation time by 93% (16 hours to 1 hour) by refactoring the
  simulation code, adding multithreading and moving the pandas logic to PySpark
- Cut batch feature computation time and cost by 77% by moving it from PostgreSQL to PySpark on
  Databricks
- Built anomaly detection for fraud risk analysis on Databricks (Unity Catalog, Delta Lake, MLflow,
  PySpark MLlib)

### Lead MLOps Engineer, Elemeno AI

*June 2021 – July 2022 · San Francisco, CA, USA (remote)*

- Designed and built a full open-source MLOps stack on Kubeflow (KServe, Katib), MinIO, ArgoCD and
  GitLab CI on Google Kubernetes Engine, provisioned with Terraform and Helm, for Americanas
  (BVMF: AMER3): in effect an open-source distribution of what managed platforms such as the early
  Vertex AI offered
- Gave data scientists a self-service experimentation platform (JupyterHub, Elyra, MLflow); three
  open-source repositories published at [github.com/elemeno-ai](https://github.com/elemeno-ai)

### Senior Software Engineer, Broad (Y Combinator, W21)

*November 2020 – June 2021 · London, UK (remote)*

- Built the single source of truth for banking events in Scala, ZIO, Event Sourcing and Kafka Streams,
  integrating BIN-sponsorship and foreign-exchange providers

### Software Engineer, iU Pay / Guiabolso

*May 2019 – November 2020 · São Paulo, Brazil (remote)*

- Core contributor to Brazil's first instant cross-bank transaction engine, delivered eight months
  before the public launch of Pix: the transaction engine, the clearing process and the Apache
  Cassandra data model
- Processed transactions from Apache Kafka with Event Sourcing and RPA; stayed on through the
  Guiabolso acquisition

### Software Developer, Stone (Nasdaq: STNE)

*October 2017 – April 2019 · Rio de Janeiro, Brazil (remote)*

- Churn forecasting: improved the F1-score and the training speed of the churn-prediction models by
  migrating legacy Bayesian networks to XGBoost/LightGBM on Apache Spark
- Cut the logistics cost of switching mobile carriers on point-of-sale terminals by 35% with a
  recommendation system based on signal quality and geographic proximity

### Student Researcher, LIOC – Ocean Instrumentation Laboratory, COPPE/UFRJ

*September 2015 – October 2017 · Rio de Janeiro, Brazil*

- FPGA signal processing in LabVIEW (NI cRIO-9068) for a Brazilian Navy underwater-communication
  programme, and real-time GPS tracking of boats in competitions on the TI MSP430 with Python, PHP
  and MySQL

## Skills

- **Machine Learning Operations (MLOps)**: end-to-end ML pipelines, model training and deployment,
  experiment tracking (MLflow), Kubeflow, Amazon SageMaker, feature engineering
- **Data Engineering**: Apache Spark, PySpark, Databricks, Delta Lake, Apache Airflow, dbt, ETL/ELT, SQL
- **Cloud & Infrastructure**: Amazon Web Services (AWS: S3, EC2, EKS, EMR, Kinesis, Glue, DynamoDB,
  Redshift), Google Cloud (GKE), Kubernetes, Docker, Terraform, Helm, ArgoCD, CI/CD (GitHub Actions,
  GitLab CI, Jenkins)
- **Backend & Distributed Systems**: Scala, Python, TypeScript, FastAPI, REST APIs, Apache Kafka,
  Event Sourcing, Akka, ZIO, PostgreSQL, Apache Cassandra
- **LLM & AI Engineering**: RAG, Model Context Protocol (MCP), DSPy, fine-tuning (QLoRA, DPO),
  Claude Code

## Education

### Bachelor's in Electronics and Computer Engineering, Federal University of Rio de Janeiro (UFRJ)

*2013 – present · Rio de Janeiro, Brazil*

Final project in progress on the GPU optimisation of the WAVEWATCH III ocean wave model with
LabECO/UFSC ([github.com/h0ffmann/ww3-gpu](https://github.com/h0ffmann/ww3-gpu)). Key topics:
software engineering, big data and HPC.

### Technician in Electronics, Federal Center of Technological Education CEFET/RJ

*2010 – 2012 · Rio de Janeiro, Brazil*

Industrial electronics and instrumentation.

## Languages, certifications and honours

English (C1, fluent), Portuguese (native), Spanish (reading).

<p align="left">
<img src="https://img.shields.io/badge/AWS-Cloud%20Practitioner-FF9900?style=flat-square" alt="AWS Certified Cloud Practitioner" />
<img src="https://img.shields.io/badge/AWS-ML%20Specialty-FF9900?style=flat-square" alt="AWS Certified Machine Learning – Specialty" />
<img src="https://img.shields.io/badge/AWS-ML%20Engineer%20Associate-FF9900?style=flat-square" alt="AWS Certified Machine Learning Engineer – Associate" />
<img src="https://img.shields.io/badge/AWS-Data%20Engineer%20Associate-FF9900?style=flat-square" alt="AWS Certified Data Engineer – Associate" />
<img src="https://img.shields.io/badge/PADI-Rescue%20Diver-0B5FA5?style=flat-square" alt="PADI Rescue Diver" />
</p>

Oceanman Rio de Janeiro, 3rd place in the 30–39 age group, 10 km open-water swim (September 2025).
Signifyd "Values VIP: Tenacious" award for technical excellence, voted by employees (February 2024).

References available on request.
