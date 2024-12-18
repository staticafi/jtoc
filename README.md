# JtoC

JtoC is a program used for translation of Java 8 programs to C through JBMC's GOTO program representation.

---

## Installation

1. Clone the repository and download the submodules
```bash
git clone https://github.com/staticafi/jtoc.git
cd jbmc
git submodule update --init --recursive
```
2. Then follow the instructions in the file `jbmc/COMPILING.md` and compile the `JBMC`.

3. After the compilation there should be the `JBMC` binary called `jbmc` (If you compiled the project using CMake approach, the binary should be on path `jbmc/build/bin/jbmc`). Move this binary into the folder `jbmc` as `JtoC` expects the `JBMC` binary to be on path `jbmc/jbmc`.

Now you can start using `JtoC`!

### Java benchmarks installation

You need to clone the Java benchmarks only if you want to test the `JtoC`. They are not the part of the source code.

To run the tests on the java benchmarks, you need to clone the java category benchmarks into folder `src/java_benchmarks`.

Use these commands:

```bash
git clone https://gitlab.com/sosy-lab/benchmarking/sv-benchmarks.git
mkdir java_benchmarks
mv sv-benchmarks/java/* java_benchmarks
```

## Usage

### JtoC
After cloning this repository, you can use the `JtoC` program like this:

```bash
python3 ./src/jtoc.py <path_to_class_name> [<c_file_name>]
```

- **<path_to_class_name>** is the name of the class residing in the file named `<class_name>.java`. 
`JtoC` expects this file to be in the subdirectory of `tests/`.
- **<c_file_name>** is optional name of the file into which the output of `JtoC` will be put.

### Unit tests
Use the command

```bash
python3 ./src/run_unit_tests.py
```

to run the unit tests located in `tests/` folder.

### Java benchmarks
Use the command

```bash
python3 ./src/run_benchmarks.py
```

to run the java benchmarks. You need to clone the java benchmarks into the `src/java_benchmarks` folder!


