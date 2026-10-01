import subprocess
from pathlib import Path
import sys

INPUTS_DIR = Path("inputs")
EXPECTED_DIR = Path("expected")
OUTPUTS_DIR = Path("test_outputs")


def run_test(input_file):
    expected_file = EXPECTED_DIR / (input_file.stem + ".html")
    output_file = OUTPUTS_DIR / (input_file.stem + ".html")

    if not expected_file.exists():
        print(f"Erro: {input_file.name}: ficheiro esperado não encontrado")
        return False

    # Executa o conversor
    result = subprocess.run(
        [sys.executable, "conversor.py", str(input_file), str(output_file)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Erro: {input_file.name}: o conversor terminou com erro")
        print(result.stderr)
        return False

    # Lê os resultados
    expected = expected_file.read_text(encoding="utf-8").strip()
    actual = output_file.read_text(encoding="utf-8").strip()

    # Compara
    if actual == expected:
        print(f"Exito: {input_file.name}")
        return True

    print(f"Erro: {input_file.name}: resultado diferente do esperado")

    print("\n--- Esperado ---")
    print(expected)

    print("\n--- Obtido ---")
    print(actual)

    return False


def main():
    OUTPUTS_DIR.mkdir(exist_ok=True)

    input_files = sorted(INPUTS_DIR.glob("*.md"))

    if not input_files:
        print("Nenhum ficheiro .md encontrado em inputs/")
        return

    passed = 0

    for input_file in input_files:
        if run_test(input_file):
            passed += 1

    total = len(input_files)

    print()
    print(f"{passed}/{total} testes passaram.")

    if passed != total:
        sys.exit(1)


if __name__ == "__main__":
    main()