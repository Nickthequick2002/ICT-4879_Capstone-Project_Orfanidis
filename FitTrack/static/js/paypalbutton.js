/** Initliazes the paypal payment button
 * for the FitTrack premium checkout flow 
 * and redirects to a success page
 */

window.initPayPalButtons = function () {

    paypal.Buttons({

        // Styling how the paypal button appears on the page
        style: {
            layout: 'vertical',
            color: 'gold',
            shape: 'pill',
            label: 'pay',
        },

        // Creates the order on the Paypal's side
        createOrder: function (data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: { value: "4.99" }, // This is the membership price
                    description: "FitTrack Premium Membership"
                }]
            });
        },

        // Called when the payment is successfully approved 
        onApprove: function (data, actions) {
            return actions.order.capture().then(function (details) {
                console.log("Payment approved:", details); // Used during the developemnt

                // Redirect the user to a success page
                window.location.href = "/payments/success/?orderID=" + data.orderID;
            });
        },

        // This is a generic error handling when there is an issue with PayPal
        onError: function (err) {
            console.error("PayPal ERROR:", err);
            alert("Payment failed. Try again.");
        }

    }).render("#paypal-button-container"); // Renders the PayPal button
};
