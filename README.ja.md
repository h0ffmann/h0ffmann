<!-- cv:skip -->
<p align="right"><a href="pdf/cv.ja.pdf">📄 履歴書 (ja)</a> · <a href="pdf/cv.pdf">📄 cv (en)</a> · <a href="pdf/cv.pt-BR.pdf">📄 cv (pt-BR)</a> · <a href="README.md">🇬🇧 english</a> · <a href="README.pt-BR.md">🇧🇷 português</a></p>
<!-- cv:end -->

## 👋 自己紹介

決済処理と不正対策を中心に、スケーラブルなソリューションを構築してきた**8年**の経験を持つシニアソフトウェアエンジニア。現在は **[marola-dev](https://github.com/marola-dev)** でオープンソースの海洋テックを開発中
<!-- cv:skip -->
<p align="left">
<a href="https://www.linkedin.com/in/mhoffmannbr/" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
</p>
<!-- cv:end -->

## 🌊 オープンソース — [marola-dev](https://github.com/marola-dev)

<a href="https://marola.dev" target="_blank"><img src="marola-qr.svg" alt="marola.dev の QR コード" title="スキャンして marola.dev を開く" align="right" width="120" /></a>

ブラジル沿岸のための市民科学による**海のインテリジェンスレイヤー**、**[marola](https://github.com/marola-dev/marola)** をオープンに開発しています。フロリアノポリス、リオデジャネイロ、サルバドールの各ビーチについて「明日泳げる？何時がいい？」に答え、うねり・風・潮汐・UV・公式の海水浴場水質速報から最適な時間を選び、その*理由*をわかりやすい言葉で説明します。**[marola.dev](https://marola.dev)** で公開中です。

- **水質を最優先に**：公式の採水地点（IMA/SC、INEA、INEMA）をすべて地図に載せ、最新の速報で色分け。不適な水質は Scala 3（[Kyo](https://getkyo.io)）の決定論的なコードでスコアをゼロにし、LLM は説明するだけで判定を覆すことはありません
- **目の前の海**：ビーチごとの潮汐・うねり・風・UV・クラゲとクジラの出現可能性、出典付きの「ご存じですか？」、そして「海に聞く」：Ollama 上の引用付き RAG、MCP ツールサーバー、独自の小型モデル [marola-sea](https://huggingface.co/h0ffmann/marola-sea-tiny-GGUF)。アカウントや API キーは不要
- **公開の場で設計**：重要な変更はすべて公開設計書（[MIP](https://github.com/marola-dev/marola/tree/main/docs/MIPs)）から始まります。次は風・波・衛星・海水温の地図レイヤー、*ressaca*（高波）警報、WAVEWATCH III を含む波浪モデルのアンサンブル、ビーチと水質のオープンなデータレイク

<p align="left">
<a href="https://marola.dev" target="_blank"><img src="https://img.shields.io/badge/%F0%9F%8C%8A_marola.dev-0077BE?style=for-the-badge" alt="marola.dev" /></a>
<a href="https://github.com/marola-dev" target="_blank"><img src="https://img.shields.io/badge/FOSS-marola--dev-2EA043?style=for-the-badge&logo=github&logoColor=white" alt="github: marola-dev" /></a>
<a href="https://docs.marola.dev" target="_blank"><img src="https://img.shields.io/badge/docs-docs.marola.dev-0077BE?style=for-the-badge&logo=materialformkdocs&logoColor=white" alt="docs.marola.dev" /></a>
<a href="https://github.com/marola-dev/marola/blob/main/LICENSE" target="_blank"><img src="https://img.shields.io/badge/license-MIT-2EA043?style=for-the-badge" alt="MIT ライセンス" /></a>
</p>
<!-- cv:skip -->
<p align="left">
<a href="https://github.com/marola-dev/marola/commits/main"><img src="https://img.shields.io/github/last-commit/marola-dev/marola?style=flat-square&logo=github&label=%E6%9C%80%E7%B5%82%E3%82%B3%E3%83%9F%E3%83%83%E3%83%88" alt="marola-dev/marola の最終コミット" /></a>
<a href="https://github.com/marola-dev/marola/graphs/commit-activity"><img src="https://img.shields.io/github/commit-activity/m/marola-dev/marola?style=flat-square&logo=github&label=%E3%82%B3%E3%83%9F%E3%83%83%E3%83%88%E6%95%B0" alt="marola-dev/marola の月間コミット数" /></a>
<a href="https://github.com/marola-dev/marola/actions/workflows/ci.yml"><img src="https://github.com/marola-dev/marola/actions/workflows/ci.yml/badge.svg" alt="marola CI" /></a>
<a href="https://github.com/marola-dev/marola-site/actions/workflows/site.yml"><img src="https://github.com/marola-dev/marola-site/actions/workflows/site.yml/badge.svg" alt="marola.dev のビルドとデプロイ" /></a>
</p>
<!-- cv:end -->

<!-- cv:skip -->
| リポジトリ | 内容 |
| --- | --- |
| [marola](https://github.com/marola-dev/marola) | 全体の取りまとめ：設計書、ロードマップ、[docs.marola.dev](https://docs.marola.dev)、以下の各リポジトリをサブモジュールとして収録 |
| [marola-app](https://github.com/marola-dev/marola-app) | 本体：Scala 3 + Kyo のパイプライン、スコアと安全拒否権、CLI、MCP ツールサーバー |
| [marola-site](https://github.com/marola-dev/marola-site) | [marola.dev](https://marola.dev) の地図、3時間ごとに再構築 |
| [marola-corpus](https://github.com/marola-dev/marola-corpus) | すべての回答が引用する、出典付きの海洋知識 |
| [marola-ml](https://github.com/marola-dev/marola-ml) | オフラインの Python：DSPy によるプロンプトのコンパイル、ベンチマークゲート、marola-sea モデル |
| [marola-oods](https://github.com/marola-dev/marola-oods) | Open Ocean Data Store：ビーチと海水浴場水質サンプルのオープンなデータレイク（開発中） |
| [marola-devkit](https://github.com/marola-dev/marola-devkit) | 共通の開発基盤：nix ツール、フック、Claude Code スキル、CI ワークフロー |
| [awesome-ocean-science](https://github.com/marola-dev/awesome-ocean-science) | オープンな海洋モデル、データ、ツール、研究機関の厳選リスト |
| [open-sustainable-technology](https://github.com/marola-dev/open-sustainable-technology) | オープンなサステナビリティ技術のコミュニティリストのフォーク |
| [awesome-open-climate-science](https://github.com/marola-dev/awesome-open-climate-science) | オープンな気候科学のコミュニティリストのフォーク |
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

> 🔓 人間も AI エージェントも、コントリビューター歓迎 — コードは不要です：地図を使って間違いを教えてください、海の地域知識を共有してください、または **[marola-dev/marola](https://github.com/marola-dev/marola)** で issue や PR を。メールでも：**mhoffmannfs[at]gmail.com**

## 💼 職務経歴ハイライト

- **[itv](https://www.itvplc.com)（英国）**：AWS 上の ML/MLOps（視聴者数予測）（2025〜2026年）
- **[signifyd](https://www.signifyd.com)（米国・2024年2月 tenacious 賞受賞）**：Databricks 上の損失予測・リスク分析を担当する ML エンジニア（2023〜2024年）
- **[elemeno AI](https://github.com/elemeno-ai)（米国・ブラジル顧客 bvmf: AMER3）**：GCP 上の k8s による MLOps エンジニア（2021〜2022年）
- **[broad](https://broad.app)（英国・[YC W21](https://www.ycombinator.com/companies/broad)）**：GCP 上のデジタルバンキング向け Scala シニアソフトウェアエンジニア（2020年）
- **[stone](https://www.stone.com.br)（ブラジル・nasdaq: STNE）**：AWS 上の Scala による ML・ソフトウェアエンジニア（2017〜2019年）
- **[LIOC](http://www.lioc.oceanica.ufrj.br)（ブラジル・UFRJ/COPPE）**：海洋計測ラボでの学術研究、ROV、マイコン開発（2016〜2017年）

<!-- cv:skip -->
## 🧰 技術スタック
<!-- cv:end -->

### 🫀 コアスキル
<p align="left">
<img src="https://img.shields.io/badge/Scala-DC322F?style=flat-square&logo=scala&logoColor=white" alt="Scala" />
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Machine_Learning-5C2D91?style=flat-square" alt="Machine Learning" />
<img src="https://img.shields.io/badge/Claude_Code-D97757?style=flat-square&logo=claude&logoColor=white" alt="Claude Code" />
<img src="https://img.shields.io/badge/Nix-5277C3?style=flat-square&logo=nixos&logoColor=white" alt="Nix" />
<img src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=mysql&logoColor=white" alt="SQL" />
<img src="https://img.shields.io/badge/Apache_Airflow-017CEE?style=flat-square&logo=apacheairflow&logoColor=white" alt="Apache Airflow" />

</p>

### ⚡ 大規模データ処理
<p align="left">
<img src="https://img.shields.io/badge/Apache_Kafka-231F20?style=flat-square&logo=apache-kafka&logoColor=white" alt="Apache Kafka" />
<img src="https://img.shields.io/badge/Apache_Spark-FFFFFF?style=flat-square&logo=apachespark&logoColor=E35A16" alt="Apache Spark" />
<img src="https://img.shields.io/badge/PySpark-E25A1C?style=flat-square&logo=apachespark&logoColor=white" alt="PySpark" /> 
<img src="https://img.shields.io/badge/Delta_Lake-00ADD8?style=flat-square&logo=databricks&logoColor=white" alt="Delta Lake" />
<img src="https://img.shields.io/badge/Databricks-FF3621?style=flat-square&logo=databricks&logoColor=white" alt="Databricks" />
<img src="https://img.shields.io/badge/Akka_%2F_Pekko-15A9CE?style=flat-square" alt="Akka / Apache Pekko" />
<img src="https://img.shields.io/badge/CUDA-76B900?style=flat-square&logo=nvidia&logoColor=white" alt="CUDA" />
</p>

### 🤖 機械学習
<p align="left">
<img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" alt="scikit-learn" />
<img src="https://img.shields.io/badge/MLflow-0194E2?style=flat-square&logo=mlflow&logoColor=white" alt="MLflow" />
<img src="https://img.shields.io/badge/Kubeflow-326CE5?style=flat-square" alt="Kubeflow" />
<img src="https://img.shields.io/badge/Amazon_SageMaker-FF9900?style=flat-square&logo=amazonsagemaker&logoColor=white" alt="Amazon SageMaker" />
<img src="https://img.shields.io/badge/XGBoost-006ACC?style=flat-square&logo=xgboost&logoColor=white" alt="XGBoost" /> 
<img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" alt="PyTorch" />
<img src="https://img.shields.io/badge/Optuna-2FA7BB?style=flat-square&logo=optuna&logoColor=white" alt="Optuna" />
</p>

### 🧠 LLM & エージェント
<p align="left">
<img src="https://img.shields.io/badge/MCP-000000?style=flat-square&logo=modelcontextprotocol&logoColor=white" alt="Model Context Protocol" />
<img src="https://img.shields.io/badge/A2A-4285F4?style=flat-square" alt="Agent2Agent プロトコル (A2A)" />
<img src="https://img.shields.io/badge/DSPy-B5121B?style=flat-square" alt="DSPy" />
<img src="https://img.shields.io/badge/RAG-6E40C9?style=flat-square" alt="RAG (retrieval-augmented generation)" />
<img src="https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama&logoColor=white" alt="Ollama" />
<img src="https://img.shields.io/badge/OpenCode-000000?style=flat-square" alt="OpenCode" />
<img src="https://img.shields.io/badge/Hugging_Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black" alt="Hugging Face" />
<img src="https://img.shields.io/badge/LoRA_%2F_DPO_fine--tuning-8E44AD?style=flat-square" alt="LoRA / DPO fine-tuning (PEFT, GGUF export)" />
<img src="https://img.shields.io/badge/Langfuse-000000?style=flat-square" alt="Langfuse" />
</p>

### ☁️ クラウド & インフラ
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
## 📊 統計

<!-- .github/workflows/metrics.yml (lowlighter/metrics) が毎日生成 -->

<p align="left">
  <img src="metrics.base.svg" alt="全期間のコントリビューション" />
</p>
<p align="left">
  <img src="metrics.languages.svg" alt="よく使う言語" />
</p>
<!-- cv:end -->

## 🏅 資格

<p align="left">
<img src="https://img.shields.io/badge/AWS-Cloud%20Practitioner-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS Cloud Practitioner" height="24" />
<img src="https://img.shields.io/badge/AWS-ML%20Specialty-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS ML Specialty" height="24" />
<img src="https://img.shields.io/badge/AWS-ML%20Engineer%20Associate-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS ML Engineer Associate" height="24" />
<img src="https://img.shields.io/badge/AWS-Data%20Engineer%20Associate-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS Data Engineer Associate" height="24" />
</p>

## 📚 学習中

<a href="https://github.com/h0ffmann/gcp-agentic-architect" target="_blank"><img src="https://img.shields.io/badge/GCP-Professional_Agentic_Architect_(学習中)-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white" alt="Google Cloud Professional Agentic Architect を学習中" /></a>

## 🏊 その他
<a href="https://strava.com/athletes/144282698" target="_blank"><img src="https://img.shields.io/badge/Strava-オープンウォータースイミング-FC4C02?style=for-the-badge&logo=strava&logoColor=white" alt="strava（オープンウォータースイミング）" /></a>
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
