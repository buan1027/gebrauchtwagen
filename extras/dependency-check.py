"""Run OWASP Dependency-Check for the Gebrauchtwagen project."""

from __future__ import annotations

import os
import subprocess  # noqa: S404
from pathlib import Path
from shutil import which
from sysconfig import get_platform

PROJECT = "gebrauchtwagen"
ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "dependency-check"
DATA_DIR = Path(
    os.environ.get("DEPENDENCY_CHECK_DATA", "C:/Zimmermann/dependency-check-data")
)
SUPPRESSION_FILE = ROOT / "extras" / "dependency-check-suppression.xml"

# Analog zum Beispielprojekt kann hier lokal ein eigener NVD API Key eingetragen
# werden. Fuer Commits bleibt der Wert leer; bevorzugt wird NVD_API_KEY.
nvd_api_key = ""


def find_dependency_check() -> Path:
    """Find dependency-check in PATH or in the course tooling directory."""
    executable = (
        "dependency-check.bat"
        if get_platform().startswith("win")
        else "dependency-check"
    )
    path_candidate = which(executable)
    if path_candidate:
        return Path(path_candidate)

    if get_platform().startswith("win"):
        return Path("C:/Zimmermann/dependency-check/bin") / executable

    return Path("Zimmermann/dependency-check/bin") / executable


def main() -> None:
    """Execute Dependency-Check with settings for this repository."""
    script = find_dependency_check()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    command = [
        str(script),
        "--project",
        PROJECT,
        "--scan",
        str(ROOT),
        "--suppression",
        str(SUPPRESSION_FILE),
        "--out",
        str(REPORT_DIR),
        "--data",
        str(DATA_DIR),
        "--format",
        "HTML",
        "--format",
        "JSON",
        "--disableArchive",
        "--disableAssembly",
        "--disableAutoconf",
        "--disableBundleAudit",
        "--disableCarthageAnalyzer",
        "--disableCentral",
        "--disableCentralCache",
        "--disableCmake",
        "--disableCocoapodsAnalyzer",
        "--disableComposer",
        "--disableCpan",
        "--disableDart",
        "--disableGolangDep",
        "--disableGolangMod",
        "--disableJar",
        "--disableMavenInstall",
        "--disableMixAudit",
        "--disableMSBuild",
        "--disableNodeAudit",
        "--disableNodeAuditCache",
        "--disableNodeJS",
        "--disableNugetconf",
        "--disableNuspec",
        "--disableOssIndex",
        "--disablePipfile",
        "--disablePnpmAudit",
        "--disableRubygems",
        "--disableSwiftPackageManagerAnalyzer",
        "--disableSwiftPackageResolvedAnalyzer",
        "--disableYarnAudit",
    ]

    effective_nvd_api_key = os.environ.get("NVD_API_KEY") or nvd_api_key
    if effective_nvd_api_key:
        command.extend(["--nvdApiKey", effective_nvd_api_key])

    result = subprocess.run(command, check=False)  # noqa: S603
    if result.returncode != 0:
        raise SystemExit(
            "OWASP Dependency-Check ist fehlgeschlagen. Details stehen in der "
            "Ausgabe oberhalb; ein eventuell gesetzter NVD_API_KEY wird nicht "
            "ausgegeben."
        )


if __name__ == "__main__":
    main()
