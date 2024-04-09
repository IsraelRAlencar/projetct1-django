function my_scope() {
    const forms = document.querySelectorAll('.form-delete');

    for (const form of forms) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            const confirmed = confirm('Are you sure you want to delete this item?');

            if (confirmed){
                form.submit();
            }
        });
    }
}

my_scope();