$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-leave").modal("show");
            },
            success: function (data) {
                $("#modal-leave .modal-content").html(data.html_form);
            }
        });
    };

      var saveForm = function () {
        var form = $(this);
        var formData = new FormData(form[0]);
        $.ajax({
            url: form.attr("action"),
            data: formData,
            type: form.attr("method"),
            dataType: 'json',
            async: true,
            cache: false,
            contentType: false,
            enctype: form.attr("enctype"),
            processData: false,
            success: function (data) {
                if (data.form_is_valid) {
                    $("#leave-table tbody").html(data.html_leave_list);
                    $("#modal-leave").modal("hide");
                } else {
                    $("#modal-leave .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create leave
    $(".js-create-leave").click(loadForm);
    $("#modal-leave").on("submit", ".js-leave-create-form", saveForm);

    // Update leave
    $("#leave-table").on("click", ".js-update-leave", loadForm);
    $("#modal-leave").on("submit", ".js-leave-update-form", saveForm);


    // Delete leave
    $("#leave-table").on("click", ".js-delete-leave", loadForm);
    $("#modal-leave").on("submit", ".js-leave-delete-form", saveForm);

});