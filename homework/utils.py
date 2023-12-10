import libcst as cst

from typing import  Union


def create_attribute_or_name_node(trace: tuple[str]):
    if len(trace) == 1:
        return cst.Name(value=trace[0])
    elif len(trace) == 2:
        return cst.Attribute(value=cst.Name(value=trace[0]), attr=cst.Name(value=trace[1]))

    value_node = create_attribute_or_name_node(trace[:-1])
    attr_node = cst.Name(value=trace[-1])
    return cst.Attribute(value=value_node, attr=attr_node)


def create_import_statement_line_node(import_trace: tuple[str]):
    import_alias_node = cst.ImportAlias(name=create_attribute_or_name_node(import_trace))
    import_node = cst.Import(names=[import_alias_node])
    simple_statement_line_node = cst.SimpleStatementLine(body=[import_node])
    return simple_statement_line_node


class AttributeVisitor(cst.CSTVisitor):
    def __init__(self):
        self.traces = []

    def visit_Import(self, import_node: cst.Import):
        for import_alias_node in import_node.names:
            self.traces.append(getTraceFromAttributeOrName(import_alias_node.name))

    def visit_ImportFrom(self, import_node: cst.ImportFrom):
        trace = getTraceFromAttributeOrName(import_node.module)
        for import_alias_node in import_node.names:
            if isinstance(import_alias_node, cst.ImportAlias):
                self.traces.append(trace + getTraceFromAttributeOrName(import_alias_node.name))


def getTraceFromAttributeOrName(attribute_node: Union[cst.Attribute, cst.Name]) -> tuple[str]:
        if isinstance(attribute_node, cst.Name):
             return (attribute_node.value,)
        
        if isinstance(attribute_node.value, cst.Attribute):
            trace = getTraceFromAttributeOrName(attribute_node.value)
        else:
            trace = (attribute_node.value.value,)
        trace += (attribute_node.attr.value,)

        return trace


def getAccessTrace(traces: list[tuple[str]], storage_trace: tuple[str]) -> tuple[str]:
    trace = tuple()
    for tr in traces:
        possible_trace = checkAccessTrace(tr, storage_trace)
        if len(trace) == 0 or len(possible_trace) != 0 and len(trace) > len(possible_trace):
            trace = possible_trace
    return trace


def checkAccessTrace(trace: tuple[str], storage_trace: tuple[str]) -> tuple[str]:
    trace_size = len(trace)
    storage_trace_size = len(storage_trace)
    if trace[:min(trace_size, storage_trace_size)] != storage_trace[:min(trace_size, storage_trace_size)]:
        return tuple()
    else:
        return storage_trace[min(trace_size, storage_trace_size) - 1:]