# Use a base image
FROM python:3.11.8-slim-bullseye

# Set the working directory

# Install Vim
RUN apt-get update && apt-get install -y vim libopenblas-dev ninja-build build-essential pkg-config git

# Copy the app.py file to the working directory
COPY app /app

# RUN mkdir /app/model_weight
# RUN mkdir /llama
# RUN mkdir /llama/models
# RUN mkdir /llama/models/model_weight

WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .


# Install any dependencies
RUN pip install -r requirements.txt
ENV CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS -DCMAKE_C_FLAGS='-pthread' -DCMAKE_CXX_FLAGS='-pthread' -DCMAKE_EXE_LINKER_FLAGS='-lpthread'"
ENV LDFLAGS="-lpthread"
RUN pip install --upgrade pip && pip install llama_cpp_python --verbose

# Set the command to run the app.py file
CMD ["python", "app.py"]

