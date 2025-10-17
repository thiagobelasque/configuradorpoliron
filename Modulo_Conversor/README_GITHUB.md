# ⚡ Módulo Conversor Poliron

Sistema automatizado para conversão de especificações técnicas de cabos elétricos para códigos da marca Poliron.

## 🚀 Acesso ao Aplicativo

**Link do aplicativo:** [Clique aqui para acessar](https://share.streamlit.io) *(será atualizado após deploy)*

## 📋 Funcionalidades

- ⚡ Conversão automática de especificações para códigos Poliron
- 📊 Suporte para VFD, Instrumentação, Energia e Controle
- 🎯 Interface web intuitiva
- 📥 Download direto em Excel
- ✅ Validação automática dos códigos

## 🎯 Tipos de Cabos Suportados

- **VFD** - Inversores de Frequência (Concêntrico e Simétrico)
- **Instrumentação** - Pares, Ternas e Quadras
- **Energia/Potência** - Até 5 condutores
- **Controle** - Mais de 5 condutores

## 💻 Como Usar

1. Acesse o aplicativo pelo link acima
2. Carregue sua planilha Excel com as especificações
3. Selecione a coluna que contém as descrições
4. Clique em "Converter"
5. Faça o download do resultado

## 📊 Exemplo de Conversão

| Entrada | Saída |
|---------|-------|
| `3Cx4mm2+1Cx4mm2` | `VFD CONCENTRICO 3X4MM2 + 4MM2 SHF1 (PT/BR/AZ)` |
| `12Px2.5mm2` | `225 ITA PVC/E-ST1 12 FR PT` |
| `1Cx70mm2` | `70 CE HEPR/ST2 01 CL5 FR PT CIL (PT)` |

## 🛠️ Tecnologias

- Python 3.11
- Streamlit
- Pandas
- OpenPyXL

## 📄 Licença

Uso interno - Todos os direitos reservados

## 📞 Suporte

Para questões ou sugestões, entre em contacto com a equipa responsável.

---

**Versão:** 2.0 | **Última atualização:** Outubro 2025

