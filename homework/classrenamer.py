import libcst as cst
from pathlib import Path
from homework.baserenamer import BaseRenamer

from homework.utils import AttributeVisitor, getAccessTrace, getTraceFromAttributeOrName


class ClassRenamer(BaseRenamer):
    #class definition
    def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.CSTNode:
        if (original_node.name.value,) == self.call_trace:
            updated_node = updated_node.with_changes(name = cst.Name(self.new_name))
        return updated_node

    # rename when class in Annotation
    def leave_Annotation(self, original_node: cst.Annotation, updated_node: cst.Annotation) -> cst.CSTNode:
        if type(original_node.annotation) not in (cst.Name, cst.Attribute):
            return updated_node
        
        trace = getTraceFromAttributeOrName(original_node.annotation)
        if trace == self.call_trace:
            if isinstance(original_node.annotation, cst.Attribute):
                updated_node = updated_node.with_changes(annotation = updated_node.annotation.with_changes(attr = cst.Name(self.new_name)))
            else:
                updated_node = updated_node.with_changes(annotation = cst.Name(self.new_name))
        return updated_node
    
    # rename when class as index, ex a: Union[A, int]
    def leave_Index(self, original_node: cst.Index, updated_node: cst.Index) -> cst.CSTNode:
        return self.change_name(original_node, updated_node)

    # rename when class in bin op, ex a: A | int
    def leave_BinaryOperation(self, original_node: cst.BinaryOperation, updated_node: cst.BinaryOperation) -> cst.CSTNode:
        if type(original_node.left) in (cst.Name, cst.Attribute):
            trace = getTraceFromAttributeOrName(original_node.left)
            if trace == self.call_trace:
                if isinstance(original_node.left, cst.Attribute):
                    updated_node = updated_node.with_changes(left = updated_node.left.with_changes(attr = cst.Name(self.new_name)))
                else:
                    updated_node = updated_node.with_changes(left = cst.Name(self.new_name))
        
        if type(original_node.right) in (cst.Name, cst.Attribute):
            trace = getTraceFromAttributeOrName(original_node.right)
            if trace == self.call_trace:
                if isinstance(original_node.right, cst.Attribute):
                    updated_node = updated_node.with_changes(right = updated_node.right.with_changes(attr = cst.Name(self.new_name)))
                else:
                    updated_node = updated_node.with_changes(right = cst.Name(self.new_name))

        return updated_node


# rename class in file where it was created
def rename_class_in_original_file(path: Path, name: str, new_name: str) -> str:
    tree = cst.parse_module(path.read_text())
    class_renamer = ClassRenamer((name,), (name,),  new_name)
    new_tree = tree.visit(class_renamer)
    return new_tree.code


# rename class in other file in project
def rename_class_in_other_file(path: Path, name: str, class_project_location: tuple[str], new_name: str) -> str:
    tree = cst.parse_module(path.read_text())
    attr_visitor = AttributeVisitor()
    tree.visit(attr_visitor)
    class_calling_trace = getAccessTrace(attr_visitor.traces, class_project_location)

    class_renamer = ClassRenamer(class_project_location, class_calling_trace,  new_name)
    new_tree = tree.visit(class_renamer)
    return new_tree.code
