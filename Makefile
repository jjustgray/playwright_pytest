# Run all tests in parallel (2 threads) on Chromium
test:
	python -m pytest -n 2 --browser chromium --headed

# Run certain spec test-suit with logs (-v) in open browser mode (--headed) with slow execution(--slowmo 1000)
test-suit:
	pytest specs/test_contactus.py -v --headed --slowmo 1000

# Run all tests sequentially across all 3 browsers
test-all-browsers:
	python -m pytest --browser chromium --browser firefox --browser webkit

# Run smoke tests only
test-smoke:
	python -m pytest -m smoke

# Generate and open Allure report locally
report:
	allure generate allure-results --clean -o allure-report
	allure open allure-report

# Clean up allure results and temporary files
clean:
	rm -rf allure-results allure-report .pytest_cache