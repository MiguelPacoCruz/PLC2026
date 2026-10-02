import difflib
import subprocess
from pathlib import Path
import sys

CONVERSOR = "conversor.py"
INPUTS_DIR = Path("inputs")
EXPECTED_DIR = Path("expected")
OUTPUTS_DIR = Path("test_outputs")

VERBOSE = "-v" in sys.argv


def run_test(input_file):
    """Devolve (passou: bool, detalhe: str)."""
    expected_file = EXPECTED_DIR / (input_file.stem + ".html")
    output_file = OUTPUTS_DIR / (input_file.stem + ".html")

    if not expected_file.exists():
        return False, "ficheiro esperado não encontrado"

    result = subprocess.run(
        [sys.executable, CONVERSOR, str(input_file), str(output_file)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        # só a última linha do traceback (o erro em si)
        linhas = result.stderr.strip().splitlines()
        return False, "o conversor terminou com erro: " + (linhas[-1] if linhas else "?")

    expected = expected_file.read_text(encoding="utf-8").strip()
    actual = output_file.read_text(encoding="utf-8").strip()

    if actual == expected:
        return True, ""

    if VERBOSE:
        detalhe = "\n".join(
            [f"- {l}" for l in expected.splitlines()]
            + [f"+ {l}" for l in actual.splitlines()]
        )
    else:
        diff = difflib.unified_diff(
            expected.splitlines(),
            actual.splitlines(),
            lineterm="",
            n=0,
        )
        # salta os cabeçalhos "---"/"+++" e as linhas "@@"
        detalhe = "\n".join(
            l for l in list(diff)[2:] if not l.startswith("@@")
        )
    return False, detalhe


def main():
    OUTPUTS_DIR.mkdir(exist_ok=True)
    print("Legenda: '-' linha esperada, '+' linha obtida\n")

    input_files = sorted(INPUTS_DIR.glob("*.md"))

    if not input_files:
        print("Nenhum ficheiro .md encontrado em inputs/")
        return

    passed = []
    failed = []

    for input_file in input_files:
        ok, detalhe = run_test(input_file)
        if ok:
            passed.append(input_file.name)
            print(f"✓ {input_file.name}")
        else:
            failed.append(input_file.name)
            print(f"✗ {input_file.name}")
            if detalhe:
                print("    " + detalhe.replace("\n", "\n    "))

    total = len(input_files)
    print()
    print(f"{len(passed)}/{total} testes passaram.")
    if passed:
        print("  Passaram: " + ", ".join(passed))
    if failed:
        print("  Falharam: " + ", ".join(failed))

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()