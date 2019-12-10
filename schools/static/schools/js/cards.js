$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-card").modal("show");
            },
            success: function (data) {
                $("#modal-card .modal-content").html(data.html_form);
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
                    $("#card-table tbody").html(data.html_card_list);
                    $("#modal-card").modal("hide");
                } else {
                    $("#modal-card .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create card
    $(".js-create-card").click(loadForm);
    $("#modal-card").on("submit", ".js-card-create-form", saveForm);

    // view card
    $("#card-table").on("click", ".js-view-card", loadForm);
    $("#modal-card").on("submit", ".js-card-view-form", saveForm);

    // Update card
    $("#card-table").on("click", ".js-update-card", loadForm);
    $("#modal-card").on("submit", ".js-card-update-form", saveForm);

    // Delete card
    $("#card-table").on("click", ".js-delete-card", loadForm);
    $("#modal-card").on("submit", ".js-card-delete-form", saveForm);

});