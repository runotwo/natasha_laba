var QQ;
var search_items = {
    date__gte: null,
    date__lte: null
};

var countries_list = [];

var Voucher = React.createClass({

    getInitialState: function () {
        return {
            selected: false
        }
    },

    render: function () {
        var rowClass = 't-row row v-row font-3';
        if (this.state.selected) {
            rowClass += ' v-row-selected';
        }
        return (
            <div className={rowClass}>
                <div className="col-3 cell">{this.props.title}</div>
                <div className="col-3 cell">{this.props.count}</div>
                <div className="col-3 cell">{this.props.sum_price}</div>
                <div className="col-3 cell">{this.props.sum_val}</div>
            </div>
        )
    },
});

function List(props) {
    const vouchers = props.v;
    const listItems = vouchers.map((voucher) =>
        <Voucher title={voucher.name}
                 count={voucher.number}
                 sum_price={voucher.count}
                 sum_val={voucher.total}
                 />
    );
    return (
        <div>{listItems}</div>
    );
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


function updateFilter() {
    var field = $('#filters-details');
    var text = '';
    if (search_items.museum_id) {
        var title = $('.listitem[data-id="' + search_items.museum_id + '"]').text();
        text += '(' + title;
        if (search_items.date__gte) text += ', '
    }
    if (search_items.date__gte) {
        if (!text) {
            text += '('
        }
        text += search_items.date__gte;
        if (search_items.date__lte) {
            text += ' — ' + search_items.date__lte;
        }
    }
    if (text) {
        text += ')'
    }
    field.text(text)
}

function requestVouchers() {
    var url = '/analytics_u/items/?';
    for (var key in search_items) {
        if (search_items[key]) {
            url += key + '=' + search_items[key] + '&'
        }
    }
    axios.get(url)
        .then(function (response) {
            var v = response.data;
            ReactDOM.render(<List v={v}/>, document.getElementById('elems'));
            if (v.length) {
                $('#not-found').addClass('hidden')
            }
            else
                $('#not-found').removeClass('hidden')

        })
        .catch(function (error) {
            console.log(error);
        }).then(function () {
    });
}

function getCountriesList(word) {
    return countries_list.filter(wl => wl.startsWith(word)).slice(0, 5)
}

$(function () {
    requestVouchers();


    $('button[name="daterange"]').daterangepicker({
        "locale": {
            "format": "DD.MM.YY",
            "separator": " - ",
            "applyLabel": "Выбрать",
            "cancelLabel": "Очистить",
            "daysOfWeek": [
                "Вс",
                "Пн",
                "Вт",
                "Ср",
                "Чт",
                "Пт",
                "Сб"
            ],
            "monthNames": [
                "Январь",
                "Февраль",
                "Март",
                "Апрель",
                "Май",
                "Июнь",
                "Июль",
                "Август",
                "Сентябрь",
                "Октябрь",
                "Ноябрь",
                "Декабрь"
            ],
            "firstDay": 1
        }
    }, function (start, end, label) {
        search_items.date__gte = start.format('DD.MM.YY');
        console.log(end);
        if (end) search_items.date__lte = end.format('DD.MM.YY');
        if (search_items.date__gte === search_items.date__lte) {
            search_items.date__lte = null
        }
        requestVouchers();
        updateFilter();
    });
    $('button[name="daterange"]').on('cancel.daterangepicker', function (ev, picker) {
        search_items.date__gte = null;
        search_items.date__lte = null;
        requestVouchers();
        updateFilter();
    });
    $('button[name="daterange"]').on('apply.daterangepicker', function (ev, picker) {
        picker.callback(picker.startDate, picker.endDate, null)
    });
});

$(document).keyup(function (e) {
    if (e.keyCode == 27) {
        var focused = document.activeElement;
        $(focused).val(focused.dataset.default);
        $(focused).blur()
    }
    if (e.keyCode == 13) {
        var focused = document.activeElement;
        $(focused).blur()
    }
});

function mainSelect() {
    var selected = $('.v-row-selected');
    var all = $('.v-row');
    if (selected.length == all.length) unselectAll();
    else selectAll();
}

$('.dropdown').on("show.bs.dropdown", function (e) {
    setTimeout(function (target) {
        $(target).addClass('dropup');
        $(target).removeClass('dropdown');
    }, 50, e.target);
});

$('.dropdown').on("hide.bs.dropdown", function (e) {
    setTimeout(function (target) {
        $(target).addClass('dropdown');
        $(target).removeClass('dropup');
    }, 50, e.target);
});

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}