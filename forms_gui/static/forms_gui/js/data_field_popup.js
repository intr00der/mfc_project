$(document).ready(() => {
    $('div.field-data').hide();
    $('select#id_type').change(event => {
        const select = event.target;
        const val = select.value;

        if (val !== "date" && val !== "text") {
            $('div.field-data').show();
        } else {
            $('div.field-data').hide();
        }
    });
});