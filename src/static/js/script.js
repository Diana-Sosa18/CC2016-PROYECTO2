document.addEventListener('DOMContentLoaded', function () {
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
    const congratsModal = document.getElementById('congratsModal');
    const nuevoEstiloBtn = document.getElementById('nuevoEstiloBtn');
    const similaresScreen = document.getElementById('similaresScreen');
    const similaresScreen2 = document.getElementById('similaresScreen2'); // NUEVO

    // Variables de estado
    let ocasionSeleccionada = null;
    let currentOutfit = null;
    let currentSimilarLevel = 1;

    // Abrir modales
    loginBtn.addEventListener('click', function () {
        loginModal.style.display = 'block';
    });

    registerBtn.addEventListener('click', function () {
        registerModal.style.display = 'block';
    });

    // Cerrar modales
    closeBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            loginModal.style.display = 'none';
            registerModal.style.display = 'none';
        });
    });

    // Cerrar al hacer clic fuera
    window.addEventListener('click', function (event) {
        if (event.target === loginModal) loginModal.style.display = 'none';
        if (event.target === registerModal) registerModal.style.display = 'none';
        if (event.target === congratsModal) congratsModal.style.display = 'none';
    });

    // Manejar login
    loginForm.addEventListener('submit', function (e) {
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
    registerForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const name = document.getElementById('name').value;
        const gender = document.querySelector('input[name="gender"]:checked').value;

        if (!name.trim()) {
            alert('Por favor ingrese su nombre');
            return;
        }

        alert(`Registro exitoso: ${name} (${gender})`);
        registerModal.style.display = 'none';
    });

    // Selección de estilos
    styleOptions.forEach(option => {
        option.addEventListener('click', function () {
            styleOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
        });
    });

    // Confirmar selección de estilo
    confirmBtn.addEventListener('click', function () {
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
        option.addEventListener('click', function () {
            ocasionOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
            ocasionSeleccionada = this.dataset.ocasion;
        });
    });

    // Finalizar selección de ocasión
    finalizarBtn.addEventListener('click', function () {
        if (ocasionSeleccionada) {
            ocasionScreen.style.display = 'none';
            climaScreen.style.display = 'block';
            obtenerClima();
        } else {
            alert('Por favor selecciona una ocasión');
        }
    });

    // Función para obtener el clima
    function obtenerClima() {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(function (position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                weatherResult.textContent = "Buscando datos meteorológicos...";

                setTimeout(() => {
                    weatherResult.innerHTML = `
                        <div>🌡️ Temperatura: 24°C</div>
                        <div>🌦 Condición: Soleado</div>
                    `;
                }, 1500);
            }, function (error) {
                console.error("Error de geolocalización:", error);
                weatherResult.textContent = "Clima: Soleado, 24°C";
            });
        } else {
            weatherResult.textContent = "Clima: Soleado, 24°C";
        }
    }

    // Continuar al dashboard
    continuarBtn.addEventListener('click', function () {
        climaScreen.style.display = 'none';
        outfitsScreen.style.display = 'block';
    });

    // Función para mostrar outfits similares
    function showSimilarOutfits(baseOutfit, level) {
        currentOutfit = baseOutfit;
        currentSimilarLevel = level;

        if (level === 1) {
            outfitsScreen.style.display = 'none';
            similaresScreen.style.display = 'block';
            console.log(`Mostrando 3 outfits similares a: ${baseOutfit}`);
        } else if (level === 2) {
            similaresScreen.style.display = 'none';
            similaresScreen2.style.display = 'block';
            console.log(`Mostrando 3 outfits adicionales similares a: ${baseOutfit}`);
        }
    }

    // Botones "Ver similares"
    outfitsScreen.querySelectorAll('.more-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const card = this.closest('.outfit-card');
            showSimilarOutfits(card.querySelector('.outfit-image').alt, 1);
        });
    });

    similaresScreen.querySelectorAll('.more-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const card = this.closest('.outfit-card');
            showSimilarOutfits(card.querySelector('.outfit-image').alt, 2);
        });
    });

    similaresScreen2.querySelectorAll('.more-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const card = this.closest('.outfit-card');
            alert(`No hay más outfits similares disponibles para ${card.querySelector('.outfit-image').alt}`);
        });
    });

    // Botones de retroceso
    const backButtons = document.querySelectorAll('.back-btn');

    backButtons.forEach(button => {
        button.addEventListener('click', function () {
            const currentScreen = this.closest('div[id$="Screen"]');

            if (currentScreen.id === 'stylesScreen') {
                currentScreen.style.display = 'none';
                mainScreen.style.display = 'block';
            }
            else if (currentScreen.id === 'ocasionScreen') {
                currentScreen.style.display = 'none';
                stylesScreen.style.display = 'block';
            }
            else if (currentScreen.id === 'climaScreen') {
                currentScreen.style.display = 'none';
                ocasionScreen.style.display = 'block';
            }
            else if (currentScreen.id === 'outfitsScreen') {
                currentScreen.style.display = 'none';
                climaScreen.style.display = 'block';
            }
            else if (currentScreen.id === 'similaresScreen') {
                currentScreen.style.display = 'none';
                outfitsScreen.style.display = 'block';
            }
            else if (currentScreen.id === 'similaresScreen2') {
                currentScreen.style.display = 'none';
                similaresScreen.style.display = 'block';
            }
        });
    });

    // Botones "Me gusta"
    outfitsScreen.querySelectorAll('.like-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const card = this.closest('.outfit-card');
            const img = card.querySelector('.outfit-image').alt;

            this.innerHTML = '<span>✓</span> ¡Me gusta!';
            this.style.backgroundColor = '#45a049';

            congratsModal.style.display = 'block';
        });
    });

    nuevoEstiloBtn.addEventListener('click', function () {
        congratsModal.style.display = 'none';
        outfitsScreen.style.display = 'none';
        stylesScreen.style.display = 'block';
    });
});
