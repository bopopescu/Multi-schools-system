$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-dispatch").modal("show");
            },
            success: function (data) {
                $("#modal-dispatch .modal-content").html(data.html_form);
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
                    $("#dispatch-table tbody").html(data.html_dispatch_list);
                    $("#modal-dispatch").modal("hide");
                } else {
                    $("#modal-dispatch .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create dispatch
    $(".js-create-dispatch").click(loadForm);
    $("#modal-dispatch").on("submit", ".js-dispatch-create-form", saveForm);

    // view dispatch
    $("#dispatch-table").on("click", ".js-view-dispatch", loadForm);
    $("#modal-dispatch").on("submit", ".js-dispatch-view-form", saveForm);

    // Update dispatch
    $("#dispatch-table").on("click", ".js-update-dispatch", loadForm);
    $("#modal-dispatch").on("submit", ".js-dispatch-update-form", saveForm);

    // Delete dispatch
    $("#dispatch-table").on("click", ".js-delete-dispatch", loadForm);
    $("#modal-dispatch").on("submit", ".js-dispatch-delete-form", saveForm);

});