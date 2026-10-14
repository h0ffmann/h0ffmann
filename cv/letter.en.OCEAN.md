```{=latex}
\vspace{10pt}
\noindent Florianópolis, 14 October 2026
\vspace{6pt}
```

Dear Directors and Research Committee,

I am writing to present myself for research and engineering work at an institute devoted to the
ocean, where the observation of the sea, the sharing of ocean data and the forecasting of what the sea
will do next are structuring work, and where the results are meant to reach the people and the public
policies of the coast. My curriculum vitae is attached; this letter says what I would bring.

Since 2017 I have built forecasting systems that run in production every day and the data and MLOps
platforms that keep them running: churn forecasting for a payment company, loss forecasting for an
e-commerce fraud platform, audience forecasting for a broadcaster. More recently I turned that
practice to the sea, in three works that each have a DOI, a public repository and a reproducible
toolchain.

- **Wave modelling on GPUs.** A port of the expensive kernels of the WAVEWATCH III spectral wave model
  to GPUs that does not change the answer: the nonlinear interaction term is bit-identical to the
  Fortran on CPU and CUDA backends, and every benchmark carries the command that reproduces it. This
  is the discipline an operational model needs when it moves to new hardware.
- **An open platform on public data.** marola gathers the sea, wind, wave and tide forecasts and the
  official bathing-water bulletins of three state agencies for the beaches of Florianópolis, Rio de
  Janeiro and Salvador, standardises them, and publishes a daily signal with its sources; plain rules
  decide anything that concerns a swimmer's safety. It is a small, working example of data
  infrastructure that serves the public directly.
- **A benchmark proposal.** marola-bench proposes a public benchmark for forecasts on the Brazilian
  coast in the WeatherBench tradition, with ocean-wave scores and in-situ instruments as the ground
  truth, so that forecasters can be compared at the same observation points over time.

Before industry, I spent two years in an ocean instrumentation laboratory at UFRJ, on signal
processing for a Navy underwater-communication programme and on real-time GPS tracking of boats, so I
know what the data of a sensor looks like before it reaches a model. I am also an open-water swimmer
and a rescue diver: the sea I write software about is one I swim in.

What I would bring to a research group, then, is the engineering between an observation and a
forecast that people can use: numerical modelling on GPUs, operational pipelines with verification
built in, data platforms that gather and standardise observations from many sources, and the habit of
writing the design down, testing it, and publishing the result in the open with a DOI. I would be glad
to discuss where this fits the institute's projects, and I am available for a conversation at your
convenience.

Yours faithfully,

```{=latex}
\vspace{18pt}
\noindent{\bfseries Matheus Hoffmann}\\
{\color{muted}\small mhoffmannfs@gmail.com \textbar\ linkedin.com/in/mhoffmannbr \textbar\ github.com/h0ffmann}

\vspace{10pt}
{\footnotesize\color{muted}\raggedright\hyphenpenalty=10000\exhyphenpenalty=10000\noindent The works, each with a DOI:
marola \href{https://doi.org/10.5281/zenodo.23224155}{10.5281/zenodo.23224155};
ww3-gpu \href{https://doi.org/10.5281/zenodo.23221351}{10.5281/zenodo.23221351};
marola-bench \href{https://doi.org/10.5281/zenodo.23352633}{10.5281/zenodo.23352633};
closed source \href{https://doi.org/10.5281/zenodo.23333656}{10.5281/zenodo.23333656};
picasso \href{https://doi.org/10.5281/zenodo.23311208}{10.5281/zenodo.23311208};
nashkell \href{https://doi.org/10.5281/zenodo.23356739}{10.5281/zenodo.23356739}.\par}
```
