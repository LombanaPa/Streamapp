FROM python:3.7
LABEL maitainer "Alaska"
COPY . /streamapp
WORKDIR /streamapp
RUN pip3 install -r /streamapp/requirements.txt
ENTRYPOINT ['python3']
CMD ['streamlit run 1_🎡_Homepage.py'] 


