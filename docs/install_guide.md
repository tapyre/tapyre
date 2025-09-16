# 📦 Installation Guide

This guide will walk you through installing Ollama and running the Python script.

---

## 1️⃣ Install Ollama

Ollama is the tool used for managing and running language models.

### For Arch Linux (Pacman)

```bash
sudo pacman -S ollama
```

This uses the **pacman** package manager to install Ollama directly on Arch-based systems.

### For Debian/Ubuntu (APT)

```bash
sudo apt install curl
curl -fsSL https://ollama.com/install.sh | sh
```

* First, install `curl` if it’s not already installed.
* Then download and run the official Ollama installation script.

---

## 2️⃣ Pull Your Model

After installing Ollama, you need to download the model you want to use.

```bash
ollama pull <model-name-from-config>
```

Replace `<model-name-from-config>` with the model name defined in your project configuration, for example `llama2` or `mistral`.

---

## 3️⃣ Run the Script

Finally, start the project with:

```bash
uv run main.py
```

This runs your Python script using `uv`, which manages environments and dependencies automatically.
