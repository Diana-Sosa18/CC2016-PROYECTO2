document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    const loginModal = document.getElementById('loginModal');
    const registerModal = document.getElementById('registerModal');
    const closeBtns = document.querySelectorAll('.close');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const mainScreen = document.getElementById('mainScreen');
    const stylesScreen = document.getElementById('stylesScreen');
    const styleOptions = document.querySelectorAll('.style-option');
    const confirmBtn = document.getElementById('confirmBtn');
    const ocasionScreen = document.getElementById('ocasionScreen');
    const ocasionOptions = document.querySelectorAll('.ocasion-option');
    const finalizarBtn = document.getElementById('finalizarBtn');
    const climaScreen = document.getElementById('climaScreen');
    const weatherResult = document.getElementById('weatherResult');
    const continuarBtn = document.getElementById('continuarBtn');
    const outfitsScreen = document.getElementById('outfitsScreen');
    const similaresScreen = document.getElementById('similaresScreen');
    const similaresScreen2 = document.getElementById('similaresScreen2');
    const congratsModal = document.getElementById('congratsModal');
    const nuevoEstiloBtn = document.getElementById('nuevoEstiloBtn');
    const outfitActions = document.getElementById('outfitActions');
    const likeOutfitBtn = document.getElementById('likeOutfitBtn');
    const moreOutfitsBtn = document.getElementById('moreOutfitsBtn');
    const similaresActions1 = document.getElementById('similaresActions1');
    const similaresActions2 = document.getElementById('similaresActions2');

    // Variables de estado
    let ocasionSeleccionada = null;
    let currentOutfit = null;

    // Abrir modales
    loginBtn.addEventListener('click', () => loginModal.style.display = 'block');
    registerBtn.addEventListener('click', () => registerModal.style.display = 'block');

    // Cerrar modales
    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            loginModal.style.display = 'none';
            registerModal.style.display = 'none';
        });
    });

    window.addEventListener('click', function(event) {
        if (event.target === loginModal) loginModal.style.display = 'none';
        if (event.target === registerModal) registerModal.style.display = 'none';
        if (event.target === congratsModal) congratsModal.style.display = 'none';
    });

    // Manejar login
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (!username.trim() || !password.trim()) {
            alert('Por favor complete todos los campos');
            return;
        }

        loginModal.style.display = 'none';
        mainScreen.style.display = 'none';
        stylesScreen.style.display = 'block';
    });

    // Manejar registro
    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const name = document.getElementById('name').value;

        if (!name.trim()) {
            alert('Por favor ingrese su nombre');
            return;
        }

        alert(`¡Bienvenido/a ${name}! Ahora puedes iniciar sesión`);
        registerModal.style.display = 'none';
    });

    // Selección de estilos
    styleOptions.forEach(option => {
        option.addEventListener('click', function() {
            styleOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
        });
    });

    // Confirmar selección de estilo
    confirmBtn.addEventListener('click', function() {
        const selected = document.querySelector('.style-option.selected');
        if (selected) {
            stylesScreen.style.display = 'none';
            ocasionScreen.style.display = 'block';
        } else {
            alert('Por favor selecciona un estilo');
        }
    });

    // Selección de ocasión
    ocasionOptions.forEach(option => {
        option.addEventListener('click', function() {
            ocasionOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
            ocasionSeleccionada = this.dataset.ocasion;
        });
    });

    // Finalizar selección de ocasión
    finalizarBtn.addEventListener('click', function() {
        if (ocasionSeleccionada) {
            ocasionScreen.style.display = 'none';
            climaScreen.style.display = 'block';
            obtenerClima();
        } else {
            alert('Por favor selecciona una ocasión');
        }
    });

    // Obtener clima simulado
    function obtenerClima() {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(function(position) {
                weatherResult.textContent = "Buscando datos meteorológicos...";
                setTimeout(() => {
                    weatherResult.innerHTML = `
                        <div>🌡️ Temperatura: 24°C</div>
                        <div>🌦 Condición: Soleado</div>
                    `;
                }, 1500);
            }, function(error) {
                weatherResult.textContent = "Clima: Soleado, 24°C";
            });
        } else {
            weatherResult.textContent = "Clima: Soleado, 24°C";
        }
    }

    continuarBtn.addEventListener('click', function() {
        climaScreen.style.display = 'none';
        outfitsScreen.style.display = 'block';
    });

    // Mostrar outfits similares
    function showSimilarOutfits(baseOutfit, level) {
        currentOutfit = baseOutfit;
        outfitsScreen.style.display = 'none';
        similaresScreen.style.display = 'none';
        similaresScreen2.style.display = 'none';

        if (level === 1) {
            similaresScreen.style.display = 'block';
        } else if (level === 2) {
            similaresScreen2.style.display = 'block';
        }
    }

    // Configurar interacción con outfits
    function setupOutfitSelection() {
        // Configurar selección en pantalla principal de outfits
        const outfitCards = outfitsScreen.querySelectorAll('.outfit-card');
        outfitCards.forEach(card => {
            card.addEventListener('click', function() {
                outfitCards.forEach(c => c.classList.remove('selected'));
                this.classList.add('selected');
                outfitActions.classList.remove('hidden');
            });
        });

        // Configurar botón "Me gusta"
        likeOutfitBtn.addEventListener('click', function() {
            congratsModal.style.display = 'block';
            outfitActions.classList.add('hidden');
            outfitCards.forEach(c => c.classList.remove('selected'));
        });

        // Configurar botón "Ver similares"
        moreOutfitsBtn.addEventListener('click', function() {
            const selected = outfitsScreen.querySelector('.outfit-card.selected');
            if (selected) {
                showSimilarOutfits(selected.dataset.outfit, 1);
                outfitActions.classList.add('hidden');
                outfitCards.forEach(c => c.classList.remove('selected'));
            }
        });

        // Configurar selección en pantalla de similares nivel 1
        const similaresCards1 = similaresScreen.querySelectorAll('.outfit-card');
        similaresCards1.forEach(card => {
            card.addEventListener('click', function() {
                similaresCards1.forEach(c => c.classList.remove('selected'));
                this.classList.add('selected');
                similaresActions1.classList.remove('hidden');
            });
        });

        // Configurar botones en pantalla de similares nivel 1
        similaresActions1.querySelector('.like-btn').addEventListener('click', function() {
            congratsModal.style.display = 'block';
            similaresActions1.classList.add('hidden');
            similaresCards1.forEach(c => c.classList.remove('selected'));
        });

        similaresActions1.querySelector('.more-btn').addEventListener('click', function() {
            const selected = similaresScreen.querySelector('.outfit-card.selected');
            if (selected) {
                showSimilarOutfits(selected.dataset.outfit, 2);
                similaresActions1.classList.add('hidden');
                similaresCards1.forEach(c => c.classList.remove('selected'));
            }
        });

        // Configurar selección en pantalla de similares nivel 2
        const similaresCards2 = similaresScreen2.querySelectorAll('.outfit-card');
        similaresCards2.forEach(card => {
            card.addEventListener('click', function() {
                similaresCards2.forEach(c => c.classList.remove('selected'));
                this.classList.add('selected');
                similaresActions2.classList.remove('hidden');
            });
        });

        // Configurar botón en pantalla de similares nivel 2
        similaresActions2.querySelector('.like-btn').addEventListener('click', function() {
            congratsModal.style.display = 'block';
            similaresActions2.classList.add('hidden');
            similaresCards2.forEach(c => c.classList.remove('selected'));
        });
    }

    function setupBackButtons() {
        document.querySelectorAll('.back-btn').forEach(button => {
            button.addEventListener('click', function() {
                const currentScreen = this.closest('div[id$="Screen"]');
                if (currentScreen.id === 'stylesScreen') {
                    currentScreen.style.display = 'none';
                    mainScreen.style.display = 'block';
                } else if (currentScreen.id === 'ocasionScreen') {
                    currentScreen.style.display = 'none';
                    stylesScreen.style.display = 'block';
                } else if (currentScreen.id === 'climaScreen') {
                    currentScreen.style.display = 'none';
                    ocasionScreen.style.display = 'block';
                } else if (currentScreen.id === 'outfitsScreen') {
                    currentScreen.style.display = 'none';
                    climaScreen.style.display = 'block';
                    outfitActions.classList.add('hidden');
                    currentScreen.querySelectorAll('.outfit-card').forEach(c => c.classList.remove('selected'));
                } else if (currentScreen.id === 'similaresScreen') {
                    currentScreen.style.display = 'none';
                    outfitsScreen.style.display = 'block';
                    similaresActions1.classList.add('hidden');
                    currentScreen.querySelectorAll('.outfit-card').forEach(c => c.classList.remove('selected'));
                } else if (currentScreen.id === 'similaresScreen2') {
                    currentScreen.style.display = 'none';
                    similaresScreen.style.display = 'block';
                    similaresActions2.classList.add('hidden');
                    currentScreen.querySelectorAll('.outfit-card').forEach(c => c.classList.remove('selected'));
                }
            });
        });
    }

    nuevoEstiloBtn.addEventListener('click', function() {
        congratsModal.style.display = 'none';
        outfitsScreen.style.display = 'none';
        similaresScreen.style.display = 'none';
        similaresScreen2.style.display = 'none';
        stylesScreen.style.display = 'block';
        
        // Limpiar selecciones
        outfitActions.classList.add('hidden');
        similaresActions1.classList.add('hidden');
        similaresActions2.classList.add('hidden');
        document.querySelectorAll('.outfit-card').forEach(c => c.classList.remove('selected'));
    });

    // Inicialización
    setupOutfitSelection();
    setupBackButtons();
});