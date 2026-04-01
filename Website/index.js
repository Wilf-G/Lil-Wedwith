/* ============================================================
   1. ADD TO CART LOGIC (Home & Product Page)
   ============================================================ */
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('order-btn') || e.target.classList.contains('add-btn')) {
        
        const itemName = e.target.getAttribute('data-name');
        const itemPrice = parseFloat(e.target.getAttribute('data-price'));
        
        // Find quantity input in the same card
        const qtyInput = e.target.parentElement.querySelector('.qty-input');
        const quantity = parseInt(qtyInput.value) || 1;

        let cart = JSON.parse(sessionStorage.getItem('foodCart')) || [];
        
        // Check if item already exists
        const existingItem = cart.find(item => item.name === itemName);
        if (existingItem) {
            existingItem.qty = quantity; 
        } else {
            cart.push({ name: itemName, price: itemPrice, qty: quantity });
        }
        
        sessionStorage.setItem('foodCart', JSON.stringify(cart));
        window.location.href = 'Checkout.html';
    }
});

/* ============================================================
   2. CHECKOUT UI & SUMMARY
   ============================================================ */
if (window.location.pathname.includes('Checkout.html')) {
    renderSummary();
}

function renderSummary() {
    const cart = JSON.parse(sessionStorage.getItem('foodCart')) || [];
    const summaryList = document.getElementById('cart-items-list');
    const totalDisplay = document.getElementById('total-price');

    if (!summaryList) return;
    summaryList.innerHTML = ""; 

    if (cart.length === 0) {
        summaryList.innerHTML = "<p style='text-align:center;'>Your cart is empty.</p>";
        if(document.getElementById('proceed-to-service')) document.getElementById('proceed-to-service').style.display = 'none';
        if(totalDisplay) totalDisplay.innerText = "";
    } else {
        let total = 0;
        cart.forEach((item, index) => {
            const itemTotal = item.price * item.qty;
            total += itemTotal;
            summaryList.innerHTML += `
                <p>
                    <span>${item.qty}x ${item.name}</span>
                    <span>£${itemTotal.toFixed(2)}</span>
                    <button onclick="removeItem(${index})" style="background:#f0f0f0; border:1px solid #ccc; padding:2px 8px; font-size:11px;">Remove</button>
                </p>`;
        });
        if(totalDisplay) totalDisplay.innerText = `Total: £${total.toFixed(2)}`;
    }
}

window.removeItem = function(index) {
    let cart = JSON.parse(sessionStorage.getItem('foodCart')) || [];
    cart.splice(index, 1);
    sessionStorage.setItem('foodCart', JSON.stringify(cart));
    renderSummary();
};

document.getElementById('proceed-to-service')?.addEventListener('click', () => {
    document.getElementById('summary-section').style.display = 'none';
    document.getElementById('service-choice-section').style.display = 'block';
});

window.showDetailsForm = function(type) {
    document.getElementById('service-choice-section').style.display = 'none';
    document.getElementById('details-section').style.display = 'block';
    
    document.getElementById('delivery-fields').style.display = (type === 'delivery') ? 'block' : 'none';
    document.getElementById('table-fields').style.display = (type === 'table') ? 'block' : 'none';
    document.getElementById('form-title').innerText = (type === 'delivery') ? "Delivery Details" : "Table Booking";
};

/* ============================================================
   3. REAL-TIME CARD DETECTION
   ============================================================ */
const cardInput = document.getElementById('card-num');
const brandBadge = document.getElementById('card-brand-badge');

if (cardInput) {
    cardInput.addEventListener('input', function(e) {
        let val = e.target.value.replace(/\D/g, ''); 
        e.target.value = val.replace(/(.{4})/g, '$1 ').trim();
        brandBadge.style.opacity = val.length > 0 ? "1" : "0";
        
        if (val.startsWith('4')) {
            brandBadge.innerText = "Visa";
            cardInput.className = "visa-style";
        } else if (val.startsWith('5')) {
            brandBadge.innerText = "Mastercard";
            cardInput.className = "mastercard-style";
        } else {
            brandBadge.innerText = "Card";
            cardInput.className = "";
        }
    });
}

/* ============================================================
   4. FINAL SUBMISSION TO PYTHON DATABASE
   ============================================================ */
document.getElementById('final-order-form')?.addEventListener('submit', function(e) {
    e.preventDefault();

    const cart = JSON.parse(sessionStorage.getItem('foodCart')) || [];
    let total = 0;
    cart.forEach(item => total += (item.price * item.qty));

    // Determine if it's delivery or table based on which field is visible
    const isDelivery = document.getElementById('delivery-fields').style.display === 'block';
    
    const orderData = {
        name: document.getElementById('cust-name').value,
        type: isDelivery ? 'Delivery' : 'Table',
        location: isDelivery ? document.getElementById('address').value : document.getElementById('table-no').value,
        total: total,
        items: cart
    };

    // !!! REPLACE THIS URL WITH YOUR COPIED "FORWARDED ADDRESS" FROM THE PORTS TAB !!!
    const BACKEND_URL = 'https://jubilant-orbit-7v7jvgqw75992xv7x-5000.app.github.dev/api/order';

    fetch(BACKEND_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
        // Success: Hide form and show receipt with Order Number
        document.getElementById('details-section').style.display = 'none';
        const receipt = document.getElementById('order-receipt');
        const content = document.getElementById('receipt-content');
        
        content.innerHTML = `
            <h3 style="color:var(--navy); font-size:24px;">Order #${data.order_id}</h3>
            <p>Thank you, <b>${orderData.name}</b>! Your order has been sent to the kitchen.</p>
            <p>A receipt has been generated for our staff.</p>
        `;
        receipt.style.display = 'block';
        
        // Clear cart memory
        sessionStorage.removeItem('foodCart');
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Server error! Please make sure your Python server is running and Port 5000 is Public.");
    });
});