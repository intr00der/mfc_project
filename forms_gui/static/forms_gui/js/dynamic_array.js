$( document ).ready(function() {
    const widgets = document.querySelectorAll('.dynamic-array-widget');

    if (widgets.length) {
        for (let i = 0; i < widgets.length; i++) {
            const currentWidget = widgets[i];

            const addButton = currentWidget.querySelector('.add-array-item');
            const removeButton = currentWidget.querySelector('.remove-array-item');
            const ul = currentWidget.querySelector('ul');

            addButton.onclick = () => {
                const elements = currentWidget.querySelectorAll('.array-item');
                const lastElement = elements[elements.length - 1];
                const clonedElement = lastElement.querySelector('input').cloneNode();
                const id_parts = clonedElement.getAttribute('id').split('_');
                const id = id_parts.slice(0, -1).join('_') + '_' + String(parseInt(id_parts.slice(-1)[0]) + 1)
                clonedElement.setAttribute('id', id);
                clonedElement.value = '';
                const newListItem = lastElement.cloneNode();
                newListItem.append(clonedElement);
                ul.append(newListItem);
            }

            removeButton.onclick = () => {
                const elements = currentWidget.querySelectorAll('.array-item');
                ul.removeChild(elements[elements.length - 1]);
            }
        }
    }
});


//const $last = $(this).find('.array-item');
//console.log($(this).find('.array-item'));
//var $new = $last.clone();
//var id_parts = $new.find('input').attr('id').split('_');
//var id = id_parts.slice(0, -1).join('_') + '_' + String(parseInt(id_parts.slice(-1)[0]) + 1)
//$new.find('input').attr('id', id);
//$new.find('input').prop('value', '');
//$new.insertAfter($last);