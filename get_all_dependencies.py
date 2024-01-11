
import sys
import ast
import logging


def main(recipe_file: str) -> int:  # noqa: MC0001
    with open(recipe_file, encoding='utf-8') as file:
        recipe_lines = file.readlines()
    source = "".join(recipe_lines)

    def process_require(arg: ast.AST) -> None:
        if not isinstance(arg, ast.Constant):
            logging.warning("Unable to get non constant dependency in %s:%s : `%s`", recipe_file, arg.lineno, ast.get_source_segment(source, arg))
            return
        oldref = arg.value
        parts = oldref.split("/")
        version = parts[1]
        if version == "<host_version>":
            return
        name = parts[0]
        print(f"{name}/{version}")

    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in ["requires", "build_requires", "tool_requires"]:
            process_require(node.args[0])
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if not isinstance(target, ast.Name) or target.id not in ["requires", "build_requires", "tool_requires"]:
                    continue
                if isinstance(node.value, (ast.List, ast.Tuple)):
                    for elt in node.value.elts:
                        process_require(elt)
                if isinstance(node.value, ast.Constant):
                    process_require(node.value)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
