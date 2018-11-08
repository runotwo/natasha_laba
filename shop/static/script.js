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
    for (i = 0; i < cart.length; i++) {
        if (cart[i].good.id == id) {
            return cart[i]
        }
    }

}

function registrationSubmit() {
    email = $('#email')[0].value;
    pass = $('#pass')[0].value;
    pass_repeat = $('#pass-repeat')[0].value;
    first_name = $('#name')[0].value;
    phone = $('#phone')[0].value;
    send = true;
    if (!email) {
        $('#email').addClass('border-danger');
        $('#email').addClass('border');
        send = false;
    }
    if (!pass) {
        $('#pass').addClass('border-danger');
        $('#pass').addClass('border');
        send = false;
    }
    if (!pass_repeat) {
        $('#pass-repeat').addClass('border-danger');
        $('#pass-repeat').addClass('border');
        send = false;
    }
    if (!first_name) {
        $('#name').addClass('border-danger');
        $('#name').addClass('border');
        send = false;
    }
    if (!phone) {
        $('#phone').addClass('border-danger');
        $('#phone').addClass('border');
        send = false;
    }
    if (email) {
        $('#email').removeClass('border-danger');
        $('#email').removeClass('border')
    }
    if (pass) {
        $('#pass').removeClass('border-danger');
        $('#pass').removeClass('border')
    }
    if (pass_repeat) {
        $('#pass-repeat').removeClass('border-danger');
        $('#pass-repeat').removeClass('border')
    }
    if (first_name) {
        $('#name').removeClass('border-danger');
        $('#name').removeClass('border')
    }
    if (phone) {
        $('#phone').removeClass('border-danger');
        $('#phone').removeClass('border')
    }
    if (pass != pass_repeat) {
        $('#pass-repeat').addClass('border-danger');
        $('#pass-repeat').addClass('border');
        send = false;
    }
    if (send) {
        axios({
                method: 'post',
                url: '/registration/',
                data: {
                    email: email,
                    pass: pass,
                    first_name: first_name,
                    phone: phone
                },
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            },
        )
            .then(function (response) {
                window.location.replace(response.data.redirect)
            })
            .catch(function (error) {
                console.log(error);
            });
    }
}

$(function () {
    axios.get('/api/order/', {
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(function (response) {
            cart = response.data.cart;
            $('#nowItems').text(cart.length);
        })
        .catch(function (error) {
            console.log(error);
        });
});

app = new Vue({
    el: '#app',
    data: {
        order: false,
        delivery: true,
        cart: []
    },
    mounted: function () {
        self = this;
        axios.get('/api/order/', {
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
            .then(function (response) {
                self.cart = response.data.cart;
            })
            .catch(function (error) {
                console.log(error);
            });
    },
    methods: {
        deleteItem: function (id) {
            self = this;
            item = self.cart[id];
            axios({
                    method: 'delete',
                    url: '/api/cart/' + item.good.id,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                },
            )
                .then(function (response) {
                    self.cart = response.data.cart;
                    $('#nowItems').text(response.data.cart.length)
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
        addItem: function (id) {
            self = this;
            item = self.cart[id];
            axios({
                    method: 'post',
                    url: '/api/cart/',
                    data: {
                        good_id: item.good.id
                    },
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                },
            )
                .then(function (response) {
                    self.cart = response.data.cart;
                    $('#nowItems').text(response.data.cart.length)
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
        confirmOrder: function () {
            if (this.delivery) {
                city = $('#city')[0].value;
                street = $('#street')[0].value;
                house_number = $('#house_number')[0].value;
                apartment_number = $('#apartment_number')[0].value;
                index = $('#index')[0].value;
                send = true;
                if (!city) {
                    $('#city').addClass('border-danger');
                    $('#city').addClass('border');
                    send = false;
                }
                if (!street) {
                    $('#street').addClass('border-danger');
                    $('#street').addClass('border');
                    send = false;
                }
                if (!house_number) {
                    $('#house_number').addClass('border-danger');
                    $('#house_number').addClass('border');
                    send = false;
                }
                if (!apartment_number) {
                    $('#apartment_number').addClass('border-danger');
                    $('#apartment_number').addClass('border');
                    send = false;
                }
                if (!index) {
                    $('#index').addClass('border-danger');
                    $('#index').addClass('border');
                    send = false;
                }
                if (send) {
                    axios({
                            method: 'post',
                            url: '/order/',
                            data: {
                                city: city,
                                street: street,
                                house_number: house_number,
                                apartment_number: apartment_number,
                                index: index
                            },
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken')
                            }
                        },
                    )
                        .then(function (response) {
                            alert('Заказ создан');
                            window.location.replace(response.data.redirect)
                        })
                        .catch(function (error) {
                            console.log(error);
                        });

                }
            }
            else {
                axios({
                        method: 'post',
                        url: '/order/',
                        data: {},
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    },
                )
                    .then(function (response) {
                        alert('Заказ создан');
                        window.location.replace(response.data.redirect)
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
            }
        }
    }
});

