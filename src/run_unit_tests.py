import os
import shutil
import subprocess
import unittest

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

from capture.compiling import capture, compile, parse_functions, parse_symbols, prepare_test_files
from processing.program_processor import ProgramProcessor
from static import TEST_DIR, logger, COMPILE_DIR


class Result(Enum):
    OK = 0
    JAVA_COMPILATION_FAIL = 1
    JTOC_TRANSLATION_FAIL = 2
    CLANG_COMPILATION_FAIL = 3
    DIFFERENT_OUTPUTS = 4


@dataclass
class TestResult:
    test_suite: str
    test_name: str
    java_compilation_time: timedelta
    jtoc_translation_time: timedelta
    gcc_compilation_time: timedelta
    execution_time: timedelta
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
        execution = self.execution_time.total_seconds()
        total = self.test_time.total_seconds()

        return f'{self.test_name:<30} | {self.result.name:<22} | {java:<9.2f} | {jtoc:<9.2f} | {gcc:<9.2f} | {execution:<10.2f} | {total:<9.2f}'


class TestBenchmarks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results: dict[str, list[TestResult]] = {}
        cls.test_files: list[Path] = []

        for test_suite in TEST_DIR.iterdir():
            for test_file in test_suite.iterdir():
                cls.test_files.append(test_file)

    @classmethod
    def tearDownClass(cls):
        cls.clean_files()
        with open(COMPILE_DIR / 'test_summary.txt', 'w') as file:
            for test_suite in cls.results:
                print(f'Summary of test suite {test_suite}:', file=file)        
                print('Test Name                      | Test result            | Java [ms] | JtoC [ms] | GCC [ms] | exec [ms] | Total ', file=file)
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

    def compile_java(self, test_file: Path) -> Result:
        classname = Path(test_file).stem

        try:
            prepare_test_files(test_file)
            compile(classname)
        except:
            return Result.JAVA_COMPILATION_FAIL
        else: 
            return Result.OK

    def run_jtoc(self, test_file: Path) -> Result:
        try:
            goto, symbol = capture(test_file.stem)

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

    def execute_test(self, test_file: Path) -> Result:
        os.chdir(COMPILE_DIR)

        c_binary = COMPILE_DIR / 'a.out'
        compiled = subprocess.run(c_binary, capture_output=True)
        original = subprocess.run(['java', test_file.stem], capture_output=True)

        with self.subTest(test_file=test_file):
            self.assertEqual(compiled.stdout, original.stdout, 
                             msg=f'stdout of {test_file.stem} does not match.')
            self.assertEqual(compiled.stderr, original.stderr, 
                             msg=f'stderr of {test_file.stem} does not match.')
            self.assertEqual(compiled.returncode, original.returncode,
                             msg=f'return code of {test_file.stem} does not match')

        if compiled.stdout != original.stdout or \
           compiled.stderr != original.stderr or \
           compiled.returncode != original.returncode:
            return Result.DIFFERENT_OUTPUTS

        return Result.OK

    def run_one_test(self, test_file: Path) -> TestResult:
        no_time = timedelta(seconds=0)
        test_suite = test_file.parent.stem
        test_start = datetime.now()
        java_result = self.compile_java(test_file)
        java_end = datetime.now()

        if java_result != Result.OK:
            return TestResult(
                test_suite=test_suite,
                test_name=test_file.stem,
                java_compilation_time=java_end - test_start,
                jtoc_translation_time=no_time,
                gcc_compilation_time=no_time,
                execution_time=no_time,
                test_time=java_end - test_start,
                result=java_result
            )
        
        jtoc_start = datetime.now()
        jtoc_result = self.run_jtoc(test_file)
        jtoc_end = datetime.now()

        if jtoc_result != Result.OK:
            return TestResult(
                test_suite=test_suite,
                test_name=test_file.stem,
                java_compilation_time=java_end - test_start,
                jtoc_translation_time=jtoc_end - jtoc_start,
                gcc_compilation_time=no_time,
                execution_time=no_time,
                test_time=jtoc_end - test_start,
                result=jtoc_result
            )

        gcc_start = datetime.now()
        gcc_result = self.compile_gcc()
        gcc_end = datetime.now()

        if gcc_result != Result.OK:
            return TestResult(
                test_suite=test_suite,
                test_name=test_file.stem,
                java_compilation_time=java_end - test_start,
                jtoc_translation_time=jtoc_end - jtoc_start,
                gcc_compilation_time=gcc_end - gcc_start,
                execution_time=no_time,
                test_time=gcc_end - test_start,
                result=gcc_result
            )
    
        exec_start = datetime.now()
        exec_result = self.execute_test(test_file)
        test_end = datetime.now()

        return TestResult(
            test_suite=test_suite,
            test_name=test_file.stem,
            java_compilation_time=java_end - test_start,
            jtoc_translation_time=jtoc_end - jtoc_start,
            gcc_compilation_time=gcc_end - gcc_start,
            execution_time=test_end - exec_start,
            test_time=test_end - test_start,
            result=exec_result
        )

    def test_all_unit_tests(self):
        for index, test_file in enumerate(self.test_files, start=1):
            logger.info(f'[{index}/{len(self.test_files)}]')
            self.clean_files()

            test_result = self.run_one_test(test_file)

            if not self.results.get(test_result.test_suite, None):
                self.results[test_result.test_suite] = []
            self.results[test_result.test_suite].append(test_result)

            with self.subTest(test_file=test_file):
                self.assertEqual(test_result.result, Result.OK, 
                                 msg=f'Test {test_result.full_name} failed: {test_result.result.name}')


if __name__ == '__main__':
    unittest.main()