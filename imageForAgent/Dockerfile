FROM jenkins/inbound-agent:jdk21

USER root

# Install required packages for Docker and kubectl
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    git \
    iptables \
    iproute2 \
    bash \
    lsb-release \
    gnupg2 \
    socat \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CE
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
       > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y docker-ce docker-ce-cli containerd.io \
    && rm -rf /var/lib/apt/lists/*

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
    && rm kubectl

# Add jenkins user to docker group
RUN usermod -aG docker jenkins

# Set working directory
WORKDIR /home/jenkins

USER jenkins
