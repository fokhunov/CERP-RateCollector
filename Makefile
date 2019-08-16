install-deps:
	pip install -r requirements.txt -t ./build


fast-build:
	cp -r ./src/ build/


build: install-deps fast-build


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

fast-deploy: fast-build
	./deployment/deploy.sh $(c) $(e) $(v) $(ll)


deploy: build fast-deploy
