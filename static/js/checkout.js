$(document).ready(function () {

    $('.payWithRazorpay').click(function (e) {
        e.preventDefault();

        var fname = $("[name = 'fname']").val();
        var lname = $("[name = 'lname']").val();
        var email = $("[name = 'email']").val();
        var phone = $("[name = 'phone']").val();
        var address = $("[name = 'address']").val();
        var city = $("[name = 'city']").val();
        var state = $("[name = 'state']").val();
        var country = $("[name = 'country']").val();
        var pincode = $("[name = 'pincode']").val();

        if(fname == "" || lname == "" || email == "" || phone == "" || address == "" || city == "" || state == "" || country == "" || pincode == "")
        {
            alert("All fields are mandatory");
            return false
        }
        else
        {
            var options = {
            "key": "YOUR_KEY_ID", // Enter the Key ID generated from the Dashboard
            "amount": "50000", // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
            "currency": "INR",
            "name": "Acme Corp", //your business name
            "description": "Test Transaction",
            "image": "https://example.com/your_logo",
            "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
            "handler": function (response){
                alert(response.razorpay_payment_id);
                alert(response.razorpay_order_id);
                alert(response.razorpay_signature)
            },
            "prefill": {
                "name": "Gaurav Kumar", //your customer's name
                "email": "gaurav.kumar@example.com",
                "contact": "9000090000"
            },
            "notes": {
                "address": "Razorpay Corporate Office"
            },
            "theme": {
                "color": "#3399cc"
            }
        };
        var rzp1 = new Razorpay(options);

        rzp1.open();

        }


        
    });
});