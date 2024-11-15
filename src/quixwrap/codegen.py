import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional

import yaml
from jinja2 import Template


@dataclass
class VariableInfo:
    name: str
    required: bool
    type: str
    default: Optional[Any]


def readfile(name):
    with open(Path(__file__).parent / name, mode="r", encoding="utf-8") as f:
        return f.read()


@dataclass
class DeploymentInfo:
    name: str
    variables: List[VariableInfo]

    @classmethod
    def from_dict(cls, deployment: dict) -> "DeploymentInfo":
        variables = []
        for item in deployment["variables"]:
            v = VariableInfo(
                name=item["name"],
                required=item.get("required"),
                type=item.get("inputType"),
                default=item.get("value"),
            )
            variables.append(v)
        return cls(deployment["name"], variables)


class Deployment:
    __template__ = "deployment.jinja2"
    __basepy__ = "base.py"

    def __init__(self, info: DeploymentInfo):
        self.info = info

    def title(self):
        return self.info.name.title().replace("-", "").replace("_", "")

    def as_py(self, standalone=True):
        template_str = readfile(Deployment.__template__)
        basecode = (
            readfile(Deployment.__basepy__)
            if standalone
            else "from quixwrap import DeploymentWrapper, Config, Variable"
        )
        return Template(template_str).render(
            title=self.title(),
            variables=self.info.variables,
            basecode=basecode,
        )


class QuixYaml:
    def __init__(
        self,
        filepath: os.PathLike,
        local_variables_path: os.PathLike = ".quix.yaml.variables",
    ):
        self.path = os.path.normpath(os.path.abspath(filepath))
        self.conf: dict = {}

        self.local_variables_path = local_variables_path

        self.variables = {}
        # build variable replacement mapping from local variables file
        if os.path.exists(self.local_variables_path):
            with open(self.local_variables_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = [line for line in content.splitlines() if line]
                for line in lines:
                    items = line.strip().split("=")
                    key, val = tuple(items)
                    self.variables[key] = val
        else:
            with open(self.path, "r", encoding="utf-8") as f:
                content = f.read()
                if len(re.findall(r"\{\{([A-Z]+)\}\}", content)) > 0:
                    raise FileNotFoundError(
                        "Placeholder variables detected, but Local variables yaml not found."
                    )

    def read(self):
        if not self.conf:
            with open(self.path, "r", encoding="utf-8") as f:
                content = f.read()
                # replace config file placeholders with values
                # from local variables yaml
                for k, v in self.variables.items():
                    content = content.replace("{{" + k + "}}", v)
                self.conf = yaml.safe_load(content)

    def deployments(self, skip_non_existing=False) -> List[Optional[DeploymentInfo]]:
        items = []
        self.read()
        for deployment in self.conf.get("deployments", []):
            if skip_non_existing:
                if os.path.exists(
                    str(Path(__file__).parent / deployment["application"])
                ):
                    items.append(DeploymentInfo.from_dict(deployment))
            else:
                items.append(DeploymentInfo.from_dict(deployment))
        return items

    def deployment(self, name) -> Optional[DeploymentInfo]:
        for app in self.deployments():
            if app.name == name:
                return app


class QuixWrap:

    def __init__(self, config_file, yaml_variables_file):
        self.quixyaml = QuixYaml(config_file, yaml_variables_file)

    def deployment(self, name) -> Optional[Deployment]:
        return self.deployments(name)[0]

    def deployments(self, name: str = None) -> List[Deployment]:
        items = (
            [self.quixyaml.deployment(name)] if name else self.quixyaml.deployments()
        )
        return [Deployment(item) for item in items]
