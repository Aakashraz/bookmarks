(function () {
    const siteUrl = 'https://127.0.0.1:8000/';
    const styleUrl = siteUrl + 'static/css/bookmarklet.css';
    const minWidth = 200;
    const minHeight = 200;

// load CSS
    let head = document.getElementsByTagName('head')[0];
// It first gets a reference to the <head> element of the current web page
    let link = document.createElement('link');
// It then creates a new <link> element
    link.rel = 'stylesheet';
    link.type = 'text/css';
// The rel and type attributes of the <link> element are set.
    link.href = styleUrl + '?r=' + Math.floor(Math.random()*9999999999999999);
    head.appendChild(link);

// The above code generates an object equivalent to the following JavaScript code and appends it to
// the <head> element of the HTML page:
// <link rel="stylesheet" type="text/css" href= "//127.0.0.1:8000/static/css/bookmarklet.css?r=1234567890123456">


// load HTML
    let body = document.getElementsByTagName('body')[0]
// Define an HTML template as a string that will be injected into the page
    let boxHtml = `
        <div id="bookmarklet">
    <!--    A close button (<a> with &times; which displays an "×" symbol)-->
        <a href="#" id="close">&times;</a>
        <h1>Select an image to bookmark:</h1>
        <div class="images"></div>
        <!-- This container is initially empty and will be filled with the images found on the site. -->
        </div>`;
    body.innerHTML += boxHtml;
// body.innerHTML += boxHtml appends the entire HTML template to the existing content of the <body> element.
// The += operator means this new content is added to the end of whatever already exists in the body,
// without replacing the existing content.

// function to launch the bookmarklet
    // define a global function
    window.bookmarkletLaunch = function() {
        const bookmarklet = document.getElementById('bookmarklet');
        if (!bookmarklet) {
            console.error('Bookmarklet container not found!');
        }
        const imagesFound = bookmarklet.querySelector('.images');
        if (!imagesFound) {
            console.error('.images container not found!')
        }

        // the image container is cleared by setting its innerHTML attribute to an empty string
        imagesFound.innerHTML = '';
        // display bookmarklet by setting the 'display CSS' property to 'block'
        bookmarklet.style.display = 'block';

        // close button event
        // When  users click the element, the bookmarklet's main container is hidden by setting
        // its 'display' property to 'none'.
        const closeButton = bookmarklet.querySelector('#close');
            if (closeButton) {
                closeButton.addEventListener('click', function() {
                    bookmarklet.style.display = 'none';
                })
            }

        // find images in the DOM with the minimum dimensions
        let images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]');
        // The above line will find the DOM elements whose src attribute finishes with .jpg, .jpeg and .png respectively
        console.log(`TOTAL IMAGES FOUND: ${images.length}`);

        // The arrow function syntax image => {} is essentially syntactic sugar for
        // a traditional function declaration function(image) {}.

        images.forEach(image => {
            if (image.naturalWidth >= minWidth && image.naturalHeight >= minHeight) {
                let imageElement = document.createElement('img');
                imageElement.src = image.src;
                imagesFound.append(imageElement);
                console.log("IMAGES ADDED TO BOOKMARKLET");
            }
            // A new <img> element is created for each image found, where the src source URL attribute is
            // copied from the original image and added to the imagesFound container
        })

        // Add a check if no images were found
        if (imagesFound.children.length === 0) {
            console.warn('NO IMAGES MEETING SIZE CRITERIA FOUND.')
        }

        // select image event
        imagesFound.querySelectorAll('img').forEach(image => {
            image.addEventListener('click', function(event){
                // When the event is triggered (i.e. when an image is clicked), event.target refers
                // to the image element that was clicked.
                let imageSelected = event.target;
                // the bookmarklet is then hidden by setting its display property to none.
                bookmarklet.style.display = 'none';
                window.open(siteUrl + 'images/create/?url='
                + encodeURIComponent(imageSelected.src)
                + '&title='
                + encodeURIComponent(document.title),
                '_blank');
                // A new browser window is opened with the URL to bookmark a new image on the site. The
                // content of the <title> element of the website is passed to the URL in the title GET parameter
                // and the selected image URL is passed in the url parameter.
            })
        })
    }

// launch the bookmarklet
    window.bookmarkletLaunch();
})();
