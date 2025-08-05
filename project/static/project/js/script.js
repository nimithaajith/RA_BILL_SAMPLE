// document.getElementById('wo_boq_xl').addEventListener('change', function(event) {
//     var xlfile = event.target.files[0];
    
//     if (xlfile) {
//         var formData = new FormData();
//         formData.append('xlfile', xlfile); 
//         console.log(csrfToken);
//         console.log(ajaxurl);
//         $.ajax({
//             headers: { "X-CSRFToken": csrfToken },
//             url: ajaxurl,
//             type: 'POST',
//             data: formData,
//             dataType: 'json',
//             processData: false,  
//             contentType: false, 
//             success: function (data) {
//                 if(data.headings){
//                     headings=data.headings;

//                     var dropdown = document.getElementById('serialno');
//                     var descriptiondropdown = document.getElementById('description');
//                     var ratedropdown = document.getElementById('rate');
//                     var quantitydropdown = document.getElementById('quantity');
//                     var unitdropdown = document.getElementById('unit');
//                     var amountdropdown = document.getElementById('amount');
                    
//                     var innerhtml='<option value="">Click here and select</option>';
//                     headings.forEach(function(heading) {
//                         innerhtml=innerhtml+ '<option value="'+heading+'">'+heading+'</option>';

//                     });
//                     dropdown.innerHTML=innerhtml;
//                     descriptiondropdown.innerHTML=innerhtml;
//                     ratedropdown.innerHTML=innerhtml;
//                     quantitydropdown.innerHTML=innerhtml;
//                     unitdropdown.innerHTML=innerhtml;
//                     amountdropdown.innerHTML=innerhtml;
                    
//                 }
                
//             },
//             error: function (request, error) {
//                 alert("Something went wrong ! Try again.. " );
//             }
//         });
//     }
// });
