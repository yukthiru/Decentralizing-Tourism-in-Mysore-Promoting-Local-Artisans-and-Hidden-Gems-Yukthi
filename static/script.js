document.addEventListener('DOMContentLoaded', () => {

    // --- MOBILE MENU & DROPDOWN TOGGLE ---
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => navLinks.classList.toggle('active'));
    }
    
    const dropdownToggle = document.querySelector('.dropdown-toggle');
    if (dropdownToggle && window.innerWidth <= 768) {
        dropdownToggle.addEventListener('click', (e) => {
            e.preventDefault();
            e.target.parentElement.classList.toggle('active');
        });
    }

    // --- FADE IN ON SCROLL ---
    const faders = document.querySelectorAll('.fade-in');
    const appearOnScroll = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('appear');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" });
    faders.forEach(fader => appearOnScroll.observe(fader));

    // --- BACK TO TOP BUTTON ---
    const backToTopBtn = document.getElementById('back-to-top');
    if (backToTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) backToTopBtn.classList.add('visible');
            else backToTopBtn.classList.remove('visible');
        });
        backToTopBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // --- MARKETPLACE FILTERS ---
    const marketFilter = document.getElementById('market-filter');
    const productGrid = document.getElementById('product-grid');
    if (marketFilter && productGrid) {
        window.fetchProducts = (category) => {
            productGrid.innerHTML = '<p>Loading products...</p>';
            fetch(`/api/products?category=${category}`)
                .then(r => r.json())
                .then(data => {
                    productGrid.innerHTML = '';
                    if (data.length === 0) { productGrid.innerHTML = '<p>No products found.</p>'; return; }
                    data.forEach(p => {
                        const card = document.createElement('div');
                        card.className = 'card product-card fade-in appear';
                        card.innerHTML = `
                            <h3>${p.product_name}</h3>
                            <span class="card-badge">${p.category}</span>
                            <p>${p.description}</p>
                            <p class="product-price">₹${p.price_inr}</p>
                            <p><small>By: <a href="/artisans/${p.artisan_id}" style="color:var(--saffron); text-decoration:underline;">${p.artisan_name}</a></small></p>
                            <a href="https://wa.me/${p.artisan_whatsapp ? p.artisan_whatsapp.replace(/\D/g,'') : ''}?text=I'm interested in ${encodeURIComponent(p.product_name)}" target="_blank" class="btn btn-primary" style="margin-top:auto;">Contact Artisan</a>
                        `;
                        productGrid.appendChild(card);
                    });
                });
        };
        marketFilter.addEventListener('click', (e) => {
            if (e.target.classList.contains('filter-btn')) {
                document.querySelectorAll('#market-filter .filter-btn').forEach(btn => btn.classList.remove('active'));
                e.target.classList.add('active');
                fetchProducts(e.target.dataset.filter);
            }
        });
    }

    // --- HIDDEN GEMS MAP ---
    if (document.getElementById('gems-map')) {
        window.initGemsMap = () => {
            const map = L.map('gems-map').setView([12.3051, 76.6551], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap' }).addTo(map);
            
            const markers = [];
            const grid = document.getElementById('all-gems-grid');
            
            fetch('/api/gems/map').then(r => r.json()).then(data => {
                const renderGems = () => {
                    markers.forEach(m => map.removeLayer(m));
                    markers.length = 0;
                    grid.innerHTML = '';
                    
                    const checkedCats = Array.from(document.querySelectorAll('#map-filters input:checked')).map(i => i.value);
                    
                    data.forEach(gem => {
                        if(checkedCats.includes(gem.category)) {
                            if(gem.lat && gem.lng) {
                                const m = L.marker([gem.lat, gem.lng]).addTo(map);
                                m.bindPopup(`<b>${gem.name}</b><br><i>${gem.category}</i><br><a href="${gem.directions_url}" target="_blank">Directions</a>`);
                                markers.push(m);
                            }
                            const card = document.createElement('div');
                            card.className = 'card fade-in appear';
                            card.innerHTML = `
                                <h3>${gem.name}</h3>
                                <span class="card-badge">${gem.category}</span>
                                <p>${gem.description}</p>
                                ${gem.local_tip ? `<p class="local-secret">💡 ${gem.local_tip}</p>` : ''}
                                <p><small>Time: ${gem.best_time_to_visit || 'Anytime'} | Fee: ${gem.entry_fee || 'Free'}</small></p>
                                <a href="${gem.directions_url}" target="_blank" class="btn btn-secondary" style="margin-top:auto;">Directions</a>
                            `;
                            grid.appendChild(card);
                        }
                    });
                };
                renderGems();
                document.getElementById('map-filters').addEventListener('change', renderGems);
            });
        };
        window.initGemsMap();
    }

    // --- FOOD DISCOVERY ---
    if (document.getElementById('food-grid')) {
        window.initFoodDiscovery = () => {
            const map = L.map('food-map').setView([12.3051, 76.6551], 12);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
            const markers = [];
            const grid = document.getElementById('food-grid');
            const vegToggle = document.getElementById('veg-toggle');
            
            const fetchFood = (type) => {
                const veg = vegToggle.checked;
                grid.innerHTML = '<p>Loading food spots...</p>';
                fetch(`/api/food?type=${type}&veg=${veg}`).then(r => r.json()).then(data => {
                    markers.forEach(m => map.removeLayer(m));
                    markers.length = 0;
                    grid.innerHTML = '';
                    
                    data.forEach(f => {
                        if(f.lat && f.lng) {
                            const m = L.marker([f.lat, f.lng]).addTo(map);
                            m.bindPopup(`<b>${f.name}</b><br>${f.specialty_dish}`);
                            markers.push(m);
                        }
                        const card = document.createElement('div');
                        card.className = 'card food-card fade-in appear';
                        card.innerHTML = `
                            <h3>${f.name} ${f.is_vegetarian ? '🟢' : '🔴'}</h3>
                            <span class="card-badge">${f.food_type}</span>
                            <p>${f.description}</p>
                            <p><b>Must Try:</b> ${f.specialty_dish}</p>
                            <p class="price-range">${f.price_range}</p>
                            ${f.local_secret ? `<p class="local-secret">🤫 ${f.local_secret}</p>` : ''}
                        `;
                        grid.appendChild(card);
                    });
                });
            };
            
            fetchFood('All');
            vegToggle.addEventListener('change', () => {
                const activeType = document.querySelector('#food-filter .active').dataset.filter;
                fetchFood(activeType);
            });
            document.getElementById('food-filter').addEventListener('click', (e) => {
                if (e.target.classList.contains('filter-btn')) {
                    document.querySelectorAll('#food-filter .filter-btn').forEach(btn => btn.classList.remove('active'));
                    e.target.classList.add('active');
                    fetchFood(e.target.dataset.filter);
                }
            });
        };
        window.initFoodDiscovery();
    }

    // --- WALKING TOUR GENERATOR ---
    const tourForm = document.getElementById('tour-form');
    if (tourForm) {
        tourForm.addEventListener('submit', (e) => {
            e.preventDefault();
            document.getElementById('tour-spinner').style.display = 'block';
            document.getElementById('generate-btn').disabled = true;
            
            const interests = Array.from(document.querySelectorAll('.interest-check:checked')).map(i => i.value);
            const payload = {
                duration_hours: document.getElementById('duration').value,
                start_location: document.getElementById('start-location').value,
                pace: document.getElementById('pace').value,
                interests: interests
            };
            
            fetch('/api/generate-tour', {
                method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
            }).then(r => r.json()).then(data => {
                document.getElementById('tour-spinner').style.display = 'none';
                document.getElementById('generate-btn').disabled = false;
                document.getElementById('tour-form-container').style.display = 'none';
                document.getElementById('tour-results').style.display = 'block';
                
                const tl = document.getElementById('tour-timeline');
                tl.innerHTML = '';
                const map = L.map('tour-map').setView([12.3051, 76.6551], 14);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
                const latlngs = [];
                
                data.stops.forEach(stop => {
                    tl.innerHTML += `
                        <div class="timeline-item">
                            <h4>${stop.order}. ${stop.name} <span class="card-badge" style="float:right;">${stop.type}</span></h4>
                            <p>${stop.description}</p>
                            <p><small>⏱ ${stop.duration_mins} mins | 🚶 Walking from prev: ${stop.walking_from_prev}</small></p>
                            ${stop.tip ? `<p class="local-secret">${stop.tip}</p>` : ''}
                        </div>
                    `;
                    if(stop.lat && stop.lng) {
                        latlngs.push([stop.lat, stop.lng]);
                        L.marker([stop.lat, stop.lng]).addTo(map).bindPopup(stop.name);
                    }
                });
                if(latlngs.length > 0) {
                    L.polyline(latlngs, {color: 'red'}).addTo(map);
                    map.fitBounds(L.polyline(latlngs).getBounds());
                }
                
                document.getElementById('tour-narrative').innerHTML = `
                    <p><b>Total Distance:</b> ${data.total_distance_km} | <b>Total Time:</b> ${data.total_time_mins}</p>
                    <p>${data.tour_narrative}</p>
                `;
            }).catch(e => {
                alert("Error generating tour. If API key is missing, ensure fallback works.");
                document.getElementById('tour-spinner').style.display = 'none';
                document.getElementById('generate-btn').disabled = false;
            });
        });
        document.getElementById('regenerate-btn').addEventListener('click', () => {
            document.getElementById('tour-results').style.display = 'none';
            document.getElementById('tour-form-container').style.display = 'block';
        });
    }

    // --- TOUR PLANNER ---
    const plannerForm = document.getElementById('planner-form');
    if(plannerForm) {
        plannerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            document.getElementById('planner-spinner').style.display = 'block';
            
            const interests = Array.from(document.querySelectorAll('.plan-interest:checked')).map(i => i.value);
            const payload = {
                budget_inr: document.getElementById('budget').value,
                days: document.getElementById('days').value,
                travelers: document.getElementById('travelers').value,
                interests: interests,
                accommodation_type: document.getElementById('stay-type').value,
                dietary_preference: document.getElementById('diet').value
            };
            
            fetch('/api/plan-tour', {
                method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
            }).then(r => r.json()).then(data => {
                document.getElementById('planner-spinner').style.display = 'none';
                document.getElementById('planner-results').style.display = 'block';
                
                const stayGrid = document.getElementById('stay-suggestions');
                stayGrid.innerHTML = '';
                data.stay_suggestions.forEach(s => {
                    stayGrid.innerHTML += `
                        <div class="card">
                            <h3>${s.name}</h3>
                            <p><b>Type:</b> ${s.type}</p>
                            <p class="price-range">₹${s.price_per_night_inr} / night</p>
                            <p><small>${s.amenities}</small></p>
                        </div>
                    `;
                });
                
                const acc = document.getElementById('itinerary-accordion');
                acc.innerHTML = '';
                data.itinerary.forEach((day, idx) => {
                    acc.innerHTML += `
                        <div class="day-accordion">
                            <div class="day-header" onclick="this.nextElementSibling.classList.toggle('active')">
                                Day ${day.day} <span>&#9662;</span>
                            </div>
                            <div class="day-content ${idx === 0 ? 'active' : ''}">
                                <p><b>Morning:</b> ${day.morning}</p>
                                <p><b>Afternoon:</b> ${day.afternoon}</p>
                                <p><b>Evening:</b> ${day.evening}</p>
                                <p><b>Meals:</b> ${day.meals}</p>
                                <p><b>Est. Spend:</b> ₹${day.estimated_spend}</p>
                            </div>
                        </div>
                    `;
                });
                
                const total = data.budget_breakdown.total || 1;
                document.querySelector('.budget-segment.accom').style.width = (data.budget_breakdown.accommodation / total * 100) + '%';
                document.querySelector('.budget-segment.food').style.width = (data.budget_breakdown.food / total * 100) + '%';
                document.querySelector('.budget-segment.trans').style.width = (data.budget_breakdown.transport / total * 100) + '%';
                document.querySelector('.budget-segment.act').style.width = ((data.budget_breakdown.activities + data.budget_breakdown.artisan_purchases) / total * 100) + '%';
                
                document.getElementById('budget-legend').innerHTML = `
                    <span>🟩 Accom: ₹${data.budget_breakdown.accommodation}</span>
                    <span>🟧 Food: ₹${data.budget_breakdown.food}</span>
                    <span>🟦 Trans: ₹${data.budget_breakdown.transport}</span>
                    <span>🟪 Acts: ₹${data.budget_breakdown.activities + data.budget_breakdown.artisan_purchases}</span>
                `;
                document.getElementById('budget-status').textContent = `Status: ${data.budget_status.toUpperCase()} (Total: ₹${total})`;
                document.getElementById('planner-tips').innerHTML = data.tips.map(t => `<li>${t}</li>`).join('');
                
            }).catch(e => {
                alert("Error generating plan.");
                document.getElementById('planner-spinner').style.display = 'none';
            });
        });
    }

    // --- VIRTUAL MARKET ---
    if(document.getElementById('market-area-tabs')) {
        let sessionId = sessionStorage.getItem('mysore_cart_session');
        if(!sessionId) {
            sessionId = 'sess_' + Math.random().toString(36).substr(2, 9);
            sessionStorage.setItem('mysore_cart_session', sessionId);
        }
        
        const updateCartUI = () => {
            fetch(`/api/cart?session_id=${sessionId}`).then(r => r.json()).then(data => {
                document.getElementById('cart-count').textContent = data.length;
                const itemsContainer = document.getElementById('cart-items');
                itemsContainer.innerHTML = data.length ? '' : 'Cart is empty';
                
                let whatsappText = "Hello, I am interested in inquiring about the following items from the Virtual Market:%0A";
                
                data.forEach(item => {
                    itemsContainer.innerHTML += `
                        <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem; border-bottom:1px solid #eee; padding-bottom:0.5rem;">
                            <span>${item.product_name || item.stall_name}</span>
                            <button onclick="removeCartItem(${item.id})" style="background:none; border:none; color:red; cursor:pointer;">❌</button>
                        </div>
                    `;
                    whatsappText += `- ${item.product_name || item.stall_name}%0A`;
                });
                
                document.getElementById('send-inquiry-btn').onclick = () => {
                    if(data.length > 0) window.open(`https://wa.me/919000000000?text=${whatsappText}`, '_blank');
                };
            });
        };
        
        window.removeCartItem = (id) => {
            fetch(`/api/cart/${id}`, {method: 'DELETE'}).then(() => updateCartUI());
        };
        
        window.addToCart = (productId, stallId) => {
            fetch('/api/cart/add', {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({session_id: sessionId, product_id: productId, stall_id: stallId})
            }).then(() => {
                document.getElementById('cart-body').style.display = 'block';
                updateCartUI();
            });
        };
        
        window.initVirtualMarket = () => {
            updateCartUI();
            document.getElementById('cart-toggle').addEventListener('click', () => {
                const b = document.getElementById('cart-body');
                b.style.display = b.style.display === 'none' ? 'block' : 'none';
            });
            
            const fetchStalls = (area) => {
                const c = document.getElementById('stalls-container');
                c.innerHTML = '<p>Loading stalls...</p>';
                fetch(`/api/market-stalls?area=${area}`).then(r => r.json()).then(data => {
                    c.innerHTML = '';
                    data.forEach(stall => {
                        c.innerHTML += `
                            <div class="card stall-card fade-in appear" style="flex-direction:row; flex-wrap:wrap; gap:2rem; align-items:center;">
                                <div style="flex:2; min-width:300px;">
                                    <h3>${stall.stall_name} <span class="card-badge">${stall.market_area}</span></h3>
                                    <p><b>Specialty:</b> ${stall.products_sold}</p>
                                    <p>${stall.story}</p>
                                    <p><small>Open: ${stall.open_days} | ${stall.open_time}</small></p>
                                    ${stall.demo_video_url ? `<button class="btn btn-secondary">Watch Demo</button>` : ''}
                                    <button class="btn btn-primary" onclick="addToCart(null, ${stall.id})" style="margin-top:1rem;">Add to Inquiry</button>
                                </div>
                            </div>
                        `;
                    });
                });
            };
            
            fetchStalls('All');
            document.getElementById('market-area-tabs').addEventListener('click', (e) => {
                if(e.target.classList.contains('filter-btn')) {
                    document.querySelectorAll('#market-area-tabs .filter-btn').forEach(btn => btn.classList.remove('active'));
                    e.target.classList.add('active');
                    fetchStalls(e.target.dataset.area);
                }
            });
            
            let walkInterval;
            document.getElementById('virtual-walk-toggle').addEventListener('click', (e) => {
                if(walkInterval) {
                    clearInterval(walkInterval);
                    walkInterval = null;
                    e.target.textContent = 'Start Virtual Walk';
                } else {
                    e.target.textContent = 'Stop Virtual Walk';
                    let cards = document.querySelectorAll('.stall-card');
                    let idx = 0;
                    walkInterval = setInterval(() => {
                        if(idx >= cards.length) { clearInterval(walkInterval); e.target.textContent = 'Start Virtual Walk'; return; }
                        cards[idx].scrollIntoView({behavior: 'smooth', block: 'center'});
                        idx++;
                    }, 3000);
                }
            });
        };
        window.initVirtualMarket();
    }

    // --- EXPLORE GEMS ---
    const gemFilter = document.querySelector('.explore-header .filter-bar');
    const gemGrid = document.getElementById('gem-grid');
    if (gemFilter && gemGrid) {
        window.fetchExploreGems = (category) => {
            gemGrid.innerHTML = '<p>Loading gems...</p>';
            fetch(`/api/gems?category=${category}`)
                .then(r => r.json())
                .then(data => {
                    gemGrid.innerHTML = '';
                    if (data.length === 0) { gemGrid.innerHTML = '<p>No gems found.</p>'; return; }
                    data.forEach(gem => {
                        const card = document.createElement('div');
                        card.className = 'card fade-in appear';
                        card.innerHTML = `
                            <h3>${gem.name}</h3>
                            <span class="card-badge">${gem.category}</span>
                            <p>${gem.description}</p>
                            ${gem.local_tip ? `<p class="local-secret">💡 ${gem.local_tip}</p>` : ''}
                            <a href="${gem.directions_url}" target="_blank" class="btn btn-secondary" style="margin-top:auto;">Get Directions</a>
                        `;
                        gemGrid.appendChild(card);
                    });
                });
        };
        gemFilter.addEventListener('click', (e) => {
            if (e.target.classList.contains('filter-btn')) {
                gemFilter.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
                e.target.classList.add('active');
                fetchExploreGems(e.target.dataset.filter);
            }
        });
        fetchExploreGems('All');
    }

    const contactForm = document.getElementById('contact-form');
    const formMessage = document.getElementById('form-message');
    if (contactForm && formMessage) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;
            fetch('/contact', {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: document.getElementById('name').value,
                    email: document.getElementById('email').value,
                    message: document.getElementById('message').value
                })
            }).then(r => r.json()).then(data => {
                submitBtn.textContent = originalText; submitBtn.disabled = false;
                if (data.success) {
                    formMessage.textContent = 'Message sent successfully.';
                    formMessage.className = 'success-msg local-secret';
                    formMessage.style.display = 'block';
                    contactForm.reset();
                }
            });
        });
    }
});
