function confirmDelete(product_id) {
    if (confirm('Are you sure?')) {
        window.location.href = `/profile/delete-product/${product_id}`;
    }
}