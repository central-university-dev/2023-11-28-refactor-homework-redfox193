import libcst as cst
from pathlib import Path
from homework.baserenamer import BaseRenamer

from homework.utils import AttributeVisitor, getAccessTrace

class FunctionRenamer(BaseRenamer):
    #function definition
    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef) -> cst.CSTNode:
        if (original_node.name.value,) == self.call_trace:
            updated_node = updated_node.with_changes(name = cst.Name(self.new_name))
        return updated_node


# rename function in file where it was created
def rename_function_in_original_file(path: Path, name: str, new_name: str) -> str:
    tree = cst.parse_module(path.read_text())
    func_renamer = FunctionRenamer((name,), (name,),  new_name)
    new_tree = tree.visit(func_renamer)
    return new_tree.code


# rename function in other file in project
def rename_function_in_other_file(path: Path, name: str, func_project_location: tuple[str], new_name: str) -> str:
    tree = cst.parse_module(path.read_text())

    attr_visitor = AttributeVisitor()
    tree.visit(attr_visitor)
    func_calling_trace = getAccessTrace(attr_visitor.traces, func_project_location)

    func_renamer = FunctionRenamer(func_project_location, func_calling_trace,  new_name)
    new_tree = tree.visit(func_renamer)
    return new_tree.code
