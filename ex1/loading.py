import importlib


DEPENDENCIES = {
    "pandas": "Data manipulation",
    "numpy": "Numerical computation",
    "matplotlib": "Visualization",
}


def load_modules() -> dict[str, object | None]:
    """Loads each mandatory packages dynamically"""
    modules: dict[str, object | None] = {}
    for name in DEPENDENCIES:
        try:
            modules[name] = importlib.import_module(name)
        except ImportError:
            modules[name] = None
    return modules


def check_required_modules(modules: dict[str, object | None]) -> list[str]:
    """Checks for mandatory packages and 
    returns a list with the missing ones"""
    missing: list[str] = []
    for name in ("pandas", "numpy", "matplotlib"):
        if modules[name] is None:
            missing.append(name)
    return missing


def compare_package_versions(modules: dict[str, object | None]) -> str:
    """Checks for each pacage version and returns the formatted output"""
    lines = ["Checking dependencies:"]
    for name, purpose in DEPENDENCIES.items():
        module = modules[name]
        if module is None:
            lines.append(f"[MISSING] {name} - {purpose} unavailable")
            continue
        module_version = getattr(module, "__version__", "unknown")
        lines.append(f"[OK] {name} ({module_version}) - {purpose} ready")
    return "\n".join(lines)


def installation_message(missing: list[str]) -> str | None:
    """Returns a message to guide package installation
    if at least one is missing"""
    if not missing:
        return None
    packages = " ".join(missing)
    return "\n".join([
        "Missing required dependencies.",
        "\nInstall with pip:",
        f"pip install {packages}",
        "\nOr with the provided dependency files:",
        "With pip: pip install -r requirements.txt",
        "With Poetry: poetry install",
    ])


def generate_matrix_data(
    np_module: object, size: int = 1000
) -> dict[str, object]:
    """Generates random data for time, energy and stability"""
    time = np_module.random.randint(0, 100, size=size)
    energy = np_module.random.normal(loc=50, scale=15, size=size)
    stability = np_module.random.uniform(0, 1, size=size)
    return {
        "time": time,
        "energy": energy,
        "stability": stability,
    }


def analyze_matrix_data(
    pd_module: object,
    raw_data: dict[str, object],
) -> tuple[object, dict[str, float | int]]:
    """Creates the dataframe and summary"""
    dataframe = pd_module.DataFrame(raw_data)
    dataframe["is_unstable"] = dataframe["stability"] > 0.8
    summary = {
        "rows": int(len(dataframe)),
        "mean_energy": float(dataframe["energy"].mean()),
        "max_energy": float(dataframe["energy"].max()),
        "unstable_count": int(dataframe["is_unstable"].sum()),
    }
    return dataframe, summary


def generate_visualization(
    plt_module: object,
    dataframe: object,
    output_file: str = "matrix_analysis.png",
) -> str:
    """Generates the data visualization"""
    figure, axis = plt_module.subplots(figsize=(10, 5))
    axis.scatter(dataframe["time"], dataframe["energy"])
    axis.set_title("Matrix Energy Readings")
    axis.set_xlabel("Time")
    axis.set_ylabel("Energy")
    figure.tight_layout()
    figure.savefig(output_file)
    plt_module.close(figure)
    return output_file


if __name__ == "__main__":
    print("LOADING STATUS: Loading programs...\n")

    modules = load_modules()

    print(compare_package_versions(modules))
    print("")

    missing = check_required_modules(modules)

    if missing:
        print(installation_message(missing))

    else:
        pandas_module = modules["pandas"]
        numpy_module = modules["numpy"]

        pyplot_module = importlib.import_module("matplotlib.pyplot")

        print("Analyzing Matrix data...")

        raw_data = generate_matrix_data(numpy_module, 1000)
        dataframe, summary = analyze_matrix_data(pandas_module, raw_data)

        print(f"Processing {summary['rows']} data points...")
        print("Generating visualization...")

        output_file = generate_visualization(pyplot_module, dataframe)

        print("\nAnalysis complete!")
        print(f"Results saved to: {output_file}")
