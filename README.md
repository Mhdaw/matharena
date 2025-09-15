<div align="center">
    <h1><img height="150px" src="./images/matharena_icon.png" alt="MathArena"><br>MathArena</h1>

  <a href="https://www.python.org/">
<img alt="Build" src="https://img.shields.io/badge/Python-3.12-1f425f.svg?color=blue">
  </a>
  <a href="https://opensource.org/licenses/MIT">
<img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg">
  </a>
  <a href="https://huggingface.co/MathArena">
<img alt="MathArena Datasets" src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Matharena-ffc107?color=ffc107&logoColor=white">
  </a>
</div>

## 👋 Overview

MathArena is a platform for the evaluation of LLMs on the latest math competitions and olympiads. It is hosted on [matharena.ai](https://matharena.ai/). This repository contains all the code used for model evaluation of the competitions. The README explains how to run your models or add a new competition. 

## 📑 Table of Contents
- [Installation](#installation)
- [Evaluating a New Model](#evaluating-a-new-model)
  - [Model Configuration](#model-configuration)
  - [Running the Model](#running-the-model)
  - [Project Euler](#project-euler)
- [Adding a Competition](#adding-a-competition)
  - [Setting Up Competition Files](#setting-up-competition-files)
  - [Verifying Problem Statements](#verifying-problem-statements)
  - [Running Models on Competitions](#running-models-on-competitions)
  - [Competitions Requiring Grading](#competitions-requiring-grading)
- [Viewing Results](#viewing-results)
- [Evaluation logs](#evaluation-logs)

## 🚀 Installation

MathArena uses [UV](https://github.com/astral-sh/uv) to manage dependencies. If you want to run local models, uncomment the vllm installation in `pyproject.toml`.

### Install UV

- **macOS and Linux:**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Windows:**
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
---

### Alternative installation

As an alternative to UV, you can also create a conda environment and install the package as follows:
```bash
conda create -n matharena python=3.12
conda activate matharena
python -m pip install -e .
```
If you choose this option, disregard `uv run` in all instructions and use python directly instead.

## 🤖 Evaluating a New Model

### Model Configuration

Create a configuration file in the `configs/models` folder. Each config must include:
- **Required:**
  - `model`: Model name. Reasoning effort of OpenAI models can be set by appending `--[low/medium/high]` to the model name, e.g., `o3-mini--high`.
  - `api`: API provider. The API key should be defined as environment variable when using the specified API. The supported options with their corresponding API keys are:
    - **openai**: `OPENAI_API_KEY`
    - **anthropic**: `ANTHROPIC_API_KEY`
    - **together**: `TOGETHER_API_KEY`
    - **google**: `GOOGLE_API_KEY`
    - **deepseek**: `DEEPSEEK_API_KEY`
    - **openrouter**: `OPENROUTER_API_KEY`
    - **vllm**: (runs locally; no API key required)
  - `human_readable_id`: A unique, descriptive identifier.
- **Optional Parameters:**
  - API settings like `temperature`, `top_p`, and `top_k` (default: `temperature` is from competition config, see [Adding a Competition](#adding-a-competition)).
  - `max_tokens`: Max number of tokens for the model (default: from competition config, see [Adding a Competition](#adding-a-competition)).
  - `concurrent_requests`: Number of parallel requests to API (default: 30).
  - `timeout`: Request timeout in seconds (default: 2000).
  - `max_retries`: Retry attempts to API (default: 50).
  - `read_cost` & `write_cost`: Cost per million tokens in USD for input and output tokens (default: 1 each).
  - `date`: Creation date of the model in the format "yyyy-mm-dd".
  - `batch_processing`: If set to true, the model will be queried using batch processing. Only available for OpenAI and Anthropic models.

### Running the model
Execute the following command to evaluate a model on a competition:
```bash
uv run python scripts/run.py --configs path/to/your/config --comp path/to/competition
```
- `path/to/your/config`: Relative path from the `configs/models` folder to the model configuration (excluding the `.yaml` extension).
- `path/to/competition`: Relative path from the `configs/competition` folder to the competition folder (excluding the `.yaml` extension).

**Example:**
```bash
uv run python scripts/run.py --configs openai/gpt-4o --comp aime/aime_2025
```

**Additional Flags:**
- `--skip-existing`: Skip problems already processed through the model.
- `--n`: Number of runs per problem (default: 4).

*Note*: Errors thrown by the API provider are retried every minute up to 50 times. If no answer is returned after 50 tries, the answer will be counted as incorrect. Running again with `skip-existing` enabled will attempt to run the problems on which this occurred again.

### Uploading answers to HuggingFace
You can upload the model answers to HuggingFace as follows:
```bash
uv run python scripts/curation/upload_outputs.py --org your_org --repo-name your_repo_name --comp path/to/competition
```
This will upload all model answers to a private repository named `your_org/your_repo_name`. `path/to/competition` is the relative path from the `configs/competition` folder to the competition folder (excluding the `.yaml` extension).

### Project Euler
For Project Euler, several additional steps need to be taken. Please check README_euler.md for the full details.


## ➕ Adding a Competition

### Competition Format
MathArena supports the addition of any benchmark or competition uploaded to HuggingFace (or locally saved using the `datasets` library) that has the following columns:
- `problem_idx` (int): The id associated with the problem.
- `problem`(str): The problem statement.
- `answer` (str, Optional): The answer to the problem. Required for competitions with final answers.
- `points` (int, Optional): The number of points associated with the problem. Only required for competitions without final answers.
- `sample_solution` (str, Optional): Sample solution to the problem. Only required for competitions without final answers and during autograding.
- `sample_grading` (str, Optional): Example of how the grading format should look like. Only required for competitions without final answers and during autograding.
- `grading_scheme` (list, Optional): The grading scheme for the problem. Only required for competitions without final answers.
We refer to [the instructions regarding graded competitions](#competitions-requiring-grading) for the specific format of the grading scheme.

### Configuration
To set up MathArena for evaluation on the competition, you should add a competition config file in the `configs/competitions` folder with the following parameters:
- `instruction`: Instructions for the model. *Must* require the final answer be in `\boxed{}`.
- `default_temperature`: Default temperature.
- `default_max_tokens`: Default max tokens.
- `strict_parsing`: `true` for strict format matching (e.g., only `\boxed{43}` is accepted) or `false` for lenient parsing.
- `n_problems`: Total number of problems.
- `date`: Date of the competition, in the format "YYYY-MM-DD".
- `dataset_path`: Path to the dataset uploaded on HuggingFace or stored locally.
- `final_answer` (optional): If set to false, the competition is one that is manually graded with judges. Defaults to true if not set.

### Manual Curation and Creation
To create a pipeline that enables quick curation and easy generation of new competitions, we describe our full process for dataset creation. Note that you do not have to follow these steps if you have another way to generate your benchmark in the appropriate format.

#### Setting Up Competition Files
In the `data/` folder, create a new directory for your competition with the following structure:
1. **Problems:**  
   - Create a subfolder `problems/` and add each problem as a separate LaTeX file named `1.tex`, `2.tex`, ..., `{k}.tex`, where `k` is the number of problems in your competition. You can skip a problem if you want/need to.
2. **Answers:**  
   - If the competition is one based on final answers, add an `answers.csv` file with columns `id` and `answer`.
     - `id`: The problem filename (without the `.tex` extension).
     - `answer`: The integer answer.
   - If the competition is evaluated using human judges, add a `grading_scheme.json` file. This file should consist of a list of dictionaries, each of which contain the following fields:
     - `id`: The problem filename (without the `.tex` extension).
     - `points`: The maximum number of points for the question.
     - `scheme`: A list of dictionaries, each containing substeps for which points are awarded. Each dictionary contains the following keys:
        - `points`: Points associated with this step.
        - `title`: Title of the step. Should be unique across all dictionaries in this scheme.
        - `desc`: Description of the step.

#### Verifying Problem Statements
Ensure your LaTeX problems compile correctly:
```bash
uv run python scripts/curation/check_latex.py --comp path/to/competition
```
Then, build the `latex/main.tex` to generate a PDF and confirm all problems appear as expected.

#### Upload to HuggingFace
Finally, you can upload the competition to HuggingFace:
```bash
uv run python scripts/curation/upload_competition.py --org your_org --repo-name your_repo_name --comp path/to/competition
```
This will upload all answers in the appropriate format to a private repository named `your_org/your_repo_name`. `path/to/competition` is the relative path from the `configs/competition` folder to the competition folder (excluding the `.yaml` extension). Thus, you need to have created the configuration file before uploading to HuggingFace.

### Running Models on Competitions
To run multiple models (possibly across different APIs), use:
```bash
uv run python scripts/run_multiple.py --apis openai google anthropic together --comp path/to/competition
```
This will run models from the same API sequentially and from different APIs concurrently.
**Options:**
- `--simul`: Run all models in parallel, even if they use the same API.
- `models`: Provide space-separated regex patterns to filter models. A model is only run if it matches any of the regexes.
- `skip-existing`: Skip problems already processed through the model.
- `n`: Number of runs per problem (default: 4).

*Note:* For local vllm usage, ensure the vllm server is running as described above. Logs will be found in the `logs/` folder.

### Competitions Requiring Grading
For competitions requiring human grading, we use the Open Proof Corpus repository: https://github.com/insait-institute/open-proof-corpus. This repository contains instructions to run models on questions and competitions and contains a nice grading interface for judges. It also contains a script that converts that format to the MathArena format. The result of this script should simply be copy-pasted to `outputs/path/to/competition` for use and display in this repository.

## 📊 Viewing Results

Launch a local web server to inspect the results:
```bash
uv run python scripts/app.py --comp path/to/competition
```
Access the app at [http://localhost:5001/](http://localhost:5001/). Warning signs for solutions indicate a potential problem with the model run and should be manually verified. Any warning is caused by one of the following problems:

* 💀: parser threw an error or encountered something unexpected.
* ⚠️: The correct answer might be present in the model answer, but it was not extracted.
* ❕: Model likely hit max token limit.

If issues are found, delete the corresponding output file or fix the parser and rerun the model with `skip-existing`. If the parser requires a manual overwrite, you can edit `src/matharena/parse_manual.py` and add a key-value pair mapping the model solution to a parsable solution.

### Creating a Leaderboard
If in addition you prefer to see a leaderboard with rigorous confidence intervals, you can run
```bash
uv run python scripts/extraction/leaderboard.py --comps path/to/competition1 path/to/competition2
```
This script has several additional important parameters:
- `--keep-comps` (bool): In addition to the average across the listed competitions, whether to also keep the results for each competition separately in the leaderboard.
- `--compute-variance` (bool): Whether to compute the confidence intervals. Note: computing confidence intervals is expensive and can take several minutes.
- `--alpha` (Default: 0.05): Significance level associated with the confidence intervals.
- `--human-quantiles` (list[float]): Which quantiles of human performance to add to the leaderboard. Is only possible for AIME, SMT, and HMMT 2025.


## 🪵 Evaluation Logs

You can find logs from our evaluation containing full reasoning traces (if available) and solutions produced by the models at the following link: [https://huggingface.co/MathArena](https://huggingface.co/MathArena).

## 📜 Scripts
`scripts` contains various small files that serve purposes from curation and verification of model outputs to extracting the raw data into latex tables. We briefly describe the purpose of the files that have not been explained yet here.

### Curation
`scripts/curation` contains various files that make the curation of the model outputs easier. Most of these files have been explained before, but there are a couple still worth mentioning.

After making a change to the parser, and before rerunning models, you can test your updates using:
```bash
uv run python scripts/curation/test_parser_changes.py
```
This script will automatically extract every possible model output in the `outputs` folder and verify that the stored results match the new parser's output. The script will list all outputs that do not satisfy this, essentially serving as a rigorous test for the new parser.

After verifying the new parser's result, one can run 
```bash
uv run python scripts/curation/reparse_all.py
```
This script reparses all outputs in the `outputs` folder, simplifying the process of making full parser updates.

To verify with a judge model whether the rule-based parser returns the correct answers, one can run 
```bash
uv run python scripts/curation/judge_parser.py --comp aime/aime_2025
```
This will verify and check all decisions by the rule-based parser using Gemini-Flash-2.5. Outputs where the model disagrees with the parser are logged in `parser_judge_logs`.

### Extraction
This folder contains scripts that extract the answers from the raw data and creates plots and a leaderboard.

To compare model performance between several competitions in a plot, one can run
```bash
uv run python scripts/extraction/comparison.py --old-comps aime/aime_2024 hmmt/hmmt_feb_2024 --new-comps aime/aime_2025 hmmt/hmmt_feb_2025
```

To compare the spearman correlation between different competitions, run
```bash
uv run python scripts/extraction/rank_correlation.py --comps aime/aime_2025  hmmt/hmmt_feb_2025
```

To create a plot of the Pareto-Frontier of model performance vs cost or model release date, run
```bash
uv run python scripts/extraction/timeline.py --comps aime/aime_2025  hmmt/hmmt_feb_2025
```
Here, specify the `--cost` parameter if you prefer the Pareto-Frontier for cost.

To create a table containing results per category (Combinatorics, Number Theory, ...), run
```bash
uv run python scripts/extraction/type_scoring.py --comps aime/aime_2025  hmmt/hmmt_feb_2025
```


## 📚 Citation

```
@misc{balunovic_srimatharena_2025,
	title = {MathArena: Evaluating LLMs on Uncontaminated Math Competitions},
  author = {Mislav Balunović and Jasper Dekoninck and Ivo Petrov and Nikola Jovanović and Martin Vechev},
	copyright = {MIT},
	url = {https://matharena.ai/},
	publisher = {SRI Lab, ETH Zurich},
	month = feb,
	year = {2025},
}
```
