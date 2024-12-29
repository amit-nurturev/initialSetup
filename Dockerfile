FROM public.ecr.aws/lambda/python:3.9

# Install the function's dependencies using file requirements.txt
# from your project folder.

# LAMBDA_TASK_ROOT is provided by AWS as an environment variable along with its image
RUN yum install -y gcc python27 python27-devel postgresql-devel
COPY requirements.txt  .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

WORKDIR ${LAMBDA_TASK_ROOT}
# Copy function code
COPY domains/new_dev_project/ ${LAMBDA_TASK_ROOT}
ADD constants ${LAMBDA_TASK_ROOT}/constants
ADD utils ${LAMBDA_TASK_ROOT}/utils
ADD infrastructure ${LAMBDA_TASK_ROOT}/infrastructure

CMD [ "db_dump_lambda_handler.handler" ]