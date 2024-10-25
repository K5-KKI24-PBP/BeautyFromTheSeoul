function openProductModal(productId = null) {
    console.log(document.getElementById('productModal'));
    var productModal = new bootstrap.Modal(document.getElementById('productModal'));
    productModal.show();
    
    const modalTitle = document.getElementById('productModalLabel');
    const formFields = document.getElementById('formFields');
    const productForm = document.getElementById('productForm');

    if (productId) {
        modalTitle.textContent = 'Edit Product';
        productForm.action = `/catalogue/edit/${productId}/`;
        fetch(`/catalogue/edit/${productId}/`)
            .then(response => response.text())
            .then(html => {
                formFields.innerHTML = html;
            });
    } else {
        modalTitle.textContent = 'Add Product';
        productForm.action = `/catalogue/add/`;
        fetch(`/catalogue/add/`)
            .then(response => response.text())
            .then(html => {
                formFields.innerHTML = html;
            });
    }
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