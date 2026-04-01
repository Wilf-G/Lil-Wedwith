/* ============================================================
   1. ADD TO CART LOGIC (Home & Product Page)
   ============================================================ */
document.addEventListener('click', function(e) {
    // Looks for any button with class 'order-btn' or 'add-btn'
    if (e.target.classList.contains('order-btn') || e.target.classList.contains('add-btn')) {
        
        const itemName = e.target.getAttribute('data-name');
        const itemPrice = parseFloat(e.target.getAttribute('data-price'));
        
        // Find the quantity input in the same card as the button
        const qtyInput = e.target.parentElement.querySelector('.qty-input');
        const quantity = parseInt(qtyInput.value) || 1;

        // Use sessionStorage (clears when tab closes) to store the cart
        let cart = JSON.parse(sessionStorage.getItem('foodCart')) || [];
        
        // Check if item already exists in cart
        const existingItem = cart.find(item => item.name === itemName);
        if (existingItem) {
            existingItem.qty = quantity; // Update quantity
        } else {
            cart.push({ name: itemName, price: itemPrice, qty: quantity });
        }
        
        // Save back to memory and go to checkout
        sessionStorage.setItem('foodCart', JSON.stringify(cart));
        window.location.href = 'Checkout.html';
    }
});

/* ============================================================
   2. CHECKOUT PAGE LOGIC (Summary & Flow)
   ============================================================ */
if (window.location.pathname.includes('Checkout.html')) {
    renderSummary();
}

// Draws the items and total in the Checkout Summary box
function renderSummary() {
    const cart = JSON.parse(sessionStorage.getItem('foodCart')) || [];
    const summaryList = document.getElementById('cart-items-list');
    const totalDisplay = document.getElementById('total-price');

    if (!summaryList) return;

    // Clear the box before redrawing (Prevents duplicates on refresh)
    summaryList.innerHTML = ""; 

    if (cart.length === 0) {
        summaryList.innerHTML = "<p style='text-align:center; padding:20px;'>Your cart is empty.</p>";
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
                    <button onclick="removeItem(${index})" style="background:#f0f0f0; color:#333; padding:5px 10px; font-size:12px; border-radius:5px; border:1px solid #ccc;">Remove</button>
                </p>`;
        });
        if(totalDisplay) totalDisplay.innerText = `Total: £${total.toFixed(2)}`;
    }
}

// Function to remove a specific item from the list
window.removeItem = function(index) {
    let cart = JSON.parse(sessionStorage.getItem('foodCart')) || [];
    cart.splice(index, 1);
    sessionStorage.setItem('foodCart', JSON.stringify(cart));
    renderSummary();
};

// Flow: Step 1 (Summary) -> Step 2 (Service Choice)
document.getElementById('proceed-to-service')?.addEventListener('click', () => {
    document.getElementById('summary-section').style.display = 'none';
    document.getElementById('service-choice-section').style.display = 'block';
});

// Flow: Step 2 (Choice) -> Step 3 (Form Details)
window.showDetailsForm = function(type) {
    document.getElementById('service-choice-section').style.display = 'none';
    document.getElementById('details-section').style.display = 'block';
    
    const deliveryFields = document.getElementById('delivery-fields');
    const tableFields = document.getElementById('table-fields');
    const formTitle = document.getElementById('form-title');

    if (type === 'delivery') {
        formTitle.innerText = "Delivery Details";
        deliveryFields.style.display = 'block';
        tableFields.style.display = 'none';
    } else {
        formTitle.innerText = "Table Booking Details";
        deliveryFields.style.display = 'none';
        tableFields.style.display = 'block';
    }
};

/* ============================================================
   3. REAL-TIME CARD DETECTION & VALIDATION
   ============================================================ */
const cardInput = document.getElementById('card-num');
const brandBadge = document.getElementById('card-brand-badge');

if (cardInput) {
    cardInput.addEventListener('input', function(e) {
        // 1. Format digits with spaces (1234 5678...)
        let val = e.target.value.replace(/\D/g, ''); 
        e.target.value = val.replace(/(.{4})/g, '$1 ').trim();
        
        // 2. Show/Hide Badge
        brandBadge.style.opacity = val.length > 0 ? "1" : "0";
        
        // 3. Detect Brand (Visa = 4, Mastercard = 5)
        if (val.startsWith('4')) {
            brandBadge.innerText = "Visa";
            cardInput.className = "visa-style";
        } else if (val.startsWith('5')) {
            brandBadge.innerText = "Mastercard";
            cardInput.className = "mastercard-style";
        } else if (val.length > 0) {
            brandBadge.innerText = "Credit Card";
            cardInput.className = "";
        }
    });
}

// Final Order Completion
document.getElementById('final-order-form')?.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Simple validation for card length
    const rawCard = document.getElementById('card-num').value.replace(/\s/g, '');
    if (rawCard.length < 16) {
        alert("Please enter a valid 16-digit card number.");
        return;
    }

    // Hide form and show Receipt
    document.getElementById('details-section').style.display = 'none';
    const receipt = document.getElementById('order-receipt');
    const content = document.getElementById('receipt-content');
    
    content.innerHTML = `
        <p>Thank you for your purchase, <strong>${document.getElementById('cust-name').value}</strong>!</p>
        <p>Your payment has been processed and your order is being prepared.</p>
    `;
    receipt.style.display = 'block';
    
    // Wipe the session cart after order is finished
    sessionStorage.removeItem('foodCart');
});