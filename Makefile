fmt:
	ruff format --force-exclude

lint: fmt
	-ruff check --force-exclude --fix

start: lint
	ENVIRONMENT=local uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

build: lint
	aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin xxxx.dkr.ecr.ap-southeast-1.amazonaws.com
	docker build --platform linux/amd64 -t xxxx .
	docker tag xxx:latest xxxx.dkr.ecr.ap-southeast-1.amazonaws.com/sample/xxx:latest
	docker push xx.dkr.ecr.ap-southeast-1.amazonaws.com/sample/xxx:latest

build-lambda: lint
	aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin xxxx.dkr.ecr.ap-southeast-1.amazonaws.com
	docker build --platform linux/amd64 -t xxxx-lambda . -f Dockerfile.aws.lambda
	docker tag xxxx-lambda:latest xxxx.dkr.ecr.ap-southeast-1.amazonaws.com/xxxx-lambda:latest
	docker push xxxx.dkr.ecr.ap-southeast-1.amazonaws.com/xxxx-lambda:latest

sls: build-lambda
	AWS_SDK_LOAD_CONFIG=1 sls deploy --stage dev --region ap-southeast-1

ecs: lint
	copilot deploy

clean-lambda:
	-docker stop sample-lambda
	-docker rm sample-lambda

start-lambda: lint
	docker build -t sample-lambda . -f Dockerfile.aws.lambda
	docker run -d -p 9000:8080 --name sample-lambda sample-lambda:latest 

local:
	AWS_ACCESS_KEY_ID="test" AWS_SECRET_ACCESS_KEY="test" AWS_DEFAULT_REGION="us-east-1" localstack start -d

start-docker:
	docker-compose -f deploy/docker-compose.yaml up -d --build

stop-docker:
	docker-compose -f deploy/docker-compose.yaml down --remove-orphans

stop-local:
	localstack stop

install-dev:
	. venv/bin/activate; pip install -r requirements-dev.txt

install:
	. venv/bin/activate; pip install -r requirements.txt

test: install-dev install
	. venv/bin/activate; pytest

push:
	git add . && git commit -m "update" && git push

.PHONY: lint fmt local