# Unittests and Integration Tests

This project focuses on writing unit tests and integration tests in Python. The goal is to learn how to test small pieces of logic in isolation and how to test full code paths end-to-end. You will work with the `unittest` framework, use `parameterized` for cleaner tests, and apply the `mock` library to simulate external dependencies such as network and database calls.

Unit tests ensure that a single function works exactly as expected under different inputs. They help you confirm that the logic inside a function is correct when everything around it behaves normally. Integration tests check how different components of the program interact together when running through a full workflow.

All tests in this project follow Python’s `unittest` style guide and are executed using:

```bash
python3 -m unittest

