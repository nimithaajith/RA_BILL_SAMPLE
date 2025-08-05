console.log("inside js");
function deleteLastRow() {
    console.log("inside deleteLastRow");
    const table = document.getElementById("billtable");
    const lastRowIndex = table.rows.length - 1;

    if (lastRowIndex >= 0) {
        // Get the last row element
        const lastRow = table.rows[lastRowIndex];
        console.log('Last row to delete:', lastRow);

        // Delete the last row
        table.deleteRow(lastRowIndex);
        console.log('Last row deleted');
    }
}   