FROM python:2.7-slim-stretch as base
FROM base as builder

RUN mkdir /code
WORKDIR /code

RUN apt-get update && \ 
     # installing basic tool chain
     apt-get -y install build-essential

COPY requirements.txt .

RUN pip install virtualenv
RUN virtualenv doubtnut-venv && chmod a+x doubtnut-venv/bin/activate

RUN /bin/bash -c 'source doubtnut-venv/bin/activate && python -m pip install pip==19.2.1'
RUN /bin/bash -c 'source doubtnut-venv/bin/activate && pip install -r requirements.txt'

###

FROM base

WORKDIR /code

RUN apt update && apt install -y wget procps && apt clean 

# Install Wkhtmltopdf 12.4 with patched Qt , since the package is not currenly updated in repository
#  and casses issues https://github.com/wkhtmltopdf/wkhtmltopdf/issues/3001#issuecomment-419520841
RUN apt-get install -y xz-utils && \
    wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
    tar xvf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
    mv wkhtmltox/bin/wkhtmlto* /usr/local/bin && \
    apt-get install -y openssl libssl-dev libxrender-dev libx11-dev libxext-dev libfontconfig1-dev libfreetype6-dev fontconfig

RUN apt-get install -y libssl1.0-dev

COPY --from=builder /code/ .
COPY . .

ENV PATH="/code/doubtnut-venv/bin:$PATH"
ENTRYPOINT ["python", "main.py"]
