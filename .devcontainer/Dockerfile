FROM almalinux:9

# Basic tooling
RUN dnf -y install \
        sudo \
        git \
        rpm-build \
        rpmdevtools \
        make \
        golang \
        which \
        vim \
    && dnf clean all

# Create an unprivileged user that VS Code will use
RUN useradd -m vscode && echo "vscode ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/vscode

USER vscode
WORKDIR /workspace
