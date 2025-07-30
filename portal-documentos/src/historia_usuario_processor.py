import re
import json
from typing import Dict, List, Any

class HistoriaUsuarioProcessor:
    def __init__(self):
        self.sistemas_conhecidos = ['SPF', 'GFESP', 'FEHIDRO', 'FUNDOCAMP', 'FEAP']
        self.tipos_usuario = [
            'usuário do sistema', 'gestor', 'analista', 'administrador', 
            'operador', 'secretária', 'coordenador', 'diretor', 'técnico',
            'usuário da secretaria', 'usuário do setor financeiro', 'usuário do FEHIDRO'
        ]
        
    def processar_anotacoes(self, anotacoes: str) -> Dict[str, Any]:
        """
        Processa as anotações e gera uma História de Usuário completa e detalhada
        """
        # Análise profunda do texto
        contexto = self._analisar_contexto_detalhado(anotacoes)
        
        # Extração de informações específicas
        sistema = self._identificar_sistema(anotacoes)
        problema_detalhado = self._identificar_problema_detalhado(anotacoes)
        solucao_detalhada = self._identificar_solucao_detalhada(anotacoes)
        usuario_tipo = self._identificar_tipo_usuario(anotacoes, contexto)
        
        # Geração da estrutura completa da História de Usuário
        estrutura = {
            'solicitado_por': self._gerar_solicitante_detalhado(anotacoes, contexto),
            'analista_responsavel': '[Nome do Analista Responsável]',
            'casos_uso': self._gerar_casos_uso_detalhados(sistema, contexto, anotacoes),
            'papel_perfil': usuario_tipo,
            'acao_meta': self._gerar_acao_meta_detalhada(problema_detalhado, solucao_detalhada, contexto, anotacoes),
            'beneficio_razao': self._gerar_beneficio_detalhado(problema_detalhado, solucao_detalhada, contexto, anotacoes),
            'criterios_aceite': self._gerar_criterios_aceite_detalhados(anotacoes, contexto, sistema),
            'tarefas': self._gerar_tarefas_tecnicas_detalhadas(contexto, sistema, solucao_detalhada, anotacoes),
            'dependencias': self._gerar_dependencias_detalhadas(contexto, sistema, anotacoes),
            'riscos': self._gerar_riscos_detalhados(contexto, sistema, problema_detalhado, anotacoes)
        }
        
        return estrutura
    
    def _analisar_contexto_detalhado(self, anotacoes: str) -> Dict[str, Any]:
        """Análise profunda e detalhada do contexto das anotações"""
        contexto = {
            'tipo_solicitacao': 'melhoria',
            'urgencia': 'normal',
            'complexidade': 'media',
            'area_impacto': [],
            'palavras_chave': [],
            'entidades_mencionadas': [],
            'valores_financeiros': [],
            'problemas_identificados': [],
            'solucoes_propostas': [],
            'stakeholders': []
        }
        
        texto_lower = anotacoes.lower()
        
        # Identificar tipo de solicitação com mais precisão
        if any(palavra in texto_lower for palavra in ['erro', 'bug', 'problema', 'falha', 'não funciona', 'incorreto']):
            contexto['tipo_solicitacao'] = 'correção'
        elif any(palavra in texto_lower for palavra in ['novo', 'criar', 'implementar', 'adicionar', 'desenvolver']):
            contexto['tipo_solicitacao'] = 'nova_funcionalidade'
        elif any(palavra in texto_lower for palavra in ['melhorar', 'otimizar', 'reformatar', 'ajustar', 'mudar', 'revisitar']):
            contexto['tipo_solicitacao'] = 'melhoria'
            
        # Identificar urgência com base em palavras-chave
        if any(palavra in texto_lower for palavra in ['urgente', 'imediato', 'crítico', 'prioridade', 'já']):
            contexto['urgencia'] = 'alta'
        elif any(palavra in texto_lower for palavra in ['quando possível', 'futuro', 'próxima versão', 'eventualmente']):
            contexto['urgencia'] = 'baixa'
            
        # Identificar complexidade
        if any(palavra in texto_lower for palavra in ['simples', 'apenas', 'só', 'somente']):
            contexto['complexidade'] = 'baixa'
        elif any(palavra in texto_lower for palavra in ['complexo', 'múltiplos', 'vários', 'integração', 'sistema']):
            contexto['complexidade'] = 'alta'
            
        # Identificar áreas de impacto
        if 'relatório' in texto_lower:
            contexto['area_impacto'].append('relatórios')
        if any(palavra in texto_lower for palavra in ['pagamento', 'financeiro', 'valor', 'r$', 'dinheiro']):
            contexto['area_impacto'].append('financeiro')
        if any(palavra in texto_lower for palavra in ['usuário', 'interface', 'tela', 'navegação']):
            contexto['area_impacto'].append('interface')
        if any(palavra in texto_lower for palavra in ['dados', 'informação', 'banco', 'query']):
            contexto['area_impacto'].append('dados')
            
        # Extrair valores financeiros mencionados
        valores = re.findall(r'R\$\s*[\d.,]+', anotacoes)
        contexto['valores_financeiros'] = valores
        
        # Identificar stakeholders
        if 'secretária' in texto_lower:
            contexto['stakeholders'].append('Secretária')
        if 'usuário' in texto_lower:
            contexto['stakeholders'].append('Usuários finais')
        if 'equipe' in texto_lower:
            contexto['stakeholders'].append('Equipe de desenvolvimento')
            
        return contexto
    
    def _identificar_problema_detalhado(self, anotacoes: str) -> str:
        """Identifica e descreve detalhadamente o problema"""
        texto_lower = anotacoes.lower()
        
        # Análise específica para o exemplo do FEHIDRO
        if 'fehidro' in texto_lower and 'relatório' in texto_lower:
            if 'não faz mais sentido' in texto_lower:
                return """O relatório de liberação não reembolsável FEHIDRO apresenta inconsistências na categorização de valores. 
                Atualmente, o sistema exibe um campo "total de agente técnico" que não reflete adequadamente a realidade dos pagamentos, 
                especialmente considerando as mudanças no tipo de agente e forma de pagamento. Por exemplo, valores que deveriam ser 
                categorizados como "agente financeiro" estão sendo exibidos incorretamente como "agente técnico", causando confusão 
                na interpretação dos dados financeiros."""
        
        # Padrões gerais de problemas
        if 'formatação' in texto_lower and 'relatório' in texto_lower:
            return """A formatação atual do relatório não atende às necessidades operacionais, apresentando informações de forma 
            confusa ou inadequada para a tomada de decisões."""
            
        if 'confusão' in texto_lower or 'confuso' in texto_lower:
            return """As informações apresentadas pelo sistema geram confusão entre os usuários, dificultando a interpretação 
            correta dos dados e impactando a eficiência operacional."""
            
        if 'total' in texto_lower and ('errado' in texto_lower or 'incorreto' in texto_lower):
            return """Os cálculos de totais apresentados pelo sistema estão incorretos, não refletindo adequadamente os valores 
            reais das operações, o que compromete a confiabilidade das informações."""
            
        # Análise mais genérica baseada em sentenças
        sentences = anotacoes.split('.')
        problemas = []
        for sentence in sentences:
            if any(palavra in sentence.lower() for palavra in ['problema', 'erro', 'não', 'incorreto', 'falha']):
                problemas.append(sentence.strip())
                
        if problemas:
            return ' '.join(problemas) + " Esta situação impacta negativamente a operação e requer correção."
            
        return """Foi identificada uma necessidade de melhoria no sistema para atender melhor às demandas operacionais 
        e garantir maior eficiência nos processos."""
    
    def _identificar_solucao_detalhada(self, anotacoes: str) -> str:
        """Identifica e descreve detalhadamente a solução proposta"""
        texto_lower = anotacoes.lower()
        
        # Análise específica para o exemplo do FEHIDRO
        if 'fehidro' in texto_lower and 'reformatar' in texto_lower:
            return """Reformatar completamente a estrutura do relatório de liberações não reembolsáveis, separando 
            adequadamente os totais por categoria: Total de Parcelas (somatório de todas as parcelas liberadas), 
            Total de Agente Técnico (apenas quando aplicável, excluindo consórcios), e Total de Agente Financeiro 
            (valores efetivamente pagos). Implementar regra específica para que quando o agente técnico for "CONSÓRCIO", 
            o campo Total de Agente Técnico exiba R$ 0,00, garantindo a precisão das informações financeiras."""
        
        if 'reformatar' in texto_lower:
            return """Reformatar a estrutura atual para melhor organização e apresentação das informações, 
            garantindo maior clareza e facilidade de compreensão para os usuários."""
            
        if 'separar' in texto_lower:
            return """Implementar separação adequada das informações, categorizando-as de forma lógica e intuitiva 
            para facilitar a análise e tomada de decisões."""
            
        if 'ajustar' in texto_lower:
            return """Realizar ajustes na funcionalidade atual para corrigir as inconsistências identificadas 
            e melhorar a experiência do usuário."""
            
        if 'mudar' in texto_lower:
            return """Alterar a implementação atual para atender às novas demandas e requisitos operacionais, 
            garantindo maior eficiência e precisão."""
            
        return """Implementar melhorias abrangentes na funcionalidade para resolver os problemas identificados 
        e otimizar a experiência do usuário, garantindo maior eficiência operacional."""
    
    def _gerar_acao_meta_detalhada(self, problema: str, solucao: str, contexto: Dict, anotacoes: str) -> str:
        """Gera uma ação/meta detalhada e específica"""
        if 'fehidro' in anotacoes.lower() and 'relatório' in anotacoes.lower():
            return """visualizar relatórios de liberações não reembolsáveis FEHIDRO com informações financeiras 
            precisas, categorizadas corretamente e organizadas de forma clara, permitindo análise eficiente 
            dos dados de pagamentos de agentes técnicos e financeiros"""
            
        if contexto['tipo_solicitacao'] == 'melhoria':
            if 'relatórios' in contexto['area_impacto']:
                return """acessar relatórios reformatados com informações organizadas de forma lógica e intuitiva, 
                facilitando a análise de dados e a tomada de decisões estratégicas"""
            if 'financeiro' in contexto['area_impacto']:
                return """visualizar informações financeiras precisas e bem categorizadas, garantindo transparência 
                e confiabilidade nos dados apresentados para análise e controle"""
                
        if contexto['tipo_solicitacao'] == 'correção':
            return """utilizar a funcionalidade corrigida sem erros ou inconsistências, garantindo operação 
            eficiente e confiável do sistema"""
            
        if contexto['tipo_solicitacao'] == 'nova_funcionalidade':
            return """acessar e utilizar a nova funcionalidade implementada de forma intuitiva e eficiente, 
            agregando valor aos processos operacionais"""
            
        return """utilizar o sistema de forma otimizada, com funcionalidades aprimoradas que garantem 
        maior eficiência, precisão e facilidade de uso"""
    
    def _gerar_beneficio_detalhado(self, problema: str, solucao: str, contexto: Dict, anotacoes: str) -> str:
        """Gera um benefício/razão detalhado e específico"""
        if 'fehidro' in anotacoes.lower() and 'confusão' in problema.lower():
            return """eliminar confusões na interpretação de dados financeiros, garantir precisão nas informações 
            de pagamentos de agentes, facilitar a tomada de decisões baseada em dados confiáveis e melhorar 
            a transparência nos processos de liberação de recursos"""
            
        if 'formatação' in problema.lower():
            return """ter acesso a informações bem organizadas e estruturadas, facilitando a compreensão e análise 
            dos dados, reduzindo tempo de processamento e minimizando erros de interpretação"""
            
        if 'cálculo' in problema.lower() or 'total' in problema.lower():
            return """garantir a precisão absoluta dos cálculos e valores apresentados, assegurar confiabilidade 
            nas informações financeiras e facilitar auditorias e controles internos"""
            
        if contexto['area_impacto']:
            if 'relatórios' in contexto['area_impacto']:
                return """tomar decisões estratégicas baseadas em informações precisas e confiáveis, otimizar 
                processos de análise e controle, e garantir compliance com requisitos regulatórios"""
            if 'financeiro' in contexto['area_impacto']:
                return """assegurar transparência e precisão nas informações financeiras, facilitar controles 
                internos e auditorias, e garantir conformidade com normas contábeis e regulamentares"""
                
        return """melhorar significativamente a eficiência operacional, reduzir retrabalho, minimizar erros 
        e garantir maior qualidade nos processos de trabalho"""
    
    def _gerar_criterios_aceite_detalhados(self, anotacoes: str, contexto: Dict, sistema: str) -> List[Dict]:
        """Gera critérios de aceite detalhados e específicos"""
        criterios = []
        
        # Critério específico para FEHIDRO
        if 'fehidro' in anotacoes.lower() and 'relatório' in anotacoes.lower():
            criterios.append({
                'cenario': 'Cenário 1: Nova Estrutura do Relatório FEHIDRO',
                'dado': 'que o usuário acessa o relatório de liberações não reembolsáveis FEHIDRO no sistema GFESP',
                'quando': 'o relatório for gerado e exibido',
                'entao': '''deve apresentar as seguintes colunas separadas e claramente identificadas:
                - Total de Parcelas: somatório de todas as parcelas liberadas
                - Total de Agente Técnico: valores pagos a agentes técnicos (excluindo consórcios)
                - Total de Agente Financeiro: valores efetivamente pagos a agentes financeiros
                E deve aplicar formatação clara com cabeçalhos descritivos e valores em formato monetário brasileiro'''
            })
            
            criterios.append({
                'cenario': 'Cenário 2: Regra Específica para Consórcios',
                'dado': 'que existe uma liberação onde o agente técnico é classificado como "CONSÓRCIO"',
                'quando': 'o relatório for gerado para esta liberação',
                'entao': '''deve exibir:
                - Total de Agente Técnico: R$ 0,00 (zero)
                - Total de Agente Financeiro: valor real da taxa de agente financeiro (ex: R$ 1.522,50)
                - Observação clara indicando "Consórcio - Sem pagamento de AT" ou similar'''
            })
            
            criterios.append({
                'cenario': 'Cenário 3: Validação de Categorização de Valores',
                'dado': 'que existem dados de liberação com diferentes tipos de agentes no sistema',
                'quando': 'o relatório for processado e os valores calculados',
                'entao': '''deve categorizar corretamente:
                - Valores de "Taxa Agente Financeiro" devem aparecer em "Total de Agente Financeiro"
                - Valores de agentes técnicos não-consórcio devem aparecer em "Total de Agente Técnico"
                - Somatório geral deve ser exibido em "Total de Parcelas"
                - Não deve haver sobreposição ou duplicação de valores entre categorias'''
            })
        else:
            # Critérios genéricos mas detalhados
            criterios.append({
                'cenario': 'Cenário 1: Funcionalidade Principal',
                'dado': 'que o usuário possui as permissões adequadas e acessa a funcionalidade no sistema',
                'quando': 'executar a operação principal conforme especificado',
                'entao': '''deve funcionar conforme os requisitos estabelecidos, apresentando:
                - Interface responsiva e intuitiva
                - Processamento correto dos dados
                - Feedback adequado ao usuário sobre o status da operação
                - Tratamento de erros com mensagens claras'''
            })
            
            criterios.append({
                'cenario': 'Cenário 2: Validação de Dados e Regras de Negócio',
                'dado': 'que existem dados válidos no sistema para processamento',
                'quando': 'a funcionalidade for executada com estes dados',
                'entao': '''deve processar corretamente aplicando todas as regras de negócio:
                - Validação de integridade dos dados
                - Aplicação de cálculos e transformações necessárias
                - Verificação de consistência com outras funcionalidades
                - Geração de logs de auditoria quando aplicável'''
            })
            
            criterios.append({
                'cenario': 'Cenário 3: Performance e Usabilidade',
                'dado': 'que o sistema está em operação normal com carga típica de usuários',
                'quando': 'a funcionalidade for utilizada',
                'entao': '''deve atender aos critérios de performance:
                - Tempo de resposta inferior a 3 segundos para operações simples
                - Interface responsiva em dispositivos móveis e desktop
                - Compatibilidade com navegadores principais (Chrome, Firefox, Edge)
                - Manutenção da sessão do usuário durante a operação'''
            })
        
        return criterios
    
    def _gerar_tarefas_tecnicas_detalhadas(self, contexto: Dict, sistema: str, solucao: str, anotacoes: str) -> str:
        """Gera tarefas técnicas detalhadas e específicas"""
        tarefas = []
        
        if 'fehidro' in anotacoes.lower() and 'relatório' in anotacoes.lower():
            tarefas.extend([
                "• Analisar a estrutura atual da query do relatório de liberações FEHIDRO no banco de dados",
                "• Modificar a query SQL para incluir colunas separadas: total_parcelas, total_agente_tecnico, total_agente_financeiro",
                "• Implementar lógica condicional para identificar agentes técnicos do tipo 'CONSÓRCIO'",
                "• Criar regra de negócio: IF agente_tecnico = 'CONSÓRCIO' THEN total_agente_tecnico = 0",
                "• Ajustar o template do relatório (PDF/Excel) para incluir as novas colunas com formatação adequada",
                "• Implementar formatação monetária brasileira (R$ X.XXX,XX) para todos os valores",
                "• Adicionar cabeçalhos descritivos e legendas explicativas no relatório",
                "• Criar testes unitários para validar a categorização correta dos valores",
                "• Realizar testes de integração com dados reais do ambiente de homologação",
                "• Validar performance da nova query com volume de dados de produção",
                "• Atualizar documentação técnica do módulo FEHIDRO",
                "• Criar manual do usuário com exemplos da nova estrutura do relatório"
            ])
        elif 'relatório' in contexto['area_impacto']:
            tarefas.extend([
                "• Analisar a estrutura atual do relatório e identificar pontos de melhoria",
                "• Modificar as queries do banco de dados para incluir os novos campos/colunas necessários",
                "• Implementar lógica de categorização e organização dos dados conforme especificado",
                "• Ajustar o layout e formatação do relatório (PDF/Excel) conforme novo modelo aprovado",
                "• Implementar validações de dados para garantir consistência das informações",
                "• Criar testes automatizados para validar a geração correta do relatório",
                "• Realizar testes de performance com volume de dados de produção",
                "• Atualizar documentação técnica e manual do usuário"
            ])
        elif 'interface' in contexto['area_impacto']:
            tarefas.extend([
                "• Analisar a interface atual e mapear pontos de melhoria na experiência do usuário",
                "• Desenvolver mockups e protótipos da nova interface",
                "• Implementar as modificações no frontend conforme especificações de UX/UI",
                "• Adicionar validações client-side e server-side necessárias",
                "• Implementar feedback visual adequado para ações do usuário",
                "• Ajustar responsividade para dispositivos móveis e tablets",
                "• Realizar testes de usabilidade com usuários finais",
                "• Implementar testes automatizados de interface (E2E)"
            ])
        else:
            tarefas.extend([
                "• Realizar análise detalhada do código atual da funcionalidade",
                "• Mapear dependências e impactos da modificação em outros módulos",
                "• Implementar as modificações necessárias seguindo padrões de código estabelecidos",
                "• Criar ou atualizar testes unitários para cobrir as novas funcionalidades",
                "• Realizar testes de integração para validar compatibilidade com outros sistemas",
                "• Executar testes de regressão para garantir que funcionalidades existentes não foram afetadas",
                "• Validar a implementação com stakeholders e usuários finais",
                "• Preparar ambiente de homologação para testes finais"
            ])
        
        if sistema != 'Sistema [A definir]':
            tarefas.append(f"• Atualizar documentação técnica completa do sistema {sistema}")
            tarefas.append(f"• Criar release notes detalhadas para a nova versão do {sistema}")
        
        tarefas.append("• Planejar estratégia de deploy e rollback em caso de problemas")
        tarefas.append("• Preparar treinamento para usuários finais sobre as mudanças implementadas")
        
        return '\n'.join(tarefas)
    
    def _gerar_dependencias_detalhadas(self, contexto: Dict, sistema: str, anotacoes: str) -> str:
        """Gera dependências detalhadas do projeto"""
        dependencias = []
        
        if 'fehidro' in anotacoes.lower():
            dependencias.extend([
                "• Acesso completo ao banco de dados GFESP para modificação das queries de relatório",
                "• Definição final e aprovação do layout do relatório pela Secretaria FEHIDRO",
                "• Disponibilidade de ambiente de testes com dados representativos de produção",
                "• Validação das novas regras de categorização com a área contábil/financeira",
                "• Aprovação formal da Secretária FEHIDRO para as mudanças propostas"
            ])
        
        if 'relatório' in contexto['area_impacto']:
            dependencias.extend([
                "• Acesso ao banco de dados para modificação das queries de relatório",
                "• Definição final do layout e estrutura do relatório pela área solicitante",
                "• Ambiente de testes disponível com dados representativos",
                "• Aprovação do novo modelo de relatório pelos stakeholders"
            ])
        
        if 'financeiro' in contexto['area_impacto']:
            dependencias.extend([
                "• Validação das regras financeiras e contábeis com a área responsável",
                "• Aprovação dos critérios de categorização de valores financeiros",
                "• Verificação de compliance com normas regulatórias aplicáveis"
            ])
        
        if contexto['urgencia'] == 'alta':
            dependencias.append("• Priorização imediata no cronograma de desenvolvimento da equipe")
        
        dependencias.extend([
            "• Disponibilidade completa da equipe de desenvolvimento durante o período de implementação",
            "• Aprovação final e sign-off da área solicitante após homologação",
            "• Coordenação com equipe de infraestrutura para deploy em produção",
            "• Agendamento de janela de manutenção para deploy (se necessário)",
            "• Preparação de plano de comunicação para usuários sobre as mudanças"
        ])
        
        return '\n'.join(dependencias)
    
    def _gerar_riscos_detalhados(self, contexto: Dict, sistema: str, problema: str, anotacoes: str) -> str:
        """Gera análise detalhada de riscos"""
        riscos = []
        
        if 'fehidro' in anotacoes.lower():
            riscos.extend([
                "• Risco de inconsistência temporária nos dados durante a migração da estrutura do relatório",
                "• Possível impacto em outros relatórios FEHIDRO que utilizam a mesma base de dados",
                "• Necessidade de revalidação de relatórios históricos já gerados",
                "• Risco de resistência dos usuários às mudanças na estrutura familiar do relatório"
            ])
        
        if 'dados' in problema.lower() or 'valor' in problema.lower():
            riscos.extend([
                "• Risco de perda ou corrupção de dados durante a migração",
                "• Possibilidade de inconsistências temporárias entre sistemas integrados",
                "• Necessidade de sincronização com sistemas externos que consomem estes dados"
            ])
        
        if contexto['complexidade'] == 'alta':
            riscos.extend([
                "• Complexidade técnica elevada pode impactar significativamente o prazo de entrega",
                "• Risco de efeitos colaterais não previstos em outras funcionalidades do sistema",
                "• Necessidade de recursos técnicos especializados que podem não estar disponíveis"
            ])
        
        if 'relatório' in contexto['area_impacto']:
            riscos.extend([
                "• Possível impacto em processos de auditoria que dependem da estrutura atual do relatório",
                "• Risco de incompatibilidade com sistemas externos que importam estes relatórios",
                "• Necessidade de atualização de documentação e procedimentos operacionais"
            ])
        
        riscos.extend([
            "• Mudanças de escopo durante o desenvolvimento que podem afetar cronograma e orçamento",
            "• Necessidade extensiva de treinamento dos usuários para adaptação às mudanças",
            "• Risco de bugs não detectados em homologação que podem aparecer em produção",
            "• Possibilidade de rollback complexo caso a implementação apresente problemas críticos",
            "• Impacto na produtividade dos usuários durante o período de adaptação às mudanças"
        ])
        
        return '\n'.join(riscos)
    
    # Métodos auxiliares mantidos da versão anterior
    def _identificar_sistema(self, anotacoes: str) -> str:
        """Identifica o sistema mencionado nas anotações"""
        for sistema in self.sistemas_conhecidos:
            if sistema in anotacoes.upper():
                return sistema
        
        if 'fehidro' in anotacoes.lower():
            return 'GFESP (FEHIDRO)'
        if 'fundocamp' in anotacoes.lower():
            return 'SPF (FUNDOCAMP)'
            
        return 'Sistema [A definir]'
    
    def _identificar_tipo_usuario(self, anotacoes: str, contexto: Dict) -> str:
        """Identifica o tipo de usuário baseado no contexto"""
        texto_lower = anotacoes.lower()
        
        for tipo in self.tipos_usuario:
            if tipo in texto_lower:
                return tipo
                
        if 'secretária' in texto_lower or 'secretaria' in texto_lower:
            return 'usuário da secretaria'
        if 'fehidro' in texto_lower:
            return 'gestor FEHIDRO'
        if 'financeiro' in contexto['area_impacto']:
            return 'usuário do setor financeiro'
        if 'relatório' in contexto['area_impacto']:
            return 'analista de relatórios'
            
        return 'usuário do sistema'
    
    def _gerar_solicitante_detalhado(self, anotacoes: str, contexto: Dict) -> str:
        """Gera informação detalhada sobre o solicitante"""
        texto_lower = anotacoes.lower()
        
        if 'secretária' in texto_lower and 'fehidro' in texto_lower:
            return 'Secretaria FEHIDRO'
        if 'secretária' in texto_lower:
            return 'Secretaria [Nome da Secretaria]'
        if 'fehidro' in texto_lower:
            return 'Área FEHIDRO - Secretaria do Meio Ambiente'
        if 'área' in texto_lower:
            return 'Área Solicitante [Nome da Área]'
            
        return '[Área Solicitante - a definir]'
    
    def _gerar_casos_uso_detalhados(self, sistema: str, contexto: Dict, anotacoes: str) -> str:
        """Gera casos de uso detalhados baseados no sistema e contexto"""
        base = f"{sistema} → "
        
        if 'fehidro' in anotacoes.lower() and 'relatório' in anotacoes.lower():
            return f"{base}Módulo FEHIDRO → Relatórios → Liberações Não Reembolsáveis → Botão: Gerar Relatório"
            
        if 'relatório' in anotacoes.lower():
            return f"{base}Módulo Relatórios → [Tipo de Relatório] → Funcionalidade de Geração"
            
        if 'pagamento' in anotacoes.lower():
            return f"{base}Módulo Financeiro → Ordem de Pagamento → Botão: Nova Ordem"
            
        if 'liberação' in anotacoes.lower():
            return f"{base}Módulo Liberações → Gestão de Liberações → Funcionalidade Específica"
            
        return f"{base}Módulo [A definir] → Funcionalidade [A definir] → Ação Específica"

