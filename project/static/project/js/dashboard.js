
function closeSuggestions() {
    $('#suggestionsContainer').hide(); // Hide the container
    $('#overlay').show();
}
function closeOwnerForm() {
    const emailInput = document.querySelector(`#owneremailid`);           
    emailInput.removeEventListener('blur', handleBlur);
    $('#addOwnerContainer').hide(); // Hide the container

    $('#overlay').show();
}
function closeCompanyForm() {
    const emailInput = document.querySelector(`#companyemailid`);           
    emailInput.removeEventListener('blur', handleBlur);
    console.log('closing company form');
    $('#addCompanyContainer').hide(); // Hide the container
    $('#overlay').show();
}
function closeConsultantForm() {
    const emailInput = document.querySelector(`#consultantemailid`);           
    emailInput.removeEventListener('blur', handleBlur);
    console.log('closing consultant form');
    $('#addConsultantContainer').hide(); // Hide the container
    $('#overlay').show();
}

$(document).ready(function () {
    // Example: Fetch and display user suggestions
    $('#owner').on('input', function () {
        let query = $(this).val();
        let suggestions = $('#suggestionsContainer'); 
        if (query.length >= 4) {
            $.ajax({
                url: ajaxurl_getowners, 
                headers: { 'X-CSRFToken': csrfToken }, 
                data: { q: query },
                success: function (data) {
                    
                    suggestions.empty(); // Clear previous suggestions
                    if (data.length == 0) {
                        // add new owner appears
                        suggestions.hide();                         
                        AddNewOwnerForm();
                    }else{
                        suggestions.append(`
                            <div class="suggestion-header">
                                
                                <button class="close-btn" onclick="closeSuggestions()">X</button>
                            </div>
                            <h3>Existing Owners</h3>
                            <hr>
                        `); 
                        data.forEach(owner => {
                            suggestions.append(
                                 `<div class="suggestion-item py-3">
                                
                                <button class="form-btn-custom w-100" data-id="${owner.id}" data-name="${owner.owner_name}" onclick="selectOwner('${owner.id}', '${owner.owner_name}')">${owner.owner_name}</button>
                                </div>`
                            ); 
                        }); 
                        //$('#suggestionsContainer').css('width', 'auto');
                        
                        // $('#suggestionsContainer').fadeIn('slow');
                        console.log('showing line=29')
                        suggestions.show(); 
                        $('#overlay').fadeOut('slow');
                    }
                    
                },
            });           
            
        } else {
            suggestions.hide();
            $('#overlay').show();
        }
    });


    //company suggestions
    $('#company').on('input', function () {
        let query = $(this).val();
        let suggestions = $('#suggestionsContainer'); 
        if (query.length >= 4) {
            console.log('inside company ajax');
            $.ajax({
                url: ajaxurl_getcompanies, 
                headers: { 'X-CSRFToken': csrfToken }, 
                data: { q: query },
                success: function (data) {
                    
                    suggestions.empty(); // Clear previous suggestions
                    if (data.length == 0) {
                        // add new owner appears
                        suggestions.hide();                         
                        AddNewCompanyForm();
                    }else{
                        suggestions.append(`
                            <div class="suggestion-header">
                                
                                <button class="close-btn" onclick="closeSuggestions()">X</button>
                            </div>
                            <h3>Existing Companies</h3>
                            <hr>
                        `); 
                        data.forEach(company => {
                            suggestions.append(
                                 `<div class="suggestion-item py-3">
                                
                                <button class="form-btn-custom w-100" data-id="${company.id}" data-name="${company.company_name}" onclick="selectCompany('${company.id}', '${company.company_name}')">${company.company_name}</button>
                                </div>`
                            ); 
                        }); 
                        //$('#suggestionsContainer').css('width', 'auto');
                        
                        // $('#suggestionsContainer').fadeIn('slow');
                        console.log('showing line=94')
                        suggestions.show(); 
                        $('#overlay').fadeOut('slow');
                    }
                    
                },
            });
            
        } else {
            $('#suggestions').empty();
        }
    });  
        
    
});

function handleBlur(event) {
    const emailInput = event.target;
    const email = emailInput.value;  

    if (email) {
        // Send an AJAX request to check if the email exists
        fetch(`${emailUrl}?email=${encodeURIComponent(email)}`)
            .then(response => response.json())
            .then(data => {
                if (data.result === 'reject') {
                    alert('Email ID already exists!');
                    emailInput.value="";
                }
            })
            .catch(error => console.error('Error:', error));
    }
}

//Add new company
function AddNewOwnerForm(){
    console.log('inside show owner form');    
    $('#addOwnerContainer').show();

    $('#overlay').fadeOut('slow');
    const emailInput = document.querySelector(`#owneremailid`);           
    emailInput.addEventListener('blur', handleBlur);

}

function CreateOwner(){
    let ownercompanyname = $('#ownercompanyname').val();
    let owneremailid = $('#owneremailid').val();
    let owneraddress=$('#owneraddress').val();
    let ownercountrycode=$('#ownercountrycode').val();
    let ownerphone=$('#ownerphone').val();
    $.ajax({
        url: ajax_addowner, // Replace with your Django view URL
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken }, // Include CSRF token for Django
        data: {
            ownercompanyname: ownercompanyname,
            owneremailid: owneremailid,
            owneraddress: owneraddress,
            ownercountrycode: ownercountrycode,
            ownerphone: ownerphone
        },
        success: function (response) {
            alert(response.message);
            
            let newOwnerId = response.id;
            let newOwnerName = response.name;
            $('#owner').val(newOwnerName);               
            $('#ownerId').val(newOwnerId);
            $('#addOwnerContainer').hide();
            $('#overlay').show();

        },
        error: function (xhr, status, error) {
            alert('An error occurred while adding the owner.');
            console.error(error); // Handle error response
            $('#addOwnerContainer').hide(); 
            $('#overlay').show();               
        }
    });
    

}






//select owner from owner suggestions
function selectOwner(id, name) {
    
    
    // Hide suggestions
    $('#suggestionsContainer').hide();
    $('#overlay').show();
    // Set name in visible input
    $('#owner').val(name);
    
    // Set ID in hidden input
    $('#ownerId').val(id);
    $.ajax({
        url: ajaxurl_getconsultants, // Replace with your URL
        method: 'GET',
        data: { owner_id: id }, // Pass owner ID
        success: function (data) {
            let consultantDropdown = $('#consultant');
            consultantDropdown.empty(); // Clear old options

            if (data.length > 0) {
                consultantDropdown.append(
                    `<option value="">Select project consultant here</option>`
                );
                data.forEach(consultant => {
                    console.log(consultant);
                    consultantDropdown.append(
                        `<option value="${consultant.id}">${consultant.consultant_name}</option>`
                    );
                });
            }else{
                consultantDropdown.append(
                    `<option value="">click Add Consultant button</option>`
                );
            }
        },
        error: function () {
            alert('Error loading consultants.');
        },
    });
}


//select company from company suggestions
function selectCompany(id, name) {
    
    
    // Hide suggestions
    $('#suggestionsContainer').hide();
    $('#overlay').show();
    // Set name in visible input
    $('#company').val(name);
    
    // Set ID in hidden input
    $('#companyId').val(id);
    
}



//Add new company
function AddNewCompanyForm(){
    console.log('inside show company form');    
    $('#addCompanyContainer').show();
    $('#overlay').fadeOut('slow');
    const emailInput = document.querySelector(`#companyemailid`);           
    emailInput.addEventListener('blur', handleBlur);

}

function CreateCompany(){
    let contractorcompanyname = $('#contractorcompanyname').val();
    let companyemailid = $('#companyemailid').val();
    let companyaddress=$('#companyaddress').val();
    let companycountrycode=$('#companycountrycode').val();
    let companyphone=$('#companyphone').val();
    $.ajax({
        url: ajax_addcompany, // Replace with your Django view URL
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken }, // Include CSRF token for Django
        data: {
            contractorcompanyname: contractorcompanyname,
            companyemailid: companyemailid,
            companyaddress: companyaddress,
            companycountrycode: companycountrycode,
            companyphone: companyphone
        },
        success: function (response) {
            alert(response.message);
            
            let newId = response.id;
            let newName = response.name;
            $('#company').val(newName);  
            // $('#ownerId').val(newOwnerId);            
            $('#companyId').val(newId);
            $('#addCompanyContainer').hide();
            $('#overlay').show();

        },
        error: function (xhr, status, error) {
            alert('An error occurred while adding the company. Try adding again.');
            console.error(error); // Handle error response
            $('#addCompanyContainer').hide(); 
            $('#overlay').show();               
        }
    });
    

}


//add new consultant

function AddNewConsultantForm(){
    console.log('inside show consultant form');    
    $('#addConsultantContainer').show();
    $('#overlay').fadeOut('slow');
    const emailInput = document.querySelector(`#consultantemailid`);           
    emailInput.addEventListener('blur', handleBlur);

}

function CreateConsultant(){
    let consultantcompanyname = $('#consultantcompanyname').val();
    let consultantemailid = $('#consultantemailid').val();
    let consultantaddress=$('#consultantaddress').val();
    let consultantcountrycode=$('#consultantcountrycode').val();
    let consultantphone=$('#consultantphone').val();
    let ownerid= $('#ownerId').val();    
    $.ajax({
        url: ajax_addconsultant, // Replace with your Django view URL
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken }, // Include CSRF token for Django
        data: {
            consultantcompanyname: consultantcompanyname,
            consultantemailid: consultantemailid,
            consultantaddress: consultantaddress,
            consultantcountrycode: consultantcountrycode,
            consultantphone: consultantphone,
            ownerid: ownerid,
        },
        success: function (response) {
            alert(response.message);
            
            let newId = response.id;
            let newName = response.name;

            let consultantDropdown = $('#consultant');
            consultantDropdown.empty(); // Clear old options            
            consultantDropdown.append(`<option value="${newId}">${newName}</option>`);
            consultantDropdown.val(newId);
            
            $('#addConsultantContainer').hide();
            $('#overlay').show();

        },
        error: function (xhr, status, error) {
            alert('An error occurred while adding the consultant.');
            console.error(error); // Handle error response
            $('#addConsultantContainer').hide(); 
            $('#overlay').show();               
        }
    });
    

}

// $('#overlay form').on('submit', function(event) {
//     event.preventDefault(); // Stop the form from reloading the page
//     console.log('Form submission prevented');
// });