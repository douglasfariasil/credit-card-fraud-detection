from pathlib import Path


def test_business_rules_document_exists() -> None:
    assert Path("BUSINESS_RULES.md").is_file()


def test_architecture_document_exists() -> None:
    assert Path("ARCHITECTURE.md").is_file()
