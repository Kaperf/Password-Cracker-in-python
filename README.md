# Python Password Cracker

An educational command-line password-cracking project written in Python.

The application demonstrates how password hashes can be tested using several recovery techniques:

* dictionary attacks,
* brute-force attacks,
* mask attacks,
* rainbow tables.

The project was created to practise object-oriented programming, generators, file handling, command-line interfaces, hashing algorithms and basic cryptographic concepts in Python.

> **Warning**
>
> This project is intended exclusively for educational purposes and authorized security testing.
> Use it only with hashes and systems that you own or have explicit permission to test.

---

## Features

### Dictionary attack

The program reads passwords from a wordlist without loading the entire file into memory.

Optional mutations include:

* capitalization,
* uppercase conversion,
* common numeric suffixes,
* common symbol suffixes,
* basic leetspeak substitutions.

Examples of generated variants:

```text
password
Password
PASSWORD
password1
password123
p@ssword
```

### Brute-force attack

The brute-force mode generates every possible password using:

* a configurable character set,
* a minimum password length,
* a maximum password length.

The implementation also contains methods for:

* calculating the total keyspace,
* converting an index into a password,
* converting a password into its corresponding index.

These methods can later be used for checkpointing and dividing the keyspace between multiple processes.

### Mask attack

Mask mode allows the user to describe the expected structure of a password.

Supported mask tokens:

| Token | Meaning                 |
| ----- | ----------------------- |
| `?u`  | Uppercase letter        |
| `?l`  | Lowercase letter        |
| `?d`  | Digit                   |
| `?s`  | Special character       |
| `?a`  | Any supported character |

Example mask:

```text
?u?l?l?l?d?d
```

This mask generates passwords containing:

1. one uppercase letter,
2. three lowercase letters,
3. two digits.

Literal characters can also be used:

```text
Admin?d?d
```

This generates candidates such as:

```text
Admin00
Admin01
Admin02
...
Admin99
```

### Rainbow tables

The project includes an educational implementation of rainbow tables.

It supports:

* generating password chains,
* reducing hashes back into password candidates,
* storing chain endpoints,
* saving tables in JSON format,
* loading previously generated tables,
* reconstructing chains,
* searching for a password using a target hash.

Each rainbow table stores metadata describing:

* the hashing algorithm,
* the character set,
* the password length,
* the chain length.

The metadata must match the attack configuration.

### Supported hashing algorithms

* MD5
* SHA-1
* SHA-224
* SHA-256
* SHA-384
* SHA-512
* SHA3-224
* SHA3-256
* SHA3-384
* SHA3-512

### Salt support

The application supports an optional salt placed:

* before the password,
* after the password.

Examples:

```text
salt + password
```

```text
password + salt
```

### Attack statistics

The application records:

* number of tested candidates,
* elapsed time,
* current candidate,
* calculated hash rate,
* estimated progress when the keyspace is known,
* estimated remaining time.

A configurable time limit can be used to stop an attack automatically.

---

## Project status

The project is currently a **work in progress**.

The main attack algorithms and object-oriented architecture have been implemented. Some parts still require additional testing, refactoring and integration.

Parallel processing is not currently available in the working attack modes.

An experimental `ParallelAttackManager` using Python's `multiprocessing` module was started, but integrating it correctly with:

* shared stop events,
* process-safe statistics,
* task distribution,
* result queues,
* graceful process termination

proved more complex than expected. For this reason, parallel execution was postponed and remains an important TODO item.

---

## Requirements

* Python 3.10 or newer
* No external Python packages are required

The project uses only modules from the Python standard library, including:

* `argparse`,
* `hashlib`,
* `itertools`,
* `multiprocessing`,
* `pathlib`,
* `secrets`,
* `json`,
* `time`.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Kaperf/Password-Cracker-in-python.git
```

Enter the project directory:

```bash
cd Password-Cracker-in-python
```

Display the available arguments:

```bash
python main.py --help
```

On some systems, the command may be:

```bash
python3 main.py --help
```

---

## Usage

General command structure:

```bash
python main.py \
    --hash <TARGET_HASH> \
    --algorithm <ALGORITHM> \
    --mode <ATTACK_MODE> \
    [OPTIONS]
```

Available attack modes:

```text
dictionary
bruteforce
mask
rainbow
```

---

## Dictionary attack example

Create or obtain a wordlist containing candidate passwords.

Run the dictionary attack:

```bash
python main.py \
    --hash 25f43b1486ad95a1398e3eeb3d83bc4010015fcc9bedb35b432e00298d5021f7 \
    --algorithm sha256 \
    --mode dictionary \
    --wordlist ./wordlist.txt
```

Enable mutations and leetspeak substitutions:

```bash
python main.py \
    --hash 25f43b1486ad95a1398e3eeb3d83bc4010015fcc9bedb35b432e00298d5021f7 \
    --algorithm sha256 \
    --mode dictionary \
    --wordlist ./wordlist.txt \
    --mutations
```

The example hash represents a test password created for demonstration purposes.

---

## Brute-force attack example

The following command searches for lowercase passwords between one and three characters long:

```bash
python main.py \
    --hash 77af778b51abd4a3c51c5ddd97204a9c3ae614ebccb75a606c3b6865aed6744e \
    --algorithm sha256 \
    --mode bruteforce \
    --charset abcdefghijklmnopqrstuvwxyz \
    --min-length 1 \
    --max-length 3
```

The example target password is:

```text
cat
```

A smaller character set can be used for faster testing:

```bash
python main.py \
    --hash ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad \
    --algorithm sha256 \
    --mode bruteforce \
    --charset abc \
    --min-length 1 \
    --max-length 3
```

---

## Mask attack example

Search for a password containing one uppercase letter, three lowercase letters and two digits:

```bash
python main.py \
    --hash 176344d4b7feeec6e6cdc05ac78b35496367bb0620d2b24292dd7c26cda6e550 \
    --algorithm sha256 \
    --mode mask \
    --mask "?u?l?l?l?d?d"
```

The example target password is:

```text
Test12
```

Quotes around the mask are recommended because some shells interpret special characters.

---

## Salt example

Test a hash created from:

```text
password + salt
```

```bash
python main.py \
    --hash <TARGET_HASH> \
    --algorithm sha256 \
    --mode dictionary \
    --wordlist ./wordlist.txt \
    --salt example-salt \
    --salt-position after
```

For:

```text
salt + password
```

use:

```bash
--salt-position before
```

---

## Rainbow table example

Generate the included test table:

```bash
python generate_test_table.py
```

The script:

1. creates a small SHA-256 rainbow table,
2. saves it as `test_rainbow_table.json`,
3. prints a test password and hash,
4. prints the beginning and endpoint of the generated chain.

Use the printed hash in rainbow-table mode:

```bash
python main.py \
    --hash <HASH_PRINTED_BY_THE_GENERATOR> \
    --algorithm sha256 \
    --mode rainbow \
    --rainbow-table test_rainbow_table.json \
    --charset abc
```

The character set must match the metadata stored in the rainbow table.

---

## Command-line arguments

| Argument          | Description                                     |
| ----------------- | ----------------------------------------------- |
| `--hash`          | Target password hash                            |
| `--algorithm`     | Hashing algorithm                               |
| `--mode`          | Selected attack mode                            |
| `--wordlist`      | Path to a dictionary file                       |
| `--charset`       | Characters used in brute-force mode             |
| `--min-length`    | Minimum candidate length                        |
| `--max-length`    | Maximum candidate length                        |
| `--mask`          | Password structure used in mask mode            |
| `--mutations`     | Enables dictionary mutations                    |
| `--salt`          | Optional salt                                   |
| `--salt-position` | Places the salt before or after the password    |
| `--time-limit`    | Maximum attack duration in seconds              |
| `--rainbow-table` | Path to a saved rainbow-table file              |
| `--processes`     | Reserved for future parallel-processing support |

---

## Example output

```text
Password has been found: cat
Attack mode: bruteforce
Attempts: 2074
Elapsed time: 0.01 seconds
Hash rate: 207400.00 hashes/second
```

The execution time and hash rate depend on the computer, Python version, selected algorithm and candidate space.

---

## Architecture

The application uses a modular object-oriented structure.

| Component               | Responsibility                                |
| ----------------------- | --------------------------------------------- |
| `CrackTarget`           | Stores and validates the target hash          |
| `Crackoptions`          | Stores and validates attack configuration     |
| `PasswordHasher`        | Generates password hashes                     |
| `CandidateTester`       | Tests individual password candidates          |
| `ProgressStats`         | Tracks attempts, time and progress            |
| `CrackResult`           | Stores and formats the final result           |
| `BaseAttack`            | Defines the common interface for attacks      |
| `DictionaryAttack`      | Performs dictionary attacks                   |
| `BruteForce`            | Performs brute-force attacks                  |
| `MaskAttack`            | Generates candidates from masks               |
| `ReductionFunction`     | Converts hashes into rainbow-chain candidates |
| `RainbowChain`          | Generates and reconstructs individual chains  |
| `RainbowTable`          | Stores and loads rainbow-table data           |
| `RainbowTableGenerator` | Creates rainbow tables                        |
| `RainbowTableAttack`    | Searches a rainbow table                      |
| `PasswordCracker`       | Selects and starts the requested attack       |
| `CLIParser`             | Parses command-line arguments                 |
| `ParallelAttackManager` | Experimental multiprocessing manager          |

---

## Simplified program flow

```text
CLIParser
    |
    v
CrackTarget + Crackoptions
    |
    v
PasswordCracker
    |
    v
PasswordHasher + CandidateTester
    |
    v
Selected attack implementation
    |
    v
CrackResult
```

---

## Educational goals

This project demonstrates:

* object-oriented programming,
* inheritance and abstract classes,
* type annotations,
* Python generators,
* Cartesian products,
* command-line argument parsing,
* file streaming,
* JSON serialization,
* password hashing,
* validation and error handling,
* basic performance measurements,
* rainbow-table concepts,
* initial experimentation with multiprocessing.

---

## Limitations

* The program is written in pure Python and is not optimized for high-performance cracking.
* Parallel execution has not been completed.
* Rainbow tables work only with the exact algorithm, character set, password length and reduction function used during generation.
* Rainbow tables are not suitable for hashes protected with unique salts.
* The project does not support modern password-storage algorithms such as Argon2, bcrypt or scrypt.
* The project should not be treated as a replacement for professional auditing tools.
* Some modules still require additional automated testing and refactoring.

---

## TODO

* [ ] Integrate `ParallelAttackManager` with brute-force attacks.
* [ ] Add multiprocessing support to dictionary and mask attacks.
* [ ] Implement process-safe progress statistics.
* [ ] Add checkpoint and resume support for brute-force attacks.
* [ ] Add automated unit tests.
* [ ] Add integration tests for the command-line interface.
* [ ] Add benchmark results for different hashing algorithms.
* [ ] Improve exception handling and user-facing error messages.
* [ ] Refactor module and class names to follow consistent Python naming conventions.
* [ ] Move the project into a Python package structure.
* [ ] Add continuous integration with GitHub Actions.

### Parallel programming TODO

Parallel programming was attempted using Python's `multiprocessing` module.

A preliminary process manager was created, but the complete integration was postponed because correctly synchronizing workers, stopping all processes after finding a password and collecting shared statistics introduced additional complexity.

The current implementation therefore uses a single process. Finishing and integrating parallel execution is planned as a future improvement.

---

## Possible future improvements

* benchmark comparison between Python and C implementations,
* configurable mutation rules,
* user-defined mask character sets,
* rainbow-table duplicate and collision statistics,
* binary rainbow-table storage,
* progress display refreshed during an attack,
* exportable JSON or CSV attack reports,
* pause and resume functionality,
* configuration files,
* more extensive documentation.

---

## Author

Created by **Kaperf** as an educational Python and cybersecurity portfolio project.
