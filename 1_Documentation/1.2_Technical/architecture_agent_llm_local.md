# NoXoZ_job: Architecture Complète pour Agent LLM Local Gratuit

**Auteur**: Bruno Delnoz
**Date**: 2026-02-04
**Version**: 1.0
**Repo GitHub**: [NoXoZ_job](https://github.com/<ton_user>/NoXoZ_job)
**Dossier Local big files**: `/mnt/data1_100g/agent_llm_local/`
**Dossier Local project files**: `/mnt/data1_100g/agent_llm_local/`

---

## Aperçu Général

Ce projet propose une **architecture 100% locale et gratuite** pour un agent LLM capable d’ingérer tes CV, exports de chats (Le Chat, ChatGPT, Grok, Claude), et générer des documents personnalisés (lettres de motivation, CV, mails de réponse aux offres d’emploi). L’objectif est de déployer ce système via des pipelines CI/CD (GitHub Actions) et de le rendre réutilisable dans une VM VirtualBox.
Ce document décrit l'architecture d'un agent local d'AI conçu pour ingérer, analyser et générer des documents professionnels (CV, lettres de motivation, emails) à partir de données personnelles et d'historiques de chat. L'objectif est de déployer cet agent dans un environnement local, avec une architecture modulaire, réutilisable et open-source.

## Objectifs & Fonctionnalités clés 
- **github** : https://github.com/bdelnoz/NoXoZ_job.git
- **local github location** : /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job
- **OLLAMA_MODELS location** : OLLAMA_MODELS=/mnt/data1_100g/agent_llm_local/models
- **Modularité** : Pipelines, API, base de données
- **Ingestion de données** : CV, exports de chats (Le Chat, ChatGPT, Grok, Claude)
- **Ingestion de fichiers**: `.md`, `.docx`, `.pdf`, `.json`, `.xml`
- **Génération de documents** : Lettres de motivation, CV personnalisés, emails
- **Génération de documents**: `.docx`, `.md`, `.pdf`
- **API RESTful** (FastAPI) pour interagir avec l’agent
- **Base de données** (SQLite + Chroma pour les embeddings)
- **Déploiement local** : d'abord en local puis utilisation de VirtualBox pour la virtualisation
- **Open-source** : Tous les codes et scripts seront hébergés sur un dépôt GitHub nommé `NoXoZ_job`
- **Déploiement conteneurisé** : d'abord en local puis (Docker Compose)
- **Pipeline CI/CD** (GitHub Actions)
- **100% local et offline** après le setup initial
- tout doit etre installé et configuré par scripting avec des variables etc pour permettre une réutilisation sur un autre systeme ou une vbox
- **Système d'exploitation** : Linux Kali / Debian


## Folder structure big files /mnt/data1_100g/agent_llm_local/ 
- **Localisation** big files  : `/mnt/data1_100g/agent_llm_local/`
┌──(nox㉿casablanca)-[/mnt/data1_100g/agent_llm_local]
└─$ tree  -L 3 -h
[4.0K]  .
├── [4.0K]  documentation
├── [4.0K]  llama.cpp
│   ├── [4.3K]  AGENTS.md
│   ├── [ 47K]  AUTHORS
│   ├── [4.0K]  benches
│   │   └── [4.0K]  dgx-spark
│   ├── [ 21K]  build-xcframework.sh
│   ├── [4.0K]  ci
│   │   ├── [1.3K]  README.md
│   │   ├── [1.0K]  README-MUSA.md
│   │   └── [ 27K]  run.sh
│   ├── [ 106]  CLAUDE.md
│   ├── [4.0K]  cmake
│   │   ├── [ 555]  arm64-apple-clang.cmake
│   │   ├── [ 592]  arm64-windows-llvm.cmake
│   │   ├── [1.3K]  build-info.cmake
│   │   ├── [2.0K]  common.cmake
│   │   ├── [ 717]  git-vars.cmake
│   │   ├── [1.4K]  license.cmake
│   │   ├── [ 979]  llama-config.cmake.in
│   │   ├── [ 311]  llama.pc.in
│   │   ├── [1.3K]  riscv64-spacemit-linux-gnu-gcc.cmake
│   │   └── [ 139]  x64-windows-llvm.cmake
│   ├── [9.4K]  CMakeLists.txt
│   ├── [4.5K]  CMakePresets.json
│   ├── [5.5K]  CODEOWNERS
│   ├── [4.0K]  common
│   │   ├── [164K]  arg.cpp
│   │   ├── [5.2K]  arg.h
│   │   ├── [ 13K]  base64.hpp
│   │   ├── [ 198]  build-info.cpp.in
│   │   ├── [127K]  chat.cpp
│   │   ├── [9.3K]  chat.h
│   │   ├── [ 64K]  chat-parser.cpp
│   │   ├── [4.8K]  chat-parser.h
│   │   ├── [ 42K]  chat-parser-xml-toolcall.cpp
│   │   ├── [2.2K]  chat-parser-xml-toolcall.h
│   │   ├── [4.1K]  chat-peg-parser.cpp
│   │   ├── [4.9K]  chat-peg-parser.h
│   │   ├── [4.8K]  CMakeLists.txt
│   │   ├── [ 62K]  common.cpp
│   │   ├── [ 36K]  common.h
│   │   ├── [ 40K]  console.cpp
│   │   ├── [ 953]  console.h
│   │   ├── [ 44K]  download.cpp
│   │   ├── [3.1K]  download.h
│   │   ├── [2.0K]  http.h
│   │   ├── [ 16K]  json-partial.cpp
│   │   ├── [1.7K]  json-partial.h
│   │   ├── [ 48K]  json-schema-to-grammar.cpp
│   │   ├── [1.4K]  json-schema-to-grammar.h
│   │   ├── [8.5K]  llguidance.cpp
│   │   ├── [ 11K]  log.cpp
│   │   ├── [5.2K]  log.h
│   │   ├── [ 11K]  ngram-cache.cpp
│   │   ├── [4.0K]  ngram-cache.h
│   │   ├── [ 64K]  peg-parser.cpp
│   │   ├── [ 17K]  peg-parser.h
│   │   ├── [ 16K]  preset.cpp
│   │   ├── [2.8K]  preset.h
│   │   ├── [8.2K]  regex-partial.cpp
│   │   ├── [1.5K]  regex-partial.h
│   │   ├── [ 26K]  sampling.cpp
│   │   ├── [5.2K]  sampling.h
│   │   ├── [ 12K]  speculative.cpp
│   │   ├── [1.0K]  speculative.h
│   │   ├── [2.4K]  unicode.cpp
│   │   └── [ 790]  unicode.h
│   ├── [ 10K]  CONTRIBUTING.md
│   ├── [523K]  convert_hf_to_gguf.py
│   ├── [ 25K]  convert_hf_to_gguf_update.py
│   ├── [ 19K]  convert_llama_ggml_to_gguf.py
│   ├── [ 20K]  convert_lora_to_gguf.py
│   ├── [4.0K]  docs
│   │   ├── [4.0K]  android
│   │   ├── [5.9K]  android.md
│   │   ├── [4.0K]  backend
│   │   ├── [ 33K]  build.md
│   │   ├── [4.0K]  build-riscv64-spacemit.md
│   │   ├── [ 11K]  build-s390x.md
│   │   ├── [4.0K]  development
│   │   ├── [8.5K]  docker.md
│   │   ├── [ 20K]  function-calling.md
│   │   ├── [1.1K]  install.md
│   │   ├── [3.7K]  llguidance.md
│   │   ├── [4.0K]  multimodal
│   │   ├── [3.9K]  multimodal.md
│   │   ├── [4.0K]  ops
│   │   ├── [ 11K]  ops.md
│   │   └── [2.8K]  preset.md
│   ├── [4.0K]  examples
│   │   ├── [4.0K]  batched
│   │   ├── [4.0K]  batched.swift
│   │   ├── [1.0K]  CMakeLists.txt
│   │   ├── [ 60K]  convert_legacy_llama.py
│   │   ├── [4.0K]  convert-llama2c-to-ggml
│   │   ├── [4.0K]  debug
│   │   ├── [4.0K]  deprecation-warning
│   │   ├── [4.0K]  diffusion
│   │   ├── [4.0K]  embedding
│   │   ├── [4.0K]  eval-callback
│   │   ├── [4.0K]  gen-docs
│   │   ├── [4.0K]  gguf
│   │   ├── [4.0K]  gguf-hash
│   │   ├── [4.0K]  idle
│   │   ├── [3.1K]  json_schema_pydantic_example.py
│   │   ├── [ 34K]  json_schema_to_grammar.py
│   │   ├── [4.0K]  llama.android
│   │   ├── [4.0K]  llama.swiftui
│   │   ├── [ 26K]  llama.vim
│   │   ├── [4.0K]  lookahead
│   │   ├── [4.0K]  lookup
│   │   ├── [4.0K]  model-conversion
│   │   ├── [4.0K]  parallel
│   │   ├── [4.0K]  passkey
│   │   ├── [ 13K]  pydantic_models_to_grammar_examples.py
│   │   ├── [ 55K]  pydantic_models_to_grammar.py
│   │   ├── [ 363]  reason-act.sh
│   │   ├── [ 431]  regex_to_grammar.py
│   │   ├── [4.0K]  retrieval
│   │   ├── [4.0K]  save-load-state
│   │   ├── [ 969]  server_embd.py
│   │   ├── [ 798]  server-llama2-13B.sh
│   │   ├── [4.0K]  simple
│   │   ├── [4.0K]  simple-chat
│   │   ├── [4.0K]  simple-cmake-pkg
│   │   ├── [4.0K]  speculative
│   │   ├── [4.0K]  speculative-simple
│   │   ├── [4.0K]  sycl
│   │   ├── [4.0K]  training
│   │   └── [ 928]  ts-type-to-grammar.sh
│   ├── [1.5K]  flake.lock
│   ├── [7.1K]  flake.nix
│   ├── [4.0K]  ggml
│   │   ├── [4.0K]  cmake
│   │   ├── [ 20K]  CMakeLists.txt
│   │   ├── [4.0K]  include
│   │   └── [4.0K]  src
│   ├── [4.0K]  gguf-py
│   │   ├── [4.0K]  examples
│   │   ├── [4.0K]  gguf
│   │   ├── [1.0K]  LICENSE
│   │   ├── [1.2K]  pyproject.toml
│   │   ├── [3.3K]  README.md
│   │   └── [4.0K]  tests
│   ├── [4.0K]  grammars
│   │   ├── [ 177]  arithmetic.gbnf
│   │   ├── [1.3K]  c.gbnf
│   │   ├── [ 565]  chess.gbnf
│   │   ├── [ 242]  english.gbnf
│   │   ├── [ 249]  japanese.gbnf
│   │   ├── [ 796]  json_arr.gbnf
│   │   ├── [ 601]  json.gbnf
│   │   ├── [ 109]  list.gbnf
│   │   └── [ 18K]  README.md
│   ├── [4.0K]  include
│   │   ├── [ 900]  llama-cpp.h
│   │   └── [ 78K]  llama.h
│   ├── [1.1K]  LICENSE
│   ├── [4.0K]  licenses
│   │   ├── [1.1K]  LICENSE-curl
│   │   └── [1.0K]  LICENSE-jsonhpp
│   ├── [ 257]  Makefile
│   ├── [4.0K]  media
│   │   ├── [141K]  llama0-banner.png
│   │   ├── [176K]  llama0-logo.png
│   │   ├── [ 33K]  llama1-banner.png
│   │   ├── [ 16K]  llama1-icon.png
│   │   ├── [2.7K]  llama1-icon.svg
│   │   ├── [ 14K]  llama1-icon-transparent.png
│   │   ├── [2.6K]  llama1-icon-transparent.svg
│   │   ├── [ 32K]  llama1-logo.png
│   │   ├── [2.3K]  llama1-logo.svg
│   │   ├── [259K]  matmul.png
│   │   └── [ 51K]  matmul.svg
│   ├── [4.0K]  models
│   │   ├── [4.6M]  ggml-vocab-aquila.gguf
│   │   ├── [1.3M]  ggml-vocab-baichuan.gguf
│   │   ├── [613K]  ggml-vocab-bert-bge.gguf
│   │   ├── [1.9K]  ggml-vocab-bert-bge.gguf.inp
│   │   ├── [1.6K]  ggml-vocab-bert-bge.gguf.out
│   │   ├── [ 10M]  ggml-vocab-command-r.gguf
│   │   ├── [1.9K]  ggml-vocab-command-r.gguf.inp
│   │   ├── [1.9K]  ggml-vocab-command-r.gguf.out
│   │   ├── [1.1M]  ggml-vocab-deepseek-coder.gguf
│   │   ├── [1.9K]  ggml-vocab-deepseek-coder.gguf.inp
│   │   ├── [2.0K]  ggml-vocab-deepseek-coder.gguf.out
│   │   ├── [3.8M]  ggml-vocab-deepseek-llm.gguf
│   │   ├── [1.9K]  ggml-vocab-deepseek-llm.gguf.inp
│   │   ├── [1.9K]  ggml-vocab-deepseek-llm.gguf.out
│   │   ├── [2.2M]  ggml-vocab-falcon.gguf
│   │   ├── [1.9K]  ggml-vocab-falcon.gguf.inp
│   │   ├── [2.0K]  ggml-vocab-falcon.gguf.out
│   │   ├── [1.7M]  ggml-vocab-gpt-2.gguf
│   │   ├── [1.9K]  ggml-vocab-gpt-2.gguf.inp
│   │   ├── [2.1K]  ggml-vocab-gpt-2.gguf.out
│   │   ├── [1.7M]  ggml-vocab-gpt-neox.gguf
│   │   ├── [7.5M]  ggml-vocab-llama-bpe.gguf
│   │   ├── [1.9K]  ggml-vocab-llama-bpe.gguf.inp
│   │   ├── [1.7K]  ggml-vocab-llama-bpe.gguf.out
│   │   ├── [707K]  ggml-vocab-llama-spm.gguf
│   │   ├── [1.9K]  ggml-vocab-llama-spm.gguf.inp
│   │   ├── [2.6K]  ggml-vocab-llama-spm.gguf.out
│   │   ├── [1.7M]  ggml-vocab-mpt.gguf
│   │   ├── [1.9K]  ggml-vocab-mpt.gguf.inp
│   │   ├── [1.9K]  ggml-vocab-mpt.gguf.out
│   │   ├── [6.5M]  ggml-vocab-nomic-bert-moe.gguf
│   │   ├── [709K]  ggml-vocab-phi-3.gguf
│   │   ├── [1.9K]  ggml-vocab-phi-3.gguf.inp
│   │   ├── [2.6K]  ggml-vocab-phi-3.gguf.out
│   │   ├── [5.7M]  ggml-vocab-qwen2.gguf
│   │   ├── [1.9K]  ggml-vocab-qwen2.gguf.inp
│   │   ├── [1.7K]  ggml-vocab-qwen2.gguf.out
│   │   ├── [1.6M]  ggml-vocab-refact.gguf
│   │   ├── [1.9K]  ggml-vocab-refact.gguf.inp
│   │   ├── [1.9K]  ggml-vocab-refact.gguf.out
│   │   ├── [1.6M]  ggml-vocab-starcoder.gguf
│   │   ├── [1.9K]  ggml-vocab-starcoder.gguf.inp
│   │   ├── [1.9K]  ggml-vocab-starcoder.gguf.out
│   │   └── [4.0K]  templates
│   ├── [ 163]  mypy.ini
│   ├── [4.0K]  pocs
│   │   ├── [ 216]  CMakeLists.txt
│   │   └── [4.0K]  vdot
│   ├── [122K]  poetry.lock
│   ├── [1.3K]  pyproject.toml
│   ├── [ 653]  pyrightconfig.json
│   ├── [ 29K]  README.md
│   ├── [4.0K]  requirements
│   │   ├── [ 575]  requirements-all.txt
│   │   ├── [  53]  requirements-compare-llama-bench.txt
│   │   ├── [ 360]  requirements-convert_hf_to_gguf.txt
│   │   ├── [  43]  requirements-convert_hf_to_gguf_update.txt
│   │   ├── [ 101]  requirements-convert_legacy_llama.txt
│   │   ├── [  43]  requirements-convert_llama_ggml_to_gguf.txt
│   │   ├── [ 216]  requirements-convert_lora_to_gguf.txt
│   │   ├── [  42]  requirements-gguf_editor_gui.txt
│   │   ├── [  49]  requirements-pydantic.txt
│   │   ├── [  79]  requirements-server-bench.txt
│   │   ├── [  13]  requirements-test-tokenizer-random.txt
│   │   └── [ 203]  requirements-tool_bench.txt
│   ├── [ 551]  requirements.txt
│   ├── [4.0K]  scripts
│   │   ├── [4.0K]  apple
│   │   ├── [1.9K]  bench-models.sh
│   │   ├── [ 717]  build-info.sh
│   │   ├── [4.3K]  check-requirements.sh
│   │   ├── [1.8K]  compare-commits.sh
│   │   ├── [ 45K]  compare-llama-bench.py
│   │   ├── [9.4K]  compare-logprobs.py
│   │   ├── [6.8K]  create_ops_docs.py
│   │   ├── [5.0K]  debug-test.sh
│   │   ├── [3.9K]  fetch_server_test_models.py
│   │   ├── [ 345]  gen-authors.sh
│   │   ├── [6.3K]  gen-unicode-data.py
│   │   ├── [2.8K]  get_chat_template.py
│   │   ├── [1.3K]  get-flags.mk
│   │   ├── [ 271]  get-hellaswag.sh
│   │   ├── [1.4K]  get-pg.sh
│   │   ├── [ 218]  get-wikitext-103.sh
│   │   ├── [ 261]  get-wikitext-2.sh
│   │   ├── [ 300]  get-winogrande.sh
│   │   ├── [2.3K]  hf.sh
│   │   ├── [ 802]  install-oneapi.bat
│   │   ├── [4.0K]  jinja
│   │   ├── [1.9K]  pr2wt.sh
│   │   ├── [ 13K]  server-bench.py
│   │   ├── [3.3K]  serve-static.js
│   │   ├── [4.0K]  snapdragon
│   │   ├── [4.5K]  sync-ggml-am.sh
│   │   ├── [  41]  sync-ggml.last
│   │   ├── [ 788]  sync-ggml.sh
│   │   ├── [2.3K]  sync_vendor.py
│   │   ├── [ 15K]  tool_bench.py
│   │   ├── [5.9K]  tool_bench.sh
│   │   ├── [2.4K]  verify-checksum-models.py
│   │   └── [ 641]  xxd.cmake
│   ├── [6.6K]  SECURITY.md
│   ├── [4.0K]  src
│   │   ├── [4.7K]  CMakeLists.txt
│   │   ├── [ 18K]  llama-adapter.cpp
│   │   ├── [2.0K]  llama-adapter.h
│   │   ├── [118K]  llama-arch.cpp
│   │   ├── [ 16K]  llama-arch.h
│   │   ├── [ 28K]  llama-batch.cpp
│   │   ├── [6.3K]  llama-batch.h
│   │   ├── [ 38K]  llama-chat.cpp
│   │   ├── [2.1K]  llama-chat.h
│   │   ├── [125K]  llama-context.cpp
│   │   ├── [ 11K]  llama-context.h
│   │   ├── [ 100]  llama-cparams.cpp
│   │   ├── [1.0K]  llama-cparams.h
│   │   ├── [ 50K]  llama.cpp
│   │   ├── [ 53K]  llama-grammar.cpp
│   │   ├── [6.8K]  llama-grammar.h
│   │   ├── [ 75K]  llama-graph.cpp
│   │   ├── [ 30K]  llama-graph.h
│   │   ├── [5.7K]  llama-hparams.cpp
│   │   ├── [9.1K]  llama-hparams.h
│   │   ├── [6.0K]  llama-impl.cpp
│   │   ├── [1.8K]  llama-impl.h
│   │   ├── [ 380]  llama-io.cpp
│   │   ├── [ 788]  llama-io.h
│   │   ├── [ 69K]  llama-kv-cache.cpp
│   │   ├── [ 13K]  llama-kv-cache.h
│   │   ├── [9.9K]  llama-kv-cache-iswa.cpp
│   │   ├── [4.0K]  llama-kv-cache-iswa.h
│   │   ├── [ 13K]  llama-kv-cells.h
│   │   ├── [1.5K]  llama-memory.cpp
│   │   ├── [4.4K]  llama-memory.h
│   │   ├── [8.9K]  llama-memory-hybrid.cpp
│   │   ├── [4.2K]  llama-memory-hybrid.h
│   │   ├── [ 38K]  llama-memory-recurrent.cpp
│   │   ├── [5.6K]  llama-memory-recurrent.h
│   │   ├── [ 23K]  llama-mmap.cpp
│   │   ├── [1.6K]  llama-mmap.h
│   │   ├── [472K]  llama-model.cpp
│   │   ├── [ 18K]  llama-model.h
│   │   ├── [ 50K]  llama-model-loader.cpp
│   │   ├── [6.0K]  llama-model-loader.h
│   │   ├── [ 14K]  llama-model-saver.cpp
│   │   ├── [1.0K]  llama-model-saver.h
│   │   ├── [ 48K]  llama-quant.cpp
│   │   ├── [  13]  llama-quant.h
│   │   ├── [124K]  llama-sampling.cpp
│   │   ├── [ 919]  llama-sampling.h
│   │   ├── [153K]  llama-vocab.cpp
│   │   ├── [6.2K]  llama-vocab.h
│   │   ├── [4.0K]  models
│   │   ├── [ 43K]  unicode.cpp
│   │   ├── [164K]  unicode-data.cpp
│   │   ├── [ 630]  unicode-data.h
│   │   └── [3.8K]  unicode.h
│   ├── [4.0K]  tests
│   │   ├── [ 10K]  CMakeLists.txt
│   │   ├── [ 594]  get-model.cpp
│   │   ├── [  53]  get-model.h
│   │   ├── [4.0K]  peg-parser
│   │   ├── [ 399]  run-json-schema-to-grammar.mjs
│   │   ├── [ 22K]  test-alloc.cpp
│   │   ├── [8.5K]  test-arg-parser.cpp
│   │   ├── [ 712]  test-autorelease.cpp
│   │   ├── [341K]  test-backend-ops.cpp
│   │   ├── [ 46K]  test-backend-sampler.cpp
│   │   ├── [7.5K]  test-barrier.cpp
│   │   ├── [  38]  test-c.c
│   │   ├── [187K]  test-chat.cpp
│   │   ├── [ 27K]  test-chat-parser.cpp
│   │   ├── [ 32K]  test-chat-peg-parser.cpp
│   │   ├── [ 54K]  test-chat-template.cpp
│   │   ├── [1.8K]  test-double-float.cpp
│   │   ├── [3.3K]  test-gbnf-validator.cpp
│   │   ├── [ 45K]  test-gguf.cpp
│   │   ├── [ 40K]  test-grammar-integration.cpp
│   │   ├── [ 39K]  test-grammar-llguidance.cpp
│   │   ├── [ 17K]  test-grammar-parser.cpp
│   │   ├── [5.3K]  test-json-partial.cpp
│   │   ├── [ 46K]  test-json-schema-to-grammar.cpp
│   │   ├── [ 11K]  test-llama-grammar.cpp
│   │   ├── [1.1K]  test-log.cpp
│   │   ├── [5.5K]  test-lora-conversion-inference.sh
│   │   ├── [ 763]  test-model-load-cancel.cpp
│   │   ├── [2.2K]  test-mtmd-c-api.c
│   │   ├── [ 39K]  test-opt.cpp
│   │   ├── [ 572]  test-peg-parser.cpp
│   │   ├── [7.0K]  test-quantize-fns.cpp
│   │   ├── [ 14K]  test-quantize-perf.cpp
│   │   ├── [ 16K]  test-quantize-stats.cpp
│   │   ├── [ 11K]  test-regex-partial.cpp
│   │   ├── [8.0K]  test-rope.cpp
│   │   ├── [ 16K]  test-sampling.cpp
│   │   ├── [4.4K]  test-state-restore-fragmented.cpp
│   │   ├── [5.5K]  test-thread-safety.cpp
│   │   ├── [ 11K]  test-tokenizer-0.cpp
│   │   ├── [1.9K]  test-tokenizer-0.py
│   │   ├── [ 929]  test-tokenizer-0.sh
│   │   ├── [4.8K]  test-tokenizer-1-bpe.cpp
│   │   ├── [3.6K]  test-tokenizer-1-spm.cpp
│   │   ├── [ 22K]  test-tokenizer-random.py
│   │   └── [ 893]  test-tokenizers-repo.sh
│   ├── [4.0K]  tools
│   │   ├── [4.0K]  batched-bench
│   │   ├── [4.0K]  cli
│   │   ├── [ 871]  CMakeLists.txt
│   │   ├── [4.0K]  completion
│   │   ├── [4.0K]  cvector-generator
│   │   ├── [4.0K]  export-lora
│   │   ├── [4.0K]  fit-params
│   │   ├── [4.0K]  gguf-split
│   │   ├── [4.0K]  imatrix
│   │   ├── [4.0K]  llama-bench
│   │   ├── [4.0K]  mtmd
│   │   ├── [4.0K]  perplexity
│   │   ├── [4.0K]  quantize
│   │   ├── [4.0K]  rpc
│   │   ├── [4.0K]  server
│   │   ├── [4.0K]  tokenize
│   │   └── [4.0K]  tts
│   └── [4.0K]  vendor
│       ├── [4.0K]  cpp-httplib
│       ├── [4.0K]  miniaudio
│       ├── [4.0K]  minja
│       ├── [4.0K]  nlohmann
│       ├── [4.0K]  sheredom
│       └── [4.0K]  stb
├── [199K]  ls.llama.cpp.txt
├── [2.9M]  ls.poc_mistral.txt
├── [4.0K]  models
│   ├── [ 12K]  blobs
│   │   ├── [8.2K]  sha256-097a36493f718248845233af1d3fefe7a303f864fae13bc31a3a9704229378ca
│   │   ├── [ 487]  sha256-1064e17101bdd2460dd5c4e03e4f5cc1b38a4dee66084dc91faba294ccb64a92
│   │   ├── [ 487]  sha256-161ddde4c9cd07c9f1ccb4e0167c434bce72caeb3fc1844262fa66bc877b0426
│   │   ├── [ 799]  sha256-1ff5b64b61b9a63146475a24f70d3ca2fd6fdeec44247987163479968896fc0b
│   │   ├── [ 483]  sha256-23291dc44752bac878bf46ab0f2b8daf75c710060f80f1a351151c7be2f5ee0f
│   │   ├── [  65]  sha256-2490e7468436707d5156d7959cf3c6341cc46ee323084cfa3fcf30fe76e397dc
│   │   ├── [  91]  sha256-266582a12719dff4148c5a5116dc48ad4ec1531a19878245230116e439418a75
│   │   ├── [  59]  sha256-2e0493f67d0c8c9c68a8aeacdf6a38a2151cb3c4c1d42accf296e19810527988
│   │   ├── [ 529]  sha256-316526ac7323d6f42305c5bbf1939e1197487c1e6ea1f01292ceb5e3040b707a
│   │   ├── [  52]  sha256-33eb43a1488dfe4da10339f40a7f1918179c804bae1ba36ae8a04052cc4f518a
│   │   ├── [ 561]  sha256-34bb5ab01051a11372a91f95f3fbbc51173eed8e7f13ec395b9ae9b8bd0e242b
│   │   ├── [3.6G]  sha256-3a43f93b78ec50f7c4e4dc8bd1cb3fff5a900e7d574c51a6f7495e48486e0dac
│   │   ├── [ 487]  sha256-40fb844194b25e429204e5163fb379ab462978a262b86aadd73d8944445c09fd
│   │   ├── [ 11K]  sha256-43070e2d4e532684de521b885f385d0841030efa2b1a20bafb76133a5e1379c1
│   │   ├── [ 200]  sha256-4b21bfc435b4b81b8c258c196160ddc87a51a0dceafe0693d72371213ec0c9c0
│   │   ├── [ 148]  sha256-542b217f179c7825eeb5bca3c77d2b75ed05bafbd3451d9188891a60a85337c6
│   │   ├── [  96]  sha256-56bb8bd477a519ffa694fc449c2413c6f0e1d3b1c88fa7e3c9d88d3ae49d4dcb
│   │   ├── [3.8G]  sha256-5768750fc96e296081ba7531933c7eb5c5bacfafbd06b81d1bb495e97f6a4b20
│   │   ├── [4.7K]  sha256-590d74a5569b8a20eb2a8b0aa869d1d1d3faf6a7fdda1955ae827073c7f502fc
│   │   ├── [1.8G]  sha256-5ee4f07cdb9beadbbb293e85803c569b01bd37ed059d2715faa7bb405f31caa6
│   │   ├── [2.0G]  sha256-633fc5be925f9a484b61d6f9b9a78021eeb462100bd557309f01ba84cac26adf
│   │   ├── [7.4G]  sha256-64e8f4d6856fca67b11f0875f9552264e62ababbe68fd6ddd0129015ee6df70a
│   │   ├── [1.8G]  sha256-66002b78c70a22ab25e16cc9a1736c6cc6335398c7312e3eb33db202350afe66
│   │   ├── [  68]  sha256-66b9ea09bd5b7099cbb4fc820f31b575c0366fa439b08245566692c6784e281e
│   │   ├── [1.0K]  sha256-6e4c38e1172f42fdbff13edf9a7a017679fb82b0fde415a3e8b3c31c6ed4a4e4
│   │   ├── [1.5G]  sha256-7462734796d67c40ecec2ca98eddf970e171dbb6b370e43fd633ee75b69abe1b
│   │   ├── [3.8G]  sha256-77bf5506c1e863c73d1f7ed41ecbf27929a04144d19a2688148fabb127d2e692
│   │   ├── [ 120]  sha256-7f6a57943a88ef021326428676fe749d38e82448a858433f41dae5e05ac39963
│   │   ├── [6.9K]  sha256-8c17c2ebb0ea011be9981cc3922db8ca8fa61e828c5d3f44cb6ae342bf80460b
│   │   ├── [  78]  sha256-8dde1baf1db03d318a2ab076ae363318357dff487bdd8c1703a29886611e581f
│   │   ├── [  89]  sha256-93ca9b3d83dc541f11062c0b994ae66a7b327146f59a9564aafef4a4c15d1ef5
│   │   ├── [1.4K]  sha256-966de95ca8a62200913e3f8bfbf84c8494536f1b94b49166851e76644e966396
│   │   ├── [4.4G]  sha256-96c415656d377afbff962f6cdb2394ab092ccbcbaab4b82525bc4ca800fe8a49
│   │   ├── [5.9K]  sha256-a70ff7e570d97baaf4e62ac6e6ad9975e04caa6d900d3742d37698494479e0cd
│   │   ├── [5.7G]  sha256-b183354255015d9f61f5738b5a50b5297ab679d289ef5296022c1de42a7119e5
│   │   ├── [7.2K]  sha256-b5c0e5cf74cf51af1ecbc4af597cfcd13fd9925611838884a681070838a14a50
│   │   ├── [  67]  sha256-bf99dec66c971b7bf13c630e756d036d7ffc5b537029a869bb282148c9550b2f
│   │   ├── [ 556]  sha256-c5ad996bda6eed4df6e3b605a9869647624851ac248209d22fd5e2c0cc1121d3
│   │   ├── [ 484]  sha256-c96afb4d9900b521ba602d2dee1245fc8eced936e7511e4fc570ddf3ab630929
│   │   ├── [ 409]  sha256-d46e54e2a9984f81638067f64cf8ec77d1c7d1bad02c724321ebfece89e3028e
│   │   ├── [  95]  sha256-dd90d0f2b7eeb7a0944377398fb3add658f2ff4b6d0ec5065d6ae68bb052648b
│   │   ├── [ 410]  sha256-ddbf18e70a9fe012221a094594b0d1a62f65cd5e04d6bffa810fd8271e2a578c
│   │   ├── [1.9G]  sha256-dde5aa3fc5ffc17176b5e8bdc82f587b24b2678c6c66101bf7da77af9f7ccdff
│   │   ├── [ 358]  sha256-e0a42594d802e5d31cdc786deb4823edb8adff66094d49de8fffe976d753e348
│   │   ├── [ 487]  sha256-e18ad7af7efbfaecd8525e356861b84c240ece3a3effeb79d2aa7c0f258f71bd
│   │   ├── [  86]  sha256-e399adb0b8c6fbfe502f7eb1b5e0c793cce5a9b3c9a823eba679c1df34a21634
│   │   ├── [4.9G]  sha256-e6a7edc1a4d7d9b2de136a221a57336b76316cfe53a252aeba814496c5ae439d
│   │   ├── [1.4K]  sha256-eb4402837c7829a690fa845de4d7f3fd842c2adee476d5341da8a46ea9255175
│   │   ├── [  30]  sha256-ed11eda7790d05b49395598a42b155812b17e263214292f7b87d15e14003d337
│   │   ├── [ 179]  sha256-ed8474dc73db8ca0d85c1958c91c3a444e13a469c2efb10cd777ca9baeaddcb7
│   │   ├── [ 148]  sha256-f4d24e9138dd4603380add165d2b0d970bef471fac194b436ebd50e6147c6588
│   │   ├── [  87]  sha256-f507449d49be6c11df68a04f3ac713de6d1b728c00c2f56f8b9411f420883c5d
│   │   ├── [4.1G]  sha256-f5074b1221da0f5a2910d33b642efa5b9eb58cfdddca1c79e16d7ad28aa2b31f
│   │   ├── [ 483]  sha256-f5a875414a6f0000eab6cab4f8f4be9fabe0f47de4f221f07675bbf114616477
│   │   ├── [ 487]  sha256-f64cd5418e4b038ef90cf5fab6eb7ce6ae8f18909416822751d3b9fca827c2ab
│   │   ├── [1.1K]  sha256-fa8235e5b48faca34e3ca98cf4f694ef08bd216d28b58071a1f85b1d50cb814d
│   │   ├── [7.5K]  sha256-fcc5a6bec9daf9b561a68827b67ab6088e1dba9d1fa2a50d7bbcc8384e0a265d
│   │   └── [ 455]  sha256-fd52b10ee3ee9d753b9ed07a6f764ef2d83628fde5daf39a3d84b86752902182
│   └── [4.0K]  manifests
│       └── [4.0K]  registry.ollama.ai
├── [ 139]  Pipfile
├── [4.0K]  poc_mistral
│   ├── [4.0K]  creation_log
│   │   ├── [ 891]  log.create_repo.v5.6.20251230_005012.log
│   │   └── [3.1K]  log.create_repo.v5.6.20251230_005105.log
│   ├── [ 17K]  install_POC.sh
│   ├── [4.0K]  py
│   │   ├── [ 110]  create_env.py
│   │   ├── [4.0K]  poc_mistral
│   │   └── [1.5K]  size_models.py
│   └── [  14]  README.md
├── [4.0K]  scripts
│   ├── [   0]  create-repo.sh
│   ├── [ 10K]  init_project.sh
│   └── [4.0K]  old_versions
│       ├── [   0]  all_my_scripts.old_versions.txt
│       ├── [7.6K]  create_structure.sh
│       └── [2.8K]  setup_agent_llm.sh
└── [4.0K]  vectors

103 directories, 386 files


## Folder structure project files /mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job
- **Localisation** project files  : `/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job/`
┌──(NoXoZ_job-wtw5guxt)(nox㉿casablanca)-[/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job]
└─$ tree -h -L 3
[4.0K]  .
├── [4.0K]  1_Documentation
│   ├── [4.0K]  1.1_General
│   │   ├── [ 36K]  INSTALL.docx
│   │   ├── [2.6K]  ollama-models-guide.md
│   │   └── [ 36K]  WHY.docx
│   └── [4.0K]  1.2_Technical
│       ├── [ 36K]  API_SPECIFICATIONS.docx
│       ├── [4.1K]  architecture_agent_llm_local.md
│       ├── [ 36K]  ARCHITECTURE.docx
│       ├── [5.7K]  LECHAT-architecture_agent_llm_local.md
│       ├── [8.2K]  OLLAMA_all_models_with_token_limits.md
│       ├── [8.3K]  OLLAMA_commandes.md
│       ├── [1.1K]  structure.md
│       └── [ 945]  table.csv
├── [4.0K]  2_Sources
│   ├── [4.0K]  2.1_Python
│   │   └── [   0]  main_agent.py
│   └── [4.0K]  2.2_Bash
│       └── [   0]  create_structure.sh
├── [4.0K]  3_Data
│   ├── [4.0K]  3.1_Vectors
│   │   ├── [  39]  chroma_link -> /mnt/data1_100g/agent_llm_local/vectors
│   │   └── [  38]  models_link -> /mnt/data1_100g/agent_llm_local/models
│   └── [4.0K]  3.2_Metadata
├── [4.0K]  4_Logs
├── [4.0K]  5_Outputs
│   ├── [4.0K]  5.1_DOCX
│   └── [4.0K]  5.2_PDF
├── [4.0K]  6_Results
│   ├── [4.0K]  6.1_Bugs
│   └── [4.0K]  6.2_Innovations
├── [4.0K]  7_Infos
│   └── [ 924]  PERMANENT_MEMORY.md
├── [4.0K]  8_Scripts
│   ├── [4.0K]  8.1_Init
│   │   ├── [9.4K]  config_paths.sh
│   │   ├── [1.5K]  fix_ollama_group_permissions.sh
│   │   ├── [4.0K]  logs
│   │   ├── [9.7K]  ollama-batch-download.sh
│   │   ├── [2.2K]  reset_ollama_service.sh
│   │   └── [4.0K]  results
│   └── [4.0K]  8.2_Utils
│       └── [9.6K]  count_tokens.sh
├── [4.0K]  9_Templates
├── [   0]  docker-compose.yml
├── [4.0K]  logs
│   ├── [4.0K]  CONFIG_PATHS
│   └── [4.0K]  INIT
├── [ 250]  Pipfile
├── [178K]  Pipfile.lock
├── [  12]  README.md
├── [   0]  requirements.txt
└── [ 272]  start_ollama.sh

29 directories, 25 files


---




## Composants Clés

| Composant                  | Technologie                                             | Rôle                                                                 |
|----------------------------|---------------------------------------------------------|----------------------------------------------------------------------|
| **LLM Engine**             | Ollama (Mistral-7B)                                     | Inférence locale du modèle de langage (gratuit, téléchargeable)      |
| **Document Ingestion**     | LangChain Loaders                                       | Parsing des fichiers (PDF, DOCX, MD, JSON, XML)                      |
| **Vector Store**           | Chroma                                                  | Stockage persistant des embeddings sur disque                        |
| **Agent Logic**            | LangChain (ReAct)                                       | Raisonnement et actions (génération de docs basés sur les données)   |
| **API Layer**              | FastAPI                                                 | Endpoints pour upload, requêtes et génération de documents           |
| **DB**                     | SQLite + Chroma                                         | Métadonnées utilisateur et stockage vectoriel                        |
| **Output Generation**      | Pandoc, python-docx                                     | Conversion et génération de fichiers (MD → PDF/DOCX)                 |
| **Deployment**             | Docker Compose                                          | Conteneurisation pour réutilisation en VBox                          |
| **Storage big files**      | `/mnt/data1_100g/agent_llm_local/`                      | Stockage centralisé des gros volumes                                 |
| **Storage project files**  | `/mnt/data2_78g/Security/scripts/AI_Projects/NoXoZ_job` | Stockage centralisé des fichiers du projet github                    |

---

## Architecture Diagramme (Text-Based)

```text
+-------------+     +-------------+
| User Input  |     | GitHub Repo |
| (CLI/API)   |<--->| NoXoZ_job   |
+-------------+     +-------------+
         |                  ^
         v                  |
 +----------------+     +----------+
 | FastAPI Server |<--->| Pipelines|
 +----------------+     | (CI/CD)  |
         |              +----------+
         v
 +-----------------+
 | LangChain Agent |
 | (ReAct + Tools) |
 +-----------------+
         |
         v
 +-----------------+     +-----------------+
 | Ollama LLM      |<--->| Chroma Vector DB|
 | (Mistral-7B)    |     | + SQLite Meta   |
 +-----------------+     +-----------------+
         |                        |
         v                        v
 +-----------------+     +-----------------+
 | Doc Loaders     |     | Persistent Storage|
 | (.md/.docx/etc) |     | /mnt/data1_100g/ |
 +-----------------+     +-----------------+
         |
         v
 +-----------------+
 | Output Generators|
 | (Pandoc/Docx)   |
 +-----------------+


