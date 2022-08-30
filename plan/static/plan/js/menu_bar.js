/*
* Start Bootstrap - Simple Sidebar v6.0.5 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/
//
// Scripts
//

// arrows

// const leftArrowClass = "bi-chevron-double-left";
// const rightArrowClass = "bi-chevron-double-right";
// const arrowClass = "bi"
// const arrowElem = document.querySelector("." + leftArrowClass);
// var statebar = true;

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

// underlines active menus on top nav bar.
   $(document).ready(function () {

        jQuery(function ($) {
          var path_top_nav = window.location.href;
          $('.nav-link').each(function () {
            if (this.href === path_top_nav) {
              $(this).addClass('active-top-bar');
            }
          });
        });
      });
