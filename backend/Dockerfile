FROM public.ecr.aws/lambda/python:3.11 AS builder

# Add system install dependencies here

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "/app" -U --no-cache-dir

FROM public.ecr.aws/lambda/python:3.11

# Copy from the builder stage
COPY --from=builder /app ${LAMBDA_TASK_ROOT}

# Copy function code
COPY ./src ${LAMBDA_TASK_ROOT}

CMD ["cheap.main.handler" ]
