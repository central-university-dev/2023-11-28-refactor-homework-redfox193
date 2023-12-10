from pathlib import Path
from homework.funcrenamer import rename_function_in_original_file, rename_function_in_other_file
from homework.classrenamer import rename_class_in_original_file, rename_class_in_other_file
from homework.funcmover import (
    remove_function_def_from_original_file,
    modify_function_access_in_other_file,
    add_function_def_into_file
)
from homework.classmover import (
    remove_class_def_from_original_file,
    modify_class_access_in_other_file,
    add_class_def_into_file
)


def test_rename_function_in_original_file():
    got = rename_function_in_original_file(
        Path('tests/fixtures/function_renaming/in_original_file/source.py'),
        'foo',
        'myfunc',
    )

    assert got == Path('tests/fixtures/function_renaming/in_original_file/expected.py').read_text()


def test_rename_function_in_other_file():
    for i in range(4):
        got = rename_function_in_other_file(
            Path(f'tests/fixtures/function_renaming/in_other_file{i}/source.py'),
            "foo", 
            ("some", "module", "foo"), 
            "myfunc"
        )

        assert got == Path(f'tests/fixtures/function_renaming/in_other_file{i}/expected.py').read_text()


def test_rename_class_in_original_file():
    got = rename_class_in_original_file(
        Path('tests/fixtures/class_renaming/in_original_file/source.py'),
        'A',
        'C',
    )

    assert got == Path('tests/fixtures/class_renaming/in_original_file/expected.py').read_text()


def test_rename_class_in_other_file():
    for i in range(4):
        got = rename_class_in_other_file(
            Path(f'tests/fixtures/class_renaming/in_other_file{i}/source.py'),
            "A", 
            ("some", "module", "A"), 
            "C"
        )

        assert got == Path(f'tests/fixtures/class_renaming/in_other_file{i}/expected.py').read_text()


def test_move_function_def_in_other_file():
    func_name = "foo"
    old_func_project_location = ("some", "module", "source", "foo")
    new_func_project_location = ("some", "module", "source1", "foo")

    function_removed_from_file, func_def_node = remove_function_def_from_original_file(
        Path('tests/fixtures/function_moving/source.py'),
        func_name,
        new_func_project_location
    )

    function_added_into_file = add_function_def_into_file(
        Path('tests/fixtures/function_moving/source1.py'),
        func_name,
        old_func_project_location,
        func_def_node
    )

    function_access_modified_other_file = modify_function_access_in_other_file(
        Path('tests/fixtures/function_moving/source2.py'),
        old_func_project_location,
        new_func_project_location
    )

    assert function_removed_from_file == Path('tests/fixtures/function_moving/expected.py').read_text()
    assert function_added_into_file == Path('tests/fixtures/function_moving/expected1.py').read_text()
    assert function_access_modified_other_file == Path('tests/fixtures/function_moving/expected2.py').read_text()


def test_move_class_def_in_other_file():
    class_name = "A"
    old_class_project_location = ("some", "module", "source", "A")
    new_class_project_location = ("some", "module", "source1", "A")

    function_removed_from_file, func_def_node = remove_class_def_from_original_file(
        Path('tests/fixtures/class_moving/source.py'),
        class_name,
        new_class_project_location
    )

    function_added_into_file = add_class_def_into_file(
        Path('tests/fixtures/class_moving/source1.py'),
        class_name,
        old_class_project_location,
        func_def_node
    )

    function_access_modified_other_file = modify_class_access_in_other_file(
        Path('tests/fixtures/class_moving/source2.py'),
        old_class_project_location,
        new_class_project_location
    )

    assert function_removed_from_file == Path('tests/fixtures/class_moving/expected.py').read_text()
    assert function_added_into_file == Path('tests/fixtures/class_moving/expected1.py').read_text()
    assert function_access_modified_other_file == Path('tests/fixtures/class_moving/expected2.py').read_text()