## Perfil

Engenheiro de software e de machine learning com sistemas de previsão em produção desde 2017: previsão de perdas numa plataforma de
prevenção a fraude, previsão de churn numa empresa de pagamentos e previsão de audiência numa
emissora de TV. Desde 2026 essa prática se volta para o mar. A pesquisa atual é o porte do modelo
de ondas WAVEWATCH III (WW3) para GPU sem mudar a resposta do modelo, bit a bit, como projeto final
de graduação na Escola Politécnica da UFRJ, com coorientação no LabECO/UFSC. Antes da indústria,
dois anos de iniciação científica no Laboratório de Instrumentação Oceanográfica (LIOC) da
COPPE/UFRJ, com veículos submarinos e rastreamento de embarcações.

## Pesquisa

**ww3-gpu** · Hoffmann, M. (2026). *WW3 GPU Lab: agentic coding and agentic research on a bit-for-bit
GPU port of WAVEWATCH III.* Software, v0.1.3.
DOI [10.5281/zenodo.23221351](https://doi.org/10.5281/zenodo.23221351)
<a href="https://github.com/h0ffmann/ww3-gpu"><img src="https://img.shields.io/badge/GitHub-h0ffmann%2Fww3--gpu-181717?style=flat-square" alt="GitHub: h0ffmann/ww3-gpu" /></a>\
Os números abaixo foram lidos no repositório no commit
[`1cb9f78`](https://github.com/h0ffmann/ww3-gpu/commit/1cb9f78) (16/10/2026).

- **Problema.** Levar para GPU os núcleos mais caros do WW3, modelo espectral de terceira geração,
  sem alterar a física. O ponto de partida é um perfil gprof medido no próprio repositório: no caso
  `bench_small` (grade 120 x 80, 9 520 pontos de mar, 12 h de simulação, WW3 no commit `6d1bcdfe`),
  o termo de interação não linear entre quatro ondas (W3SNL1, aproximação DIA) ocupa 48,4 % do
  tempo próprio, a dissipação W3SDS4 ocupa 23,2 % e a entrada de vento W3SIN4, 12,7 %. A ordem do
  porte segue esse tempo medido.
- **Método.** Tradução literal do Fortran para C++/Kokkos (Serial, OpenMP e CUDA com o mesmo
  código), sem reordenar somas, sem trocar limitadores e com contração desligada
  (`-ffp-contract=off`, `--fmad=false`). O WW3 vem de um fork, `h0ffmann/WW3`, que só acrescenta
  uma interface `bind(C)` e escolhe em tempo de execução entre o Fortran original e o Kokkos
  (`WW_KOKKOS_SNL1`). A validação usa somente os regtests do próprio WW3, comparados com `test.comp`
  e `nccmp-tol` (decisão ADR-0010, commit
  [`a59625a`](https://github.com/h0ffmann/ww3-gpu/commit/a59625a)). A toolchain Fortran, MPI e
  NetCDF é fixada em Nix.
- **Resultado do W3SNL1.** Dentro do executável do WW3, na CPU (OpenMP), o DIA em Kokkos dá os
  mesmos bytes que o Fortran: 0 arquivo diferente no `test.comp` nas 100 entradas da matriz de
  regtests ([`7fd6bb2`](https://github.com/h0ffmann/ww3-gpu/commit/7fd6bb2)) e nas 25 entradas com
  OpenMP de memória compartilhada ([`f32640c`](https://github.com/h0ffmann/ww3-gpu/commit/f32640c));
  diferença relativa máxima de `hs` igual a 0 em 119 652 valores. A última diferença, de cerca de
  1e-7 relativo em `hs`, vinha das tabelas do INSNL1: com `-O3`, o gfortran calcula `x**11` como
  `x5*x6`, e o porte usava a cadeia de `-O0`, que termina em `x3*x8`. A correção está no commit
  [`e305841`](https://github.com/h0ffmann/ww3-gpu/commit/e305841).
- **Estado do porte.** Há tradução para Kokkos de 184 das 1 023 rotinas do WW3, que somam 99,3 %
  do tempo de execução do perfil; o WW3 chama o código Kokkos em 10 rotinas (87,4 % do tempo); e
  duas rotinas (W3SNL1 e INSNL1, 48,4 % do tempo) passaram nos regtests. O W3SRCE, com W3SLN1,
  W3SBT1 e W3SDB1, foi traduzido no commit
  [`a052f82`](https://github.com/h0ffmann/ww3-gpu/commit/a052f82) e ainda espera o seu regtest.
- **Medidas.** O núcleo do DIA isolado, com 1 000 pontos por chamada (i9-14900 e RTX 4090, mediana
  de três execuções), leva 25,88 ms em Serial, 5,95 ms em OpenMP com 32 threads e 0,75 ms em CUDA;
  só o kernel CUDA leva 0,047 ms, e o resto é cópia de memória da fase 1. Dentro do WW3, com uma
  thread, a fase 1 ainda é mais lenta que o Fortran (`bench_small`: 217,9 s contra 152,7 s), porque
  copia o espectro a cada chamada. Nenhum ganho de velocidade é declarado antes da fase 2, com o
  espectro residente na GPU, e nenhuma execução do WW3 na GPU foi feita ainda.
- **Publicação.** Código aberto e livro em 17 lições sobre o porte; v0.1.0 a v0.1.3 no Zenodo.

## Experiência

### Fundador, marola.dev

*Setembro de 2026 – atual · Florianópolis, Brasil*

- Plataforma aberta e sem fins lucrativos que classifica as praias de Florianópolis, Rio de Janeiro
  e Salvador para hoje e amanhã, a partir de previsões de mar, vento, ondas e maré e dos boletins
  oficiais de balneabilidade de três órgãos estaduais; regras simples, e não um modelo, decidem tudo
  o que envolve a segurança de quem nada. Seis autores, em três países

### Engenheiro Sênior de Machine Learning Operations (MLOps), TXP / ITV

*Julho de 2025 – agosto de 2026 · Londres, Reino Unido (remoto)*

- Reestruturei um pipeline de previsão de audiência de um só canal numa plataforma de ML
  multicanal, e estendi as previsões para ITV2, ITV3 e ITV Quiz
- Fui responsável pelo pipeline de ponta a ponta, da ingestão à previsão publicada: AWS Glue,
  Amazon SageMaker e MLflow, orquestrados no Apache Airflow (MWAA), servidos pelo Amazon DynamoDB

### Engenheiro Sênior de ML II (L5), Signifyd (pela aquisição da Legiti, março de 2023)

*Junho de 2022 – novembro de 2024 · San Jose, CA, EUA (remoto)*

- Previsão de perdas: reduzi o tempo de experimentação do modelo em 93 % (de 16 horas para 1 hora),
  com a refatoração do código de simulação, multithreading e a troca de pandas por PySpark
- Reduzi em 77 % o tempo e o custo do cálculo de features em lote, do PostgreSQL para PySpark no
  Databricks
- Detecção de anomalias para análise de risco de fraude no Databricks (Unity Catalog, Delta Lake,
  MLflow, PySpark MLlib)

### Engenheiro Líder de MLOps, Elemeno AI

*Junho de 2021 – julho de 2022 · San Francisco, CA, EUA (remoto)*

- Projetei e construí uma plataforma de MLOps inteiramente de código aberto para as Americanas
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

- Previsão de churn: migrei modelos de redes bayesianas para XGBoost/LightGBM no Apache Spark
- Reduzi em 35 % o custo logístico da troca de operadora móvel das maquininhas de cartão de crédito, com um
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

Projeto final em andamento: otimização do modelo de ondas WAVEWATCH III em GPU, com o LabECO/UFSC
([github.com/h0ffmann/ww3-gpu](https://github.com/h0ffmann/ww3-gpu)). Temas principais: engenharia
de software, big data e HPC.

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
{\small\color{muted}Outras obras com DOI: \emph{marola} (\href{https://doi.org/10.5281/zenodo.23224155}{\mbox{10.5281/zenodo.23224155}}); \emph{marola-bench} (\href{https://doi.org/10.5281/zenodo.23352633}{\mbox{10.5281/zenodo.23352633}}); \emph{picasso} (\href{https://doi.org/10.5281/zenodo.23311208}{\mbox{10.5281/zenodo.23311208}}); \emph{Closed Source: The God that Failed} (\href{https://doi.org/10.5281/zenodo.23333656}{\mbox{10.5281/zenodo.23333656}}); \emph{Nashkell: Rhizomatic experiments} (\href{https://doi.org/10.5281/zenodo.23356739}{\mbox{10.5281/zenodo.23356739}}).\par}
```
