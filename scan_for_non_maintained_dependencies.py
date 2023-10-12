
import sys
import ast
import logging


def main(recipe_file: str) -> None:
    with open(recipe_file, encoding='utf-8') as f:
        recipe_lines = f.readlines()
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
            if version.startswith("[") or version.endswith("]"):
                logging.info("Unable to get version of %s because it uses a version range", oldref)
                continue
            if version == "<host_version>":
                continue
            name = parts[0]
            print(f"{name}/{version}")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
