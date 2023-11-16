
import sys
import ast
import logging


def main(recipe_file: str) -> int:
    with open(recipe_file, encoding='utf-8') as file:
        recipe_lines = file.readlines()
    source = "".join(recipe_lines)

    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in ["requires", "build_requires", "tool_requires"]:
            arg = node.args[0]
            if not isinstance(arg, ast.Constant):
                logging.warning("Unable to get non constant dependency in %s:%s : `%s`", recipe_file, arg.lineno, ast.get_source_segment(source, arg))
                continue
            oldref = arg.value
            parts = oldref.split("/")
            version = parts[1]
            if version == "<host_version>":
                continue
            name = parts[0]
            print(f"{name}/{version}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
