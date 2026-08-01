  ## Notes on AI-generated Text

  Claude was used for the entirety of this assignment. Listed below are details of how I used AI, what was generated, what I verified or edited, and what I rejected outright.

  ## Generated Text

  The general outline and structure of the project (models.py / storage.py / main.py), along with first drafts of all three files.
  The Pydantic model definitions in models.py, which include the ExpenseCreate / Expense split ("input"/"stored").
  Initial FastAPI route implementations in main.py.
  A first draft of the pytest suite in tests/test_expenses.py.


  ## What I validated, tested, or changed, and why

  (1) Manually tested each API endpoint through the Swagger UI (/docs) and the command line interface. Added expenses, filtered by category, and checked the totals, both overall and for each category to ensure they were calculated correctly (e.g. two food expenses of 45.50 and 5 totaling 50.5).


  (2) Had an issue with a Windows-specific problem testing from Powershell. It turns out that the curl command in Powershell is not curl, but is really the Invoke-WebRequest commandlet, which did not handle JSON body parameters in quotes properly (Cannot bind parameter 'Headers' followed by JSON decode failure even after trying to escape quote marks). Used Invoke-RestMethod, which handles single-quoted JSON bodies properly, instead. Not sure if this was a bug in the API itself or the client command shell, but the point is that the README examples of curl on Windows failed. Hence the extra Windows powershell section added to the README documentation.


  (3) Clarified the behavior where browser and Powershell do not sync — initially I expected adding an expense via Powershell to update what I see in the open Swagger tab automatically. But no, both are just two different clients accessing the same server state, and each one will only show the current server state when the request is re-executed there. Basic knowledge, but something worth mentioning because it could be easily missed reading through the code only.


  (4) Status codes for delete endpoint verified manually: 204 when trying to delete a real id, and 404 when trying to delete it again — done explicitly since AI code may have a tendency to just return some lazy 200 response.
  Ran full pytest suite and analyzed its output rather than just looking for "passed" message — verified that all 6 tests passed and checked they really test required behaviors (add, list, filter, overall total, per category total, delete + delete-again 404).


  (5) Added setup_function() decorator to reset the store before each test runs. At first version of the tests shared the state between test functions, which made test results depend on their order (e.g., test_list_all_expenses would get expenses added by some previous test function). I requested such modification because flaky and order dependent tests are worse than having no tests at all.


  (6) Matched the required package versions with actual versions of installed packages (pip freeze). As the install instruction in README is used verbatim by grader, it would make sense to check it.

  (7) Got a genuine bug by testing on a fresh checkout. The following works fine in my development environment: python -m pytest, while pytest tests/ that is mentioned in the README failed on a fresh checkout because of ModuleNotFoundError: No module named 'src', since python -m pytest automatically includes the current directory in sys.path but not the bare pytest. Because according to the guidelines, the commands from the README will be executed as specified, I have created a pytest.ini file with pythonpath = .


## AI suggestions I did not adopt
Claude offered to persist costs to a local JSON file on disk. I opted not to do so, because the assignment stated that no database was needed, and adding file I/O would involve writing additional code that needed testing (for instance, file locking, corrupted file handling, etc.) for something not called for by the assignment.

Claude offered to implement the bonus (optional) part (search / monthly summary / Docker). I skipped this one – as FastAPI has an auto-generated Swagger documentation at the /docs endpoint, it would be free of charge, and I thought it was better to have a fully tested core rather than an unfinished bonus.