FROM debian

#set noninteractive timezone to german
ENV DEBIAN_FRONTEND noninteractive
ENV TZ "Europe/Berlin"
RUN echo "Europe/Berlin" | tee /etc/timezone

# streamlit-specific commands for config
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'

RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'

# exposing default port for streamlit
EXPOSE 8501

#Install git
RUN apt-get update && apt-get install -y\
    git\
    python\

#Set working directory
WORKDIR /var/lib
#clone git
RUN git clone https://github.com/kkranenberg/bdcp.git

#Set working directory
WORKDIR /var/lib/bdcp

# install pip then packages
RUN pip3 install -r requirements.txt

#download acled
RUN python acled-dl.py
# cmd to launch app when container is run
CMD streamlit run streamlit_bdcp.py
