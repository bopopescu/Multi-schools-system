$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-application").modal("show");
            },
            success: function (data) {
                $("#modal-application .modal-content").html(data.html_form);
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
                    $("#application-table tbody").html(data.html_application_list);
                    $("#modal-application").modal("hide");
                } else {
                    $("#modal-application .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create application
    $(".js-create-application").click(loadForm);
    $("#modal-application").on("submit", ".js-application-create-form", saveForm);

    // Update application
    $("#application-table").on("click", ".js-update-application", loadForm);
    $("#modal-application").on("submit", ".js-application-update-form", saveForm);


    // Delete application
    $("#application-table").on("click", ".js-delete-application", loadForm);
    $("#modal-application").on("submit", ".js-application-delete-form", saveForm);

});