$(function() {
    $('#capture').click(function() {
        $.ajax({
            type: 'GET',
            url: '/camera/open',
            success: (data) => {
                $('#registerImg').attr('src', '');
                $('#registerImg').attr('src', data.url);
                $('#getPlate').removeClass('d-none');
            } 
        })
    })

    $('#capureForObserve').click(function() {
        $.ajax({
            type: 'GET',
            url: '/camera/open',
            success: (data) => {
                $('#registerImg').attr('src', '');
                $('#observeImg').attr('src', data.url);
                $('#getPlateObserve').removeClass('d-none');
            } 
        })
    });

    $('#getPlate').click(function() {
        $.ajax({
            type: 'GET',
            url: '/image',
            success: (data) => {
                $('#plate').val(data.response);
                $('#signup').attr('disabled', false);
            } 
        })
    })

    $('#getPlateObserve').click(function() {
        let plate;
        $.ajax({
            type: 'GET',
            url: '/image',
            success: (data) => {
                plate = data.response;
                $('#plateResult').val(plate);
                $('#updateInfo').attr('disabled', false);
                $.ajax({
                    type: 'POST',
                    url: '/image/info',
                    data: {
                        plate
                    },
                    success: (info) => {
                        const moneyBack = info.money - 5000;
                        $('#cmndByPlate').val(info.cmnd);
                        $('#nameByPlate').val(info.name);
                        $.ajax({
                            type: 'POST',
                            url: '/users/info',
                            data: {
                                plate,
                                moneyBack
                            },
                            success: (res) =>{
                                $('#moneyByPlate').val(moneyBack);
                            }
                        })
                    },
                    error: (err) => {
                        alert("Tài khoản bạn chưa đăng kí")
                    }
                })
            }
        })
    })

    $('#signup').on('click', function() {
        let cmnd = $('#cmnd').val();
        let name = $('#name').val();
        let money = $('#money').val();
        let plate = $('#plate').val();
        const data = {
            cmnd,
            name,
            money,
            plate
        }

        if (!cmnd || !name || !money || !plate) {
            alert('You can\'t let field empty');
            return;
        }
        $.ajax({
            url: '/signUp',
            data,
            type: 'POST',
            success: function(response) {
                $('#cmnd').val() = '';
                $('#name').val() = '';
                $('#money').val() = '';
                $('#plate').val() = '';
                alert('Success');
            },
            error: function(error) {
                alert('Error');
            }
        });
    })
});