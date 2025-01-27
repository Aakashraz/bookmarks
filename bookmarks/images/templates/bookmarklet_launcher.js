javascript: (function(){
    if(!window.bookmarklet) {
        // it creates a new <script> element, sets its src attribute to the URL of the bookmarklet.js file, and
        // appends it to the <body>.
        const bookmarklet_js = document.createElement('script');

        bookmarklet_js.src = '//127.0.0.1:8000/static/js/bookmarklet.js?r='+Math.floor(Math.random()*9999999999999999);
        // Using a random number, we prevent the browser from loading
        // the file from the browser’s cache. If the bookmarklet JavaScript has been previously loaded,
        // the different parameter value will force the browser to load the script from the source URL
        // again. This way, we make sure the bookmarklet always runs the most up-to-date JavaScript code.

        // wait for the script to load before marking bookmarklet as loaded
        bookmarklet_js.onload = () => {
            window.bookmarklet = true;
        }
        document.body.appendChild(bookmarklet_js);
    } else {
        bookmarkletLaunch();
        // If window.bookmarklet is defined and has a truthy value, the bookmarkletLaunch() function
        // is executed. We will define bookmarkletLaunch() as a global function in the bookmarklet.js
        // script.
    }
})();