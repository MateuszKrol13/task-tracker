function modifyIssue(row, target) {
    target.querySelector("input[id='modify-entry-title']").value = row.querySelector("td[headers='row-title']").innerHTML;
    target.querySelector("input[id='modify-entry-description']").value = row.querySelector("td[headers='row-desc']").innerHTML;
    target.querySelector("input[id='modify-entry-due-date']").value = row.querySelector("td[headers='row-due']").innerHTML;

    // parse time here
    // also select prio
}