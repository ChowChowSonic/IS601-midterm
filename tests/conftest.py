""" Adds random testing data from faker to the test cases"""

from faker import Faker

faker = Faker()


def generate_test_data(len_data):
    """Generates tests dadta"""
    for _ in range(len_data):
        a = faker.random_number(digits=2)
        b = faker.random_number(digits=2)
        op = faker.random_element(elements=["add", "subtract", "multiply", "divide"])
        lambdas = {
            "add": lambda a, b: a + b,
            "subtract": lambda a, b: a - b,
            "multiply": lambda a, b: a * b,
            "divide": lambda a, b: a // b,
        }
        b = (
            b + 1
        )  # So it can't be zero (I'm assuming random_number can generate 0)
        # if op == "divide" and b == 0:
        # b = 1
        expected = lambdas[op](a, b)
        yield a, b, op, expected


def pytest_addoption(parser):
    """Adds an option to pytest"""
    parser.addoption(
        "--num_records",
        action="store",
        default=5,
        type=int,
        help="Number of test records to generate",
    )


def pytest_generate_tests(metafunc):
    """Generates the test/result pairs"""
    # Check if the test is expecting any of the dynamically generated fixtures
    if {"a_input", "b_input", "operation", "expected"}.intersection(
        set(metafunc.fixturenames)
    ):
        num_records = metafunc.config.getoption("num_records")
        # Adjust the parameterization to include both operation_name and
        # operation for broad compatibility. Ensure 'operation_name'
        # is used for identifying the operation in Calculator class tests
        # 'operation' (function reference) is used for Calculation class tests.
        parameters = list(generate_test_data(num_records))
        # Modify parameters to fit test functions' expectations
        modified_parameters = list(parameters)
        metafunc.parametrize("a_input,b_input,operation,expected", modified_parameters)
