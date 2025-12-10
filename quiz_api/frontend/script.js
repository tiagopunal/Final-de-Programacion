const API_URL = 'http://127.0.0.1:8001';
let currentUser = null;
let currentQuizSession = null;
let quizQuestions = [];
let quizCurrentIndex = 0;
let quizAnswers = [];

// CREAR PREGUNTA DE DEMO
async function crearPreguntaDemo() {
    const preguntaDemo = {
        pregunta: "¿Cuál es el planeta más grande del sistema solar?",
        opciones: ["Saturno", "Júpiter", "Tierra", "Neptuno"],
        respuesta_correcta: 1,
        explicacion: "Júpiter es el planeta más grande del sistema solar con un diámetro de 142,984 km",
        categoria: "Astronomía",
        dificultad: "fácil"
    };

    const resultDiv = document.getElementById('demo-result');
    try {
        const response = await fetch(`${API_URL}/questions/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(preguntaDemo)
        });

        if (response.ok) {
            const data = await response.json();
            resultDiv.className = 'success';
            resultDiv.innerHTML = `✅ Pregunta creada exitosamente con ID: ${data.id}`;
        } else {
            resultDiv.className = 'error';
            resultDiv.innerHTML = `❌ Error al crear la pregunta`;
        }
    } catch (error) {
        console.error('Error:', error);
        resultDiv.className = 'error';
        resultDiv.innerHTML = `❌ Error al conectar con la API`;
    }
}

// LOGIN
document.getElementById('login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value.trim();
    
    if (username) {
        currentUser = username;
        document.getElementById('username-display').textContent = `👤 ${username}`;
        document.getElementById('login-page').classList.remove('active');
        document.getElementById('main-page').classList.add('active');
        document.getElementById('username').value = '';
        
        // Mostrar solo la pestaña de preguntas después de login
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
        document.querySelector('[data-tab="questions"]').classList.add('active');
        document.getElementById('questions').classList.add('active');
        
        loadQuestions();
    }
});

// LOGOUT
document.getElementById('logout-btn').addEventListener('click', () => {
    currentUser = null;
    document.getElementById('main-page').classList.remove('active');
    document.getElementById('login-page').classList.add('active');
    currentQuizSession = null;
});

// TAB NAVIGATION
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.getAttribute('data-tab');
        
        // Remove active from all
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
        
        // Add active to clicked
        btn.classList.add('active');
        document.getElementById(tabName).classList.add('active');
        
        if (tabName === 'stats') {
            loadStatistics();
        }
    });
});

// LOAD QUESTIONS
async function loadQuestions() {
    try {
        const response = await fetch(`${API_URL}/questions/?skip=0&limit=100`);
        const data = await response.json();
        
        displayQuestions(data.questions || data);
    } catch (error) {
        console.error('Error loading questions:', error);
        alert('Error al cargar las preguntas');
    }
}

// DISPLAY QUESTIONS
function displayQuestions(questions) {
    const container = document.getElementById('questions-list');
    container.innerHTML = '';
    
    const search = document.getElementById('search').value.toLowerCase();
    const categoryFilter = document.getElementById('category-filter').value;
    const difficultyFilter = document.getElementById('difficulty-filter').value;
    
    const filtered = questions.filter(q => {
        const matchesSearch = q.pregunta.toLowerCase().includes(search);
        const matchesCategory = !categoryFilter || q.categoria === categoryFilter;
        const matchesDifficulty = !difficultyFilter || q.dificultad === difficultyFilter;
        return matchesSearch && matchesCategory && matchesDifficulty;
    });
    
    filtered.forEach(question => {
        const card = document.createElement('div');
        card.className = 'question-card';
        card.innerHTML = `
            <div class="question-header">
                <div>
                    <span class="category-badge">${question.categoria}</span>
                    <span class="difficulty-badge ${question.dificultad}">${question.dificultad}</span>
                </div>
            </div>
            <div class="question-text">${question.pregunta}</div>
            <div class="options-list">
                ${question.opciones.map((opt, i) => `
                    <div class="option-item ${i === question.respuesta_correcta ? 'correct' : ''}">
                        ${opt} ${i === question.respuesta_correcta ? '✓' : ''}
                    </div>
                `).join('')}
            </div>
            <div style="font-size: 0.9em; color: #666; margin-top: 10px;">
                <strong>Explicación:</strong> ${question.explicacion}
            </div>
            <div style="margin-top:12px; display:flex; gap:8px; justify-content:flex-end;">
                <button class="btn btn-small" onclick="deleteQuestion(${question.id})">Eliminar</button>
            </div>
        `;
        container.appendChild(card);
    });
}

// FILTER LISTENERS
document.getElementById('search').addEventListener('input', () => {
    const response = fetch(`${API_URL}/questions/?skip=0&limit=100`)
        .then(r => r.json())
        .then(data => displayQuestions(data.questions || data));
});

document.getElementById('category-filter').addEventListener('change', () => {
    const response = fetch(`${API_URL}/questions/?skip=0&limit=100`)
        .then(r => r.json())
        .then(data => displayQuestions(data.questions || data));
});

document.getElementById('difficulty-filter').addEventListener('change', () => {
    const response = fetch(`${API_URL}/questions/?skip=0&limit=100`)
        .then(r => r.json())
        .then(data => displayQuestions(data.questions || data));
});

// CREAR PREGUNTA
document.getElementById('create-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const opciones = Array.from(document.querySelectorAll('.option-input')).map(inp => inp.value);
    const respuestaIndex = parseInt(document.getElementById('respuesta').value);
    
    const questionData = {
        pregunta: document.getElementById('pregunta').value,
        opciones: opciones,
        respuesta_correcta: respuestaIndex,
        explicacion: document.getElementById('explicacion').value,
        categoria: document.getElementById('categoria').value,
        dificultad: document.getElementById('dificultad').value
    };
    
    console.log('Enviando:', questionData);
    
    try {
        const response = await fetch(`${API_URL}/questions/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(questionData)
        });
        
        if (response.ok) {
            alert('✅ Pregunta creada exitosamente');
            document.getElementById('create-form').reset();
            loadQuestions();
        } else {
            const error = await response.json();
            console.error('Error:', error);
            alert('❌ Error al crear la pregunta: ' + JSON.stringify(error));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al crear la pregunta');
    }
});

// QUIZ
async function startQuiz(count) {
    try {
        // Crear sesión
        const sessionResponse = await fetch(`${API_URL}/quiz-sessions/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ usuario_nombre: currentUser })
        });
        
        currentQuizSession = await sessionResponse.json();
        
        // Cargar preguntas aleatorias desde el backend
        // Usamos el endpoint /questions/random para obtener preguntas en orden aleatorio
        const questionsResponse = await fetch(`${API_URL}/questions/random?limit=${count}`);
        if (!questionsResponse.ok) {
            const err = await questionsResponse.json().catch(() => ({}));
            throw new Error(err.detail || 'No se pudieron obtener preguntas aleatorias');
        }
        const questions = await questionsResponse.json();
        
        quizQuestions = questions;
        quizCurrentIndex = 0;
        quizAnswers = [];
        
        displayQuizQuestion();
    } catch (error) {
        console.error('Error:', error);
        alert('Error al iniciar el quiz');
    }
}

function displayQuizQuestion() {
    const container = document.getElementById('quiz-container');
    const startContainer = document.getElementById('quiz-start');
    
    if (quizCurrentIndex >= quizQuestions.length) {
        finishQuiz();
        return;
    }
    
    startContainer.style.display = 'none';
    container.style.display = 'block';
    
    const question = quizQuestions[quizCurrentIndex];
    const progress = `${quizCurrentIndex + 1}/${quizQuestions.length}`;
    
    // Construir HTML sin handlers inline
    container.innerHTML = `
        <div style="margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <h3>Pregunta ${progress}</h3>
                <span style="color: #667eea; font-weight: bold;">${Math.round((quizCurrentIndex / quizQuestions.length) * 100)}%</span>
            </div>
            <div style="height: 5px; background: #eee; border-radius: 5px; overflow: hidden;">
                <div style="height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); width: ${(quizCurrentIndex / quizQuestions.length) * 100}%;"></div>
            </div>
        </div>
        
        <div class="quiz-question">
            <div class="quiz-question-text">${question.pregunta}</div>
            <div class="quiz-options-list" id="options-list">
                ${question.opciones.map((opt, idx) => `
                    <div class="quiz-option" data-index="${idx}">
                        ${opt}
                    </div>
                `).join('')}
            </div>
        </div>
    `;

    // Añadir event listeners a las opciones (más robusto que usar onclick inline)
    const optionEls = container.querySelectorAll('.quiz-option');
    optionEls.forEach((el) => {
        el.style.pointerEvents = 'auto';
        el.addEventListener('click', (ev) => {
            const idx = Number(el.getAttribute('data-index'));
            try {
                selectAnswer(idx);
            } catch (err) {
                console.error('Error en selectAnswer:', err);
            }
        });
    });
}

function selectAnswer(answerIndex) {
    console.log('selectAnswer called with index:', answerIndex);
    const question = quizQuestions[quizCurrentIndex];
    if (!question) {
        console.error('No hay pregunta actual');
        return;
    }
    const isCorrect = answerIndex === question.respuesta_correcta;
    const selectedText = question.opciones[answerIndex];

    // Guardamos el índice de la respuesta (entero) para que el backend lo valide correctamente
    quizAnswers.push({
        question_id: question.id,
        respuesta_seleccionada: answerIndex,
        tiempo_respuesta_segundos: 0
    });

    // Marcar respuesta visualmente
    const optionEls = document.querySelectorAll('.quiz-option');
    optionEls.forEach((optEl) => {
        const idx = Number(optEl.getAttribute('data-index'));
        if (idx === answerIndex) {
            optEl.classList.add('selected');
        }
        optEl.style.pointerEvents = 'none';
    });

    setTimeout(() => {
        quizCurrentIndex++;
        displayQuizQuestion();
    }, 600);
}

async function finishQuiz() {
    try {
        // Calcular puntuación: comparar los índices guardados con la respuesta correcta
        const totalQuestions = quizAnswers.length || quizQuestions.length || 0;
        const correctAnswers = quizAnswers.reduce((acc, a) => {
            const q = quizQuestions.find(qi => qi.id === a.question_id);
            if (!q) return acc;
            return acc + (a.respuesta_seleccionada === q.respuesta_correcta ? 1 : 0);
        }, 0);
        const score = totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0;
        
        // Registrar respuestas primero
        for (const answer of quizAnswers) {
            // Enviar sólo los campos esperados por el schema del backend
            await fetch(`${API_URL}/answers/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    quiz_session_id: currentQuizSession.id,
                    question_id: answer.question_id,
                    respuesta_seleccionada: answer.respuesta_seleccionada,
                    tiempo_respuesta_segundos: answer.tiempo_respuesta_segundos || 0
                })
            });
        }

        // Completar sesión (backend recalcula puntuación basada en respuestas)
        const completeResp = await fetch(`${API_URL}/quiz-sessions/${currentQuizSession.id}/complete`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tiempo_total_segundos: 0 })
        });

        if (completeResp.ok) {
            const sessionData = await completeResp.json();
            currentQuizSession = sessionData;
            // Refrescar estadísticas en vivo
            loadStatistics();
        }
        
        // Mostrar resultado
        const container = document.getElementById('quiz-container');
        container.innerHTML = `
            <div style="text-align: center; padding: 40px; background: #f9f9f9; border-radius: 10px;">
                <h2 style="font-size: 3em; margin-bottom: 20px;">🎉 ¡Quiz Completado!</h2>
                <div style="font-size: 2em; color: #667eea; font-weight: bold; margin-bottom: 20px;">
                    Puntuación: ${score}%
                </div>
                <div style="font-size: 1.2em; margin-bottom: 30px;">
                    Respuestas correctas: <strong>${correctAnswers}/${totalQuestions}</strong>
                </div>
                <button class="btn btn-primary" onclick="backToQuizStart()" style="max-width: 200px;">
                    Hacer otro Quiz
                </button>
            </div>
        `;
    } catch (error) {
        console.error('Error:', error);
        alert('Error al finalizar el quiz');
    }
}

function backToQuizStart() {
    document.getElementById('quiz-container').style.display = 'none';
    document.getElementById('quiz-start').style.display = 'block';
}

// STATISTICS
async function loadStatistics() {
    try {
        const response = await fetch(`${API_URL}/statistics/global`);
        const stats = await response.json();

        const container = document.getElementById('stats-container');
        if (!container) return;

        // Build global stats HTML
        const globalHtml = `
            <div class="stat-card">
                <div class="stat-label">Total de Preguntas</div>
                <div class="stat-value">${stats.total_preguntas_activas || 0}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Sesiones completadas</div>
                <div class="stat-value">${stats.total_sesiones_completadas || 0}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Promedio de aciertos</div>
                <div class="stat-value">${stats.promedio_aciertos_general || 0}%</div>
            </div>
        `;

        // Render solo estadísticas globales
        container.innerHTML = `<div style="display:flex; gap:20px; flex-wrap:wrap;">${globalHtml}</div>`;
    } catch (error) {
        console.error('Error:', error);
        alert('Error al cargar estadísticas');
    }
}

// Estadísticas removidas del frontend

// INITIAL LOAD
loadQuestions();

// ELIMINAR PREGUNTA
async function deleteQuestion(questionId) {
    if (!confirm('¿Seguro que deseas eliminar esta pregunta?')) return;

    try {
        const resp = await fetch(`${API_URL}/questions/${questionId}`, { method: 'DELETE' });
        if (resp.status === 204 || resp.ok) {
            alert('✅ Pregunta eliminada');
            loadQuestions();
        } else {
            const err = await resp.json();
            console.error('Error eliminado pregunta:', err);
            alert('❌ Error al eliminar la pregunta');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Error al conectar con la API');
    }
}
