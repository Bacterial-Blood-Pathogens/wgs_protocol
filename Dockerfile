# Use an official Ubuntu image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    sudo \
    git \
    python3-pip \
    && apt-get clean

# Download and install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda && \
    rm Miniconda3-latest-Linux-x86_64.sh

# Add Conda to PATH
ENV PATH="/opt/miniconda/bin:$PATH"

# Install Conda environments
RUN conda install -y conda && \
    conda create -y -n trim_galore -c conda-forge -c bioconda trim-galore=0.6.6 && \
    conda create -y -n shovill -c conda-forge -c bioconda -c defaults shovill=1.1.0 && \
    conda create -y -n prokka -c conda-forge -c bioconda -c defaults prokka=1.14.6 && \
    conda create -y -n mlst -c conda-forge -c bioconda -c defaults mlst==2.23.0 && \
    conda create -y -n spatyper && \
    conda run -n spatyper pip install spaTyper==0.3.3 && \
    conda create -y -n agrvate -c bioconda agrvate=1.0.1 && \
    conda create -y -n abricate -c conda-forge -c bioconda -c defaults abricate=1.0.1 && \
    conda create -y -n resfinder python=3.12 && \
    conda run -n resfinder pip install resfinder==4.5.0 && \
    conda create -y -n mob_suite -c bioconda -c conda-forge mob_suite=3.1.9 && \
    conda run -n mob_suite mob_init && \
    conda create -y -n phispy -c bioconda -c conda-forge phispy=4.2.21

# Clone ResFinder databases
RUN mkdir /opt/resfinder && \
    cd /opt/resfinder && \
    git clone https://bitbucket.org/genomicepidemiology/resfinder_db/ && \
    git clone https://bitbucket.org/genomicepidemiology/pointfinder_db/ && \
    git clone https://bitbucket.org/genomicepidemiology/disinfinder_db/

# Set default command
CMD ["/bin/bash"]
