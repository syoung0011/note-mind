from app.services import split_text


def main() -> None:
    assert split_text("short note", chunk_size=20, overlap=5) == ["short note"]
    assert split_text("ABCDEFGHIJKL", chunk_size=8, overlap=2) == [
        "ABCDEFGH",
        "GHIJKL",
    ]
    assert split_text("   ", chunk_size=8, overlap=2) == []
    try:
        split_text("test", chunk_size=4, overlap=4)
    except ValueError:
        pass
    else:
        raise AssertionError("overlap equal to chunk_size must be rejected")
    print("Chunking demo passed.")


if __name__ == "__main__":
    main()
