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
    const congratsModal = document.getElementById('congratsModal');
    const nuevoEstiloBtn = document.getElementById('nuevoEstiloBtn');
    const similaresScreen = document.getElementById('similaresScreen');
    const similaresRow = document.getElementById('similaresRow');
    
    // Variables de estado
    let ocasionSeleccionada = null;
    let currentOutfit = null;

    // Datos de outfits similares
    const outfitsSimilares = {
        'Outfit Elegante': [
            { nombre: 'Outfit Elegante Similar 1', imagen: 'imagenes/similar1.png' },
            { nombre: 'Outfit Elegante Similar 2', imagen: 'imagenes/similar2.png' },
            { nombre: 'Outfit Elegante Similar 3', imagen: 'imagenes/similar3.png' }
        ],
        'Outfit Vintage': [
            { nombre: 'Outfit Vintage Similar 1', imagen: 'imagenes/similar4.png' },
            { nombre: 'Outfit Vintage Similar 2', imagen: 'imagenes/similar5.png' },
            { nombre: 'Outfit Vintage Similar 3', imagen: 'imagenes/similar6.png' }
        ],
        'Outfit Hipster': [
            { nombre: 'Outfit Hipster Similar 1', imagen: 'imagenes/similar7.png' },
            { nombre: 'Outfit Hipster Similar 2', imagen: 'imagenes/similar8.png' },
            { nombre: 'Outfit Hipster Similar 3', imagen: 'imagenes/similar9.png' }
        ]
    };

    // Abrir modales
    loginBtn.addEventListener('click', function() {
        loginModal.style.display = 'block';
    });

    registerBtn.addEventListener('click', function() {
        registerModal.style.display = 'block';
    });

    // Cerrar modales
    closeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            loginModal.style.display = 'none';
            registerModal.style.display = 'none';
            congratsModal.style.display = 'none';
        });
    });

    // Cerrar al hacer clic fuera
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
        
        if(!username.trim() || !password.trim()) {
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
        
        if(!name.trim()) {
            alert('Por favor ingrese su nombre');
            return;
        }
        
        registerModal.style.display = 'none';
        mainScreen.style.display = 'none';
        stylesScreen.style.display = 'block';
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

    // Función para obtener el clima
    function obtenerClima() {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                
                weatherResult.textContent = "Buscando datos meteorológicos...";
                
                // Simulación (reemplazar con API real)
                setTimeout(() => {
                    weatherResult.innerHTML = `
                        <div>🌡️ Temperatura: 24°C</div>
                        <div>🌦 Condición: Soleado</div>
                    `;
                }, 1500);
                
            }, function(error) {
                console.error("Error de geolocalización:", error);
                weatherResult.textContent = "Clima: Soleado, 24°C";
            });
        } else {
            weatherResult.textContent = "Clima: Soleado, 24°C";
        }
    }

    // Continuar a outfits
    continuarBtn.addEventListener('click', function() {
        climaScreen.style.display = 'none';
        outfitsScreen.style.display = 'block';
    });

    // Configurar botones de retroceso
    const backButtons = document.querySelectorAll('.back-btn');
    
    backButtons.forEach(button => {
        button.addEventListener('click', function() {
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
        });
    });

    // Botones "Me gusta"
    function setupLikeButtons() {
        document.querySelectorAll('.like-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const card = this.closest('.outfit-card');
                const img = card.querySelector('.outfit-image').alt;
                
                this.innerHTML = '<span>✓</span> ¡Me gusta!';
                this.style.backgroundColor = '#45a049';
                
                congratsModal.style.display = 'block';
            });
        });
    }

    // Botón para volver a estilos
    nuevoEstiloBtn.addEventListener('click', function() {
        congratsModal.style.display = 'none';
        outfitsScreen.style.display = 'none';
        stylesScreen.style.display = 'block';
    });
    
    // Botones "Ver similares"
    outfitsScreen.querySelectorAll('.more-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const card = this.closest('.outfit-card');
            currentOutfit = card.querySelector('.outfit-image').alt;
            
            outfitsScreen.style.display = 'none';
            similaresScreen.style.display = 'block';
            
            cargarOutfitsSimilares(currentOutfit);
        });
    });

    // Función para cargar outfits similares
    function cargarOutfitsSimilares(outfitBase) {
        similaresRow.innerHTML = '';
        
        const similares = outfitsSimilares[outfitBase] || [];
        
        similares.forEach((outfit) => {
            const outfitCard = document.createElement('div');
            outfitCard.className = 'outfit-card';
            outfitCard.innerHTML = `
                <img src="${outfit.imagen}" alt="${outfit.nombre}" class="outfit-image">
                <div class="outfit-actions">
                    <button class="btn like-btn">✓ Me gusta</button>
                    <button class="btn more-btn">🔍 Ver similares</button>
                </div>
            `;
            similaresRow.appendChild(outfitCard);
        });
        
        // Configurar eventos para los nuevos botones
        setupLikeButtons();
        setupMoreButtons();
    }

    // Configurar botones "Ver similares" en outfits similares
    function setupMoreButtons() {
        similaresScreen.querySelectorAll('.more-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const card = this.closest('.outfit-card');
                currentOutfit = card.querySelector('.outfit-image').alt;
                cargarOutfitsSimilares(currentOutfit);
            });
        });
    }

    // Configurar eventos iniciales
    setupLikeButtons();
});