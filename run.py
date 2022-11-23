import yaml
import subprocess
import sys
import os
import pandas as pd

with open('config.yaml', "r") as f:
    config_string = f.read()
config = yaml.safe_load(config_string)

subprocess.run(["bash", "-e", "-c",
    """
    git submodule update --init --recursive
    """], check=True)

filename = sys.argv[1]

df = pd.DataFrame()
if os.path.exists(filename):
    df = pd.read_csv(filename, index_col=False)

for renderer in ['mitsuba', 'luisa']:
    for commit in config[renderer]['commits'][:2]:
        # Build
        cmake_flags = ' '.join(config[renderer]['cmake_flags'])
        subprocess.run(["bash", "-e", "-c",
            f"""
            export CXX={config[renderer]['compiler']['cxx']}
            export CC={config[renderer]['compiler']['cc']}
            cd {config[renderer]['folder']}
            git checkout {commit}
            git submodule update --init --recursive
            mkdir -p build
            cd build
            cmake {cmake_flags} ..
            {config[renderer]['build_command']}
            """], check=True)

        for i in range(config['runs']):
            # Run
            subprocess.run([f"{sys.executable}",
                "ext/LuisaBenchmark/run.py", f"{config[renderer]['name']}"],
                check=True)

            results = pd.read_csv(
                    "ext/LuisaBenchmark/outputs/results.csv",
                    index_col=False
            )
            results['commit'] = commit

            df =  pd.concat([df, results])

df.to_csv(filename, index=False)
