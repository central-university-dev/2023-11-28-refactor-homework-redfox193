from homework.utils import create_attribute_or_name_node, create_import_statement_line_node, getTraceFromAttributeOrName
import libcst as cst

class AccessModifier(cst.CSTTransformer):
    def __init__(self, old_access_trace: tuple[str], old_call_trace: tuple[str], new_access_trace: tuple[str], func_def_node: cst.FunctionDef | cst.ClassDef = None):
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
