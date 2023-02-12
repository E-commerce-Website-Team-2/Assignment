
// Global variable (script tag)
window.wretch
// This is used fetch subcategories from the backend via database and update thhe dropdown menu in the forntend.
window.addEventListener('load',function(){
  wretchData('http://localhost:5000/products/category/tree', DataSection_Category)
});

// Function to perform a request to backend and perform actions based on response.
function wretchData(url, dataFunction, index = '', params = '') {
  wretch(url)
    .get()
    .notFound(err => { window.location.href = './index.html/404.html' })
    .internalError(err => { window.location.href = './index.html/500.html' })
    .fetchError(err => { alert(err) })
    .res(response => response.json())
    .then((data) => {
      (index === '') ? dataFunction(data) : dataFunction(data, index, params);
    })
    .catch((error) => {
      console.log(error);
    });
}

// Function to load thhe category section
function DataSection_Category(data) {
  // var BackendAPI = getBackendAPI(4,{"cat":0})
  for (ind in data[1]) {
    category_element = document.getElementById("category");
    div_element = document.createElement("div");

    button_element = document.createElement("button");
    let elementAttributes = {
      "class": "btn btn-secondary dropdown-toggle",
      "type": "button",
      "id": "dropdownMenuButton1",
      "value": data[1][ind][0],
      "data-bs-toggle": "dropdown",
      "aria-expanded": "false",
    };
    setMultipleAttributesonElement(button_element, elementAttributes);

    var name = data[1][ind][1]
    name = name.charAt(0).toUpperCase() + name.slice(1)
    button_element.innerHTML = name;

    button_element.addEventListener('click', function () {
      GetProduct(this);
    });
    button_element.addEventListener('dblclick', function () {
      Link(this);
    });

    ulist_element = document.createElement("ul");
    elementAttributes = {
      "class": "dropdown-menu",
      "aria-labelledby": "dropdownMenuButton",
    }
    setMultipleAttributesonElement(ulist_element, elementAttributes);

    div_element.appendChild(button_element);
    div_element.appendChild(ulist_element);
    category_element.appendChild(div_element);
  }
}

// Function to load the product section
function DataSection_Product(data, index, params) {
  if (data[0] == 200) {
    // Get the number of products sent in the response from the backend and calculate the no of pages
    no_of_products = data[1];
    no_of_pages = Math.ceil(no_of_products / 9);
    sort = params["sort"];


    // Get the pagination section where the pagination with given pages is created
    ul_element = document.getElementsByClassName("pagination")[0];
    ul_element.innerHTML = "";

    // Get the product section where the products is going to be added
    product_element = document.getElementsByClassName("pro-container")[0];
    product_element.innerHTML = "";

    // Get the filter dropdown menu to visible and set the href attribut of the dropdown list
    document.getElementsByClassName("dropdown-3")[0].style.display = "block";

    params.sort = 1;
    filter_asc = createURL(index, params, params["pageno"]);
    params.sort = 2;
    filter_desc = createURL(index, params, params["pageno"]);
    document.getElementsByClassName("asc")[0].setAttribute("href", filter_asc);
    document.getElementsByClassName("desc")[0].setAttribute("href", filter_desc);

    if (sort == 1) {
      document.getElementsByClassName("filter")[0].innerHTML = "Sort by Asc";
    }
    if (sort == 2) {
      document.getElementsByClassName("filter")[0].innerHTML = "Sort by Desc";
    }


    //Iterate through the response data containing a list of products and append it to the html page under the product section
    for (let ind = 2; ind < data.length; ind++) {

      div_element = document.createElement("div");
      div_element.setAttribute("class", "pro");
      div_element.addEventListener("click", function () {
        DetailedProduct(data[ind]);
      });



      img_element = document.createElement("img");

      img_element.setAttribute("src", data[ind].productimage === undefined ? data[ind]["productImage"] : data[ind]["productimage"]);

      div_element.appendChild(img_element);

      div_name = document.createElement("div");
      div_name.setAttribute("class", "des");

      h5_element = document.createElement("h5");
      h5_element.innerHTML = data[ind]["name"];

      h4_element = document.createElement("h4");
      h4_element.innerHTML = data[ind]["price"];

      div_name.appendChild(h5_element);
      div_name.appendChild(h4_element);
      div_element.appendChild(div_name);


      product_element.appendChild(div_element);
      // Add the pagination section with the particular pageno and query text
      if (!document.getElementsByClassName("pagination")[0].hasChildNodes()) {
        params["pages"] = no_of_pages
        params["sort"] = sort
        createPagination(index, params, params["pageno"]);
      }
    }


  }
  else {
    window.location.href = './404.html';
  }
  document.getElementById("loading").innerHTML = "";
  document.getElementById("product1").style.display = "block";
  document.getElementById("pagination").style.display = "block";
}
// Function to set multiple attribute to a given tag.
function setMultipleAttributesonElement(elem, elemAttributes) {
  for (var name in elemAttributes) {
    elem.setAttribute(name, elemAttributes[name]);
  }
}

// This function is used to get the subcategory element of a given category and fill in the database
function GetProduct(ele) {
  parentElement = ele.parentNode;
  if (parentElement.childNodes[1].childNodes.length == 0) {
    var BackendAPI = getBackendAPI(4, { "cat": ele.value });
    fetch(BackendAPI, {
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",

      }
    }
    )
      .then((response) => response.json())
      .then((data) => {
        if (data[1].length == 0) {
          window.location.href = `./index.html?cat=${ele.value}&pageno=1`
        }

        for (ind in data[1]) {
          var list_element = document.createElement("li");
          var subcategory1 = document.createElement("a");
          let url = `./index.html?cat=${data[1][ind][0]}&pageno=1`;
          let elemAttributes = {
            "class": "dropdown-item",
            "href": url
          }
          setMultipleAttributesonElement(subcategory1, elemAttributes);
          subcategory1.innerHTML = data[1][ind][1];
          list_element.appendChild(subcategory1)
          parentElement.childNodes[1].appendChild(list_element);
        }



      })
      .catch((error) => {
        console.log(error);
      });
  }

}

// This function is used to call the category page when double click is clicked
function Link(ele) {
  window.location.href = `./index.html?cat=${ele.value}&pageno=1`;
}

// This function is used to create a url based on the index passed.
function createURL(index, params, pageno) {
  if (index === 1) {
    url = `./index.html?pageno=${pageno}&sort=${params["sort"]}`
  }
  else if (index === 2) {
    url = `./index.html?search=${params["query"]}&pageno=${pageno}&sort=${params["sort"]}`
  }
  else if (index === 3) {
    url = `./index.html?cat=${params["cat"]}&pageno=${pageno}&sort=${params["sort"]}`
  }
  else {
    url = "./404.html"
  }
  return url
}

// This function is to get the backend api url for the particular query mentioned by index as a parameter
function getBackendAPI(index, params) {
  if (index === 1) {
    url = `http://localhost:5000/products/trending/${params["pageno"]}/${params["sort"]}`
  }
  else if (index === 2) {
    url = `http://localhost:5000/products/search/${params["query"]}/${params["pageno"]}/${params["sort"]}`
  }
  else if (index === 3) {
    url = `http://localhost:5000/products/category/${params["cat"]}/${params["pageno"]}/${params["sort"]}`
  }
  else if (index === 4) {
    url = `http://localhost:5000/products/category/tree/${params["cat"]}`
  }
  else {
    url = ''
  }
  return url
}


// Below code is used to redirect to home page on searching or selecting a category
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

if (urlParams.has('search') & urlParams.has('pageno')) {
  var query = urlParams.get('search');
  var pageno = urlParams.get('pageno');
  var sort = "";
  if (urlParams.has('sort')) {
    sort = urlParams.get('sort');
  }
  params = { "query": query, "pageno": pageno, "sort": sort }
  fill_products_section(2, params);
}
else if (urlParams.has('cat') && urlParams.has('pageno')) {
  var cat = urlParams.get('cat');
  var pageno = urlParams.get('pageno');
  var sort = "";
  if (urlParams.has('sort')) {
    sort = urlParams.get('sort');
  }
  params = { "cat": cat, "pageno": pageno, "sort": sort }
  fill_products_section(3, params);
}
else if (urlParams.has('pageno') && urlParams.has('sort')) {
  var pageno = urlParams.get('pageno');
  var sort = urlParams.get('sort');
  params = { "pageno": pageno, "sort": sort }
  fill_products_section(1, params);
}
else {
  params = { "pageno": 1, "sort": "" };
  fill_products_section(1, params);
}


// Function on searching an item - Get response from backend and add the response products to the forntend page
function search(ele) {
  // If user hits enter in the search input tag
  if (event.key === 'Enter') {
    // Recieve the value from the input tag and encode the value 
    const inputelement = document.getElementById("search");
    let query = inputelement.value;
    if (query === "") { query = "*" }
    inputelement.value = "";
    query = encodeURIComponent(query);
    // Change the location with search and page parameter added to the current window.
    window.location.href = `./index.html?search=${query}&pageno=1`;

  }
}

// Function to fill the product section with products fetched from backend api for the particular query
function fill_products_section(index, params) {
  var backendapi = getBackendAPI(index, params);
  if (document.getElementById("product1"))
  {
    document.getElementById("product1").style.display = "none";
    document.getElementById("pagination").style.display = "none";
    setTimeout(() => {
      wretchData(backendapi, DataSection_Product, index, params);
    }, 500)
  }
}

// This function is called when a user clicks on a product whhichh moves to another product_detail html element with some properties sent to it.
function DetailedProduct(data) {
  // Generate a url with the respective paramaeters thhat needs to fetched in product_detail page.
  let params = {
    "uniqueId": data.uniqueId === undefined ? data.uniqueID : data.uniqueId,
    "name": data.name,
    "price": data.price,
    "image": data.productimage === undefined ? data["productImage"] : data["productimage"],
  };

  let query = Object.keys(params)
    .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
    .join('&');
  let url = './product_detail.html?' + query;
  // Change the window location to the new url created above.
  document.location.href = url;

}

// Function to change the css of pageno on clicking a page 
function SelectPage(el) {
  // This is used for making the current page selected to active which changes the css of the highleted page.
  document.querySelector('.page-item').classList.remove('active');
  document.querySelector(el).parent().classList.add('active');
}

// Function to creation pagination 
function createPagination(index, params, pageno) {

  var pages = params["pages"];
  var pageno = Number(pageno);

  // Acess the pagination section for thhe pages to be added
  ul_element = document.getElementsByClassName("pagination")[0];
  list_element = document.createElement("li");


  (pageno === 1) ? list_element.setAttribute("class", "page-item disabled") : setMultipleAttributesonElement(list_element, { "class": "page-item", "onclick": `window.location.href='${createURL(index, params, pageno - 1)}'` });


  anchor_element = document.createElement("a");
  anchor_element.setAttribute("class", "page-link");
  anchor_element.innerHTML = "Prev";
  list_element.appendChild(anchor_element);
  ul_element.appendChild(list_element);

  // Generate the max and min index of the current pageno (+5 and -5 from current page)
  (pageno - 5 <= 0) ? min_index = 1 : min_index = pageno - 5;
  (pageno + 5 >= pages) ? max_index = pages : max_index = pageno + 5;


  // Create the pages and add an extra active class to the current page
  for (var i = min_index; i <= max_index; i++) {
    list_element = document.createElement("li");

    (i === pageno) ? list_element.setAttribute("class", "page-item active") : list_element.setAttribute("class", "page-item");

    anchor_element = document.createElement("a");
    const elem_attributes = {
      "class": "page-link",
      "href": createURL(index, params, i),
      "onclick": 'SelectPage(this)',
    }
    setMultipleAttributesonElement(anchor_element, elem_attributes);
    anchor_element.innerHTML = i;

    list_element.appendChild(anchor_element);
    ul_element.appendChild(list_element);
  }


  list_element = document.createElement("li");

  (pageno === pages) ? list_element.setAttribute("class", "page-item disabled") : setMultipleAttributesonElement(list_element, { "class": "page-item", "onclick": `window.location.href='${createURL(index, params, pageno + 1)}'` });

  anchor_element = document.createElement("a");
  anchor_element.setAttribute("class", "page-link");
  anchor_element.innerHTML = "Next";

  list_element.appendChild(anchor_element);
  ul_element.appendChild(list_element);

}




