from deno_sandbox.utils import parse_link_header


def test_link_header():
    parsed = parse_link_header(
        '<https://api.example.com/resource?page=2>; rel="next", <https://api.example.com/resource?page=5>; rel="last"'
    )
    expected = {
        "next": "https://api.example.com/resource?page=2",
        "last": "https://api.example.com/resource?page=5",
    }
    assert parsed == expected
