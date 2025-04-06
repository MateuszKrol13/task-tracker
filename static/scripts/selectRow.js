function selectRow(element) {

    selectedElements = document.querySelectorAll(".selected");
    selectedElements.forEach(element => {
        element.classList.remove('selected')
    });

    element.classList.add('selected');

    target=document.getElementById('col-1');

    //title
    target.querySelectorAll('[id$="entry-title"]').forEach(e => {
        e.value = element.querySelector("td[headers='row-title']").innerHTML;
    });

    //desc
    target.querySelectorAll('[id$="entry-description"]').forEach(e => {
        e.value = element.querySelector("td[headers='row-desc']").innerHTML;
    });

    //due-date
    target.querySelectorAll('[id$="entry-due-date]"').forEach(e => {
        e.value = element.querySelector("td[headers='row-due']").innerHTML;
    });
}