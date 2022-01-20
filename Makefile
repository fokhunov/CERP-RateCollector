.PHONY: install-deps
install-deps:
	pip3 install -r requirements.txt -t build


.PHONY: fast-build
fast-build:
	mkdir -p build/src/
	cp -r src/ build/src/
	cp app.py build/


.PHONY: build
build: install-deps fast-build


.PHONY: local-invoke
local-invoke:
	sam local invoke \
	--no-event \
	--template ./deployment/template.yml \
	--profile default \
	--env-vars lambda.env.json \
	--debug


export AWS_PROFILE=cerp_prod_aws
export AWS_DEFAULT_REGION=us-east-1
c := tj
e := staging
v :=
ll := ERROR

.PHONY: fast-deploy
fast-deploy: fast-build
	./deployment/deploy.sh $(c) $(e) $(v) $(ll)


.PHONY: deploy
deploy: build fast-deploy
