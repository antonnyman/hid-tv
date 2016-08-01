var now = moment()

// On load DOM
$(document).ready(function() {
    current()
    busTimes()
    reload()
    lunch()
    inOffice()

    $('.owl-carousel').owlCarousel({
            navigation: false,
            autoplay: true,
            items: 1,
            autoplayTimeout: 10000,
            dots: false,
            loop:true,
            mouseDrag: false,
            animateIn: 'fadeIn',
            animateOut: 'fadeOut'
        })
})

function current() {
    var lundLocale = moment().locale('sv')
    var tokyoLocale = moment().locale('jp')
    var sanMateoLocale = moment().locale('en')

    var nowLund = lundLocale.format('LT')
    var nowTokyo = tokyoLocale.tz('Asia/Tokyo').format('HH:mm')
    var nowSanMateo = sanMateoLocale.tz('America/Los_Angeles').format('LT')

    var dateLund = lundLocale.format('dd DD MMM')

    $('#time-lund').html(nowLund)
    $('#time-tokyo-time').html(nowTokyo)
    $('#time-sanmateo-time').html(nowSanMateo)

    $('#date-lund').html(dateLund.toUpperCase())

    setTimeout(current, 1000)
}

function busTimes() {
    $.getJSON('/bus-times', function(data) {
        
        $('#first-bus-time-no').html(data[0]['No'])
        $('#first-bus-time-destination').html(data[0]['Towards'])
        $('#first-bus-time').html(moment(data[0]['JourneyDateTime']).format('HH:mm'))

        $('#second-bus-time-no').html(data[1]['No'])
        $('#second-bus-time-destination').html(data[1]['Towards'])
        $('#second-bus-time').html(moment(data[1]['JourneyDateTime']).format('HH:mm'))
    })

    setTimeout(busTimes, 10000)
}

function reload() {
    
    $.getJSON('/get-reload', function(data) {
        if(data.result === "true") {
            location.reload()
        }
    })

    setTimeout(reload, 5000)
}

function lunch() {
    $.getJSON('/lunch', function(data) {
        var food = data.slice(1)

        var options = '<img src="static/img/fork.png" />'
        for(var i = 0; i < food.length; i++) {
            options += '<div class="lunch-item">' + food[i] + '</div>'
        }

        $('#lunch').html(options)

    })
}

function inOffice() {
    $.getJSON('/in-office', function(data) {
        var activePeople = ''
        var people = ''
        for(var i = 0; i < data.length; i++) {
            if(data[i].hasOwnProperty('location')) {
                if(data[i].location === "Mobilvägen") {
                    activePeople += '<div class="in-office-item"><img class="avatar-active" src="' + data[i].picture + '?sz=50"><span class="in-office-item-name">' + data[i].given_name + ' &dash; in office</span></div>'
                } else {
                    people += '<div class="in-office-item"><img class="avatar" src="' + data[i].picture + '?sz=50"><span class="in-office-item-name">' + data[i].given_name + '</span></div>'
                }
            } else if(data[i].vab === true) {
                people += '<div class="in-office-item"><img class="avatar" src="' + data[i].picture + '?sz=50"><span class="in-office-item-name">' + data[i].given_name + ' &dash; VAB</span></div>'
            
            } else if(data[i].vacation === true) {
                people += '<div class="in-office-item"><img class="avatar" src="' + data[i].picture + '?sz=50"><span class="in-office-item-name">' + data[i].given_name + ' &dash; vacation</span></div>'
            } else if(data[i].ooo === true) {
                people += '<div class="in-office-item"><img class="avatar" src="' + data[i].picture + '?sz=50"><span class="in-office-item-name">' + data[i].given_name + ' &dash; OoO</span></div>'
            } else {
                people += '<div class="in-office-item"><img class="avatar" src="' + data[i].picture + '?sz=50"><span class="in-office-item-name">' + data[i].given_name + '</span></div>'
            }
        }


        
        $("#in-office").html(activePeople + people)

    })

   
}