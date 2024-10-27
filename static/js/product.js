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
    // Fetch form HTML for the product
    fetch(`/catalogue/edit/${productId}/`, {
        method: 'GET',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.form_html) {
            document.getElementById('formFields').innerHTML = data.form_html;
        } else {
            console.error("No form HTML returned");
        }
    })
    .catch(error => {
        console.error("Error fetching product form:", error);
    });

    // Initialize the modal
    const productModalElement = document.getElementById('editproductModal');
    const productModal = new bootstrap.Modal(productModalElement);

    // Remove leftover backdrops and reset modal on close
    productModalElement.addEventListener('hidden.bs.modal', () => {
        // Remove all backdrops
        document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());
        
        // Reset modal styles and classes
        document.body.classList.remove('modal-open');
        document.body.style.paddingRight = '';

        // Fully detach and reattach modal to ensure clean re-initialization
        const newModal = productModalElement.cloneNode(true);
        productModalElement.parentNode.replaceChild(newModal, productModalElement);
    });

    // Show the modal
    productModal.show();
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