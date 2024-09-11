$('.product-filter').on('click', function () {
    $('#product-filter-form').submit();
})

$(document).on('click','.cart-add',function(e){
    e.preventDefault();

    let cartProId = $(this).data('product');
    let csrfToken = $('meta[name="csrf-token"]').attr('content');
    console.log(cartProId)

    $.ajax({
        url:'/add_to_cart/',
        type:'post',
        dataType:'json',
        data:{
            'item':cartProId,
            'csrfmiddlewaretoken': csrfToken,
        },
        success:(res)=>{
            console.log(res)
            if(res['status']==0){
                // $('#loading').show();
                setTimeout(()=>{
                    // $('#loading').hide();
                    $('#login-btn')[0].click(); 
                },500)
            }else{
                sendMSG(res['status'],res['msg'],res['prod'])
                if(res.qntysts){
                    $('#cartCount').html(res.count)
                    $(this).parent().html(`
                    <a href="#" class="go-to-cart btn btn-sm text-dark p-0">
                        <i class="fas fa-shopping-cart text-primary mr-1"></i>Go To Cart
                    </a>
                    `)
                }
            }
        },
        error:(e)=>{
            //console.log(e)
            alert('something went wrong try again later')
        }
    })
})

//update cart
$(document).ready(function() {
    $('.btn-number').click(function(e) {
        e.preventDefault();

        var $button = $(this);
        var $input = $button.closest('.input-group').find('.pp');
        var $form = $button.closest('.input-group').find('.quantity-form');

        var currentVal = parseInt($input.val(), 10);
        var min = parseInt($input.attr('min'), 10);
        var max = parseInt($input.attr('max'), 10);

        if (isNaN(currentVal) || currentVal < min || currentVal > max) {
            return
        }
        if ($button.hasClass('minus')) {
                // Decrease the quantity
            if (currentVal > min) {
                $input.val(currentVal - 1).change();
                $button.siblings('.plus').attr('disabled', false);
            }
            if (currentVal === min) {
                $button.attr('disabled', true);
            }
        } else if ($button.hasClass('plus')) {
                // Increase the quantity
            if (currentVal < max) {
                $input.val(currentVal + 1).change();
                $button.siblings('.minus').attr('disabled', false);
            }
            if (currentVal === max) {
                $button.attr('disabled', true);
            }
        }

        // Submit the form after updating the quantity
        $form.submit();
    });
});
