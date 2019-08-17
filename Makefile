.PHONY: install-deps
install-deps:
	pip install -r requirements.txt -t ./build


.PHONY: fast-build
fast-build:
	cp -r ./src/ build/


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


export AWS_PROFILE=default
c := tj
e := staging
v :=
ll := ERROR

.PHONY: fast-deploy
fast-deploy: fast-build
	./deployment/deploy.sh $(c) $(e) $(v) $(ll)


.PHONY: deploy
deploy: build fast-deploy
