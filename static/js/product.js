console.log("javascript");
function openAddProductModal() {
    const productForm = document.getElementById('productForm');
    const productModal = new bootstrap.Modal(document.getElementById('productModal'));
    const modalTitle = document.getElementById('productModalLabel');
    const formFields = document.getElementById('formFields');

    modalTitle.textContent = 'Add Product';
    productForm.action = `/catalogue/add/`;
    formFields.innerHTML = ''; // Clear the form fields for a new product entry

    productModal.show(); // Show the modal
}

function openEditProductModal(productId) {
    const productForm = document.getElementById('productForm');
    const productModal = new bootstrap.Modal(document.getElementById('editproductModal')); // Ensure this refers to the correct modal
    const modalTitle = document.getElementById('productModalLabel');
    const formFields = document.getElementById('formFields');

    modalTitle.textContent = 'Edit Product';
    productForm.action = `/catalogue/edit/${productId}/`;  // Pass product_id here
    console.log('editactionurl:', productForm.action);
    // Fetch the form HTML for the existing product
    fetch(`/catalogue/edit/${productId}/`, {   
        method: 'GET',  // Change to GET for retrieving form HTML (POST is for submitting)
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.form_html) {
            formFields.innerHTML = data.form_html; // Populate form fields with product data
        } else {
            console.error("No form HTML returned");
        }
    })
    .catch(error => {
        console.error("Error fetching product form:", error);
    });

    productModal.show(); // Show the modal
}


document.getElementById('productForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const actionUrl = this.action;

    fetch(actionUrl, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            document.getElementById('formFields').innerHTML = data.form_html || `<div class="alert alert-danger">${data.error}</div>`;
        }
    });
});