/*
* Start Bootstrap - Simple Sidebar v6.0.5 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/
//




window.addEventListener('DOMContentLoaded', event => {


    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();

            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));



        });
    }


});

// Toolbox code

const category_urls = JSON.parse(document.getElementById('category-urls').textContent)



function get_current_category(link){
    // Extracts the category/building from the provided link
     let c = ''
    for(var i=0; i<category_urls.length;i++){
        if(link.includes(category_urls[i])){
            c=category_urls[i]

            break;
        }
    }
    return c
}


// underlines active menus on top nav bar.
   $(document).ready(function () {

        jQuery(function ($) {
            //current active link
          var path_top_nav = window.location.href;
          $('.nav-link').each(function () {
              // the href attribute of the elements with .nav-link class == the current link (see browser )
              let link =  this.href.split('/')
              currec_c= get_current_category(link)
              if ( path_top_nav.split('/').includes(currec_c)) {
              $(this).addClass('active-top-bar');
              return false;
            }

          });
        });
      });






