<!-- cv:skip -->
<p align="right"><a href="pdf/cv.ja.pdf">📄 履歴書 (ja)</a> · <a href="pdf/cv.pdf">📄 cv (en)</a> · <a href="pdf/cv.pt-BR.pdf">📄 cv (pt-BR)</a> · <a href="README.md">🇬🇧 english</a> · <a href="README.pt-BR.md">🇧🇷 português</a></p>
<!-- cv:end -->

## 👋 自己紹介

決済処理と不正対策を中心に、スケーラブルなソリューションを構築してきた**8年**の経験を持つシニアソフトウェアエンジニア兼ジュニア研究者。研究テーマは波浪モデリング、ゲーム理論、自己改善するアプリ。現在は **[marola-dev](https://github.com/marola-dev)** と **ouroboric-dev** で執筆と研究を行っており、商用のご依頼も歓迎します。非公開のセカンドブレイン `h0ffmann/nagori`（近日 FOSS 化）に頻繁に書いています。将来は登壇者としても活動予定です。
<!-- cv:skip -->
<p align="left">
<a href="https://www.linkedin.com/in/mhoffmannbr/" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
<a href="me/ways-of-working.md"><img src="https://img.shields.io/badge/%E5%83%8D%E3%81%8D%E6%96%B9-555555?style=for-the-badge" alt="働き方" /></a>
<a href="https://h0ffmann.github.io/closed-source/" target="_blank"><img src="https://img.shields.io/badge/%E6%B3%A8%E7%9B%AE-closed%20source%3A%20the%20god%20that%20failed-111111?style=for-the-badge&labelColor=A3201C" alt="注目：closed source: the god that failed のウェブサイト" /></a>
</p>
<!-- cv:end -->

## 🌊 オープンソース — [marola-dev](https://github.com/marola-dev)

<a href="https://marola.dev" target="_blank"><img src="marola-qr.svg" alt="marola.dev の QR コード" title="スキャンして marola.dev を開く" align="right" width="120" /></a>
<!-- cv:skip -->
<a href="https://lnt.org" target="_blank"><img src="https://img.shields.io/badge/Leave_No_Trace-affiliate-4B7F3A?style=for-the-badge" alt="Leave No Trace 加盟" title="Leave No Trace: アウトドア倫理" align="right" /></a>
<!-- cv:end -->

ブラジル沿岸のための市民科学による**海のインテリジェンスレイヤー**、**[marola](https://github.com/marola-dev/marola)** をオープンに開発しています。フロリアノポリス、リオデジャネイロ、サルバドールの各ビーチについて「明日泳げる？何時がいい？」に答え、うねり・風・潮汐・UV・公式の海水浴場水質速報から最適な時間を選び、その*理由*をわかりやすい言葉で説明します。**[marola.dev](https://marola.dev)** で公開中です。

- **水質を最優先に**：公式の採水地点（IMA/SC、INEA、INEMA）をすべて地図に載せ、最新の速報で色分け。不適な水質は Scala 3（[Kyo](https://getkyo.io)）の決定論的なコードでスコアをゼロにし、LLM は説明するだけで判定を覆すことはありません
- **目の前の海**：ビーチごとの潮汐・うねり・風・UV・クラゲとクジラの出現可能性、出典付きの「ご存じですか？」、そして「海に聞く」：Ollama 上の引用付き RAG、MCP ツールサーバー、独自の小型モデル [marola-sea](https://huggingface.co/h0ffmann/marola-sea-tiny-GGUF)。アカウントや API キーは不要
- **公開の場で設計**：重要な変更はすべて公開設計書（[MIP](https://github.com/marola-dev/marola/tree/main/docs/MIPs)）から始まります。次は風・波・衛星・海水温の地図レイヤー、*ressaca*（高波）警報、WAVEWATCH III を含む波浪モデルのアンサンブル、ビーチと水質のオープンなデータレイク
- **ひとつの傘、多数のリポジトリ**：[marola](https://github.com/marola-dev/marola) にはコードがなく、計画、人とコーディングエージェントのための共通ルール、そして他の各リポジトリをサブモジュールとして持つだけです。各リポジトリは単独でビルド・リリースします。marola が使う Claude Code のスキルとエージェントはすべて [marola-skills](https://github.com/marola-dev/marola-skills) と [marola-agents](https://github.com/marola-dev/marola-agents) に一覧があります

<p align="left">
<a href="https://marola.dev" target="_blank"><img src="https://img.shields.io/badge/%F0%9F%8C%8A_marola.dev-0077BE?style=for-the-badge" alt="marola.dev" /></a>
<a href="https://github.com/marola-dev" target="_blank"><img src="https://img.shields.io/badge/FOSS-marola--dev-24292F?style=for-the-badge&logo=github&logoColor=white" alt="github: marola-dev" /></a>
<a href="https://docs.marola.dev" target="_blank"><img src="https://img.shields.io/badge/docs-docs.marola.dev-0077BE?style=for-the-badge&logo=materialformkdocs&logoColor=white" alt="docs.marola.dev" /></a>
<a href="https://github.com/marola-dev/marola/blob/main/LICENSE" target="_blank"><img src="https://img.shields.io/badge/license-MIT-555555?style=for-the-badge" alt="MIT ライセンス" /></a>
<a href="https://doi.org/10.5281/zenodo.23224155" target="_blank"><img src="https://img.shields.io/badge/DOI-10.5281%2Fzenodo.23224155-FAB70C?style=for-the-badge&logo=doi&logoColor=black" alt="marola の DOI" /></a>
</p>
<!-- cv:skip -->
<p align="left">
<a href="https://github.com/marola-dev/marola/commits/main"><img src="https://img.shields.io/github/last-commit/marola-dev/marola?style=flat-square&logo=github&label=%E6%9C%80%E7%B5%82%E3%82%B3%E3%83%9F%E3%83%83%E3%83%88" alt="marola-dev/marola の最終コミット" /></a>
<a href="https://github.com/marola-dev/marola/graphs/commit-activity"><img src="https://img.shields.io/github/commit-activity/m/marola-dev/marola?style=flat-square&logo=github&label=%E3%82%B3%E3%83%9F%E3%83%83%E3%83%88%E6%95%B0" alt="marola-dev/marola の月間コミット数" /></a>
<a href="https://github.com/marola-dev/marola/actions/workflows/ci.yml"><img src="https://github.com/marola-dev/marola/actions/workflows/ci.yml/badge.svg" alt="marola CI" /></a>
<a href="https://github.com/marola-dev/marola-site/actions/workflows/site.yml"><img src="https://github.com/marola-dev/marola-site/actions/workflows/site.yml/badge.svg" alt="marola.dev のビルドとデプロイ" /></a>
</p>
<!-- cv:end -->

<p align="left">
<a href="https://github.com/topics/civic-tech"><img src="https://img.shields.io/badge/civic--tech-6E7781?style=flat-square" alt="civic-tech" /></a>
<a href="https://github.com/topics/disaster-risk-management"><img src="https://img.shields.io/badge/disaster--risk--management-6E7781?style=flat-square" alt="disaster-risk-management" /></a>
<a href="https://github.com/topics/forecasting"><img src="https://img.shields.io/badge/forecasting-6E7781?style=flat-square" alt="forecasting" /></a>
<a href="https://github.com/topics/meteorology"><img src="https://img.shields.io/badge/meteorology-6E7781?style=flat-square" alt="meteorology" /></a>
<a href="https://github.com/topics/non-profit"><img src="https://img.shields.io/badge/non--profit-6E7781?style=flat-square" alt="non-profit" /></a>
<a href="https://github.com/topics/oceanography"><img src="https://img.shields.io/badge/oceanography-6E7781?style=flat-square" alt="oceanography" /></a>
<a href="https://github.com/topics/water-quality"><img src="https://img.shields.io/badge/water--quality-6E7781?style=flat-square" alt="water-quality" /></a>
</p>

> 🔓 人間も AI エージェントも、コントリビューター歓迎 — コードは不要です：地図を使って間違いを教えてください、海の地域知識を共有してください、または **[marola-dev/marola](https://github.com/marola-dev/marola)** で issue や PR を。メールでも：**mhoffmannfs[at]gmail.com**

## ⚡ 研究 — [ww3-gpu](https://github.com/h0ffmann/ww3-gpu)

UFRJ（Escola Politécnica）の卒業プロジェクトで、LabECO/UFSC との共同指導です。**[WW3 GPU Lab](https://github.com/h0ffmann/ww3-gpu)** は、NOAA の波浪モデル **WAVEWATCH III** の計算コストの高いカーネルを*結果を変えずに* GPU へ移すという一つの問題を軸にした、オープンなラボであり、エージェント型コーディングとエージェント型研究についての執筆中の本です。**[picasso](https://github.com/h0ffmann/picasso)**（私の Nix ラボ）で Nix 固定した Fortran/MPI/NetCDF ツールチェーンが WW3 をビルドし、1コマンドで回帰テストを実行します。C++/**Kokkos** に移植した DIA 非線形相互作用カーネル（`W3SNL1`）は Serial・OpenMP・CUDA で Fortran とビット単位で一致し、RTX 4090 では 1,000 海洋点を 0.047 ms で処理します（シリアルでは 24.96 ms）。波スペクトルからコーディングエージェントによるカーネル移植までを扱う17回の講義が本の各章で、マージのたびに PDF と[ウェブサイト](https://h0ffmann.github.io/ww3-gpu/)に組まれます。

<p align="left">
<a href="https://github.com/h0ffmann/ww3-gpu" target="_blank"><img src="https://img.shields.io/badge/research-ww3--gpu-24292F?style=for-the-badge&logo=github&logoColor=white" alt="github: ww3-gpu" /></a>
<a href="https://doi.org/10.5281/zenodo.23221351" target="_blank"><img src="https://img.shields.io/badge/DOI-10.5281%2Fzenodo.23221351-FAB70C?style=for-the-badge&logo=doi&logoColor=black" alt="ww3-gpu の DOI" /></a>
<a href="https://github.com/h0ffmann/picasso" target="_blank"><img src="https://img.shields.io/badge/nix%20labs-picasso-24292F?style=for-the-badge&logo=nixos&logoColor=white" alt="github: picasso" /></a>
<a href="https://doi.org/10.5281/zenodo.23311208" target="_blank"><img src="https://img.shields.io/badge/DOI-10.5281%2Fzenodo.23311208-FAB70C?style=for-the-badge&logo=doi&logoColor=black" alt="picasso の DOI" /></a>
</p>
<!-- cv:skip -->

そして、ライセンスを研究している非営利のエッセイ：**[closed source: the god that failed](https://github.com/h0ffmann/closed-source)**。コーディングエージェントの時代における、リバースエンジニアリングと引用の倫理についてのポジションペーパーです。

<p align="left">
<a href="https://h0ffmann.github.io/closed-source/" target="_blank"><img src="https://img.shields.io/badge/site-h0ffmann.github.io%2Fclosed--source-A3201C?style=for-the-badge" alt="closed-source のウェブサイト" /></a>
<a href="https://github.com/h0ffmann/closed-source" target="_blank"><img src="https://img.shields.io/badge/essay-closed--source-24292F?style=for-the-badge&logo=github&logoColor=white" alt="github: closed-source" /></a>
<a href="https://doi.org/10.5281/zenodo.23333656" target="_blank"><img src="https://img.shields.io/badge/DOI-10.5281%2Fzenodo.23333656-FAB70C?style=for-the-badge&logo=doi&logoColor=black" alt="closed-source の DOI" /></a>
</p>
<p align="left">
<a href="https://github.com/topics/non-profit"><img src="https://img.shields.io/badge/non--profit-6E7781?style=flat-square" alt="non-profit" /></a>
<a href="https://github.com/h0ffmann/closed-source#licence"><img src="https://img.shields.io/badge/studying%20licenses-6E7781?style=flat-square" alt="studying licenses" /></a>
</p>
<!-- cv:end -->

## 💼 職務経歴ハイライト

[LIOC](http://www.lioc.oceanica.ufrj.br) (UFRJ) · [Stone](https://www.stone.com.br) · [Broad](https://www.ycombinator.com/companies/broad) (YC W21) · [Elemeno AI](https://github.com/elemeno-ai) · [Signifyd](https://www.signifyd.com) (US) · TXP (UK, 旧 Vigil)

推薦者はご要望に応じてご紹介します（[働き方](me/ways-of-working.md#references-on-request)）

## 🏅 資格

**AWS 認定 4件**（Cloud Practitioner、Machine Learning Specialty、Machine Learning Engineer Associate、Data Engineer Associate）・**PADI 認定 3件**（Advanced Open Water Diver、Enriched Air Nitrox Diver、Rescue Diver）

## 🏊 その他
<a href="https://strava.com/athletes/144282698" target="_blank"><img src="https://img.shields.io/badge/Strava-オープンウォータースイミング-FC4C02?style=for-the-badge&logo=strava&logoColor=white" alt="strava（オープンウォータースイミング）" /></a>

<!-- cv:skip -->
<div align="center">
<table>
<tr>
<td align="center"><img src="photos/swim-2007.svg" width="400" alt="2007年：ブラジル国旗の前で水泳のメダルを掲げる少年" /><br /><sub>2007</sub></td>
<td align="center"><img src="https://github.com/user-attachments/assets/c466f2e5-3ace-41ee-8171-f825f00d6939" width="400" alt="2025年：オーシャンマン・リオデジャネイロの3つのメダル" /><br /><sub>2025</sub></td>
</tr>
</table>
</div>
<!-- cv:end -->
