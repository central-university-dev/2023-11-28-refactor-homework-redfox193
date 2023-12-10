import libcst as cst

from homework.utils import getTraceFromAttributeOrName

class BaseRenamer(cst.CSTTransformer):
    def __init__(self, access_trace: tuple[str], call_trace: tuple[str], new_name: str):
        self.access_trace = access_trace
        self.call_trace = call_trace
        self.new_name = new_name

    # renamed when called
    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.CSTNode:
        trace = getTraceFromAttributeOrName(original_node.func)
        if trace == self.call_trace:
            if isinstance(original_node.func, cst.Attribute):
                updated_node = updated_node.with_changes(func = updated_node.func.with_changes(attr = cst.Name(self.new_name)))
            else:
                updated_node = updated_node.with_changes(func = cst.Name(self.new_name))
        return updated_node

    # to prevent code duplication
    def change_name(self, original_node: cst.CSTNode, updated_node: cst.CSTNode) -> cst.CSTNode:
        if type(original_node.value) not in (cst.Name, cst.Attribute):
            return updated_node
        
        trace = getTraceFromAttributeOrName(original_node.value)
        if trace == self.call_trace:
            if isinstance(original_node.value, cst.Attribute):
                updated_node = updated_node.with_changes(value = updated_node.value.with_changes(attr = cst.Name(self.new_name)))
            else:
                updated_node = updated_node.with_changes(value = cst.Name(self.new_name))
        return updated_node

    # renamed when passed as argument
    def leave_Arg(self, original_node: cst.Arg, updated_node: cst.Arg) -> cst.CSTNode:
        return self.change_name(original_node, updated_node)
    
    # rename when returned
    def leave_Return(self, original_node: cst.Return, updated_node: cst.Return) -> cst.CSTNode:
        return self.change_name(original_node, updated_node)
    
    # rename when assigned to variable...
    def leave_Assign(self, original_node: cst.Assign, updated_node: cst.Assign) -> cst.CSTNode:
        return self.change_name(original_node, updated_node)
    
    # rename when is an element of tuple, list...
    def leave_Element(self, original_node: cst.Element, updated_node: cst.Element) -> cst.CSTNode:
        return self.change_name(original_node, updated_node)
        
    # rename in import
    def leave_Import(self, original_node: cst.Import, updated_node: cst.Import) -> cst.CSTNode:
        names = []
        for import_alias_node in original_node.names:
            trace = getTraceFromAttributeOrName(import_alias_node.name)
            if trace == self.access_trace:
                if isinstance(import_alias_node.name, cst.Attribute):
                    names.append(import_alias_node.with_changes(name = import_alias_node.name.with_changes(attr=cst.Name(self.new_name))))
                else:
                    names.append(import_alias_node.with_changes(name = cst.Name(self.new_name)))
            else:
                names.append(import_alias_node)
        return updated_node.with_changes(names=names)

    # rename in import from
    def leave_ImportFrom(self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom) -> cst.CSTNode:
        base_trace = getTraceFromAttributeOrName(original_node.module)
        names = []
        for import_alias_node in original_node.names:
            if isinstance(import_alias_node, cst.ImportAlias):
                trace = base_trace + getTraceFromAttributeOrName(import_alias_node.name)
                if trace == self.access_trace:
                    names.append(import_alias_node.with_changes(name = cst.Name(self.new_name)))
                else:
                    names.append(import_alias_node)
        return updated_node.with_changes(names=names)
