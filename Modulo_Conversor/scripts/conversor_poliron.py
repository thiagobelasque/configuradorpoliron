#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""
Módulo Conversor Poliron - Versão Corrigida
Converte especificações técnicas de cabos para códigos Poliron
"""

import pandas as pd
import re
import json
from pathlib import Path
from typing import Optional, Dict, Tuple
from datetime import datetime

class ConversorPoliron:
    """Classe para converter especificações de cabos em códigos Poliron"""
    
    def __init__(self, config_dir: str = None):
        """Inicializa o conversor carregando as configurações"""
        if config_dir is None:
            config_dir = Path(__file__).parent.parent / "config"
        else:
            config_dir = Path(config_dir)
        
        # Carregar configurações
        with open(config_dir / "regras_conversao.json", 'r', encoding='utf-8') as f:
            self.regras = json.load(f)
        
        with open(config_dir / "padroes_especiais.json", 'r', encoding='utf-8') as f:
            self.padroes = json.load(f)
        
        self.secao_map = self.regras['secao_energia_controle']
        self.secao_inst_map = self.regras['secao_instrumentacao']
        self.elementos_map = self.regras['elementos_instrumentacao']
    
    def extrair_formacao(self, descricao: str) -> Optional[str]:
        """Extrai a formação do cabo da descrição"""
        patterns = [
            r'(\d+[Pp]x\s*\d+[,.]?\d*mm2)',  # 12Px2.5mm2
            r'(\d+[Tt]x\s*\d+[,.]?\d*mm2)',  # 8Tx2.5mm2
            r'(\d+[Qq]x\s*\d+[,.]?\d*mm2)',  # 4Qx1.5mm2
            r'(\d+[Cc]x\s*\d+[,.]?\d*mm2\s*\+\s*\d+[Cc]x\s*\d+[,.]?\d*mm2)',  # VFD
            r'(\d+[Cc]x\s*\d+[,.]?\d*mm2)',  # 1Cx70mm2
            r'(\d+x\s*\d+x\s*\d+[,.]?\d*mm2)',  # 4x2x1.5mm2
        ]
        
        for pattern in patterns:
            match = re.search(pattern, descricao, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def identificar_tipo_cabo(self, descricao: str, formacao: str) -> str:
        """Identifica o tipo de cabo com base na descrição e formação"""
        desc_upper = descricao.upper()
        form_upper = formacao.upper() if formacao else ""
        
        # VFD - Inversor de Frequência
        for palavra in self.padroes['palavras_chave_tipo']['vfd']:
            if palavra in desc_upper:
                return 'VFD'
        
        # Instrumentação - padrões específicos
        if re.search(r'\d+[PTQ]X', form_upper):
            return 'INSTRUMENTACAO'
        
        for palavra in self.padroes['palavras_chave_tipo']['instrumentacao']:
            if palavra in desc_upper:
                return 'INSTRUMENTACAO'
        
        # Controle vs Energia - baseado na quantidade de condutores
        match_condutores = re.search(r'(\d+)[Cc]x', form_upper)
        if match_condutores:
            qtd = int(match_condutores.group(1))
            if qtd > 5:
                return 'CONTROLE'
            else:
                return 'ENERGIA'
        
        # Verificar palavras-chave
        for palavra in self.padroes['palavras_chave_tipo']['controle']:
            if palavra in desc_upper:
                return 'CONTROLE'
        
        for palavra in self.padroes['palavras_chave_tipo']['energia']:
            if palavra in desc_upper:
                return 'ENERGIA'
        
        return 'DESCONHECIDO'
    
    def extrair_cores_condutores(self, descricao: str, qtd_condutores: int) -> str:
        """
        CORREÇÃO PROBLEMA 2: Extrai cores específicas dos condutores
        """
        desc_upper = descricao.upper()
        
        # Verificar se tem identificação de cores
        trigger = self.padroes['regras_cores_condutores']['trigger_pattern']
        if trigger not in desc_upper:
            return ""
        
        # Mapear cores baseado na quantidade de condutores
        mapeamento = self.padroes['regras_cores_condutores']['mapeamento_por_quantidade']
        qtd_str = str(qtd_condutores)
        
        if qtd_str in mapeamento:
            config = mapeamento[qtd_str]
            
            # Para 5 condutores, verificar verde e amarelo
            if qtd_condutores == 5:
                if re.search(config['pattern_verde_amarelo'], desc_upper):
                    return config['codigo']
            else:
                # Para outros, verificar padrão de cores
                if re.search(config['pattern'], desc_upper, re.IGNORECASE):
                    return config['codigo']
        
        return ""
    
    def verificar_cil(self, descricao: str) -> bool:
        """
        CORREÇÃO PROBLEMA 1: Verifica se deve adicionar CIL
        Apenas quando houver menção explícita a acabamento ou cobertura cilíndrica
        """
        desc_upper = descricao.upper()
        pattern = self.padroes['regras_cil']['pattern']
        
        return bool(re.search(pattern, desc_upper, re.IGNORECASE))
    
    def converter_vfd(self, descricao: str, formacao: str) -> str:
        """Converte especificação VFD para código Poliron"""
        try:
            # Extrair formação: 3Cx4mm2+1Cx4mm2 ou 3Cx4mm2+3Cx4mm2
            match = re.search(r'(\d+)[Cc]x\s*(\d+[,.]?\d*)mm2\s*\+\s*(\d+)[Cc]x\s*(\d+[,.]?\d*)mm2', 
                            formacao, re.IGNORECASE)
            if not match:
                return "Não consegui identificar a codificação (Formação VFD inválida)"
            
            qtd1 = int(match.group(1))
            secao1 = match.group(2).replace(',', '.')
            qtd2 = int(match.group(3))
            secao2 = match.group(4).replace(',', '.')
            
            # Determinar tipo: Concêntrico (3+1) ou Simétrico (3+3)
            if qtd1 == 3 and qtd2 == 1:
                tipo = "CONCENTRICO"
            elif qtd1 == 3 and qtd2 == 3:
                tipo = "SIMETRICO"
            else:
                return "Não consegui identificar a codificação (Formação VFD não padrão)"
            
            # Formatar seções
            secao1_fmt = secao1.replace('.', ',')
            secao2_fmt = secao2.replace('.', ',')
            
            # Isolação
            isolacao = ""
            if 'HEPR' in descricao.upper():
                isolacao = "HEPR "
            
            # Cobertura
            cobertura = ""
            if 'SHF1' in descricao.upper() or 'NAO HALOGENADO' in descricao.upper() or 'NÃO HALOGENADO' in descricao.upper() or 'LSZH' in descricao.upper():
                cobertura = "SHF1 "
            elif 'SHF2' in descricao.upper():
                cobertura = "SHF2 "
            
            # Cores dos condutores
            cores = ""
            if 'PRETO/BRANCO/AZUL' in descricao.upper() or 'PT/BR/AZ' in descricao.upper():
                cores = "(PT/BR/AZ)"
            elif 'PRETO/BRANCO/VERMELHO' in descricao.upper() or 'PT/BR/VM' in descricao.upper():
                cores = "(PT/BR/VM)"
            else:
                cores = "PT"
            
            # Montar código
            if tipo == "CONCENTRICO":
                codigo = f"VFD CONCENTRICO {isolacao}3X{secao1_fmt}MM2 + {secao2_fmt}MM2 {cobertura}{cores}".strip()
            else:  # SIMETRICO
                codigo = f"VFD SIMETRICO {isolacao}3X{secao1_fmt}MM2 + 3X{secao2_fmt}MM2 {cobertura}{cores}".strip()
            
            return codigo
            
        except Exception as e:
            return f"Não consegui identificar a codificação (Erro VFD: {str(e)})"
    
    def converter_instrumentacao(self, descricao: str, formacao: str) -> str:
        """
        CORREÇÃO PROBLEMA 3: Converte instrumentação SEM ESPAÇO entre elemento e seção
        """
        try:
            desc_upper = descricao.upper()
            
            # Extrair elemento e quantidade
            match = re.search(r'(\d+)([PTQ])x\s*(\d+[,.]?\d*)mm2', formacao, re.IGNORECASE)
            if match:
                qtd_elementos = int(match.group(1))
                tipo_elemento = match.group(2).upper()
                secao = match.group(3).replace(',', '.')
                
                # Mapear elemento
                elemento = self.elementos_map.get(tipo_elemento, '2')
                
                # Mapear seção para instrumentação
                secao_codigo = self.secao_inst_map.get(secao, secao.replace('.', ''))
                
                # Determinar blindagem
                if qtd_elementos == 1:
                    blindagem = "MA"
                else:
                    blindagem = "ITA"
                
                # Isolação (sempre PVC/E para instrumentação)
                isolacao = "PVC/E"
                
                # Cobertura
                cobertura = "ST1"
                if 'ST2' in desc_upper:
                    cobertura = "ST2"
                elif 'SHF1' in desc_upper or 'NAO HALOGENADO' in desc_upper or 'NÃO HALOGENADO' in desc_upper:
                    cobertura = "SHF1"
                
                # Cor
                cor = "PT"
                if 'VERMELHO' in desc_upper and 'COR VERMELHO' in desc_upper:
                    cor = "VM"
                elif 'CINZA' in desc_upper and 'COR CINZA' in desc_upper:
                    cor = "CZ"
                elif 'AZUL' in desc_upper and 'COR AZUL' in desc_upper:
                    cor = "AZ"
                
                # Quantidade de elementos formatada
                qtd_fmt = f"{qtd_elementos:02d}"
                
                # CORREÇÃO: SEM ESPAÇO entre elemento e seção
                codigo = f"{elemento}{secao_codigo} {blindagem} {isolacao}-{cobertura} {qtd_fmt} FR {cor}"
                
                return codigo
            
            return "Não consegui identificar a codificação (Formação de instrumentação inválida)"
            
        except Exception as e:
            return f"Não consegui identificar a codificação (Erro instrumentação: {str(e)})"
    
    def converter_energia_controle(self, descricao: str, formacao: str, tipo: str) -> str:
        """
        Converte especificação de energia ou controle
        INCLUI CORREÇÕES: CIL apenas quando necessário, cores dos condutores
        """
        try:
            desc_upper = descricao.upper()
            
            # Extrair quantidade de condutores e seção
            match = re.search(r'(\d+)[Cc]x\s*(\d+[,.]?\d*)mm2', formacao, re.IGNORECASE)
            if not match:
                return "Não consegui identificar a codificação (Formação inválida)"
            
            qtd_condutores = int(match.group(1))
            secao = match.group(2).replace(',', '.')
            
            # Mapear seção
            secao_codigo = self.secao_map.get(secao, secao.replace('.', ''))
            
            # Tipo de cabo
            if tipo == 'ENERGIA':
                tipo_cabo = "CE"
            else:  # CONTROLE
                tipo_cabo = "CM"
                if 'BLINDAGEM' in desc_upper:
                    if 'FITA' in desc_upper and 'ALUMINIO' in desc_upper:
                        tipo_cabo = "CA"
            
            # Isolação
            isolacao = "PVC/A"
            if 'XLPE' in desc_upper:
                isolacao = "XLPE"
            elif 'HEPR' in desc_upper:
                isolacao = "HEPR"
            elif 'PVC/E' in desc_upper or '105' in desc_upper:
                isolacao = "PVC/E"
            
            # Cobertura
            cobertura = "ST1"
            if 'ST2' in desc_upper:
                cobertura = "ST2"
            elif 'ST3' in desc_upper:
                cobertura = "ST3"
            elif 'SHF1' in desc_upper or 'NAO HALOGENADO' in desc_upper or 'NÃO HALOGENADO' in desc_upper or 'LSZH' in desc_upper:
                cobertura = "SHF1"
            elif 'SHF2' in desc_upper:
                cobertura = "SHF2"
            
            # Classe
            classe = "CL5"
            if 'CLASSE 2' in desc_upper:
                classe = "CL2"
            
            # Blindagem/Armação
            blindagem = ""
            if 'TRANCA' in desc_upper or 'TRANÇA' in desc_upper:
                blindagem = "B "
            elif 'FITA' in desc_upper and 'COBRE' in desc_upper and 'BLINDAGEM' in desc_upper:
                blindagem = "E "
            
            # Cor da capa
            cor = "PT"
            if 'COR VERMELHO' in desc_upper:
                cor = "VM"
            elif 'COR AZUL' in desc_upper:
                cor = "AZ"
            elif 'COR VERDE' in desc_upper:
                cor = "VD"
            elif 'COR CINZA' in desc_upper:
                cor = "CZ"
            
            # Material condutor
            material = ""
            if 'COBRE ESTANHADO' in desc_upper:
                material = " SN"
            
            # CORREÇÃO PROBLEMA 1: CIL apenas quando explícito
            cil = ""
            if self.verificar_cil(descricao):
                cil = " CIL"
            
            # CORREÇÃO PROBLEMA 2: Extrair cores dos condutores
            cores_condutores = self.extrair_cores_condutores(descricao, qtd_condutores)
            if cores_condutores:
                cores_condutores = f" {cores_condutores}"
            
            # Quantidade formatada
            qtd_fmt = f"{qtd_condutores:02d}"
            
            # Montar código
            if tipo == 'ENERGIA':
                codigo = f"{secao_codigo} CE {isolacao}/{cobertura} {qtd_fmt} {classe} {blindagem}FR {cor}"
            else:  # CONTROLE
                codigo = f"{secao_codigo} {tipo_cabo} {isolacao}/{cobertura} {qtd_fmt} {classe} {blindagem}FR {cor}"
            
            # Adicionar material, CIL e cores
            codigo += material + cil + cores_condutores
            
            return codigo.strip()
            
        except Exception as e:
            return f"Não consegui identificar a codificação (Erro energia/controle: {str(e)})"
    
    def converter_especificacao(self, descricao: str) -> str:
        """Converte uma especificação completa para código Poliron"""
        # Extrair formação
        formacao = self.extrair_formacao(descricao)
        if not formacao:
            return "Não consegui identificar a codificação (Formação não encontrada)"
        
        # Identificar tipo de cabo
        tipo = self.identificar_tipo_cabo(descricao, formacao)
        
        # Converter conforme o tipo
        if tipo == 'VFD':
            return self.converter_vfd(descricao, formacao)
        elif tipo == 'INSTRUMENTACAO':
            return self.converter_instrumentacao(descricao, formacao)
        elif tipo == 'ENERGIA':
            return self.converter_energia_controle(descricao, formacao, 'ENERGIA')
        elif tipo == 'CONTROLE':
            return self.converter_energia_controle(descricao, formacao, 'CONTROLE')
        else:
            return "Não consegui identificar a codificação (Tipo de cabo desconhecido)"
    
    def processar_planilha(self, df: pd.DataFrame, coluna_descricao: str = 'Descrição') -> pd.DataFrame:
        """Processa uma planilha completa"""
        resultados = []
        
        for idx, row in df.iterrows():
            descricao = str(row[coluna_descricao])
            codigo_poliron = self.converter_especificacao(descricao)
            resultados.append(codigo_poliron)
        
        df['Referência YOFC'] = resultados
        return df


def main():
    """Função principal para uso via linha de comando"""
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python conversor_poliron.py <arquivo_entrada.xlsx>")
        sys.exit(1)
    
    arquivo_entrada = sys.argv[1]
    
    # Carregar planilha
    df = pd.read_excel(arquivo_entrada)
    
    # Criar conversor
    conversor = ConversorPoliron()
    
    # Processar
    df_resultado = conversor.processar_planilha(df)
    
    # Salvar resultado
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_saida = f"convertido_{timestamp}.xlsx"
    df_resultado.to_excel(arquivo_saida, index=False)
    
    print(f"✅ Conversão concluída! Arquivo salvo: {arquivo_saida}")


if __name__ == "__main__":
    main()

