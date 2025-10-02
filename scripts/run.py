import argparse
import os
from matharena.runner import run
import yaml
from loguru import logger

parser = argparse.ArgumentParser()
parser.add_argument("--repeats", type=int, default=1, help="Number of experimental repeats")
parser.add_argument("--k", type=int, default=4, help="Number of response samples per problem")
parser.add_argument("--configs", type=str, nargs="+", required=True)
parser.add_argument("--skip-existing", action="store_true")
parser.add_argument("--comp", type=str, required=True)
parser.add_argument("--data", type=str, default=None, help="Directory to store/download competition data")
parser.add_argument("--output-folder", type=str, default="outputs")
parser.add_argument("--report-path", type=str, default=None, help="Path to save report outputs (overriding output-folder)")
parser.add_argument("--configs-folder", type=str, default="configs/models")
parser.add_argument("--competition-config-folder", type=str, default="configs/competitions")
parser.add_argument("--recompute-tokens", action='store_true', help="Recompute tokens for all models")
args = parser.parse_args()

for config_path in args.configs:
    for repeat_idx in range(args.repeats):
        config_path_yaml = config_path + ".yaml" if not config_path.endswith(".yaml") else config_path
        with open(f"{args.configs_folder}/{config_path_yaml}", 'r') as f:
            model_config = yaml.safe_load(f)
        
        model_config["k"] = model_config.get("k", args.k)
        logger.info(f"Running config: {config_path}, repeat: {repeat_idx}")
        run(model_config, config_path, args.comp, repeat_idx=repeat_idx, skip_existing=args.skip_existing,
            output_folder=args.output_folder, report_path=args.report_path, competition_config_folder=args.competition_config_folder, recompute_tokens=args.recompute_tokens, data_dir=args.data)
