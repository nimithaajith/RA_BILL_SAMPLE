console.log("inside js");
function deleteLastRow() {
    console.log("inside deleteLastRow");
    const table = document.getElementById("boqtable");
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
 function autocalculateAmount() {
    console.log("inside js");
    var itemquantity = parseFloat(document.getElementById("quantity").value) || 1;
    var itemrate = parseFloat(document.getElementById("rate").value) || 1;
    
    var itemamount = itemquantity * itemrate;
    
    document.getElementById("amount").value = itemamount.toFixed(3);
}

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("quantity").addEventListener("input", autocalculateAmount);
});
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("rate").addEventListener("input", autocalculateAmount);
});
// window.onload = document.getElementById("quantity").addEventListener("input", autocalculateAmount);
// window.onload=document.getElementById("rate").addEventListener("input", autocalculateAmount);

// document.getElementById("quantity").addEventListener("input", autocalculateAmount);
// document.getElementById("rate").addEventListener("input", autocalculateAmount);

