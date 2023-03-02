install:
	@echo "Installing pip package bcrypt..."
	pip3 install bcrypt
	@echo "Installing branchlog..."
	cd branchlog && python3 setup.py bdist_wheel && python3 -m pip install dist/branchlog-1.0-py3-none-any.whl --force-reinstall
	@echo "Installing branchweb..."
	cd branchweb && python3 setup.py bdist_wheel && python3 -m pip install dist/branchweb-1.0-py3-none-any.whl --force-reinstall

	@echo "Installing opensky-st-api"
	mkdir -p /opt/opensky-st-api
	cp -R src/ /opt/opensky-st-api
	cp opensky-st-api /usr/bin/
	chmod +x /usr/bin/opensky-st-api
	@echo "Done!"
