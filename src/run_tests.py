import os
import shutil
import subprocess
import sys

from dataclasses import dataclass
from pathlib import Path

from jtoc import process_input
from static import logger, TEST_DIR, COMPILE_DIR


@dataclass
class TestResult:
    provided: subprocess.CompletedProcess[bytes] | None = None
    expected: subprocess.CompletedProcess[bytes] | None = None
    compilation: str | None = None

    def _has_passed(self) -> bool:
        return not self.compilation and \
           self.provided.stdout == self.expected.stdout and \
           self.provided.stderr == self.expected.stderr and \
           self.provided.returncode == self.expected.returncode

    def short_result(self) -> str:
        if self._has_passed():
            return 'OK'
        return 'FAIL'

    def print_summary(self) -> None:
        if self._has_passed():
            return

        if self.compilation:
            logger.error(self.compilation)
            return 

        if self.provided.stdout != self.expected.stdout:
            logger.error(f'stdout does not match.')
            logger.info(f'compiled: {self.provided.stdout.decode()}')
            logger.info(f'expected: {self.expected.stdout.decode()}')
        if self.provided.stderr != self.expected.stderr:
            logger.error(f'stderr does not match.')
            logger.info(f'compiled: {self.provided.stderr.decode()}')
            logger.info(f'expected: {self.expected.stderr.decode()}')
        if self.provided.returncode != self.expected.returncode:
            logger.error(f'return code does not match.')
            logger.info(f'compiled: {self.provided.returncode}')
            logger.info(f'expected: {self.expected.returncode}')


class TestCase:
    def __init__(self, java_file: str) -> None:
        self.file = java_file
        self.result: TestResult | None = None

    def _compile_java(self) -> None:
        process_input(TEST_DIR / f'{self.file}.class', COMPILE_DIR / 'out.c')

    def _compile_c(self, c_file: Path, out_name: str) -> bool:
        if not c_file.exists():
            logger.error(f'C file not found: {c_file.absolute()}')

        os.chdir(COMPILE_DIR)
        result = subprocess.run(['gcc', '-std=c99', '-o', f'{out_name}.out', c_file.absolute()])
        if result.returncode != 0:
            logger.error(f'Error when compiling file {c_file.name}')
            return False

        return True

    def _compile_source_codes(self) -> TestResult | None:
        try:
            self._compile_java()
        except RuntimeError:
            return TestResult(compilation=f'[compilation fail] {self.file} -> out.c')

        compiled_file = COMPILE_DIR / 'out.c'

        if not self._compile_c(compiled_file, 'a'):
            return TestResult(compilation=f'[compilation fail] {compiled_file.name} -> a.out')

        return None

    def _run_compiled(self) -> bool:
        c_binary = COMPILE_DIR / 'a.out'
        compiled = subprocess.run(c_binary, capture_output=True)
        c_binary.unlink()

        original = subprocess.run(['java', self.file], capture_output=True)

        return TestResult(provided=compiled, expected=original)

    def test(self) -> None:
        logger.info(f'----- Test of file {self.file}.java')

        self.result = self._compile_source_codes()

        if not self.result:
            self.result = self._run_compiled()


def clean_files() -> None:
    shutil.rmtree(COMPILE_DIR)
    COMPILE_DIR.mkdir()


def load_test_cases() -> list[TestCase]:
    files = {file.name.split('.')[0] for file in TEST_DIR.iterdir()}
    results: list[TestCase] = []

    for file in files:
        results.append(TestCase(java_file=file))

    return sorted(results, key=lambda tc: tc.file)


def test_all() -> None:
    clean_files()
    test_cases = load_test_cases()

    for test_case in test_cases:
        test_case.test()

    logger.info(f"{'#' * 20} SUMMARY {'#' * 20}")
    oks, fails = 0, 0
    for test_case in test_cases:
        logger.info(f'Test of file {test_case.file}: [{test_case.result.short_result()}]')
        test_case.result.print_summary()
        logger.info('-----')
        if test_case.result._has_passed():
            oks += 1
        else:
            fails += 1
    logger.info(f'all tests: {len(test_cases)}, passed -> {oks}, failed -> {fails}')
    logger.info(f'success rate: {oks / len(test_cases) * 100}%')

    clean_files()


def test_one(filename: str) -> None:
    root = filename.split('.')[0]
    filepath = TEST_DIR / f'{root}.java'
    if not filepath.exists():
        logger.error(f'Could not find the file {filename} on path {filepath.absolute()}')
        return

    test_case = TestCase(java_file=root)
    test_case.test()
    logger.info(f'Test of file {test_case.file}: [{test_case.result.short_result()}]')
    test_case.result.print_summary()
    logger.info('-----')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        test_one(sys.argv[1])
    else: 
        test_all()