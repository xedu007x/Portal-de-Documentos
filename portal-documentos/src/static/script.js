// Estado global
let documentoAtual = null;
let tipoDocumentoAtual = null;

// Funções para manipulação da interface
function abrirFormulario(tipo) {
    tipoDocumentoAtual = tipo;
    document.getElementById('selecao-documento').style.display = 'none';
    document.getElementById('formulario-documento').style.display = 'block';
    document.getElementById('documentos-salvos').style.display = 'none';

    if (tipo === 'historia_usuario') {
        document.getElementById('titulo-formulario').innerText = 'História de Usuário';
        document.getElementById('form-historia-usuario').style.display = 'block';
        document.getElementById('form-termo-aceite').style.display = 'none';
    } else if (tipo === 'termo_aceite') {
        document.getElementById('titulo-formulario').innerText = 'Termo de Aceite';
        document.getElementById('form-historia-usuario').style.display = 'none';
        document.getElementById('form-termo-aceite').style.display = 'block';
    }
}

function voltarSelecao() {
    document.getElementById('selecao-documento').style.display = 'block';
    document.getElementById('formulario-documento').style.display = 'none';
    document.getElementById('documentos-salvos').style.display = 'block';
    limparFormularios();
    carregarDocumentosSalvos();
}

function limparFormularios() {
    document.getElementById('anotacoes-hu').value = '';
    document.getElementById('sugestao-hu').innerHTML = '';
    document.getElementById('sugestao-hu').style.display = 'none';
    document.getElementById('botoes-acao-hu').style.display = 'none';

    document.getElementById('cenarios-gherkin').value = '';
    document.getElementById('sugestao-termo-aceite').innerHTML = '';
    document.getElementById('sugestao-termo-aceite').style.display = 'none';
    document.getElementById('botoes-acao-ta').style.display = 'none';
}

// Processamento de História de Usuário
async function processarHistoriaUsuario() {
    const anotacoes = document.getElementById('anotacoes-hu').value;
    if (!anotacoes) {
        alert('Por favor, insira as anotações da solicitação de melhoria.');
        return;
    }

    try {
        const response = await fetch('/api/processar-historia-usuario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ anotacoes: anotacoes })
        });

        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }

        const data = await response.json();
        documentoAtual = { tipo: 'historia_usuario', data: data };
        mostrarSugestaoHistoriaUsuario(data);
    } catch (error) {
        console.error('Erro ao processar História de Usuário:', error);
        alert('Ocorreu um erro ao processar a História de Usuário. Verifique o console para mais detalhes.');
    }
}

function mostrarSugestaoHistoriaUsuario(data) {
    const sugestaoDiv = document.getElementById('sugestao-hu');
    sugestaoDiv.innerHTML = `
        <h3>Sugestão de História de Usuário</h3>
        <div class="campo-sugestao">
            <strong>Solicitado por:</strong> ${data.solicitado_por}
        </div>
        <div class="campo-sugestao">
            <strong>Analista responsável:</strong> ${data.analista_responsavel}
        </div>
        <div class="campo-sugestao">
            <strong>Casos de Uso:</strong> ${data.casos_uso}
        </div>
        <div class="campo-sugestao">
            <strong>História de Usuário:</strong>
            <p>Como ${data.papel_perfil}</p>
            <p>Posso ${data.acao_meta}</p>
            <p>Para ${data.beneficio_razao}</p>
        </div>
        <div class="campo-sugestao">
            <strong>Critérios de Aceite:</strong>
            ${data.criterios_aceite.map(c => `
                <div class="criterio-aceite">
                    <h4>${c.cenario}</h4>
                    <p><strong>Dado</strong> ${c.dado}</p>
                    <p><strong>Quando</strong> ${c.quando}</p>
                    <p><strong>Então</strong> ${c.entao}</p>
                </div>
            `).join('')}
        </div>
        <div class="campo-sugestao">
            <strong>TAREFAS:</strong>
            <pre>${data.tarefas}</pre>
        </div>
        <div class="campo-sugestao">
            <strong>DEPENDÊNCIAS:</strong>
            <pre>${data.dependencias}</pre>
        </div>
        <div class="campo-sugestao">
            <strong>RISCOS:</strong>
            <pre>${data.riscos}</pre>
        </div>
    `;
    sugestaoDiv.style.display = 'block';
    document.getElementById('botoes-acao-hu').style.display = 'block';
}

// Processamento de Termo de Aceite
async function processarTermoAceite() {
    const cenariosGherkin = document.getElementById('cenarios-gherkin').value;
    if (!cenariosGherkin) {
        alert('Por favor, insira os cenários Gherkin.');
        return;
    }

    try {
        const response = await fetch('/api/processar-termo-aceite', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cenarios_gherkin: cenariosGherkin })
        });

        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }

        const data = await response.json();
        documentoAtual = { tipo: 'termo_aceite', data: data };
        mostrarSugestaoTermoAceite(data);
    } catch (error) {
        console.error('Erro ao processar Termo de Aceite:', error);
        alert('Ocorreu um erro ao processar o Termo de Aceite. Verifique o console para mais detalhes.');
    }
}

function mostrarSugestaoTermoAceite(data) {
    const sugestaoDiv = document.getElementById('sugestao-termo-aceite');
    let html = `
        <h3>Sugestão de Termo de Aceite</h3>
        <h4>Informações Gerais</h4>
        <table class="info-gerais-table">
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Detalhe</th>
                </tr>
            </thead>
            <tbody>
    `;
    for (const key in data.informacoes_gerais) {
        html += `
                <tr>
                    <td>${key}</td>
                    <td>${data.informacoes_gerais[key]}</td>
                </tr>
        `;
    }
    html += `
            </tbody>
        </table>

        <h4>Etapas de Teste</h4>
        <table class="tabela-testes">
            <thead>
                <tr>
                    <th>Etapa</th>
                    <th>Executado por</th>
                    <th>Descrição da Etapa</th>
                    <th>Resultado Esperado</th>
                    <th>Resultado Obtido</th>
                    <th>Status</th>
                    <th>Observações</th>
                </tr>
            </thead>
            <tbody>
    `;
    data.tabela_testes.forEach(row => {
        html += `
                <tr>
                    <td>${row.Etapa}</td>
                    <td>${row['Executado por']}</td>
                    <td>${row['Descrição da Etapa']}</td>
                    <td><pre>${row['Resultado Esperado']}</pre></td>
                    <td>${row['Resultado Obtido']}</td>
                    <td>${row['Status']}</td>
                    <td>${row['Observações']}</td>
                </tr>
        `;
    });
    html += `
            </tbody>
        </table>
    `;
    sugestaoDiv.innerHTML = html;
    sugestaoDiv.style.display = 'block';
    document.getElementById('botoes-acao-ta').style.display = 'block';
}

// Funções de Salvar e Exportar (compartilhadas)
async function salvarDocumento() {
    if (!documentoAtual) {
        alert('Nenhum documento para salvar.');
        return;
    }

    try {
        const response = await fetch('/api/documentos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(documentoAtual)
        });

        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }

        alert('Documento salvo com sucesso!');
        carregarDocumentosSalvos();
    } catch (error) {
        console.error('Erro ao salvar documento:', error);
        alert('Ocorreu um erro ao salvar o documento. Verifique o console para mais detalhes.');
    }
}

async function exportarDocumento() {
    if (!documentoAtual) {
        alert('Nenhum documento para exportar.');
        return;
    }

    try {
        const response = await fetch('/api/exportar-documento', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(documentoAtual)
        });

        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${documentoAtual.tipo}_${new Date().toISOString().slice(0,10)}.docx`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);

        alert('Documento exportado com sucesso!');
    } catch (error) {
        console.error('Erro ao exportar documento:', error);
        alert('Ocorreu um erro ao exportar o documento. Verifique o console para mais detalhes.');
    }
}

// Carregar documentos salvos
async function carregarDocumentosSalvos() {
    try {
        const response = await fetch('/api/documentos');
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        const documentos = await response.json();
        const listaDocumentos = document.getElementById('lista-documentos-salvos');
        listaDocumentos.innerHTML = '';

        if (documentos.length === 0) {
            listaDocumentos.innerHTML = '<p>Nenhum documento salvo ainda.</p>';
            return;
        }

        documentos.forEach(doc => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span>${doc.tipo.replace('_', ' ').toUpperCase()} - ${doc.data.solicitado_por || doc.data.informacoes_gerais?.Sistema || 'Sem Título'}</span>
                <button onclick="visualizarDocumento(${doc.id})">Visualizar</button>
                <button onclick="excluirDocumento(${doc.id})">Excluir</button>
            `;
            listaDocumentos.appendChild(li);
        });
    } catch (error) {
        console.error('Erro ao carregar documentos salvos:', error);
        document.getElementById('lista-documentos-salvos').innerHTML = '<p>Erro ao carregar documentos.</p>';
    }
}

async function visualizarDocumento(id) {
    try {
        const response = await fetch(`/api/documentos/${id}`);
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        const doc = await response.json();
        documentoAtual = doc;

        document.getElementById('selecao-documento').style.display = 'none';
        document.getElementById('formulario-documento').style.display = 'block';
        document.getElementById('documentos-salvos').style.display = 'none';

        if (doc.tipo === 'historia_usuario') {
            document.getElementById('titulo-formulario').innerText = 'História de Usuário';
            document.getElementById('form-historia-usuario').style.display = 'block';
            document.getElementById('form-termo-aceite').style.display = 'none';
            mostrarSugestaoHistoriaUsuario(doc.data);
            document.getElementById('anotacoes-hu').value = '[Documento carregado do banco de dados]'; // Apenas para indicar que não é uma nova anotação
        } else if (doc.tipo === 'termo_aceite') {
            document.getElementById('titulo-formulario').innerText = 'Termo de Aceite';
            document.getElementById('form-historia-usuario').style.display = 'none';
            document.getElementById('form-termo-aceite').style.display = 'block';
            mostrarSugestaoTermoAceite(doc.data);
            document.getElementById('cenarios-gherkin').value = '[Documento carregado do banco de dados]'; // Apenas para indicar que não é uma nova anotação
        }

    } catch (error) {
        console.error('Erro ao visualizar documento:', error);
        alert('Ocorreu um erro ao visualizar o documento. Verifique o console para mais detalhes.');
    }
}

async function excluirDocumento(id) {
    if (!confirm('Tem certeza que deseja excluir este documento?')) {
        return;
    }
    try {
        const response = await fetch(`/api/documentos/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }

        alert('Documento excluído com sucesso!');
        carregarDocumentosSalvos();
    } catch (error) {
        console.error('Erro ao excluir documento:', error);
        alert('Ocorreu um erro ao excluir o documento. Verifique o console para mais detalhes.');
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    carregarDocumentosSalvos();
});


