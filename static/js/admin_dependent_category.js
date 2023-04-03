// (function($) {
//     $(document).ready(function() {
//         // Get the country dropdown element
//         var category = $('#id_product_type');
        
//         // Get the city dropdown element
//         var subCategory = $('#id_sub_category');
        
//         // Disable the city dropdown by default
//         subCategory.attr('disabled', 'disabled');
        
//         // Set up the AJAX request
//         category.change(function() {
//             var catId = $(this).val();
//             if (catId) {
//                 $.ajax({
//                     url: '/adminpanel-da/app/product/add/',
//                     data: {
//                         'id_product_type': catId
//                     },
//                     success: function(data) {
//                         // Clear the city dropdown and enable it
//                         subCategory.html(data);
//                         subCategory.removeAttr('disabled');
//                     }
//                 });
//             } else {
//                 // Disable the city dropdown if no country is selected
//                 subCategory.attr('disabled', 'disabled');
//             }
//         });
//     });
// })(django.jQuery);

document.getElementById('id_product_type').innerText = "hhhhh"
