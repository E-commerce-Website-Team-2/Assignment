// This is used fetch subcategories from the backend via database and update thhe dropdown menu in the forntend.
fetch("http://localhost:5000/products/getcategory",{
    headers:{
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Acess-Control-Allow-Methods": "GET",

      }
    }
  )
.then((response) => response.json())
.then((data) => {
  for (var subcategory in data.men){
    var list_element = document.createElement("li");
    var subcategory1 = document.createElement("a");
    var cat1 = 'men';
    var cat2 = data.men[subcategory];

    let params = {
      "cat1": cat1,
      "cat2": cat2,
      "pageno":1
      };
    
    let query = Object.keys(params)
               .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
               .join('&');
    let url = `http://localhost:8000/index.html?` + query;

    subcategory1.setAttribute("class","dropdown-item");
    subcategory1.setAttribute("href",url);
    // console.log(subcategory1);
    subcategory1.innerHTML = data.men[subcategory];
    list_element.appendChild(subcategory1)
    document.getElementsByClassName("cat1")[0].appendChild(list_element);
  }


  for (var subcategory in data.women){
    var list_element = document.createElement("li");
    var subcategory1 = document.createElement("a");
    var cat1 = 'women';
    var cat2 = data.women[subcategory];

    let params = {
      "cat1": cat1,
      "cat2": cat2,
      "pageno":1
      };
    
    let query = Object.keys(params)
               .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
               .join('&');
    let url = `http://localhost:8000/index.html?` + query;

    subcategory1.setAttribute("class","dropdown-item");
    subcategory1.setAttribute("href",url);
    // console.log(subcategory1);
    subcategory1.innerHTML = data.women[subcategory];
    list_element.appendChild(subcategory1)
    document.getElementsByClassName("cat2")[0].appendChild(list_element);
  }
})
.catch((error) => {
console.log(error);
});


// Below code is used to redirect to home page on searching or selecting a category
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
if (urlParams.has('search')&urlParams.has('pageno')){
  var query = urlParams.get('search');
  var pageno = urlParams.get('pageno');
  fill_products(query,pageno);
}
if (urlParams.has('cat1') && urlParams.has('cat2') && urlParams.has('pageno')){
  var cat1 = urlParams.get('cat1');
  var cat2 = urlParams.get('cat2');
  var pageno = urlParams.get('pageno');
  console.log(cat1,cat2,pageno);
  Category(cat1,cat2,pageno);
}


// Function to fill the home page with products sent from the backend for thhe particular search query and page number
function fill_products(query,pageno){
  fetch(`http://localhost:5000/products/search/${pageno}?query=${query}`,{
      headers:{
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Acess-Control-Allow-Methods": "GET",
    
      }
    }
  )
    .then((response) => response.json())
    .then((data) => {
      no_of_products = data[0];
      no_of_pages = Math.ceil(no_of_products/9);

      ul_element = document.getElementsByClassName("pagination")[0];
      ul_element.innerHTML = "";

      product_element = document.getElementsByClassName("pro-container")[0];
      product_element.innerHTML = "";

      for (let ind = 1; ind<data.length; ind++ ) {
        console.log( data[ind])
        div_element = document.createElement("div");
        div_element.setAttribute("class", "pro");
        div_element.setAttribute("onclick",`DetailedProduct('${data[ind]["uniqueId"]}','${data[ind]["name"]}',${data[ind]["price"]},'${data[ind]["productImage"]}')`);


        img_element = document.createElement("img");
        img_element.setAttribute("src",data[ind]["productImage"]);

        div_element.appendChild(img_element);

        div_name = document.createElement("div");
        div_name.setAttribute("class","des");

        h5_element = document.createElement("h5");
        h5_element.innerHTML = data[ind]["name"];

        h4_element = document.createElement("h4");
        h4_element.innerHTML = data[ind]["price"];

        div_name.appendChild(h5_element);
        div_name.appendChild(h4_element);
        div_element.appendChild(div_name);
        
        product_element.appendChild(div_element);

        if (!document.getElementsByClassName("pagination")[0].hasChildNodes()){
          createPagination(query,no_of_pages);
        }

        // console.log(product_element);
        // console.log(data[ind]["name"]);
      }
    })   .catch((error) => {
      console.log(error);
    });
}

// Function on searching an item - Get response from backend and add the response products to the forntend page
function search(ele){
  
  if (event.key === 'Enter'){
    
    const inputelement = document.getElementById("search");
    const query = inputelement.value;
    inputelement.value = "";
    window.location.href = `http://localhost:8000/index.html?search=${query}&pageno=1`;
    
      }
  }

// This function is used to return the products when a subcategory is selected. It asks backend for the products with subcategories.
function Category(cat1,cat2,pageno){
  console.log(cat1,cat2);
  let params = {
    "cat1": cat1,
    "cat2": cat2
    };
  
  let query = Object.keys(params)
             .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
             .join('&');
  
  let url = `http://localhost:5000/products/category/${pageno}?` + query;
  fetch(url,{
      headers:{
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Acess-Control-Allow-Methods": "GET",
    
      }
    }
    )
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        no_of_products = data[0];
        no_of_pages = Math.ceil(no_of_products/9);
        ul_element = document.getElementsByClassName("pagination")[0];
        ul_element.innerHTML = "";
        product_element = document.getElementsByClassName("pro-container")[0];
        product_element.innerHTML = "";
        for ( let ind = 1; ind<data.length; ind++ ) {
          console.log(1,data[ind]["uniqueID"])
          div_element = document.createElement("div");
          div_element.setAttribute("class", "pro");
          div_element.setAttribute("onclick",`DetailedProduct('${data[ind]["uniqueID"]}','${data[ind]["name"]}',${data[ind]["price"]},'${data[ind]["productimage"]}')`);
  
  
          img_element = document.createElement("img");
          img_element.setAttribute("src",data[ind]["productimage"]);
  
          div_element.appendChild(img_element);
  
          div_name = document.createElement("div");
          div_name.setAttribute("class","des");
  
          h5_element = document.createElement("h5");
          h5_element.innerHTML = data[ind]["name"];
  
          h4_element = document.createElement("h4");
          h4_element.innerHTML = data[ind]["price"];
  
          div_name.appendChild(h5_element);
          div_name.appendChild(h4_element);
          div_element.appendChild(div_name);
  
          
          product_element.appendChild(div_element);
          // console.log(product_element);
          // console.log(data[ind]["name"]);

        }
        if (!document.getElementsByClassName("pagination")[0].hasChildNodes()){
            createPaginationCategory(cat1,cat2,no_of_pages);
          }
      })
      .catch((error) => {
        console.log(error);
      });


  }

// This function is called when a user clicks on a product whhichh moves to another product_detail html element with some properties sent to it.
function DetailedProduct(id,name,price,image){
  let params = {
      "uniqueId": id,
      "name": name,
      "price": price,
      "image": image,
    };
    
  let query = Object.keys(params)
               .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
               .join('&');
  console.log(id);
  let url = 'http://localhost:8000/product_detail.html?' + query;
  document.location.href = url;

}

// Function to create Pagination.
function createPagination(searchText,pages){
  ul_element = document.getElementsByClassName("pagination")[0];
  list_element = document.createElement("li");
  list_element.setAttribute("class","page-item");

  anchor_element = document.createElement("a");
  anchor_element.setAttribute("class","page-link");

  anchor_element.innerHTML = "Prev";
  list_element.appendChild(anchor_element);
  ul_element.appendChild(list_element);




  for (i = 1; i<=pages;i++){
    list_element = document.createElement("li");
    list_element.setAttribute("class","page-item");

    anchor_element = document.createElement("a");
    anchor_element.setAttribute("class","page-link");
    anchor_element.setAttribute("href",`http://localhost:8000/index.html?search=${searchText}&pageno=${i}`);

    anchor_element.innerHTML = i;
    list_element.appendChild(anchor_element);
    ul_element.appendChild(list_element);
  }

  list_element = document.createElement("li");
  list_element.setAttribute("class","page-item");

  anchor_element = document.createElement("a");
  anchor_element.setAttribute("class","page-link");

  anchor_element.innerHTML = "Next";
  list_element.appendChild(anchor_element);
  ul_element.appendChild(list_element);
  
}


// Function to create Pagination when a category button is selected.
function createPaginationCategory(cat1,cat2,pages){
  ul_element = document.getElementsByClassName("pagination")[0];
  list_element = document.createElement("li");
  list_element.setAttribute("class","page-item");

  anchor_element = document.createElement("a");
  anchor_element.setAttribute("class","page-link");

  anchor_element.innerHTML = "Prev";
  list_element.appendChild(anchor_element);
  ul_element.appendChild(list_element);




  for (i = 1; i<=pages;i++){
    list_element = document.createElement("li");
    list_element.setAttribute("class","page-item");

    anchor_element = document.createElement("a");
    anchor_element.setAttribute("class","page-link");
    let params = {
      "cat1": cat1,
      "cat2": cat2,
      "pageno":i
      };
    
    let query = Object.keys(params)
               .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
               .join('&');
    
    let url = `http://localhost:8000/index.html?` + query;
    anchor_element.setAttribute("href",url);

    anchor_element.innerHTML = i;
    list_element.appendChild(anchor_element);
    ul_element.appendChild(list_element);
  }

  list_element = document.createElement("li");
  list_element.setAttribute("class","page-item");

  anchor_element = document.createElement("a");
  anchor_element.setAttribute("class","page-link");

  anchor_element.innerHTML = "Next";
  list_element.appendChild(anchor_element);
  ul_element.appendChild(list_element);
  
}