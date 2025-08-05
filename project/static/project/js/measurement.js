console.log("inside js");
function autoCalculateQuantity() {
    console.log("inside js");
    var l = parseFloat(document.getElementById("newlength").value) || 1;
    var b = parseFloat(document.getElementById("newbreadth").value) || 1;
    var h = parseFloat(document.getElementById("newheight").value) || 1;
    var c = parseFloat(document.getElementById("newcount").value) || 1;
    var n = parseFloat(document.getElementById("newnumber").value) || 1;
    
    var qnty = l*b*h*c*n;
    
    document.getElementById("newquantity").value = qnty.toFixed(3);
    checkQuantity();
    
}

function checkQuantity(){
    var available_quantity=parseFloat(document.getElementById("available_quantity").innerText);
    var newqty=parseFloat(document.getElementById("newquantity").value);
    if (available_quantity < newqty){
        document.getElementById("qtywarning").innerText ="This quantity exceeds available limit "+available_quantity;
        document.getElementById('savemeasurement').disabled= true;
    }
    else{
        document.getElementById("qtywarning").innerText ="";
        document.getElementById('savemeasurement').disabled= false;
    }

}


function update_available_quantity() {
    var div = document.getElementById("qntydiv");
    console.log("update_available_quantity........ ");
    if (div) {
        var boq_quantity = parseFloat(document.getElementById("quantity").innerText) || 0;
        var used_quantity =parseFloat(document.getElementById("current_quantity").innerText) || 0;
        console.log("boq_quantity="+boq_quantity);
        console.log("used_quantity= "+used_quantity);
        document.getElementById("available_quantity").innerText = (boq_quantity-used_quantity).toFixed(3);

    } else {
        console.log("The div is not found.");
    }   
    
}
window.onload = function() {
    update_available_quantity();
};

document.getElementById("newlength").addEventListener("input", autoCalculateQuantity);
document.getElementById("newbreadth").addEventListener("input", autoCalculateQuantity);
document.getElementById("newheight").addEventListener("input", autoCalculateQuantity);
document.getElementById("newcount").addEventListener("input", autoCalculateQuantity);
document.getElementById("newnumber").addEventListener("input", autoCalculateQuantity);
document.getElementById("newquantity").addEventListener("change", checkQuantity);

