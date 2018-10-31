function addToCart(good_id) {
    axios({
            method: 'post',
            url: '/api/cart/',
            data: {
                good_id: good_id
            },
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        },
    )
        .then(function (response) {
            cart = response.data.cart;
            item = findInCart(good_id, cart);
            $('#now_count').text(item.count)
        })
        .catch(function (error) {
            console.log(error);
        });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function findInCart(id, cart) {
    for (i=0;i<cart.length;i++){
        if (cart[i].good.id == id){
            return cart[i]
        }
    }

}