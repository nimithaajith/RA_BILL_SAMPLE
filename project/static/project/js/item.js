function showConfirm(){
    document.getElementById('deleteconfirm').style.display='inline';
}

function hideConfirm(){
    document.getElementById('deleteconfirm').style.display='none';
}

function autocalculateAmount() {
    console.log("inside js");
    var itemquantity = parseFloat(document.getElementById("quantity").value) || 1;
    var itemrate = parseFloat(document.getElementById("rate").value) || 1;
    
    var itemamount = itemquantity * itemrate;
    
    document.getElementById("amount").value = itemamount.toFixed(3);
}

document.getElementById("quantity").addEventListener("input", autocalculateAmount);
document.getElementById("rate").addEventListener("input", autocalculateAmount);
