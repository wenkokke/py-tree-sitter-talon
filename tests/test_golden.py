import typing

import pytest
import yaml

import tree_sitter_talon


def str_presenter(dumper: yaml.representer.SafeRepresenter, data: str) -> yaml.Node:
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, str_presenter)
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)


def node_dict_simplify(node_dict: dict[str, typing.Any]) -> None:
    if len(node_dict) > 4:
        del node_dict["text"]

    del node_dict["start_position"]
    del node_dict["end_position"]

    for key in node_dict.keys():
        if isinstance(node_dict[key], dict):
            node_dict_simplify(node_dict[key])
        if isinstance(node_dict[key], list):
            for val in node_dict[key]:
                if isinstance(val, dict):
                    node_dict_simplify(val)


@pytest.mark.golden_test("data/golden/*.yml")
def test_golden(golden):
    node_dict = tree_sitter_talon.parse(golden["input"]).to_dict()
    node_dict_simplify(node_dict)
    assert node_dict == golden.out["output"]
