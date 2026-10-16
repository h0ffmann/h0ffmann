## Perfil

Engenheiro de software e de machine learning, trabalhando com sistemas de previsão desde 2017:
churn numa empresa de pagamentos, perdas numa plataforma antifraude de e-commerce e audiência numa
emissora de TV, sempre com as plataformas de dados e de MLOps que mantêm esses sistemas em
produção. Desde 2026, esse trabalho se volta para a previsão do mar: o porte bit a bit do modelo de
ondas WAVEWATCH III para GPU, uma plataforma aberta que transforma dados públicos de mar, tempo e
balneabilidade num sinal diário para três cidades do litoral brasileiro, e a proposta de um
benchmark nacional que compara previsões de ondas com medições de instrumentos. A ligação com a
oceanografia vem de antes, de dois anos de iniciação científica no Laboratório de Instrumentação
Oceanográfica da COPPE/UFRJ. Cada trabalho abaixo tem DOI, repositório público e ambiente de
compilação fixado e reprodutível.

## Pesquisa

**ww3-gpu** · Hoffmann, M. (2026). *WW3 GPU Lab: agentic coding and agentic research on a bit-for-bit
GPU port of WAVEWATCH III.* Software, v0.1.3.
DOI [10.5281/zenodo.23221351](https://doi.org/10.5281/zenodo.23221351)
<a href="https://github.com/h0ffmann/ww3-gpu"><img src="https://img.shields.io/badge/GitHub-h0ffmann%2Fww3--gpu-181717?style=flat-square" alt="GitHub: h0ffmann/ww3-gpu" /></a>

- 541 commits no `main` até [`f83aa0c`](https://github.com/h0ffmann/ww3-gpu/commit/f83aa0c)
  (16/10/2026). Projeto final de graduação na Escola Politécnica da UFRJ, com coorientação no
  LabECO/UFSC: porte do WW3 para C++/Kokkos que reproduz o Fortran bit a bit, validado pelos
  regtests do próprio WW3. Traduzidas: 293 de 1 023 rotinas (53 004 de 263 375 linhas de Fortran,
  20,1 %). Chamadas pelo WW3: 10 rotinas (1,0 %), como prova de conceito. Porte concluído, com
  regtest: 2 rotinas (W3SNL1 e INSNL1, 0,2 %), que respondem por 48,4 % do tempo de execução.

**marola** · Hoffmann, M., Valério, B., Soares da Silva Junior, R. K., Oliveira, E., Almeida, L. R. e
Ribeiro, P. (2026). *marola: an open, non-profit platform for sea conditions and bathing-water quality
at Brazilian beaches, built on public data.* Software, v0.2.2.
DOI [10.5281/zenodo.23224155](https://doi.org/10.5281/zenodo.23224155)
<a href="https://github.com/marola-dev/marola"><img src="https://img.shields.io/badge/GitHub-marola--dev%2Fmarola-181717?style=flat-square" alt="GitHub: marola-dev/marola" /></a>

- Classifica as praias de Florianópolis, Rio de Janeiro e Salvador a partir de previsões de mar,
  vento, ondas e maré e dos boletins oficiais de balneabilidade; regras simples, e não um modelo,
  decidem o que envolve a segurança de quem nada. Seis autores em três países; 545 commits no
  repositório principal até [`09208c7`](https://github.com/marola-dev/marola/commit/09208c7)
  (16/10/2026). Repositórios principais (commits em 14/10/2026): **marola-app**, o produto em
  Scala 3 e Kyo (171); **marola-ml**, o marolaGPT, baseado no modelo brasileiro Tucano2
  (79); **marola-site**, o mapa em marola.dev (106); **marola-devkit**, hooks e plugin do Claude Code (167);
  **marola-corpus** (21); **marola-research**, com o marola-bench (16).

## Experiência

### Engenheiro Sênior de Machine Learning Operations (MLOps), TXP / ITV

*Julho de 2025 – agosto de 2026 · Londres, Reino Unido (remoto)*

- Reestruturação de um pipeline de previsão de audiência de um só canal numa plataforma de ML
  multicanal, com as previsões estendidas para ITV2, ITV3 e ITV Quiz
- Responsável pelo pipeline de ponta a ponta, da ingestão à previsão publicada: AWS Glue,
  Amazon SageMaker e MLflow, orquestrados no Apache Airflow (MWAA), servidos pelo Amazon DynamoDB

### Engenheiro Sênior de ML II (L5), Signifyd (pela aquisição da Legiti, março de 2023)

*Junho de 2022 – novembro de 2024 · San Jose, CA, EUA (remoto)*

- Previsão de perdas: redução de 93 % no tempo de experimentação do modelo (de 16 horas para 1 hora),
  com a refatoração do código de simulação, multithreading e a troca de pandas por PySpark
- Redução de 77 % no tempo e no custo do cálculo de features em lote, do PostgreSQL para PySpark no
  Databricks
- Detecção de anomalias para análise de risco de fraude no Databricks (Unity Catalog, Delta Lake,
  MLflow, PySpark MLlib)

### Engenheiro Líder de MLOps, Elemeno AI

*Junho de 2021 – julho de 2022 · San Francisco, CA, EUA (remoto)*

- Projeto e construção de uma plataforma de MLOps inteiramente de código aberto para as Americanas
  (BVMF: AMER3): Kubeflow (KServe, Katib), MinIO, ArgoCD e GitLab CI no Google Kubernetes Engine,
  provisionados com Terraform e Helm; três repositórios abertos em
  [github.com/elemeno-ai](https://github.com/elemeno-ai)

### Engenheiro de Software Sênior, Broad (Y Combinator, W21)

*Novembro de 2020 – junho de 2021 · Londres, Reino Unido (remoto)*

- Fonte única dos eventos bancários em Scala, ZIO, Event Sourcing e Kafka Streams

### Engenheiro de Software, iU Pay / Guiabolso

*Maio de 2019 – novembro de 2020 · São Paulo, Brasil (remoto)*

- Contribuidor central do primeiro motor brasileiro de transferências instantâneas entre bancos,
  entregue oito meses antes do lançamento do Pix: motor de transações, compensação e modelo de
  dados no Apache Cassandra, com Apache Kafka e Event Sourcing

### Desenvolvedor de Software, Stone (Nasdaq: STNE)

*Outubro de 2017 – abril de 2019 · Rio de Janeiro, Brasil (remoto)*

- Previsão de churn: migração de modelos de redes bayesianas para XGBoost/LightGBM no Apache Spark
- Redução de 35 % no custo logístico da troca de operadora móvel das maquininhas de cartão de crédito, com um
  sistema de recomendação baseado em qualidade de sinal e proximidade geográfica

### Iniciação científica, LIOC – Laboratório de Instrumentação Oceanográfica, COPPE/UFRJ

*Setembro de 2015 – outubro de 2017 · Rio de Janeiro, Brasil*

- Construção de um glider submarino
- Construção e operação de um ROV (veículo submarino operado remotamente)
- Rastreamento por GPS, em tempo real, de barcos em competições: microcontrolador TI MSP430 com
  transmissão pela rede celular GSM (2G), e servidor em Python, PHP e MySQL
- Processamento de sinais em FPGA com LabVIEW (NI cRIO-9068) para um programa de comunicação
  submarina da Marinha do Brasil

## Competências

- **Computação de alto desempenho**: C++/Kokkos, Fortran, OpenMP, MPI, CUDA, perfil com gprof,
  regtests do WW3, Nix
- **MLOps e engenharia de dados**: pipelines de ML de ponta a ponta, MLflow, Kubeflow, Amazon
  SageMaker, Apache Spark, PySpark, Databricks, Delta Lake, Apache Airflow, dbt, SQL
- **Nuvem e infraestrutura**: AWS (S3, EC2, EKS, EMR, Kinesis, Glue, DynamoDB, Redshift), Google
  Cloud (GKE), Kubernetes, Docker, Terraform, Helm, ArgoCD, CI/CD (GitHub Actions, GitLab CI)
- **Backend e IA**: Scala, Python, TypeScript, Apache Kafka, PostgreSQL, Apache Cassandra, RAG,
  MCP, DSPy, fine-tuning (QLoRA, DPO), Claude Code
- **Instrumentação**: microcontroladores (TI MSP430), FPGA (NI cRIO-9068, LabVIEW), GPS, GSM

## Formação

### Bacharelado em Engenharia Eletrônica e de Computação, Universidade Federal do Rio de Janeiro (UFRJ)

*2013 – atual · Rio de Janeiro, Brasil*

Temas principais: engenharia de software, big data e HPC.

### Técnico em Eletrônica, Centro Federal de Educação Tecnológica CEFET/RJ

*2010 – 2012 · Rio de Janeiro, Brasil*

Eletrônica industrial e instrumentação.

## Idiomas, certificações e prêmios

Português (nativo), inglês (C1, fluente), espanhol (leitura).

<p align="left">
<img src="https://img.shields.io/badge/AWS-Cloud%20Practitioner-FF9900?style=flat-square" alt="AWS Certified Cloud Practitioner" />
<img src="https://img.shields.io/badge/AWS-ML%20Specialty-FF9900?style=flat-square" alt="AWS Certified Machine Learning – Specialty" />
<img src="https://img.shields.io/badge/AWS-ML%20Engineer%20Associate-FF9900?style=flat-square" alt="AWS Certified Machine Learning Engineer – Associate" />
<img src="https://img.shields.io/badge/AWS-Data%20Engineer%20Associate-FF9900?style=flat-square" alt="AWS Certified Data Engineer – Associate" />
<img src="https://img.shields.io/badge/PADI-Rescue%20Diver-0B5FA5?style=flat-square" alt="PADI Rescue Diver" />
</p>

Oceanman Rio de Janeiro: 3º lugar na faixa de 30 a 39 anos, 10 km em águas abertas (setembro de
2025). Prêmio "Values VIP: Tenacious" da Signifyd por excelência técnica, por votação dos
funcionários (fevereiro de 2024).

```{=latex}
{\small\color{muted}Outras obras com DOI: \emph{marola-bench} (\href{https://doi.org/10.5281/zenodo.23352633}{\mbox{10.5281/zenodo.23352633}}); \emph{picasso} (\href{https://doi.org/10.5281/zenodo.23311208}{\mbox{10.5281/zenodo.23311208}}); \emph{Closed Source: The God that Failed} (\href{https://doi.org/10.5281/zenodo.23333656}{\mbox{10.5281/zenodo.23333656}}); \emph{Nashkell: Rhizomatic experiments} (\href{https://doi.org/10.5281/zenodo.23356739}{\mbox{10.5281/zenodo.23356739}}).\par}
```
