FROM ubuntu:rolling

RUN apt-get update
RUN apt-get install -y build-essential software-properties-common python3.6 python3.6-venv wget


RUN wget https://cmake.org/files/v3.8/cmake-3.8.1-Linux-x86_64.sh
RUN chmod +x ./cmake-3.8.1-Linux-x86_64.sh
RUN ./cmake-3.8.1-Linux-x86_64.sh --skip-license
RUN rm ./cmake-3.8.1-Linux-x86_64.sh

WORKDIR /opt/thinglang

ADD requirements.txt .
ADD prepare.sh .
RUN sed -i -e 's/\r$//' prepare.sh
RUN ./prepare.sh

ADD . .
RUN sed -i -e 's/\r$//' *.sh
RUN find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
RUN ./build.sh

ENV PATH="/opt/thinglang/build/thinglang/:${PATH}"

CMD ./test.sh