jQuery(function($) {

    $('select').on('change', function() {
        var new_semester = $('<div><input type="hidden" name="semesters" value="' + this.value + '"><span><label>' + this.value + '</label><label class="remove-semester">X</label></span></div>');
        $('#semesters-selection').append(new_semester);
        $('#bill_form').submit();
    })

    $('#semesters-selection').on('click', '.remove-semester', function() {
        $(this).parent().parent().remove();
        $('#bill_form').submit();
    });
});
