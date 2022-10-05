FROM python:3
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD rpc_server.py /
CMD [ "python", "./rpc_server.py" ]