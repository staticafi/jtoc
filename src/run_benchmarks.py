import glob
import os
import shutil
import subprocess
import unittest
import yaml

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

from capture.compiling import capture, parse_functions, parse_symbols
from processing.program_processor import ProgramProcessor
from static import logger, BENCHMARKS_DIR, COMPILE_DIR


COMPILE_COMMAND = ["javac", "-source", "1.8", "-Werror", "-d", str(COMPILE_DIR.absolute())]


class Result(Enum):
    OK = 0
    JAVA_COMPILATION_FAIL = 1
    JTOC_TRANSLATION_FAIL = 2
    CLANG_COMPILATION_FAIL = 3


@dataclass
class TestResult:
    test_suite: str
    test_name: str
    java_compilation_time: timedelta
    jtoc_translation_time: timedelta
    gcc_compilation_time: timedelta
    test_time: timedelta
    result: Result

    @property
    def full_name(self) -> str:
        return f'{self.test_suite}/{self.test_name}'
    
    @property
    def get_summary_line(self) -> str:
        java = self.java_compilation_time.total_seconds()
        jtoc = self.jtoc_translation_time.total_seconds()
        gcc = self.gcc_compilation_time.total_seconds()
        total = self.test_time.total_seconds()
        return f'{self.test_name:<30} | {self.result.name:<22} | {java:<9.2f} | {jtoc:<9.2f} | {gcc:<9.2f} | {total:<9.2f}'


class TestBenchmarks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results: dict[str, list[TestResult]] = {}
        cls.task_files: list[Path] = []

        for task_file in glob.iglob(str(BENCHMARKS_DIR / "**/*.yml"), recursive=True):
            cls.task_files.append(Path(task_file))

    @classmethod
    def tearDownClass(cls):
        cls.clean_files()
        with open(COMPILE_DIR / 'test_summary.txt', 'w') as file:
            for test_suite in cls.results:
                print(f'Summary of test suite {test_suite}:', file=file)        
                print('Test Name                      | Test result            | Java [ms] | JtoC [ms] | GCC [ms] | Total ', file=file)
                sorted_results = sorted(cls.results[test_suite], key=lambda ts: ts.test_name)
                for test_result in sorted_results:
                    print(test_result.get_summary_line, file=file)

                successes = sum([int(test_result.result == Result.OK) for test_result in sorted_results])
                success_rate = successes / len(sorted_results) * 100
                total_test_time = sum([test_result.test_time.total_seconds() for test_result in sorted_results])
                print(f'Tests passed: {successes}, Tests failed: {len(sorted_results) - successes}', file=file)
                print(f'{success_rate:.2f} % success rate for this suite.', file=file)
                print(f'Total time of testing: {total_test_time:.2f} seconds', file=file)
                print(f'-----', file=file)


    @classmethod
    def clean_files(cls) -> None:
        shutil.rmtree(COMPILE_DIR)
        COMPILE_DIR.mkdir()

    def compile_java(self, task_file: Path) -> Result:
        with open(task_file) as file:
            task_def = yaml.safe_load(file)

        task_dir = glob.escape(task_file.parent)
        java_files = []

        for input_path in task_def["input_files"]:
            glob_query = os.path.join(task_dir, glob.escape(input_path), "**/*.java")
            for java_file in glob.glob(glob_query, recursive=True):
                java_files.append(java_file)

        os.chdir(BENCHMARKS_DIR)
        javac = subprocess.run(COMPILE_COMMAND + java_files)

        if javac.returncode == 0:
            return Result.OK

        return Result.JAVA_COMPILATION_FAIL        

    def run_jtoc(self) -> Result:
        try:
            goto, symbol = capture('Main')

            functions = parse_functions(goto)
            symbols = parse_symbols(symbol)

            processor = ProgramProcessor(symbols, functions)
            processor.write_to_file('out.c')
        except:
            return Result.JTOC_TRANSLATION_FAIL
        else:
            return Result.OK

    def compile_gcc(self) -> Result:
        os.chdir(COMPILE_DIR)
        c_file = COMPILE_DIR / 'out.c'
        
        result = subprocess.run(['clang', '-std=c99', '-o', f'a.out', c_file.absolute()])
        if result.returncode != 0:
            return Result.CLANG_COMPILATION_FAIL

        return Result.OK

    def run_one_benchmark(self, task_file: Path) -> TestResult:
        no_time = timedelta(seconds=0)
        test_suite = task_file.parent.stem if task_file.parent.parent.stem == 'java_benchmarks' else task_file.parent.parent.stem
        test_start = datetime.now()
        java_result = self.compile_java(task_file)
        java_end = datetime.now()

        if java_result != Result.OK:
            return TestResult(
                test_suite=test_suite,
                test_name=task_file.stem,
                java_compilation_time=java_end - test_start,
                jtoc_translation_time=no_time,
                gcc_compilation_time=no_time,
                test_time=java_end - test_start,
                result=java_result
            )
        
        jtoc_start = datetime.now()
        jtoc_result = self.run_jtoc()
        jtoc_end = datetime.now()

        if jtoc_result != Result.OK:
            return TestResult(
                test_suite=test_suite,
                test_name=task_file.stem,
                java_compilation_time=java_end - test_start,
                jtoc_translation_time=jtoc_end - jtoc_start,
                gcc_compilation_time=no_time,
                test_time=jtoc_end - test_start,
                result=jtoc_result
            )

        gcc_start = datetime.now()
        gcc_result = self.compile_gcc()
        test_end = datetime.now()

        return TestResult(
            test_suite=test_suite,
            test_name=task_file.stem,
            java_compilation_time=java_end - test_start,
            jtoc_translation_time=jtoc_end - jtoc_start,
            gcc_compilation_time=test_end - gcc_start,
            test_time=test_end - test_start,
            result=gcc_result
        )

    def test_all_benchmarks(self):
        for index, task_file in enumerate(self.task_files, start=1):
            logger.info(f'[{index}/{len(self.task_files)}]')
            self.clean_files()

            test_result = self.run_one_benchmark(task_file)

            if not self.results.get(test_result.test_suite, None):
                self.results[test_result.test_suite] = []
            self.results[test_result.test_suite].append(test_result)

            with self.subTest(task_file=task_file):
                self.assertEqual(test_result.result, Result.OK, 
                                 msg=f'Test {test_result.full_name} failed: {test_result.result.name}')
            

if __name__ == '__main__':
    unittest.main()