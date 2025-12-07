/** This payment handles the checkout payment.
 * It has a different functionality from the payment success js file, beacuse here it checks the total of the payment.
 */

/** Initializes the PayPal payment button for the cart page */

window.initPayPalButtons = function () {
    

    paypal.Buttons({

        // Styling the PayPal button
        style: {
            layout: 'vertical',
            color: 'gold',
            shape: 'pill',
            label: 'pay',
        },

        // Create the order on the PayPal's side
        createOrder: function (data, actions) {
            console.log("Total price:", window.total); 
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: window.total.toString()  // Dynamically fetch the total price
                    },
                    description: "FitTrack Cart Checkout"
                }]
            });
        },

        // Called when the payment is successfully approved
        onApprove: function (data, actions) {
            return actions.order.capture().then(function (details) {
                console.log("Payment approved:", details); // Used for debugging during the deployment

                // Redirect the user to a success page or confirmation page
                window.location.href = "/fitshop/success/?orderID=" + data.orderID;
            });
        },

        // Error handling if PayPal payment fails
        onError: function (err) {
            console.error("PayPal ERROR:", err);
            alert("Payment failed. Try again.");
        }

    }).render("#paypal-button-container"); // Render the PayPal button inside the container
};
