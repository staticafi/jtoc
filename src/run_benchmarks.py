import glob
import os
import shutil
import subprocess
import yaml

from dataclasses import dataclass
from pathlib import Path

from capture.compiling import capture, parse_functions, parse_symbols
from static import logger, BENCHMARKS_DIR, COMPILE_DIR
from processing.program_processor import ProgramProcessor


COMPILE_COMMAND = ["javac", "-source", "1.8", "-Werror", "-d", str(COMPILE_DIR.absolute())]


@dataclass
class BenchmarkTestResult:
    compilation: str | None = None

    def _has_passed(self) -> bool:
        return not self.compilation

    def short_result(self) -> str:
        if self._has_passed():
            return ' OK '
        return 'FAIL'

    def print_summary(self) -> None:
        if not self.compilation:
            return

        logger.error(self.compilation)



class TestCase:
    def __init__(self, task_file: Path) -> None:
        self.task_file = task_file
        self.test_name = f'{self.task_file.parent.name}/{self.task_file.stem}'
        self.category = self.task_file.parent.name
        self.result: BenchmarkTestResult | None = None

    def _get_java_files(self) -> list[str]:
        with open(self.task_file) as file:
            task_def = yaml.safe_load(file)

        task_dir = glob.escape(self.task_file.parent)
        java_files = []

        for input_path in task_def["input_files"]:
            glob_query = os.path.join(task_dir, glob.escape(input_path), "**/*.java")
            for java_file in glob.glob(glob_query, recursive=True):
                java_files.append(java_file)

        return java_files

    def _compile_java(self) -> None:
        clean_files()
        java_files = self._get_java_files()
        
        logger.info(f'compiling {len(java_files)} Java files from {self.test_name}.yml')
        os.chdir(BENCHMARKS_DIR)
        javac = subprocess.run(COMPILE_COMMAND + java_files)
        javac.check_returncode()

    def _run_jtoc(self) -> None:
        goto, symbol = capture('Main')

        functions = parse_functions(goto)
        symbols = parse_symbols(symbol)

        processor = ProgramProcessor(symbols, functions)
        processor.write_to_file('out.c')

    def _compile_c(self, c_file: Path, out_name: str) -> bool:
        if not c_file.exists():
            logger.error(f'C file not found: {c_file.absolute()}')

        os.chdir(COMPILE_DIR)
        result = subprocess.run(['gcc', '-std=c99', '-o', f'{out_name}.out', c_file.absolute()])
        if result.returncode != 0:
            logger.error(f'Error when compiling file {c_file.name}')
            return False

        return True

    def _compile_source_codes(self) -> BenchmarkTestResult | None:
        try:
            self._compile_java()
        except subprocess.CalledProcessError:
            return BenchmarkTestResult(compilation=f'[compilation fail] {self.test_name} -> *.class')

        try:
            self._run_jtoc()
        except:
            return BenchmarkTestResult(compilation=f'[compilation fail] {self.test_name} -> out.c')

        compiled_file = COMPILE_DIR / 'out.c'

        if not self._compile_c(compiled_file, 'a'):
            return BenchmarkTestResult(compilation=f'[compilation fail] {compiled_file.name} -> a.out')

        return BenchmarkTestResult()

    def test(self) -> None:
        logger.info(f'----- Test {self.task_file.parent.name}/{self.task_file.stem}')
        self.result = self._compile_source_codes()


def clean_files() -> None:
    shutil.rmtree(COMPILE_DIR)
    COMPILE_DIR.mkdir()


def load_test_cases() -> list[TestCase]:
    test_cases: list[TestCase] = []
    for task_file in glob.iglob(str(BENCHMARKS_DIR / "**/*.yml"), recursive=True):
        test_cases.append(TestCase(Path(task_file)))

    return test_cases


def process_benchmarks() -> None:
    test_cases = load_test_cases()
    categories: dict[str, list[TestCase]] = {}

    for index, test_case in enumerate(test_cases, start=1):
        logger.info(f'[{index}/{len(test_cases)}]')
        test_case.test()
        if not categories.get(test_case.category):
            categories[test_case.category] = []
        categories[test_case.category].append(test_case)
        logger.info('-----')

    for category, cases in categories.items():
        logger.info(f"{'#' * 20} SUMMARY OF {category} {'#' * 20}")
        oks, fails = 0, 0
        for case in cases:
            logger.info(f'[{case.result.short_result()}] {case.test_name}')
            if case.result._has_passed():
                oks += 1
            else:
                fails += 1
        logger.info('-----')
        logger.info(f'all tests: {len(cases)}, passed -> {oks}, failed -> {fails}')
        logger.info(f'success rate: {oks / len(cases) * 100}%')

    clean_files()


if __name__ == '__main__':
    process_benchmarks()
