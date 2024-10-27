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
    // Ensure previous instances of the modal are removed
    const existingModal = bootstrap.Modal.getInstance(document.getElementById('editproductModal'));
    if (existingModal) existingModal.dispose();

    // Reinitialize the modal
    const productModal = new bootstrap.Modal(document.getElementById('editproductModal'), {
        backdrop: true,
        keyboard: true
    });
    
    const productForm = document.getElementById('productForm');
    const modalTitle = document.getElementById('productModalLabel');
    const formFields = document.getElementById('formFields');
    
    modalTitle.textContent = 'Edit Product';
    productForm.action = `/catalogue/edit/${productId}/`;
    console.log('editactionurl:', productForm.action);

    // Fetch form HTML for the product
    fetch(`/catalogue/edit/${productId}/`, {
        method: 'GET',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.form_html) {
            formFields.innerHTML = data.form_html;
        } else {
            console.error("No form HTML returned");
        }
    })
    .catch(error => {
        console.error("Error fetching product form:", error);
    });

    // Show the modal
    productModal.show();

    // Ensure the backdrop is removed on close
    document.getElementById('editproductModal').addEventListener('hidden.bs.modal', () => {
        document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
        document.body.classList.remove('modal-open');
        document.body.style.paddingRight = '';
    });
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