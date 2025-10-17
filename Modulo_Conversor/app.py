#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""
Módulo Conversor Poliron - Interface Web
Aplicativo Streamlit para conversão de especificações de cabos
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys
from datetime import datetime
from io import BytesIO

# Adicionar diretório de scripts ao path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from conversor_poliron import ConversorPoliron

# Configuração da página
st.set_page_config(
    page_title="Módulo Conversor Poliron",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def converter_df_para_excel(df):
    """Converte DataFrame para Excel em memória"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Conversão')
    return output.getvalue()

def main():
    """Função principal do aplicativo"""
    
    # Cabeçalho
    st.markdown('<div class="main-header">⚡ Módulo Conversor Poliron</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Conversão automática de especificações técnicas de cabos para códigos Poliron</div>', unsafe_allow_html=True)
    
    # Sidebar com informações
    with st.sidebar:
        st.header("ℹ️ Sobre o Sistema")
        st.markdown("""
        Este sistema converte automaticamente especificações técnicas de cabos elétricos 
        para o formato de códigos da marca Poliron.
        
        **Tipos de cabos suportados:**
        - ⚡ VFD (Inversor de Frequência)
        - 📊 Instrumentação
        - 🔌 Energia/Potência
        - 🎛️ Controle
        
        **Melhorias implementadas:**
        - ✅ CIL apenas quando explícito
        - ✅ Extração de cores dos condutores
        - ✅ Formato correto para instrumentação
        """)
        
        st.divider()
        
        st.header("📖 Como usar")
        st.markdown("""
        1. Carregue uma planilha Excel (.xlsx)
        2. Selecione a coluna com as descrições
        3. Clique em "Converter"
        4. Faça o download do resultado
        """)
        
        st.divider()
        
        st.markdown("**Versão:** 2.0 (Corrigida)")
        st.markdown("**Data:** Outubro 2025")
    
    # Área principal
    st.header("📁 Carregar Planilha")
    
    uploaded_file = st.file_uploader(
        "Selecione o ficheiro Excel com as especificações",
        type=['xlsx', 'xls'],
        help="Carregue uma planilha Excel contendo as especificações técnicas dos cabos"
    )
    
    if uploaded_file is not None:
        try:
            # Carregar planilha
            df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ Ficheiro carregado com sucesso! {len(df)} linhas encontradas.")
            
            # Mostrar prévia
            st.subheader("📋 Prévia dos Dados")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Selecionar coluna de descrição
            st.subheader("⚙️ Configuração")
            colunas = df.columns.tolist()
            
            coluna_descricao = st.selectbox(
                "Selecione a coluna que contém as descrições dos cabos:",
                colunas,
                index=0 if len(colunas) > 0 else None,
                help="Esta coluna deve conter as especificações técnicas completas"
            )
            
            # Opções avançadas
            with st.expander("🔧 Opções Avançadas"):
                mostrar_detalhes = st.checkbox("Mostrar detalhes da conversão", value=False)
                incluir_timestamp = st.checkbox("Incluir timestamp no nome do ficheiro", value=True)
            
            # Botão de conversão
            st.divider()
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                converter_btn = st.button(
                    "🚀 Converter Especificações",
                    type="primary",
                    use_container_width=True
                )
            
            if converter_btn:
                with st.spinner("⏳ Convertendo especificações... Por favor aguarde."):
                    # Criar conversor
                    conversor = ConversorPoliron()
                    
                    # Processar planilha
                    df_resultado = conversor.processar_planilha(df, coluna_descricao)
                    
                    # Estatísticas
                    total = len(df_resultado)
                    sucesso = len(df_resultado[~df_resultado['Referência YOFC'].str.contains('Não consegui', na=False)])
                    falhas = total - sucesso
                    taxa_sucesso = (sucesso / total * 100) if total > 0 else 0
                    
                    # Mostrar resultados
                    st.success("✅ Conversão concluída!")
                    
                    # Métricas
                    st.subheader("📊 Estatísticas da Conversão")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total de Linhas", total)
                    with col2:
                        st.metric("Convertidas", sucesso, delta=f"{taxa_sucesso:.1f}%")
                    with col3:
                        st.metric("Falhas", falhas, delta_color="inverse")
                    with col4:
                        # Contar tipos
                        vfd = len(df_resultado[df_resultado['Referência YOFC'].str.contains('VFD', na=False)])
                        inst = len(df_resultado[df_resultado['Referência YOFC'].str.match(r'^\d{3} ', na=False)])
                        st.metric("VFD + Inst.", vfd + inst)
                    
                    # Distribuição por tipo
                    if mostrar_detalhes:
                        st.subheader("📈 Distribuição por Tipo de Cabo")
                        
                        vfd_count = len(df_resultado[df_resultado['Referência YOFC'].str.contains('VFD', na=False)])
                        inst_count = len(df_resultado[df_resultado['Referência YOFC'].str.match(r'^\d{3} ', na=False)])
                        energia_count = len(df_resultado[df_resultado['Referência YOFC'].str.contains('CE ', na=False)])
                        controle_count = len(df_resultado[df_resultado['Referência YOFC'].str.contains('CM |CA ', na=False, regex=True)])
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("⚡ VFD", vfd_count)
                        with col2:
                            st.metric("📊 Instrumentação", inst_count)
                        with col3:
                            st.metric("🔌 Energia", energia_count)
                        with col4:
                            st.metric("🎛️ Controle", controle_count)
                    
                    # Mostrar resultado
                    st.subheader("📄 Resultado da Conversão")
                    st.dataframe(df_resultado, use_container_width=True)
                    
                    # Mostrar falhas se houver
                    if falhas > 0:
                        st.warning(f"⚠️ {falhas} especificação(ões) não puderam ser convertidas. Verifique os detalhes abaixo:")
                        df_falhas = df_resultado[df_resultado['Referência YOFC'].str.contains('Não consegui', na=False)]
                        st.dataframe(df_falhas[[coluna_descricao, 'Referência YOFC']], use_container_width=True)
                    
                    # Preparar download
                    st.divider()
                    st.subheader("💾 Download do Resultado")
                    
                    # Gerar nome do ficheiro
                    if incluir_timestamp:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        nome_ficheiro = f"Especificacoes_Convertidas_{timestamp}.xlsx"
                    else:
                        nome_ficheiro = "Especificacoes_Convertidas.xlsx"
                    
                    # Converter para Excel
                    excel_data = converter_df_para_excel(df_resultado)
                    
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.download_button(
                            label="📥 Download Planilha Convertida",
                            data=excel_data,
                            file_name=nome_ficheiro,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            type="primary",
                            use_container_width=True
                        )
                    
                    st.success(f"✅ Pronto para download: {nome_ficheiro}")
        
        except Exception as e:
            st.error(f"❌ Erro ao processar o ficheiro: {str(e)}")
            st.exception(e)
    
    else:
        # Instruções quando não há ficheiro carregado
        st.info("👆 Carregue uma planilha Excel para começar a conversão")
        
        st.markdown("---")
        
        # Exemplo de formato esperado
        st.subheader("📝 Formato Esperado da Planilha")
        
        exemplo_df = pd.DataFrame({
            'Descrição': [
                'CABO PARA INVERSOR DE FREQUENCIA... - 3Cx4mm2+1Cx4mm2',
                'CABO DE BAIXA TENSAO... - 1Cx70mm2',
                'CABO DE INSTRUMENTACAO... - 12Px2.5mm2'
            ]
        })
        
        st.dataframe(exemplo_df, use_container_width=True)
        
        st.markdown("""
        **Observações:**
        - A planilha deve conter uma coluna com as descrições completas dos cabos
        - A formação do cabo deve estar no final da descrição (ex: `- 3Cx4mm2+1Cx4mm2`)
        - O sistema identifica automaticamente o tipo de cabo e aplica as regras correspondentes
        """)

if __name__ == "__main__":
    main()

