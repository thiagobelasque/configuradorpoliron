# 🚀 Guia Rápido - Módulo Conversor Poliron

## Início Rápido em 3 Passos

### 1️⃣ Iniciar o Aplicativo

```bash
cd Modulo_Conversor
streamlit run app.py
```

O navegador abrirá automaticamente em `http://localhost:8501`

### 2️⃣ Carregar e Converter

1. Clique em **"Browse files"** para carregar sua planilha Excel
2. Selecione a coluna que contém as descrições dos cabos
3. Clique no botão **"🚀 Converter Especificações"**
4. Aguarde o processamento (alguns segundos)

### 3️⃣ Download do Resultado

1. Revise as estatísticas e o resultado na tela
2. Clique em **"📥 Download Planilha Convertida"**
3. Pronto! Sua planilha está convertida

---

## 📋 Formato da Planilha

Sua planilha deve ter uma coluna com descrições como estas:

```
CABO PARA INVERSOR DE FREQUENCIA... - 3Cx4mm2+1Cx4mm2
CABO DE BAIXA TENSAO... - 1Cx70mm2
CABO DE INSTRUMENTACAO... - 12Px2.5mm2
```

**Importante:** A formação do cabo (ex: `3Cx4mm2`) deve estar no final da descrição.

---

## ✅ O Que o Sistema Faz

- ⚡ Identifica automaticamente o tipo de cabo (VFD, Instrumentação, Energia, Controle)
- 🎯 Extrai a formação e todas as características técnicas
- 🔄 Converte para o código Poliron correto
- ✨ Adiciona CIL, cores e outros detalhes quando necessário
- 📊 Fornece estatísticas da conversão

---

## 🎯 Exemplos de Conversão

| Tipo | Entrada | Saída |
|------|---------|-------|
| VFD | `3Cx4mm2+1Cx4mm2` | `VFD CONCENTRICO 3X4MM2 + 4MM2 SHF1 (PT/BR/AZ)` |
| Instrumentação | `12Px2.5mm2` | `225 ITA PVC/E-ST1 12 FR PT` |
| Energia | `1Cx70mm2` | `70 CE HEPR/ST2 01 CL5 FR PT CIL (PT)` |
| Controle | `7Cx2.5mm2` | `125 CM PVC/A/ST1 07 CL5 E FR PT` |

---

## ❓ Problemas Comuns

### "Não consegui identificar a codificação"

**Solução:** Verifique se:
- A formação está no formato correto (ex: `3Cx4mm2`, não `3C x 4 mm2`)
- A formação está no final da descrição
- A descrição contém informações sobre isolação, cobertura, etc.

### Código gerado parece incorreto

**Solução:**
- Verifique se a descrição original está completa
- Compare com os exemplos no documento de especificações
- Entre em contacto para ajustes nas regras

---

## 💡 Dicas

1. **Mantenha o formato original** das descrições da planilha
2. **Não edite manualmente** as formações antes de converter
3. **Revise os resultados** antes de usar em produção
4. **Guarde as planilhas originais** como backup

---

## 📞 Precisa de Ajuda?

Consulte o **README.md** completo para:
- Documentação detalhada
- Opções avançadas
- Resolução de problemas
- Configuração personalizada

---

**Versão:** 2.0 | **Última atualização:** Outubro 2025

