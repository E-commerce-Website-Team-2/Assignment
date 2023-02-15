window.wretch;
window.onload = function () {
    var url = document.location.href,
        params = url.split('?')[1].split('&'),
        data = {}, tmp;
    for (var i = 0, l = params.length; i < l; i++) {
        tmp = params[i].split('=');
        data[tmp[0]] = decodeURIComponent(tmp[1]);
    }
    wretch(`http://localhost:5000/products/details/${data.uniqueId}`)
        .get()
        .notFound(err => { window.location.href = './index.html/404.html' })
        .internalError(err => { window.location.href = './index.html/500.html' })
        .fetchError(err => { alert(err) })
        .res(response => response.json())
        .then((data_detail) => {
            document.getElementById("MainImage").src = data.image;
            document.getElementById("price").innerHTML = "Price: $ " + data.price;
            document.getElementById("title").innerHTML = data.name;
            document.getElementById("description").innerHTML = data_detail[0];
        })
        .catch((error) => {
            console.log(error);
        });

    wretch(`http://localhost:5000/products/recommendation/${data.uniqueId}`)
        .get()
        .notFound(err => { window.location.href = './index.html/404.html' })
        .internalError(err => { window.location.href = './index.html/500.html' })
        .fetchError(err => { alert(err) })
        .res(response => response.json())
        .then((data) => {
            if (data[0] == 200) {
                // Get the number of products sent in the response from the backend and calculate the no of pages
                no_of_products = data[1];
                // Get the product section where the products is going to be added
                product_element = document.getElementsByClassName("pro-container")[0];
                product_element.innerHTML = "";
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
                }


            }
        })
        .catch((error) => {
            console.log(error);
        });
}