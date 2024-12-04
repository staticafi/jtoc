import glob
import os
import shutil
import subprocess

from pathlib import Path
import sys

import yaml

from capture import capture_only, parse_functions, parse_symbols
from static import SOURCE_DIR, logger, BENCHMARKS_DIR, COMPILE_DIR
from processing.program_processor import ProgramProcessor


COMPILE_COMMAND = ["javac", "-source", "1.8", "-Werror", "-d", str(COMPILE_DIR.absolute())]


def process_input() -> None:
    goto, symbol = capture_only('Main')

    functions = parse_functions(goto)
    symbols = parse_symbols(symbol)

    processor = ProgramProcessor(symbols, functions)
    processor.write_to_file('out.c')


def process_benchmark(task_file: str) -> None:
    with open(task_file) as f:
        task_def = yaml.safe_load(f)

    task_dir = glob.escape(os.path.dirname(task_file))
    java_files = [
        java_file
        for input_path in task_def["input_files"]
        for java_file in glob.glob(
            os.path.join(task_dir, glob.escape(input_path), "**/*.java"), recursive=True
        )
    ]

    shutil.rmtree(COMPILE_DIR)
    COMPILE_DIR.mkdir()

    os.chdir(SOURCE_DIR)
    logger.warning(f'compiling {len(java_files)} Java files from {task_file}')
    javac = subprocess.run(COMPILE_COMMAND + java_files)
    if javac.returncode:
        logger.error('[compilation failed] *.java -> *.class')
        return

    try:
        process_input()
    except:
        logger.error(f'error in file {task_file}')
        return

    gcc_compile = subprocess.run(['gcc', COMPILE_DIR / 'out.c'])
    if gcc_compile.returncode:
        logger.error('[compilation failed] out.c -> a.out')
        return
    
    jtoc_run = subprocess.run([COMPILE_DIR / 'a.out'])
    if jtoc_run.returncode:
        logger.error('[jtoc run] failed')
    else:
        logger.info('[jtoc run] success')


def process_all_benchmarks() -> None:
    for task_file in glob.iglob(str(BENCHMARKS_DIR / "**/*.yml"), recursive=True):
        process_benchmark(task_file)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        task_file = BENCHMARKS_DIR / sys.argv[1]
        process_benchmark(task_file)
    else:
        process_all_benchmarks()
