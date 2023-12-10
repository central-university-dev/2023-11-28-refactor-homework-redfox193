import libcst as cst
from pathlib import Path

from homework.utils import (
    AttributeVisitor, 
    getAccessTrace, 
    getTraceFromAttributeOrName, 
    create_attribute_or_name_node,
    create_import_statement_line_node
    )

# delete function from original file
class FunctionRemover(cst.CSTTransformer):
    def __init__(self, func_name: str):
        self.func_name = func_name
        self.removed_func = None

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.CSTNode:
        new_body = []
        for node in updated_node.body:
            if isinstance(node, cst.FunctionDef) and node.name.value == self.func_name:
                self.removed_func = node.deep_clone()
            else:
                new_body.append(node)
        return updated_node.with_changes(body = new_body)


class FunctionAccessModifier(cst.CSTTransformer):
    def __init__(self, old_access_trace: tuple[str], old_call_trace: tuple[str], new_access_trace: tuple[str], func_def_node: cst.FunctionDef = None):
        self.old_access_trace = old_access_trace
        self.old_call_trace = old_call_trace
        self.new_access_trace = new_access_trace
        self.new_call_trace =  new_access_trace[-2:] # how our function should be called after import in file (like a.b.foo)
        self.new_calling_node = create_attribute_or_name_node(self.new_call_trace)
        self.func_def_node = func_def_node

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.CSTNode:
        trace = getTraceFromAttributeOrName(original_node.func)
        if trace == self.old_call_trace:
            updated_node = updated_node.with_changes(func = self.new_calling_node.deep_clone())
        return updated_node

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.CSTNode:
        new_body = []
        if len(self.new_access_trace) > 1:
            new_body.append(create_import_statement_line_node(self.new_access_trace[:-1]))

        if self.func_def_node is not None:
            new_body.append(self.func_def_node)

        new_body += list(updated_node.body)
        return updated_node.with_changes(body = new_body)


def remove_function_def_from_original_file(
        path: Path, name: str, new_func_project_location: tuple[str]) -> (str, cst.FunctionDef):
    tree = cst.parse_module(path.read_text())
    func_renamer = FunctionRemover(name)
    new_tree = tree.visit(func_renamer)
    func_def_node = func_renamer.removed_func

    access_modifier = FunctionAccessModifier((name,), (name,), new_func_project_location) 
    new_tree = new_tree.visit(access_modifier)

    return (new_tree.code, func_def_node)


def add_function_def_into_file(
        path: Path, name: str, func_project_location: tuple[str], func_def_node: cst.FunctionDef) -> str:
    return modify_function_access_in_other_file(path, func_project_location, (name,), func_def_node)


def modify_function_access_in_other_file(
        path: Path, func_project_location: tuple[str], new_func_project_location: tuple[str],
        func_def_node: cst.FunctionDef = None) -> str:
    tree = cst.parse_module(path.read_text())

    attr_visitor = AttributeVisitor()
    tree.visit(attr_visitor)
    func_calling_trace = getAccessTrace(attr_visitor.traces, func_project_location)

    access_modifier = FunctionAccessModifier(func_project_location, func_calling_trace, new_func_project_location, func_def_node) 
    new_tree = tree.visit(access_modifier)

    return new_tree.code
