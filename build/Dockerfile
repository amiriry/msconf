FROM python
COPY rest_api.py test_api.py /app/
RUN pip install flask pytest
WORKDIR /app
CMD [ "python", "rest_api.py" ]
