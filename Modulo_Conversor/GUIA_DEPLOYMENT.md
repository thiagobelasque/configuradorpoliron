# 🌐 Guia de Deployment - Módulo Conversor Poliron

## Como Disponibilizar o Streamlit para a Equipa

Este guia apresenta diferentes opções para compartilhar o aplicativo Streamlit com a sua equipa, desde soluções gratuitas até profissionais.

---

## 🎯 Opções de Deployment

### 📊 Comparação Rápida

| Opção | Custo | Dificuldade | Tempo Setup | Recomendado Para |
|-------|-------|-------------|-------------|------------------|
| **Streamlit Cloud** | Gratuito | ⭐ Fácil | 5-10 min | Equipes pequenas/médias |
| **Rede Local** | Gratuito | ⭐⭐ Médio | 10-15 min | Uso interno na empresa |
| **Heroku** | $7/mês | ⭐⭐ Médio | 20-30 min | Projetos pequenos |
| **AWS/Azure/GCP** | $10-50/mês | ⭐⭐⭐ Difícil | 1-2 horas | Produção profissional |
| **Docker + VPS** | $5-20/mês | ⭐⭐⭐ Difícil | 1-2 horas | Controlo total |

---

## 🚀 Opção 1: Streamlit Cloud (RECOMENDADO - Mais Fácil)

### ✅ Vantagens
- **100% Gratuito** para projetos públicos
- **Gratuito com limitações** para projetos privados
- **Zero configuração** de servidor
- **Deploy automático** via GitHub
- **HTTPS incluído**
- **Atualizações automáticas**

### 📋 Requisitos
- Conta no GitHub (gratuita)
- Conta no Streamlit Cloud (gratuita)

### 🔧 Passo a Passo

#### 1. Preparar o Projeto

Criar ficheiro `requirements.txt`:
```bash
cd Modulo_Conversor
cat > requirements.txt << 'EOF'
streamlit>=1.28.0
pandas>=2.0.0
openpyxl>=3.1.0
EOF
```

#### 2. Criar Repositório no GitHub

```bash
# Inicializar git
git init
git add .
git commit -m "Initial commit - Módulo Conversor Poliron"

# Criar repositório no GitHub (via interface web)
# Depois conectar:
git remote add origin https://github.com/SEU_USUARIO/modulo-conversor-poliron.git
git branch -M main
git push -u origin main
```

#### 3. Deploy no Streamlit Cloud

1. Acesse: https://share.streamlit.io/
2. Faça login com GitHub
3. Clique em "New app"
4. Selecione:
   - Repository: `seu-usuario/modulo-conversor-poliron`
   - Branch: `main`
   - Main file path: `app.py`
5. Clique em "Deploy"

#### 4. Compartilhar o Link

Após o deploy, você receberá um link tipo:
```
https://seu-usuario-modulo-conversor-poliron-app-xxxxx.streamlit.app
```

**Este link pode ser compartilhado com toda a equipa!**

### 🔒 Tornar Privado (Opcional)

Para projetos privados no Streamlit Cloud:
- Repositório GitHub deve ser privado
- Adicionar autenticação via Streamlit (requer plano pago)
- Ou usar secrets do Streamlit para senha simples

---

## 🏢 Opção 2: Rede Local da Empresa (Uso Interno)

### ✅ Vantagens
- **Gratuito**
- **Controlo total**
- **Dados ficam na rede interna**
- **Sem dependência de serviços externos**

### 📋 Requisitos
- Servidor ou computador sempre ligado na rede
- Acesso à rede da empresa
- Permissões de firewall

### 🔧 Passo a Passo

#### 1. Preparar Servidor

```bash
# Em um servidor Linux (Ubuntu/Debian)
sudo apt update
sudo apt install python3.11 python3-pip

# Instalar dependências
pip3 install streamlit pandas openpyxl
```

#### 2. Copiar Módulo Conversor

```bash
# Copiar via SCP ou compartilhamento de rede
scp -r Modulo_Conversor/ usuario@servidor:/home/usuario/
```

#### 3. Configurar para Rede

Criar script de inicialização `start_server.sh`:
```bash
#!/bin/bash
cd /home/usuario/Modulo_Conversor
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
```

Dar permissão:
```bash
chmod +x start_server.sh
```

#### 4. Iniciar Servidor

```bash
./start_server.sh
```

#### 5. Configurar Firewall

```bash
# Ubuntu/Debian
sudo ufw allow 8501/tcp

# Windows
# Adicionar regra no Windows Firewall para porta 8501
```

#### 6. Compartilhar com Equipa

O link será:
```
http://IP_DO_SERVIDOR:8501
```

Exemplo: `http://192.168.1.100:8501`

### 🔄 Manter Sempre Ativo

Usar `systemd` (Linux):

Criar `/etc/systemd/system/conversor-poliron.service`:
```ini
[Unit]
Description=Módulo Conversor Poliron
After=network.target

[Service]
Type=simple
User=usuario
WorkingDirectory=/home/usuario/Modulo_Conversor
ExecStart=/usr/local/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
Restart=always

[Install]
WantedBy=multi-user.target
```

Ativar:
```bash
sudo systemctl enable conversor-poliron
sudo systemctl start conversor-poliron
```

---

## ☁️ Opção 3: Heroku (Cloud Simples)

### ✅ Vantagens
- **Fácil de configurar**
- **HTTPS incluído**
- **Escalável**

### 💰 Custo
- Plano Eco: $5/mês
- Plano Basic: $7/mês

### 🔧 Passo a Passo

#### 1. Preparar Projeto

Criar `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Criar `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

#### 2. Deploy

```bash
# Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Criar app
heroku create modulo-conversor-poliron

# Deploy
git push heroku main

# Abrir
heroku open
```

---

## 🏗️ Opção 4: AWS/Azure/GCP (Produção Profissional)

### ✅ Vantagens
- **Altamente escalável**
- **Controlo total**
- **Integração com outros serviços**
- **Backup automático**

### 💰 Custo Estimado
- AWS EC2 t3.small: ~$15/mês
- Azure App Service: ~$13/mês
- Google Cloud Run: ~$10/mês (pay-per-use)

### 🔧 Exemplo: AWS EC2

#### 1. Criar Instância EC2

- Tipo: t3.small (2 vCPU, 2 GB RAM)
- SO: Ubuntu 22.04
- Security Group: Permitir porta 8501

#### 2. Configurar Servidor

```bash
# Conectar via SSH
ssh -i sua-chave.pem ubuntu@ec2-xx-xx-xx-xx.compute.amazonaws.com

# Instalar dependências
sudo apt update
sudo apt install python3.11 python3-pip nginx certbot

# Copiar projeto
scp -i sua-chave.pem -r Modulo_Conversor/ ubuntu@ec2-xx-xx-xx-xx:~/

# Instalar Python packages
pip3 install streamlit pandas openpyxl
```

#### 3. Configurar Nginx (Proxy Reverso)

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

#### 4. Configurar HTTPS com Let's Encrypt

```bash
sudo certbot --nginx -d seu-dominio.com
```

---

## 🐳 Opção 5: Docker (Portabilidade Máxima)

### ✅ Vantagens
- **Funciona em qualquer lugar**
- **Fácil de replicar**
- **Isolamento completo**

### 🔧 Implementação

#### 1. Criar Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### 2. Criar docker-compose.yml

```yaml
version: '3.8'

services:
  conversor:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./dados:/app/dados
    restart: unless-stopped
```

#### 3. Build e Run

```bash
docker-compose up -d
```

#### 4. Deploy em VPS

Qualquer VPS com Docker (DigitalOcean, Linode, Vultr):
```bash
# Copiar projeto
scp -r Modulo_Conversor/ usuario@vps:~/

# Conectar e iniciar
ssh usuario@vps
cd Modulo_Conversor
docker-compose up -d
```

---

## 🔐 Adicionar Autenticação (Qualquer Opção)

### Opção A: Senha Simples no Streamlit

Adicionar no início de `app.py`:

```python
import streamlit as st

def check_password():
    """Retorna True se o usuário inseriu a senha correta."""
    
    def password_entered():
        if st.session_state["password"] == "sua_senha_aqui":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Senha", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Senha", type="password", on_change=password_entered, key="password")
        st.error("😕 Senha incorreta")
        return False
    else:
        return True

if not check_password():
    st.stop()

# Resto do código...
```

### Opção B: Autenticação OAuth (Google, Microsoft)

Usar biblioteca `streamlit-authenticator`:
```bash
pip install streamlit-authenticator
```

---

## 📊 Recomendação por Cenário

### Cenário 1: Equipe Pequena (2-10 pessoas)
**Recomendação:** Streamlit Cloud (Gratuito)
- Fácil de configurar
- Sem custos
- Link compartilhável

### Cenário 2: Uso Interno na Empresa
**Recomendação:** Rede Local
- Dados ficam internos
- Sem custos de cloud
- Controlo total

### Cenário 3: Clientes Externos
**Recomendação:** AWS/Azure + HTTPS + Autenticação
- Profissional
- Seguro
- Escalável

### Cenário 4: Teste/Desenvolvimento
**Recomendação:** Docker Local
- Rápido para testar
- Fácil de replicar
- Sem custos

---

## 🆘 Suporte e Troubleshooting

### Problema: "Connection refused"
**Solução:** Verificar firewall e porta 8501 aberta

### Problema: "App muito lento"
**Solução:** Aumentar recursos do servidor (RAM/CPU)

### Problema: "Não consigo acessar de fora"
**Solução:** Configurar port forwarding no router ou usar cloud

### Problema: "Preciso de HTTPS"
**Solução:** Usar Nginx + Let's Encrypt ou Streamlit Cloud

---

## 📞 Próximos Passos

1. **Escolher a opção** mais adequada ao seu cenário
2. **Seguir o passo a passo** correspondente
3. **Testar com a equipa** antes de usar em produção
4. **Configurar backups** dos dados
5. **Monitorar uso** e performance

---

**Precisa de ajuda com alguma opção específica? Posso detalhar qualquer um destes métodos!**

