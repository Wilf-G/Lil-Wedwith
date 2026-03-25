/* ============================================================
   1. PRODUCT PAGE & HOME PAGE LOGIC
   Saves the food data when a user clicks any "Order" button
   ============================================================ */
document.addEventListener('click', function(e) {
    // This looks for any button with the ID starting with "Order_Now" 
    // or any button with the class "add-btn"
    if (e.target && (e.target.id.includes('Order_Now') || e.target.classList.contains('add-btn'))) {
        
        const itemName = e.target.getAttribute('data-name');
        const itemPrice = e.target.getAttribute('data-price');

        if (itemName && itemPrice) {
            const orderData = {
                name: itemName,
                price: parseFloat(itemPrice),
                quantity: 1
            };

            // Save to browser memory
            localStorage.setItem('selectedItem', JSON.stringify(orderData));

            // Move to checkout
            window.location.href = 'Checkout.html';
        }
    }
});

/* ============================================================
   2. CHECKOUT PAGE LOGIC
   Runs only when a user is on the checkout page and submits a form
   ============================================================ */
const checkoutForms = document.querySelectorAll('.option-box form');

if (checkoutForms.length > 0) {
    checkoutForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // Stop page from refreshing

            const rawData = localStorage.getItem('selectedItem');
            
            if (rawData) {
                const item = JSON.parse(rawData);
                const totalCost = item.price * item.quantity;

                // Hide the forms/options
                const optionsContainer = document.querySelector('.checkout-options');
                if (optionsContainer) optionsContainer.style.display = 'none';

                // Show the receipt (Make sure you added the "order-receipt" div to your HTML!)
                const receiptSection = document.getElementById('order-receipt');
                const receiptContent = document.getElementById('receipt-content');

                if (receiptSection && receiptContent) {
                    receiptContent.innerHTML = `
                        <p><strong>Customer:</strong> ${form.querySelector('input[type="text"]').value}</p>
                        <p><strong>Item:</strong> ${item.name}</p>
                        <p><strong>Quantity:</strong> ${item.quantity}</p>
                        <p><strong>Unit Price:</strong> £${item.price.toFixed(2)}</p>
                        <hr style="border: 1px solid #000b3d; margin: 15px 0;">
                        <h3 style="font-size: 22px; color: #000b3d;">Total Paid: £${totalCost.toFixed(2)}</h3>
                    `;
                    receiptSection.style.display = 'block';
                }

                // Clear the cart
                localStorage.removeItem('selectedItem');
            } else {
                alert("Please select an item from the menu first!");
                window.location.href = 'index.html';
            }
        });
    });
}