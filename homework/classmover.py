import libcst as cst
from pathlib import Path
from homework.basemover import AccessModifier

from homework.utils import AttributeVisitor, getAccessTrace

# delete function from original file
class ClassRemover(cst.CSTTransformer):
    def __init__(self, class_name: str):
        self.class_name = class_name
        self.removed_class = None

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.CSTNode:
        new_body = []
        for node in updated_node.body:
            if isinstance(node, cst.ClassDef) and node.name.value == self.class_name:
                self.removed_class = node.deep_clone()
            else:
                new_body.append(node)
        return updated_node.with_changes(body = new_body)


def remove_class_def_from_original_file(
        path: Path, name: str, new_class_project_location: tuple[str]) -> (str, cst.FunctionDef):
    tree = cst.parse_module(path.read_text())
    print(tree)
    class_renamer = ClassRemover(name)
    new_tree = tree.visit(class_renamer)
    class_def_node = class_renamer.removed_class

    access_modifier = AccessModifier((name,), (name,), new_class_project_location) 
    new_tree = new_tree.visit(access_modifier)

    return (new_tree.code, class_def_node)


def add_class_def_into_file(
        path: Path, name: str, class_project_location: tuple[str], class_def_node: cst.FunctionDef) -> str:
    return modify_class_access_in_other_file(path, class_project_location, (name,), class_def_node)


def modify_class_access_in_other_file(
        path: Path, class_project_location: tuple[str], new_class_project_location: tuple[str],
        class_def_node: cst.FunctionDef = None) -> str:
    tree = cst.parse_module(path.read_text())

    attr_visitor = AttributeVisitor()
    tree.visit(attr_visitor)
    func_calling_trace = getAccessTrace(attr_visitor.traces, class_project_location)

    access_modifier = AccessModifier(class_project_location, func_calling_trace, new_class_project_location, class_def_node) 
    new_tree = tree.visit(access_modifier)

    return new_tree.code
