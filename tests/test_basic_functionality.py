"""My Calculator Test"""

import pytest
from main import calculate_and_print
from app.commands import Command, CommandHandler, MenuCommand


def test_cmd_register():
    """Testing Abstract Syntax Tree"""
    # AST() & AST.codegen() throws an error when called
    with pytest.raises(NotImplementedError):
        x = CommandHandler()
        x.register_command("test", Command())
        x.execute_command("test", [])


def test_menu(capsys):
    """Test that the Binary AST class throws an error"""
    x = MenuCommand(["1", "2", "3"])
    x.execute([])
    captured = capsys.readouterr()
    assert captured.out == "1\n2\n3\n"


def test_addition(capsys):
    """Test that the addition function works"""
    calculate_and_print(["1", "0", "add"])
    captured = capsys.readouterr()
    assert captured.out.strip() == "The result of 1 add 0 is equal to 1"


def test_subtraction(capsys):
    """Test that the subtraction function works"""
    calculate_and_print(["1", "0", "subtract"])
    captured = capsys.readouterr()
    assert captured.out.strip() == "The result of 1 subtract 0 is equal to 1"


def test_multiplication(capsys):
    """Test that the multiplication function works"""
    calculate_and_print(["1", "0", "multiply"])
    captured = capsys.readouterr()
    assert captured.out.strip() == "The result of 1 multiply 0 is equal to 0"


def test_division(capsys):
    """Test that the division function works"""
    calculate_and_print(["4", "2", "divide"])
    captured = capsys.readouterr()
    assert captured.out.strip() == "The result of 4 divide 2 is equal to 2"
